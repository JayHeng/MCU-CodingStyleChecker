#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
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
        self._register_callbacks()
        self._init_segment_magic()
        self.progressBar.reset()
        self.lcdNumber_errorRate.display(0)
        self.fileFolderName = None
        self.continuationContent = ''
        self.bracePairs = 0
        self.onProgressEnumName = u""
        self.isEnumOnProgress = False
        self.onProgressStructName = u""
        self.isStructOnProgress = False
        self.totalErrorLines = 0
        self.totalCodeLines = 0

    def _init_segment_magic(self):
        self.segmentMagicStart = u"/*******************************************************************************"
        self.definitionMagic   = u" * Definitions"
        self.variableMagic     = u" * Variables"
        self.prototypeMagic    = u" * Prototypes"
        self.codeMagic         = u" * Code"
        self.apiMagic          = u" * API"
        self.segmentMagicEnd   = u" ******************************************************************************/"

    def _register_callbacks(self):
        self.pushButton_browseFileFolder.clicked.connect(self.callbackBrowseFileFolder)
        self.pushButton_doCheck.clicked.connect(self.callbackDoCheck)
        self.pushButton_saveLog.clicked.connect(self.callbackSaveLog)
        self.actionMenuHelpHomePage.triggered.connect(self.callbackShowHomePage)
        self.actionMenuHelpAboutAuthor.triggered.connect(self.callbackShowAboutAuthor)
        self.actionMenuHelpRevisionHistory.triggered.connect(self.callbackShowRevisionHistory)

    def callbackBrowseFileFolder(self):
        if self.checkBox_isFolder.isChecked():
            self.fileFolderName = QtWidgets.QFileDialog.getExistingDirectory(self, u"Browse Folder", os.getcwd())
        else:
            self.fileFolderName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, u"Browse File", os.getcwd(), "All Files(*);;Source Files(*.c)")
        #self.fileFolderName = self.fileFolderName.encode('utf-8').encode("gbk")
        self.textEdit_inputFileFolder.setPlainText(self.fileFolderName)

    def _file_check_separator(self, filename):
        self.textEdit_log.append(u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>----------File----------<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.textEdit_log.append(u"Start to check  " + filename + "\n")

    def _is_utf8_ascii_file(self, filename):
        self._file_check_separator(filename)
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

    def _check_segment(self, content, segmentMagic):
        segment = self.segmentMagicStart + u"\n" + segmentMagic + u"\n" + self.segmentMagicEnd
        if content.find(segment) == -1:
            self.textEdit_log.append(u"【ERROR】: Below general comment is missed in the file")
            self.textEdit_log.append(segment)

    def _check_segments(self, filename, fileType):
        with open(filename, mode="r", encoding="utf-8") as fileObj:
            content = fileObj.read()
            self._check_segment(content, self.definitionMagic)
            if fileType == kFileType_Header:
                self._check_segment(content, self.apiMagic)
            elif fileType == kFileType_Source:
                self._check_segment(content, self.variableMagic)
                self._check_segment(content, self.prototypeMagic)
                self._check_segment(content, self.codeMagic)
            else:
                pass
            fileObj.close()

    def _update_total_error_lines(self):
        self.lineEdit_totalErrorLines.clear()
        self.lineEdit_totalErrorLines.setText(str(self.totalErrorLines))

    def _update_total_code_lines(self):
        self.lineEdit_totalCodeLines.clear()
        self.lineEdit_totalCodeLines.setText(str(self.totalCodeLines))

    def _print_common_error(self, line, error):
        if line != None:
            self.textEdit_log.append(u"【ERROR】 Line " + str(line) + u": " + error)
        else:
            self.textEdit_log.append(u"【ERROR】: " + error)
        self.totalErrorLines += 1
        self._update_total_error_lines()

    def _common_find_continuation_character(self, content):
        contIndex = content.rfind(u"\\\n")
        if (contIndex != -1) and (contIndex == len(content) - len(u"\\\n")):
            self.continuationContent += content[0:contIndex]
            return True
        else:
            if self.continuationContent != '':
                self.continuationContent += content
            return False

    def _common_remove_initial_blanks(self, content):
        startIndex = 0
        while True:
            if startIndex == len(content):
                return None
            elif content[startIndex] != u" ":
                break
            else:
                startIndex += 1
        return content[startIndex:len(content)]

    def _common_line_preprocess(self, content):
        if self._common_find_continuation_character(content):
            return None, False
        else:
            if self.continuationContent != '':
                content = self.continuationContent
                self.continuationContent = ''
        content = self._common_remove_initial_blanks(content)
        if content == None:
            return content, False
        else:
            return content, True

    def _common_find_invalid_code_line(self, content):
        return ((content.find(u"/*") == 0) or \
                (content.find(u"#if") == 0) or \
                (content.find(u"#else") == 0) or \
                (content.find(u"#endif") == 0))

    def _is_camel_case_naming_style(self, content):
        return ((content[0].isalpha() and content[0].islower()) and \
                (content.find(u"_") == -1))

    def _is_linux_underline_naming_style(self, content):
        return content.islower() and content[0] != u"_"

    def _is_pascal_naming_style(self, content):
        idx = content.find(u"_")
        if idx != -1:
            if (idx == 0) or (not (content[0:idx].isalpha() and content[0:idx].isupper())):
                return False
            idx += 1
        else:
            idx = 0
        return ((content[idx].isalpha() and content[idx].isupper()) and \
                (content[idx:len(content)].find(u"_") == -1))

    def _get_definition_word(self, content, startIdx, endChar):
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

    def _is_valid_macro_name(self, macro):
        return macro.isupper() and macro[0] != u"_"

    def _do_check_macro(self, line, content):
        idx = len(u"#define") - 1
        macro = self._get_definition_word(content, idx, u"(")
        if not self._is_valid_macro_name(macro):
            self._print_common_error(line, u"This macro <" + macro + u"> starts with '_' or it is not all capitalized")

    def _is_valid_enum_struct_type_name(self, mtype):
        return mtype.islower() and mtype[0] == u"_"

    def _is_valid_enum_struct_typedef_name(self, mtype):
        return mtype.islower() and mtype[0] != u"_" and mtype[len(mtype)-2:len(mtype)] == u"_t"

    def _is_valid_enumerator_name(self, enum):
        return enum[0] == u"k" and enum[1].isupper()

    def _do_check_enum(self, line, content):
        if not self.isEnumOnProgress:
            idx = content.find(u"enum") + len(u"enum") - 1
            enumType = self._get_definition_word(content, idx, u"{")
            if not self._is_valid_enum_struct_type_name(enumType):
                self._print_common_error(line, u"This enum type name <" + enumType + u"> is not valid")
            else:
                self.onProgressEnumName = enumType
                self.isEnumOnProgress = True
        else:
            if content[0] == "}":
                enumTypedef = self._get_definition_word(content, 0, u";")
                if enumTypedef[0] != u";" and (not self._is_valid_enum_struct_typedef_name(enumTypedef)):
                    self._print_common_error(line, u"This enum typedef name <" + enumTypedef + u"> is not valid")
                self.isEnumOnProgress = False
            elif content[0] != "{":
                # If first invalid enumerator is found, then it will stop checking the following enumerators (nno matter it is valid or not)
                if not self._is_valid_enumerator_name(content[0:2]):
                    self._print_common_error(line, u"This enum type <" + self.onProgressEnumName + u"> contains invalid enumerator name")
                    self.isEnumOnProgress = False

    def _is_valid_struct_member_name(self, struct):
        return self._is_valid_variable_name(struct, False)

    def _find_valid_local_variable(self, content, isBssSection=True):
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
        return self._is_valid_variable_name(variable, False)

    def _do_check_struct(self, line, content):
        if not self.isStructOnProgress:
            idx = content.find(u"struct") + len(u"struct") - 1
            structType = self._get_definition_word(content, idx, u"{")
            if not self._is_valid_enum_struct_type_name(structType):
                self._print_common_error(line, u"This struct type name <" + structType + u"> is not valid")
            else:
                self.onProgressStructName = structType
                self.isStructOnProgress = True
        else:
            if content[0] == "}":
                structTypedef = self._get_definition_word(content, 0, u";")
                if structTypedef[0] != u";" and (not self._is_valid_enum_struct_typedef_name(structTypedef)):
                    self._print_common_error(line, u"This struct typedef name <" + structTypedef + u"> is not valid")
                self.isStructOnProgress = False
            elif content[0] != "{":
                # If first invalid member is found, then it will stop checking the following member (nno matter it is valid or not)
                if not self._find_valid_local_variable(content):
                    self._print_common_error(line, u"This struct type <" + self.onProgressStructName + u"> contains invalid member name")
                    self.isStructOnProgress = False

    def _do_check_definition(self, line, content):
        content, status = self._common_line_preprocess(content)
        if not status:
            return
        if not (self._common_find_invalid_code_line(content)):
            if content.find(u"#define") == 0:
                self._do_check_macro(line, content)
            else:
                if self.isEnumOnProgress or \
                   (content.find(u"enum") == 0 or (content.find(u"typedef") == 0 and content.find(u"enum") != -1)):
                    self._do_check_enum(line, content)
                elif self.isStructOnProgress or \
                     (content.find(u"struct") == 0 or (content.find(u"typedef") == 0 and content.find(u"struct") != -1)):
                    self._do_check_struct(line, content)
                else:
                    pass

    def _is_valid_variable_name(self, variable, isGlobal):
        idx = 0
        if isGlobal:
            idx = 2
        return self._is_camel_case_naming_style(variable[idx:len(variable)])

    def _do_check_global_variable(self, line, content):
        content, status = self._common_line_preprocess(content)
        if not status:
            return
        if not (self._common_find_invalid_code_line(content) or \
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
                self._print_common_error(line, u"Only one variable can be defined per line")
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
                        self._print_common_error(line, u"A prefix 's_' is missed in the static variable <" + variable + u">")
                        return
                else:
                    if variable[0:2] != u"g_":
                        self._print_common_error(line, u"A prefix 'g_' is missed in the global variable <" + variable + u">")
                        return
                if not self._is_valid_variable_name(variable, True):
                    self._print_common_error(line, u"This global variable <" + variable + u"> is not named after CamelCase")
                    return

    def _is_valid_function_name(self, function):
        return self._is_pascal_naming_style(function) or self._is_linux_underline_naming_style(function)

    def _do_check_code(self, line, content):
        content, status = self._common_line_preprocess(content)
        if not status:
            return
        if not self._common_find_invalid_code_line(content):
            if not self.bracePairs:
                # Try to find function expression according to the first "("
                fndIndex = content.find(u"(")
                if fndIndex != -1:
                    expression = content[0:fndIndex]
                    # Try to find function name according to the last blank in function expression
                    blankIndex = expression.rfind(u" ")
                    function = expression[blankIndex+1:fndIndex]
                    #self.textEdit_log.insertPlainText("-- Find " + function + "\n")
                    if not self._is_valid_function_name(function):
                        self._print_common_error(line, u"This function <" + function + u"()> starts with '_' or it is not named after Pascal / Linux style")
            # Count the "{ }" pair, function name resides out of any pair
            if content.find(u"{") != -1:
                self.bracePairs += 1
            elif content.find(u"}") != -1:
                if self.bracePairs:
                    self.bracePairs -= 1
            else:
                pass

    def _do_check_source_file(self, sourceFilename):
        self._check_segments(sourceFilename, kFileType_Source)
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
                        #self.textEdit_log.insertPlainText("_do_check_definition(): \n")
                        try:
                            self._do_check_definition(lineCount, lineContent)
                        except:
                            pass
                    elif segmentType == kSegmentType_Variable:
                        #self.textEdit_log.insertPlainText("_do_check_global_variable(): \n")
                        try:
                            self._do_check_global_variable(lineCount, lineContent)
                        except:
                            pass
                    elif segmentType == kSegmentType_Prototype:
                        pass
                    elif segmentType == kSegmentType_Code:
                        #self.textEdit_log.insertPlainText("_do_check_code(): \n")
                        try:
                            self._do_check_code(lineCount, lineContent)
                        except:
                            pass
                    else:
                        pass
            fileObj.close()
            self.textEdit_log.append(u"")
            self.totalCodeLines += lineCount - blankLines
            self._update_total_code_lines()

    def _check_header_guard_macro(self, filename):
        with open(filename, mode="r", encoding="utf-8") as fileObj:
            name = os.path.split(filename)[1]
            name = name.upper()
            name = name.replace(u".", u"_")
            name = u"_" + name + u"_"
            magic = u"#ifndef " + name
            content = fileObj.read()
            if content.find(magic) == -1:
                self._print_common_error(None, u"<" + magic + u"> is missed in this header file")
            fileObj.close()

    def _do_check_header_file(self, headerFilename):
        self._check_header_guard_macro(headerFilename)
        self._check_segments(headerFilename, kFileType_Header)
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
                        #self.textEdit_log.insertPlainText("_do_check_definition(): \n")
                        try:
                            self._do_check_definition(lineCount, lineContent)
                        except:
                            pass
                    elif segmentType == kSegmentType_API:
                        pass
                    else:
                        pass
            fileObj.close()
            self.textEdit_log.append(u"")
            self.totalCodeLines += lineCount - blankLines
            self._update_total_code_lines()

    def _detect_file_type(self, filename):
        if os.path.isfile(filename):
            filetype = os.path.splitext(filename)[1]
            if filetype == kFileType_Header:
                if not self._is_utf8_ascii_file(filename):
                    return
                self._do_check_header_file(filename)
            elif filetype == kFileType_Source:
                if not self._is_utf8_ascii_file(filename):
                    return
                self._do_check_source_file(filename)
            else:
                pass

    def _showErrorRate(self):
        rate = self.totalErrorLines * 100.0 / self.totalCodeLines
        self.lcdNumber_errorRate.display(rate)

    def callbackDoCheck(self):
        self.textEdit_log.clear()
        if self.fileFolderName != None:
            self.totalErrorLines = 0
            self.totalCodeLines = 0
            self._update_total_error_lines()
            self._update_total_code_lines()
            if os.path.isdir(self.fileFolderName):
                for root, dirs, files in os.walk(self.fileFolderName, topdown=True):
                    for name in files:
                        self._detect_file_type(os.path.join(root, name))
            else:
                self._detect_file_type(self.fileFolderName)
            self._showErrorRate()

    def callbackSaveLog(self):
        logPath = os.path.abspath(os.path.dirname(__file__))
        logPath = os.path.join(os.path.dirname(logPath), u"log")
        logFilename = os.path.join(logPath, time.strftime('%Y-%m-%d_%Hh%Mm%Ss',time.localtime(time.time())) + '.txt')
        with open(logFilename, mode="w", encoding="utf-8") as fileObj:
            fileObj.write(self.textEdit_log.toPlainText())
            fileObj.close()
        QMessageBox.about(self, u"Info", u"Log is saved in file: " + logFilename + u"\n")

    def callbackShowHomePage(self):
        QMessageBox.about(self, uilang.kMsgLanguageContentDict['homePage_title'][0], uilang.kMsgLanguageContentDict['homePage_info'][0] )

    def callbackShowAboutAuthor(self):
        QMessageBox.about(self, uilang.kMsgLanguageContentDict['aboutAuthor_title'][0], uilang.kMsgLanguageContentDict['aboutAuthor_author'][0] )

    def callbackShowRevisionHistory(self):
        QMessageBox.about(self, uilang.kMsgLanguageContentDict['revisionHistory_title'][0], uilang.kMsgLanguageContentDict['revisionHistory_v1_0'][0] )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = checkerMain()
    main_win.setWindowTitle(u"MCUXpresso SDK Coding Style Checker v0.5")
    main_win.setWindowIcon(QIcon(u"../img/MCUX-SDK-CodingStyleChecker.ico"))
    main_win.show()
    sys.exit(app.exec_())