# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MCUX-SDK-CodingStyleChecker.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 580)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_codingRuleSetting = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_codingRuleSetting.setGeometry(QtCore.QRect(10, 10, 81, 71))
        self.pushButton_codingRuleSetting.setObjectName("pushButton_codingRuleSetting")
        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(10, 90, 781, 411))
        self.textEdit_log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_log.setObjectName("textEdit_log")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 510, 781, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.textEdit_fileFolderFilter = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_fileFolderFilter.setGeometry(QtCore.QRect(190, 50, 441, 31))
        self.textEdit_fileFolderFilter.setObjectName("textEdit_fileFolderFilter")
        self.label_fileFolderFilter = QtWidgets.QLabel(self.centralwidget)
        self.label_fileFolderFilter.setGeometry(QtCore.QRect(100, 50, 91, 31))
        self.label_fileFolderFilter.setObjectName("label_fileFolderFilter")
        self.textEdit_inputFileFolder = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_inputFileFolder.setGeometry(QtCore.QRect(190, 10, 441, 31))
        self.textEdit_inputFileFolder.setObjectName("textEdit_inputFileFolder")
        self.label_selectFileFolder = QtWidgets.QLabel(self.centralwidget)
        self.label_selectFileFolder.setGeometry(QtCore.QRect(100, 10, 91, 31))
        self.label_selectFileFolder.setObjectName("label_selectFileFolder")
        self.pushButton_browseFileFolder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_browseFileFolder.setGeometry(QtCore.QRect(640, 10, 71, 31))
        self.pushButton_browseFileFolder.setObjectName("pushButton_browseFileFolder")
        self.checkBox_isFolder = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_isFolder.setGeometry(QtCore.QRect(720, 10, 61, 31))
        self.checkBox_isFolder.setObjectName("checkBox_isFolder")
        self.pushButton_doCheck = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_doCheck.setGeometry(QtCore.QRect(640, 50, 71, 31))
        self.pushButton_doCheck.setObjectName("pushButton_doCheck")
        self.pushButton_saveLog = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_saveLog.setGeometry(QtCore.QRect(720, 50, 71, 31))
        self.pushButton_saveLog.setObjectName("pushButton_saveLog")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MCUXpresso SDK Coding Style Checker"))
        self.pushButton_codingRuleSetting.setText(_translate("MainWindow", "Coding Rule \n"
"\n"
" Setting"))
        self.label_fileFolderFilter.setText(_translate("MainWindow", "File/Folder Filter:"))
        self.label_selectFileFolder.setText(_translate("MainWindow", "Select File/Folder:"))
        self.pushButton_browseFileFolder.setText(_translate("MainWindow", "Browse"))
        self.checkBox_isFolder.setText(_translate("MainWindow", "Is Folder"))
        self.pushButton_doCheck.setText(_translate("MainWindow", "Check"))
        self.pushButton_saveLog.setText(_translate("MainWindow", "Save Log"))

