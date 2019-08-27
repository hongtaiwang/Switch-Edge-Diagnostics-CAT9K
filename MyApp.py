from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import P1_switch2graph_log.switch2graph_log as diag
import P2_readApphosingInfo.readAppInfo as appDiag
import P3_interface_status.InterfaceStatus as intrDiag

import sys
from MainWindow import Ui_MainWindow
from Dialog import Ui_Dialog


# dialog for fixing bugs connect functions inside mainwindow class
class CustomDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Fix it")

        self.label = QLabel(self)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setText("Do you want to fix it?")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


# dialog for interface monitoring, derived from Dialog.py
class InterfaceDialog(QDialog, Ui_Dialog):
    def __init__(self, intr):
        super(InterfaceDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Interface Detail - {}".format(intr))


# dialog for error details
class ErrDetailDialog(QDialog):
    def __init__(self, errtype, errnum=0):
        super(ErrDetailDialog, self).__init__()

        title = errtype + ' err details'
        self.setWindowTitle(title)

        self.label = QLabel(self)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        if errtype == 'input' or errtype == 'output' or errtype == 'collision':
            text = '{} {} errs exits!'.format(errnum, errtype)
        elif errtype == 'input queue' and errnum != 0:
            text = 'Input queue overflow!'
        elif errtype == 'output queue' and errnum != 0:
            text = 'Output queue overflow!'
        elif errtype == 'pd':
            text = 'No pd on this interface'
        else:
            text = 'No errors!'
        if errnum == -1:
            text = 'Interface is not up!'
        self.label.setText(text)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


# main part of the program
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # set up UI
        self.setupUi(self)
        self.setWindowTitle("Edge Diagnostics For CAT9K")

        # connect button to function on_click
        self.pushButton.clicked.connect(self.on_click)

        # initialize variables
        self.hostName = ""
        self.userName = ""
        self.psw = ""
        self.enapsw = ""
        self.intv = ""

        self.diagObj = diag.cdpDiag()
        self.appDiagObj = appDiag.AppHosting()
        self.intrDiagObj = intrDiag.IntrStatus()

        self.buttons = dict()

    # troubleshooting for iox
    def onMyToolBarButtonClick(self):
        dlg = CustomDialog(self)
        if dlg.exec_():
            self.appDiagObj.runIox()
        else:
            pass

    # troubleshooting for app interface
    def onMyToolBarButtonClick_inter(self):
        dlg = CustomDialog(self)
        if dlg.exec_():
            self.appDiagObj.runAppInter()
        else:
            pass

    # troubleshooting for insufficient power
    def onMyToolBarButtonClick_power(self, intr):
        dlg = CustomDialog(self)
        if dlg.exec_():
            self.intrDiagObj.grantPower(intr)
        else:
            pass

    #  show err details
    def onMyToolBarButtonClick_err(self, errtype='no err', errnum=0):
        dlg = ErrDetailDialog(errtype, errnum)
        if dlg.exec_():
            pass

    # display interface status
    def show_intr(self, intr, err, intrup=True):
        dlg = InterfaceDialog(intr)

        # if interface is up show red or green, otherwise, show orange(no err) or red(err exists)
        # set color for input queue
        if err[0] == 0:
            if intrup is True:
                try:
                    dlg.button_inputQ.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_inputQ.pressed.connect(lambda: self.onMyToolBarButtonClick_err('input queue'))
                dlg.button_inputQ.setStyleSheet("* { background-color: rgb(124,252,0) }")
            else:
                try:
                    dlg.button_inputQ.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_inputQ.pressed.connect(lambda: self.onMyToolBarButtonClick_err('input queue', -1))
                dlg.button_inputQ.setStyleSheet("* { background-color: rgb(255,140,0) }")
        else:
            try:
                dlg.button_inputQ.pressed.disconnect()
            except Exception:
                pass
            dlg.button_inputQ.pressed.connect(lambda: self.onMyToolBarButtonClick_err('input queue', err[0]))
            dlg.button_inputQ.setStyleSheet("* { background-color: rgb(220,20,60) }")

        # set color for output queue
        if err[1] == 0:
            if intrup is True:
                try:
                    dlg.button_outputQ.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_outputQ.pressed.connect(lambda: self.onMyToolBarButtonClick_err('output queue'))
                dlg.button_outputQ.setStyleSheet("* { background-color: rgb(124,252,0) }")
            else:
                try:
                    dlg.button_outputQ.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_outputQ.pressed.connect(lambda: self.onMyToolBarButtonClick_err('output queue', -1))
                dlg.button_outputQ.setStyleSheet("* { background-color: rgb(255,140,0) }")
        else:
            try:
                dlg.button_outputQ.pressed.disconnect()
            except Exception:
                pass
            dlg.button_outputQ.pressed.connect(lambda: self.onMyToolBarButtonClick_err('output queue', err[1]))
            dlg.button_outputQ.setStyleSheet("* { background-color: rgb(220,20,60) }")

        # set input errors
        if err[2] == 0:
            if intrup is True:
                try:
                    dlg.button_inputerr.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_inputerr.pressed.connect(lambda: self.onMyToolBarButtonClick_err('input'))
                dlg.button_inputerr.setStyleSheet("* { background-color: rgb(124,252,0) }")
            else:
                try:
                    dlg.button_inputerr.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_inputerr.pressed.connect(lambda: self.onMyToolBarButtonClick_err('input', -1))
                dlg.button_inputerr.setStyleSheet("* { background-color: rgb(255,140,0) }")
        else:
            try:
                dlg.button_inputerr.pressed.disconnect()
            except Exception:
                pass
            dlg.button_inputerr.pressed.connect(lambda: self.onMyToolBarButtonClick_err('input', err[2]))
            dlg.button_inputerr.setStyleSheet("* { background-color: rgb(220,20,60) }")

        # set output errors
        if err[3] == 0:
            if intrup is True:
                try:
                    dlg.button_outputerr.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_outputerr.pressed.connect(lambda: self.onMyToolBarButtonClick_err('output'))
                dlg.button_outputerr.setStyleSheet("* { background-color: rgb(124,252,0) }")
            else:
                try:
                    dlg.button_outputerr.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_outputerr.pressed.connect(lambda: self.onMyToolBarButtonClick_err('output', -1))
                dlg.button_outputerr.setStyleSheet("* { background-color: rgb(255,140,0) }")
        else:
            try:
                dlg.button_outputerr.pressed.disconnect()
            except Exception:
                pass
            dlg.button_outputerr.pressed.connect(lambda: self.onMyToolBarButtonClick_err('output', err[3]))
            dlg.button_outputerr.setStyleSheet("* { background-color: rgb(220,20,60) }")

        # set collisions
        if err[4] == 0:
            if intrup is True:
                try:
                    dlg.button_collisions.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_collisions.pressed.connect(lambda: self.onMyToolBarButtonClick_err('collision'))
                dlg.button_collisions.setStyleSheet("* { background-color: rgb(124,252,0) }")
            else:
                try:
                    dlg.button_collisions.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_collisions.pressed.connect(lambda: self.onMyToolBarButtonClick_err('collision', -1))
                dlg.button_collisions.setStyleSheet("* { background-color: rgb(255,140,0) }")
        else:
            try:
                dlg.button_collisions.pressed.disconnect()
            except Exception:
                pass
            dlg.button_collisions.pressed.connect(lambda: self.onMyToolBarButtonClick_err('collision', err[4]))
            dlg.button_collisions.setStyleSheet("* { background-color: rgb(220,20,60) }")

        # set powers
        if self.intrDiagObj.pd_in.get(intr):
            if self.intrDiagObj.pd_in[intr] == 'insufficient power':
                dlg.button_pd.setStyleSheet("* { background-color: rgb(220,20,60) }")
                try:
                    dlg.button_pd.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_pd.pressed.connect(lambda: self.onMyToolBarButtonClick_power(intr))
            else:
                try:
                    dlg.button_pd.pressed.disconnect()
                except Exception:
                    pass
                dlg.button_pd.pressed.connect(lambda: self.onMyToolBarButtonClick_err())
                dlg.button_pd.setStyleSheet("* { background-color: rgb(124,252,0) }")
        # no pd on interface, show orange
        else:
            try:
                dlg.button_pd.pressed.disconnect()
            except Exception:
                pass
            dlg.button_pd.pressed.connect(lambda: self.onMyToolBarButtonClick_err('pd'))
            dlg.button_pd.setStyleSheet("* { background-color: rgb(255,140,0) }")

        dlg.exec_()

    @pyqtSlot()
    def on_click(self):
        if not self.input_host.text():
            return
        self.hostName = self.input_host.text()
        self.userName = self.input_user.text()
        self.psw = self.input_psw.text()
        self.enapsw = self.input_ena.text()

        if len(self.enapsw) == 0:
            args = [" ", self.hostName, self.userName, self.psw, None, 0]
        else:
            args = [" ", self.hostName, self.userName, self.psw, self.enapsw, 0]
        if self.diagObj.host is None:
            self.diagObj = diag.cdpDiag(args)
            self.appDiagObj = appDiag.AppHosting(args)
            self.intrDiagObj = intrDiag.IntrStatus(args)

        self.diagObj.run()
        self.appDiagObj.printLog()
        self.intrDiagObj.printLog()

        # display text log
        self.textBrowser.append(self.diagObj.outputlog)
        self.textBrowser.append(self.appDiagObj.outputlog)
        self.textBrowser.append(self.intrDiagObj.outputlog)

        # display graph
        pixmap = QPixmap("./cdp_image_log.png")
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.graphicsView.setScene(scene)
        self.graphicsView.show()

        # display app-hosting issues
        if self.appDiagObj.checkRunning():
            self.button_iox.setStyleSheet("* { background-color: rgb(124,252,0) }")
            self.button_usb.setStyleSheet("* { background-color: rgb(124,252,0) }")
            if self.appDiagObj.checkApp():
                self.button_runningapp.setStyleSheet("* { background-color: rgb(124,252,0) }")
            else:
                self.button_runningapp.setStyleSheet("* { background-color: rgb(220,20,60) }")
        else:
            self.button_iox.setStyleSheet("* { background-color: rgb(220,20,60) }")
            self.button_runningapp.setStyleSheet("* { background-color: rgb(220,20,60) }")
            self.button_usb.setStyleSheet("* { background-color: rgb(220,20,60) }")
            try:
                self.button_iox.pressed.disconnect()
            except Exception:
                pass
            self.button_iox.pressed.connect(lambda: self.onMyToolBarButtonClick())

        # app interface
        if self.appDiagObj.appInterStat:
            self.button_inter.setStyleSheet("* { background-color: rgb(124,252,0) }")
        else:
            self.button_inter.setStyleSheet("* { background-color: rgb(220,20,60) }")
            try:
                self.button_inter.pressed.disconnect()
            except Exception:
                pass
            self.button_inter.pressed.connect(lambda: self.onMyToolBarButtonClick_inter())

        # interface status
        for intr in self.intrDiagObj.errInfo:
            if intr in self.buttons:
                continue
            self.buttons[intr] = QAction(intr, self)
            self.menuInterfaces.addAction(self.buttons[intr])
        for intr in self.buttons:
            try:
                self.buttons[intr].triggered.disconnect()
            except Exception:
                pass
            self.buttons[intr].triggered.connect(lambda _, intr=intr, e=self.intrDiagObj.errInfo[intr],\
                                               b=(self.intrDiagObj.intStat[intr] == 'up'): self.show_intr(intr, e, b))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
