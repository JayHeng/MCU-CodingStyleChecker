#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import chardet
import uilang
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from checkerWin import *

kFileType_Source = u".c"
kFileType_Header = u".h"

kSegmentType_Definition = 0
kSegmentType_Variable   = 1
kSegmentType_Prototype  = 2
kSegmentType_Code       = 3
kSegmentType_API        = 4

kLangKeyWord_Static     = u"static"

kLangKeyWordList_Control    = [u"if", u"else if", u"for", u"while", u"switch"]

class checkerMain(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(checkerMain, self).__init__(parent)
        self.setupUi(self)
        self._registerCallbacks()
        self._initSegmentMagic()
        self.progressBar.reset()
        self.fileFolderName = None
        self.continuationContent = ''
        self.bracePairs = 0

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
        self.actionMenuHelpHomePage.triggered.connect(self.callbackShowHomePage)
        self.actionMenuHelpAboutAuthor.triggered.connect(self.callbackShowAboutAuthor)
        self.actionMenuHelpRevisionHistory.triggered.connect(self.callbackShowRevisionHistory)

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

    def _printCommonError(self, line, error):
        self.textEdit_log.append(u"【ERROR】 Line " + str(line) + u": " + error)

    def _commonFindContinuationCharacter(self, content):
        contIndex = content.rfind(u"\\\n")
        if (contIndex != -1) and (contIndex == len(content) - len(u"\\\n")):
            self.continuationContent += content[0:contIndex]
            return True
        else:
            if self.continuationContent != '':
                self.continuationContent += content
            return False

    def _commonRemoveInitialBlanks(self, content):
        startIndex = 0
        while True:
            if content[startIndex] != u" ":
                break
            else:
                startIndex += 1
        return content[startIndex:len(content)]

    def _commonFindInvalidLine(self, content):
        return ((content.find(u"/*") == 0) or \
                (content.find(u"#if") == 0) or \
                (content.find(u"#else") == 0) or \
                (content.find(u"#endif") == 0) or \
                (content.find(u".") == 0))

    def _isCamelCaseNamingStyle(self, content):
        return ((content[0].isalpha() and content[0].islower()) and \
                (content.find(u"_") == -1))

    def _isLinuxUnderlineNamingStyle(self, content):
        return content.islower() and content[0] != u"_"

    def _isPascalNamingStyle(self, content):
        #if content == u"main":
        #    return True
        idx = content.find(u"_")
        if idx != -1:
            if (idx == 0) or (not (content[0:idx].isalpha() and content[0:idx].isupper())):
                return False
            idx += 1
        else:
            idx = 0
        return ((content[idx].isalpha() and content[idx].isupper()) and \
                (content[idx:len(content)].find(u"_") == -1))

    def _isValidVariableName(self, variable, isGlobal):
        idx = 0
        if isGlobal:
            idx = 2
        return self._isCamelCaseNamingStyle(variable[idx:len(variable)])

    def _doCheckGlobalVariable(self, line, content):
        if self._commonFindContinuationCharacter(content):
            return
        else:
            if self.continuationContent != '':
                content = self.continuationContent
                self.continuationContent = ''
        content = self._commonRemoveInitialBlanks(content)
        if not (self._commonFindInvalidLine(content) or \
                (content.find(u"{") == 0) or \
                (content.find(u"}") == 0)):
            # Try to find code expression according to the first "=" or ";"
            midIndex = content.find(u"=")
            endIndex = content.find(u";")
            variable = None
            fndIndex = 0
            if midIndex != -1:
                # In case there are more than one blanks before "="
                while True:
                    midIndex -= 1
                    if content[midIndex] != u" ":
                        break
                fndIndex = midIndex + 1
            elif endIndex != -1:
                fndIndex = endIndex
            else:
                return
            # If there is a "," in the code expression, that means each line has more than one variable
            expression = content[0:fndIndex]
            if expression.find(u",") != -1:
                self._printCommonError(line, u"Only one variable can be defined per line")
                return
            else:
                # Try to find variable word according to the last blank in code expression
                blankIndex = expression.rfind(u" ")
                variable = expression[blankIndex+1:fndIndex]
                #self.textEdit_log.insertPlainText("-- Find " + variable + "\n")
                # Special operation for pointer variable
                while True:
                    if variable[0] == u"*":
                        variable = variable[1:len(variable)]
                    else:
                        break
                # Process prefix in variable word
                if kLangKeyWord_Static in expression:
                    if variable[0:2] != u"s_":
                        self._printCommonError(line, u"A prefix 's_' is missed in the static variable <" + variable + u">")
                        return
                else:
                    if variable[0:2] != u"g_":
                        self._printCommonError(line, u"A prefix 'g_' is missed in the global variable <" + variable + u">")
                        return
                if not self._isValidVariableName(variable, True):
                    self._printCommonError(line, u"This variable <" + variable + u"> is not named after CamelCase")
                    return

    def _isValidFunctionName(self, function):
        return self._isPascalNamingStyle(function) or self._isLinuxUnderlineNamingStyle(function)

    def _doCheckCode(self, line, content):
        if not self._commonFindInvalidLine(content):
            if not self.bracePairs:
                # Try to find function expression according to the first "("
                fndIndex = content.find(u"(")
                if fndIndex != -1:
                    expression = content[0:fndIndex]
                    # Try to find function name according to the last blank in function expression
                    blankIndex = expression.rfind(u" ")
                    function = expression[blankIndex+1:fndIndex]
                    #self.textEdit_log.insertPlainText("-- Find " + function + "\n")
                    if not self._isValidFunctionName(function):
                        self._printCommonError(line, u"This function <" + function + u"()> is not named after Pascal or Linux style")
            # Count the "{ }" pair, function name resides out of any pair
            if content.find(u"{") != -1:
                self.bracePairs += 1
            elif content.find(u"}") != -1:
                if self.bracePairs:
                    self.bracePairs -= 1
            else:
                pass
    def _doCheckSourceFile(self, sourceFilename):
        self._checkSegments(sourceFilename, kFileType_Source)
        with open(sourceFilename, mode="r", encoding="utf-8") as fileObj:
            lineCount = 0
            isSegmentFound = False
            segmentType = None
            for lineContent in fileObj.readlines():
                lineCount += 1
                #self.textEdit_log.insertPlainText("Line " + str(lineCount) + lineContent)
                if isSegmentFound:
                    isSegmentFound = False
                    if lineContent.find(self.definitionMagic) != -1:
                        segmentType = kSegmentType_Definition
                    elif lineContent.find(self.variableMagic) != -1:
                        segmentType = kSegmentType_Variable
                    elif lineContent.find(self.prototypeMagic) != -1:
                        segmentType = kSegmentType_Prototype
                    elif lineContent.find(self.codeMagic) != -1:
                        segmentType = kSegmentType_Code
                    else:
                        pass
                elif lineContent.find(self.segmentMagicStart) != -1:
                     isSegmentFound = True
                else:
                    if segmentType == kSegmentType_Definition:
                        pass
                    elif segmentType == kSegmentType_Variable:
                        #self.textEdit_log.insertPlainText("_doCheckGlobalVariable(): \n")
                        self._doCheckGlobalVariable(lineCount, lineContent)
                    elif segmentType == kSegmentType_Prototype:
                        pass
                    elif segmentType == kSegmentType_Code:
                        #self.textEdit_log.insertPlainText("_doCheckCode(): \n")
                        self._doCheckCode(lineCount, lineContent)
                    else:
                        pass
            fileObj.close()

    def _doCheckHeaderFile(self, headerFilename):
        self._checkSegments(headerFilename, kFileType_Header)

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

    def callbackShowHomePage(self):
        QMessageBox.about(self, uilang.kMsgLanguageContentDict['homePage_title'][0], uilang.kMsgLanguageContentDict['homePage_info'][0] )

    def callbackShowAboutAuthor(self):
        QMessageBox.about(self, uilang.kMsgLanguageContentDict['aboutAuthor_title'][0], uilang.kMsgLanguageContentDict['aboutAuthor_author'][0] )

    def callbackShowRevisionHistory(self):
        QMessageBox.about(self, uilang.kMsgLanguageContentDict['revisionHistory_title'][0], uilang.kMsgLanguageContentDict['revisionHistory_v1_0'][0] )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = checkerMain()
    main_win.setWindowTitle(u"MCUXpresso SDK Coding Style Checker v0.2")
    main_win.setWindowIcon(QIcon(u"../img/MCUX-SDK-CodingStyleChecker.ico"))
    main_win.show()
    sys.exit(app.exec_())