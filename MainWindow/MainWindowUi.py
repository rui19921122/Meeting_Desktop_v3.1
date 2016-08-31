# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindowUi.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TitleLayout = QtWidgets.QHBoxLayout()
        self.TitleLayout.setObjectName("TitleLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.TitleLayout.addItem(spacerItem)
        self.min_button = PixPushButton(self.centralwidget)
        self.min_button.setObjectName("min_button")
        self.TitleLayout.addWidget(self.min_button)
        self.max_button = PixPushButton(self.centralwidget)
        self.max_button.setObjectName("max_button")
        self.TitleLayout.addWidget(self.max_button)
        self.close_button = PixPushButton(self.centralwidget)
        self.close_button.setObjectName("close_button")
        self.TitleLayout.addWidget(self.close_button)
        self.verticalLayout.addLayout(self.TitleLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.min_button.setText(_translate("MainWindow", "PushButton"))
        self.max_button.setText(_translate("MainWindow", "PushButton"))
        self.close_button.setText(_translate("MainWindow", "PushButton"))

from Component import PixPushButton
from resource import logo_rc
