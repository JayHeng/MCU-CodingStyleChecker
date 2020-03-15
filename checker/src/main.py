#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import chardet
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from checkerWin import *

kFileType_Source = u".c"
kFileType_Header = u".h"

class checkerMain(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(checkerMain, self).__init__(parent)
        self.setupUi(self)
        self._registerCallbacks()
        self._initSegmentMagic()
        self.progressBar.reset()
        self.fileFolderName = None

    def _initSegmentMagic(self):
        self.segmentMagicStart = u"/*******************************************************************************"
        self.definitionMagic   = u" * Definitions"
        self.variableMagic     = u" * Variables"
        self.prototypeMagic    = u" * Prototypes"
        self.codeMagic         = u" * Code"
        self.apiMagic          = u" * API"
        self.segmentMagicEnd   = u" ******************************************************************************/"

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
        self.textEdit_log.append(u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>----------File----------<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.textEdit_log.append(u"Start to check  " + filename + "\n")

    def _isUtf8AsciiFile(self, filename):
        self._fileCheckSeparator(filename)
        fileObj = open(filename,'rb')
        fileDat = fileObj.read()
        # https://chardet.readthedocs.io/en/latest/supported-encodings.html
        fileProperties = chardet.detect(fileDat)
        fileObj.close()
        if fileProperties.get('confidence') == 1.0 and \
           (fileProperties.get('encoding') != 'utf-8' or \
            fileProperties.get('encoding') != 'ascii'):
            return True
        else:
            self.textEdit_log.append(u"【ERROR】: Cannot support Non-'UTF-8'/'ASCII'(100%) encoded file \n")
            return False

    def _checkSegment(self, content, segmentMagic):
        segment = self.segmentMagicStart + u"\n" + segmentMagic + u"\n" + self.segmentMagicEnd
        if content.find(segment) == -1:
            self.textEdit_log.append(u"【ERROR】: Below general comment is missed in the file")
            self.textEdit_log.append(segment)

    def _checkSegments(self, filename, fileType):
        with open(filename, mode="r", encoding="utf-8") as fileObj:
            content = fileObj.read()
            self._checkSegment(content, self.definitionMagic)
            if fileType == kFileType_Header:
                self._checkSegment(content, self.apiMagic)
            elif fileType == kFileType_Source:
                self._checkSegment(content, self.variableMagic)
                self._checkSegment(content, self.prototypeMagic)
                self._checkSegment(content, self.codeMagic)
            else:
                pass
            fileObj.close()

    def _doCheckHeaderFile(self, headerFilename):
        self._checkSegments(headerFilename, kFileType_Header)

    def _doCheckSourceFile(self, sourceFilename):
        self._checkSegments(sourceFilename, kFileType_Source)

    def _detectFileType(self, filename):
        if os.path.isfile(filename):
            filetype = os.path.splitext(filename)[1]
            if filetype == kFileType_Header:
                if not self._isUtf8AsciiFile(filename):
                    return
                self._doCheckHeaderFile(filename)
            elif filetype == kFileType_Source:
                if not self._isUtf8AsciiFile(filename):
                    return
                self._doCheckSourceFile(filename)
            else:
                pass

    def callbackDoCheck(self):
        self.textEdit_log.clear()
        if self.fileFolderName != None:
            if os.path.isdir(self.fileFolderName):
                for root, dirs, files in os.walk(self.fileFolderName, topdown=True):
                    for name in files:
                        self._detectFileType(os.path.join(root, name))
            else:
                self._detectFileType(self.fileFolderName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = checkerMain()
    main_win.setWindowTitle(u"MCUXpresso SDK Coding Style Checker v0.1")
    main_win.setWindowIcon(QIcon(u"../img/MCUX-SDK-CodingStyleChecker.ico"))
    main_win.show()
    sys.exit(app.exec_())