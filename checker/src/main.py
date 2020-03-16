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
        self.lcdNumber_passRate.display(0)
        self.fileFolderName = None
        self.continuationContent = ''
        self.bracePairs = 0
        self.onProgressEnumName = u""
        self.isEnumOnProgress = False
        self.onProgressStructName = u""
        self.isStructOnProgress = False
        self.totalErrorLines = 0
        self.totalCodeLines = 0

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

    def _updateTotalErrorLines(self):
        self.lineEdit_totalErrorLines.clear()
        self.lineEdit_totalErrorLines.setText(str(self.totalErrorLines))

    def _updateTotalCodeLines(self):
        self.lineEdit_totalCodeLines.clear()
        self.lineEdit_totalCodeLines.setText(str(self.totalCodeLines))

    def _printCommonError(self, line, error):
        self.textEdit_log.append(u"【ERROR】 Line " + str(line) + u": " + error)
        self.totalErrorLines += 1
        self._updateTotalErrorLines()

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

    def _commonLinePreprocess(self, content):
        if self._commonFindContinuationCharacter(content):
            return None, False
        else:
            if self.continuationContent != '':
                content = self.continuationContent
                self.continuationContent = ''
        content = self._commonRemoveInitialBlanks(content)
        return content, True

    def _commonFindInvalidCodeLine(self, content):
        return ((content.find(u"/*") == 0) or \
                (content.find(u"#if") == 0) or \
                (content.find(u"#else") == 0) or \
                (content.find(u"#endif") == 0))

    def _isCamelCaseNamingStyle(self, content):
        return ((content[0].isalpha() and content[0].islower()) and \
                (content.find(u"_") == -1))

    def _isLinuxUnderlineNamingStyle(self, content):
        return content.islower() and content[0] != u"_"

    def _isPascalNamingStyle(self, content):
        idx = content.find(u"_")
        if idx != -1:
            if (idx == 0) or (not (content[0:idx].isalpha() and content[0:idx].isupper())):
                return False
            idx += 1
        else:
            idx = 0
        return ((content[idx].isalpha() and content[idx].isupper()) and \
                (content[idx:len(content)].find(u"_") == -1))

    def _getDefinitionWord(self, content, startIdx, endChar):
        wordLoc = [0, 0]
        while True:
            startIdx += 1
            if content[startIdx] == u" " or content[startIdx] == endChar or content[startIdx] == u"\n":
                if wordLoc[0] != 0:
                    wordLoc[1] = startIdx
                    break
            elif wordLoc[0] == 0:
                wordLoc[0] = startIdx
            else:
                pass
        return content[wordLoc[0]:wordLoc[1]]

    def _isValidMacroName(self, macro):
        return macro.isupper() and macro[0] != u"_"

    def _doCheckMacro(self, line, content):
        idx = len(u"#define") - 1
        macro = self._getDefinitionWord(content, idx, u"(")
        if not self._isValidMacroName(macro):
            self._printCommonError(line, u"This macro <" + macro + u"> starts with '_' or it is not all capitalized")

    def _isValidEnumStructTypeName(self, mtype):
        return mtype.islower() and mtype[0] == u"_"

    def _isValidEnumStructTypedefName(self, mtype):
        return mtype.islower() and mtype[0] != u"_" and mtype[len(mtype)-2:len(mtype)] == u"_t"

    def _isValidEnumeratorName(self, enum):
        return enum[0] == u"k" and enum[1].isupper()

    def _doCheckEnum(self, line, content):
        if not self.isEnumOnProgress:
            idx = content.find(u"enum") + len(u"enum") - 1
            enumType = self._getDefinitionWord(content, idx, u"{")
            if not self._isValidEnumStructTypeName(enumType):
                self._printCommonError(line, u"This enum type name <" + enumType + u"> is not valid")
            else:
                self.onProgressEnumName = enumType
                self.isEnumOnProgress = True
        else:
            if content[0] == "}":
                enumTypedef = self._getDefinitionWord(content, 0, u";")
                if enumTypedef[0] != u";" and (not self._isValidEnumStructTypedefName(enumTypedef)):
                    self._printCommonError(line, u"This enum typedef name <" + enumTypedef + u"> is not valid")
                self.isEnumOnProgress = False
            elif content[0] != "{":
                if not self._isValidEnumeratorName(content[0:2]):
                    self._printCommonError(line, u"This enum type <" + self.onProgressEnumName + u"> contains invalid enumerator name")
                    self.isEnumOnProgress = False

    def _isValidStructMemberName(self, struct):
        return self._isValidVariableName(struct, False)

    def _findValidLocalVariable(self, content, isBssSection=True):
        # Try to find code expression according to the first "=" or ";"
        midIndex = -1
        if not isBssSection:
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
            return True
        expression = content[0:fndIndex]
        # Try to find variable word according to the last blank in code expression
        blankIndex = expression.rfind(u" ")
        variable = expression[blankIndex+1:fndIndex]
        while True:
            if variable[0] == u"*":
                variable = variable[1:len(variable)]
            else:
                break
        return self._isValidVariableName(variable, False)

    def _doCheckStruct(self, line, content):
        if not self.isStructOnProgress:
            idx = content.find(u"struct") + len(u"struct") - 1
            structType = self._getDefinitionWord(content, idx, u"{")
            if not self._isValidEnumStructTypeName(structType):
                self._printCommonError(line, u"This struct type name <" + structType + u"> is not valid")
            else:
                self.onProgressStructName = structType
                self.isStructOnProgress = True
        else:
            if content[0] == "}":
                structTypedef = self._getDefinitionWord(content, 0, u";")
                if structTypedef[0] != u";" and (not self._isValidEnumStructTypedefName(structTypedef)):
                    self._printCommonError(line, u"This struct typedef name <" + structTypedef + u"> is not valid")
                self.isStructOnProgress = False
            elif content[0] != "{":
                if not self._findValidLocalVariable(content):
                    self._printCommonError(line, u"This struct type <" + self.onProgressStructName + u"> contains invalid member name")
                    self.isStructOnProgress = False

    def _doCheckDefinition(self, line, content):
        content, status = self._commonLinePreprocess(content)
        if not status:
            return
        if not (self._commonFindInvalidCodeLine(content)):
            if content.find(u"#define") == 0:
                self._doCheckMacro(line, content)
            else:
                if self.isEnumOnProgress or \
                   (content.find(u"enum") == 0 or (content.find(u"typedef") == 0 and content.find(u"enum") != -1)):
                    self._doCheckEnum(line, content)
                elif self.isStructOnProgress or \
                     (content.find(u"struct") == 0 or (content.find(u"typedef") == 0 and content.find(u"struct") != -1)):
                    self._doCheckStruct(line, content)
                else:
                    pass

    def _isValidVariableName(self, variable, isGlobal):
        idx = 0
        if isGlobal:
            idx = 2
        return self._isCamelCaseNamingStyle(variable[idx:len(variable)])

    def _doCheckGlobalVariable(self, line, content):
        content, status = self._commonLinePreprocess(content)
        if not status:
            return
        if not (self._commonFindInvalidCodeLine(content) or \
                (content.find(u".") == 0) or \
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
                    self._printCommonError(line, u"This global variable <" + variable + u"> is not named after CamelCase")
                    return

    def _isValidFunctionName(self, function):
        return self._isPascalNamingStyle(function) or self._isLinuxUnderlineNamingStyle(function)

    def _doCheckCode(self, line, content):
        content, status = self._commonLinePreprocess(content)
        if not status:
            return
        if not self._commonFindInvalidCodeLine(content):
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
                        self._printCommonError(line, u"This function <" + function + u"()> starts with '_' or it is not named after Pascal / Linux style")
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
            blankLines = 0
            isSegmentFound = False
            segmentType = None
            for lineContent in fileObj.readlines():
                lineCount += 1
                #self.textEdit_log.insertPlainText("Line " + str(lineCount) + lineContent)
                if lineContent == u"\n":
                    blankLines += 1
                elif isSegmentFound:
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
                        #self.textEdit_log.insertPlainText("_doCheckDefinition(): \n")
                        self._doCheckDefinition(lineCount, lineContent)
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
            self.textEdit_log.append(u"")
            self.totalCodeLines += lineCount - blankLines
            self._updateTotalCodeLines()

    def _doCheckHeaderFile(self, headerFilename):
        self._checkSegments(headerFilename, kFileType_Header)
        with open(headerFilename, mode="r", encoding="utf-8") as fileObj:
            lineCount = 0
            blankLines = 0
            isSegmentFound = False
            segmentType = None
            for lineContent in fileObj.readlines():
                lineCount += 1
                #self.textEdit_log.insertPlainText("Line " + str(lineCount) + lineContent)
                if lineContent == u"\n":
                    blankLines += 1
                elif isSegmentFound:
                    isSegmentFound = False
                    if lineContent.find(self.definitionMagic) != -1:
                        segmentType = kSegmentType_Definition
                    elif lineContent.find(self.apiMagic) != -1:
                        segmentType = kSegmentType_API
                    else:
                        pass
                elif lineContent.find(self.segmentMagicStart) != -1:
                     isSegmentFound = True
                else:
                    if segmentType == kSegmentType_Definition:
                        #self.textEdit_log.insertPlainText("_doCheckDefinition(): \n")
                        self._doCheckDefinition(lineCount, lineContent)
                    elif segmentType == kSegmentType_API:
                        pass
                    else:
                        pass
            fileObj.close()
            self.textEdit_log.append(u"")
            self.totalCodeLines += lineCount - blankLines
            self._updateTotalCodeLines()

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

    def _showPassRate(self):
        rate = int(self.totalErrorLines * 100 / self.totalCodeLines)
        self.lcdNumber_passRate.display(100 - rate)

    def callbackDoCheck(self):
        self.textEdit_log.clear()
        if self.fileFolderName != None:
            self.totalErrorLines = 0
            self.totalCodeLines = 0
            self._updateTotalErrorLines()
            self._updateTotalCodeLines()
            if os.path.isdir(self.fileFolderName):
                for root, dirs, files in os.walk(self.fileFolderName, topdown=True):
                    for name in files:
                        self._detectFileType(os.path.join(root, name))
            else:
                self._detectFileType(self.fileFolderName)
            self._showPassRate()

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