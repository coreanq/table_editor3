# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(856, 598)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabParameter = QtWidgets.QWidget()
        self.tabParameter.setObjectName("tabParameter")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabParameter)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.tabParameter)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.viewGroup = QtWidgets.QTableView(self.splitter)
        self.viewGroup.setObjectName("viewGroup")
        self.viewGroupInfo = QtWidgets.QTableView(self.splitter)
        self.viewGroupInfo.setObjectName("viewGroupInfo")
        self.viewParameter = QtWidgets.QTableView(self.splitter_2)
        self.viewParameter.setObjectName("viewParameter")
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabParameter, "")
        self.tabMessage = QtWidgets.QWidget()
        self.tabMessage.setObjectName("tabMessage")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabMessage)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter_3 = QtWidgets.QSplitter(self.tabMessage)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_4 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.viewMessage = QtWidgets.QTableView(self.splitter_4)
        self.viewMessage.setObjectName("viewMessage")
        self.viewMessageInfo = QtWidgets.QTableView(self.splitter_4)
        self.viewMessageInfo.setObjectName("viewMessageInfo")
        self.viewMessageValue = QtWidgets.QTableView(self.splitter_3)
        self.viewMessageValue.setObjectName("viewMessageValue")
        self.gridLayout_3.addWidget(self.splitter_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabMessage, "")
        self.tabVariable = QtWidgets.QWidget()
        self.tabVariable.setObjectName("tabVariable")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabVariable)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.viewVariable = QtWidgets.QTableView(self.tabVariable)
        self.viewVariable.setObjectName("viewVariable")
        self.gridLayout_4.addWidget(self.viewVariable, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabVariable, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 856, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabParameter), _translate("MainWindow", "Parameter"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMessage), _translate("MainWindow", "Message"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVariable), _translate("MainWindow", "Variable"))

