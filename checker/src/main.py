#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from checkerWin import *

class checkerMain(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(checkerMain, self).__init__(parent)
        self.setupUi(self)
        self._registerCallbacks()
        self.progressBar.reset()
        self.fileFolderName = None

    def _registerCallbacks(self):
        self.pushButton_browseFileFolder.clicked.connect(self.callbackBrowseFileFolder)

    def callbackBrowseFileFolder(self):
        if self.checkBox_isFolder.isChecked():
            self.fileFolderName = QtWidgets.QFileDialog.getExistingDirectory(self, u"Browse Folder", os.getcwd())
        else:
            self.fileFolderName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, u"Browse File", os.getcwd(), "All Files(*);;Source Files(*.c)")
        self.textEdit_inputFileFolder.setPlainText(self.fileFolderName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = checkerMain()
    main_win.setWindowTitle(u"MCUXpresso SDK Coding Style Checker v1.0.0")
    main_win.setWindowIcon(QIcon(u"../img/MCUX-SDK-CodingStyleChecker.ico"))
    main_win.show()
    sys.exit(app.exec_())