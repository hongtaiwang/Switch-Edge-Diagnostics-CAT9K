from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import P1_switch2graph_log.switch2graph_log as diag
import P2_readApphosingInfo.readAppInfo as appDiag

import sys
from MainWindow import Ui_MainWindow


class CustomDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Fix it")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class CustomDialog_appinter(QDialog):
    def __init__(self, *args, **kwargs):
        super(CustomDialog_appinter, self).__init__(*args, **kwargs)

        self.setWindowTitle("Fix it")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # set up UI
        self.setupUi(self)
        self.setWindowTitle("Edge Diagnostics For CAT9K")
        #connect button to function on_click
        self.pushButton.clicked.connect(self.on_click)

        #initialize variables
        self.hostName = ""
        self.userName = ""
        self.psw = ""
        self.enapsw = ""
        self.intv = ""

        self.diagObj = diag.cdpDiag()
        self.appDiagObj = appDiag.AppHosting()

    def onMyToolBarButtonClick(self):
        dlg = CustomDialog(self)
        if dlg.exec_():
            self.appDiagObj.runIox()
            print("Success!")
        else:
            print("Cancel!")

    def onMyToolBarButtonClick_inter(self):
        dlg = CustomDialog_appinter(self)
        if dlg.exec_():
            self.appDiagObj.runAppInter()
            print("Success!")
        else:
            print("Cancel!")

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
        print("11111111111")
        if self.diagObj.host is None:
            self.diagObj = diag.cdpDiag(args)
            self.appDiagObj = appDiag.AppHosting(args)

        self.diagObj.run()
        self.appDiagObj.printLog()

        # display text log
        self.textBrowser.append(self.diagObj.outputlog)
        self.textBrowser.append(self.appDiagObj.outputlog)

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
        if self.appDiagObj.checkAppInter():
            self.button_inter.setStyleSheet("* { background-color: rgb(124,252,0) }")
        else:
            self.button_inter.setStyleSheet("* { background-color: rgb(220,20,60) }")
            try:
                self.button_inter.pressed.disconnect()
            except Exception:
                pass
            self.button_inter.pressed.connect(lambda: self.onMyToolBarButtonClick_inter())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
