# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Josh\PycharmProjects\MixingSessionSetup\GUI\DesignerFiles\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(496, 268)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.loginToCeltxPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginToCeltxPushButton.setObjectName("loginToCeltxPushButton")
        self.gridLayout.addWidget(self.loginToCeltxPushButton, 2, 0, 1, 1)
        self.celtxScriptsListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.celtxScriptsListWidget.setObjectName("celtxScriptsListWidget")
        self.gridLayout.addWidget(self.celtxScriptsListWidget, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 496, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Setup Mixing Session"))
        self.label.setText(_translate("MainWindow", "Celtx Scripts:"))
        self.loginToCeltxPushButton.setText(_translate("MainWindow", "Login to Celtx"))
