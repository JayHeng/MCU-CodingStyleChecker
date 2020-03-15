#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import chardet
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
        self.pushButton_doCheck.clicked.connect(self.callbackDoCheck)

    def callbackBrowseFileFolder(self):
        if self.checkBox_isFolder.isChecked():
            self.fileFolderName = QtWidgets.QFileDialog.getExistingDirectory(self, u"Browse Folder", os.getcwd())
        else:
            self.fileFolderName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, u"Browse File", os.getcwd(), "All Files(*);;Source Files(*.c)")
        self.textEdit_inputFileFolder.setPlainText(self.fileFolderName)

    def _fileCheckSeparator(self, filename):
        self.textEdit_log.append(u"------------------------------------------------------------------------------")
        self.textEdit_log.append(u"Start to check  " + filename)

    def _isUtf8AsciiFile(self, filename):
        self._fileCheckSeparator(filename)
        fileObj = open(filename,'rb')
        fileDat = fileObj.read()
        # https://chardet.readthedocs.io/en/latest/supported-encodings.html
        fileProperties = chardet.detect(fileDat)
        if fileProperties.get('confidence') == 1.0 and \
           (fileProperties.get('encoding') != 'utf-8' or \
            fileProperties.get('encoding') != 'ascii'):
            return True
        else:
            self.textEdit_log.append(u"【ERROR】: Cannot support Non-'UTF-8'/'ASCII'(100%) encoded file ")
            return False

    def _doCheckSourceFile(self, sourceFilename):
        pass

    def _doCheckHeaderFile(self, headerFilename):
        pass

    def _detectFileType(self, filename):
        if os.path.isfile(filename):
            filetype = os.path.splitext(filename)[1]
            if filetype == '.h':
                if not self._isUtf8AsciiFile(filename):
                    return
                self._doCheckHeaderFile(filename)
            elif filetype == '.c':
                if not self._isUtf8AsciiFile(filename):
                    return
                self._doCheckSourceFile(filename)
            else:
                pass

    def callbackDoCheck(self):
        self.textEdit_log.clear()
        if self.fileFolderName != None:
            if os.path.isdir(self.fileFolderName):
                pass
            else:
                self._detectFileType(self.fileFolderName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = checkerMain()
    main_win.setWindowTitle(u"MCUXpresso SDK Coding Style Checker v1.0.0")
    main_win.setWindowIcon(QIcon(u"../img/MCUX-SDK-CodingStyleChecker.ico"))
    main_win.show()
    sys.exit(app.exec_())