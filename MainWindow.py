# # -*- coding: utf-8 -*-
#
# # Form implementation generated from reading ui file '.\mainwindow.ui'
# #
# # Created by: PyQt5 UI code generator 5.13.0
# #
# # WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(902, 555)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 4, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setEnabled(True)

        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 2, 1, 3)
        self.input_psw = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_psw.sizePolicy().hasHeightForWidth())
        self.input_psw.setSizePolicy(sizePolicy)
        self.input_psw.setObjectName("input_psw")
        self.gridLayout.addWidget(self.input_psw, 0, 3, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setObjectName("textBrowser")

        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 2)
        self.input_user = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_user.sizePolicy().hasHeightForWidth())
        self.input_user.setSizePolicy(sizePolicy)
        self.input_user.setObjectName("input_user")
        self.gridLayout.addWidget(self.input_user, 0, 2, 1, 1)
        self.input_host = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_host.sizePolicy().hasHeightForWidth())
        self.input_host.setSizePolicy(sizePolicy)
        self.input_host.setObjectName("input_host")
        self.gridLayout.addWidget(self.input_host, 0, 0, 1, 2)
        self.button_usb = QtWidgets.QPushButton(self.centralwidget)
        self.button_usb.setObjectName("button_usb")
        self.gridLayout.addWidget(self.button_usb, 2, 3, 1, 2)
        self.button_runningapp = QtWidgets.QPushButton(self.centralwidget)
        self.button_runningapp.setObjectName("button_runningapp")
        self.gridLayout.addWidget(self.button_runningapp, 2, 2, 1, 1)
        self.button_iox = QtWidgets.QPushButton(self.centralwidget)
        self.button_iox.setObjectName("button_iox")
        self.gridLayout.addWidget(self.button_iox, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 902, 26))
        self.menubar.setObjectName("menubar")
        self.menuDiagnostic = QtWidgets.QMenu(self.menubar)
        self.menuDiagnostic.setObjectName("menuDiagnostic")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuDiagnostic.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Refresh"))
        self.menuDiagnostic.setTitle(_translate("MainWindow", "Diagnostic"))
        self.button_runningapp.setText(_translate("MainWindow", "Running-app"))
        self.button_iox.setText(_translate("MainWindow", "IOX-Service"))
        self.button_usb.setText(_translate("MainWindow", "App Resource"))

