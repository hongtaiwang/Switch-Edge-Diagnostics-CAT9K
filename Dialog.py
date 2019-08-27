# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(421, 324)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 270, 201, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.button_inputQ = QtWidgets.QPushButton(Dialog)
        self.button_inputQ.setGeometry(QtCore.QRect(40, 20, 161, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_inputQ.sizePolicy().hasHeightForWidth())
        self.button_inputQ.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_inputQ.setFont(font)
        self.button_inputQ.setObjectName("button_inputQ")
        self.button_outputQ = QtWidgets.QPushButton(Dialog)
        self.button_outputQ.setGeometry(QtCore.QRect(40, 70, 161, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_outputQ.sizePolicy().hasHeightForWidth())
        self.button_outputQ.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_outputQ.setFont(font)
        self.button_outputQ.setObjectName("button_outputQ")
        self.button_inputerr = QtWidgets.QPushButton(Dialog)
        self.button_inputerr.setGeometry(QtCore.QRect(40, 120, 161, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_inputerr.sizePolicy().hasHeightForWidth())
        self.button_inputerr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_inputerr.setFont(font)
        self.button_inputerr.setObjectName("button_inputerr")
        self.button_outputerr = QtWidgets.QPushButton(Dialog)
        self.button_outputerr.setGeometry(QtCore.QRect(40, 170, 161, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_outputerr.sizePolicy().hasHeightForWidth())
        self.button_outputerr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_outputerr.setFont(font)
        self.button_outputerr.setObjectName("button_outputerr")
        self.button_collisions = QtWidgets.QPushButton(Dialog)
        self.button_collisions.setGeometry(QtCore.QRect(40, 220, 161, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_collisions.sizePolicy().hasHeightForWidth())
        self.button_collisions.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_collisions.setFont(font)
        self.button_collisions.setObjectName("button_collisions")
        self.button_pd = QtWidgets.QPushButton(Dialog)
        self.button_pd.setGeometry(QtCore.QRect(240, 20, 121, 231))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_pd.sizePolicy().hasHeightForWidth())
        self.button_pd.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_pd.setFont(font)
        self.button_pd.setObjectName("button_pd")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Interface Details"))
        self.button_inputQ.setText(_translate("Dialog", "Input Queue"))
        self.button_outputQ.setText(_translate("Dialog", "Output Queue"))
        self.button_inputerr.setText(_translate("Dialog", "Input errs"))
        self.button_outputerr.setText(_translate("Dialog", "Output errs"))
        self.button_collisions.setText(_translate("Dialog", "Collisions"))
        self.button_pd.setText(_translate("Dialog", "Power\nDevice"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())