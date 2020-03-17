#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

kRevision_1_0_en   =  "【v0.2】 \n" + \
                      "  Feature: \n" + \
                      "     1. Can select file or folder to check \n" + \
                      "     2. Auto detect .c/.h file, and the file should be utf-8/ascii encoded \n" + \
                      "     3. Can show statistical info of check results \n" + \
                      "     4. Can check general comment (Defintions/Variables/Prototypes/Code/API) \n" + \
                      "     5. Can check global variable name \n" + \
                      "     6. Can check function name \n" + \
                      "     7. Can check macro name \n" + \
                      "     8. Can check enumeration name \n" + \
                      "     9. Can check struct name \n\n"

kMsgLanguageContentDict = {
        'homePage_title':                     ['Home Page'],
        'homePage_info':                      ['https://github.com/JayHeng/MCUX-SDK-Coding-Style.git \n'],
        'aboutAuthor_title':                  ['About Author'],
        'aboutAuthor_author':                 [u"Author:  痞子衡 \n" + \
                                               u"Email:     jie.heng@nxp.com \n" + \
                                               u"Email:     hengjie1989@foxmail.com \n" + \
                                               u"Blog:      痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n"],
        'revisionHistory_title':              ['Revision History'],
        'revisionHistory_v1_0':               [kRevision_1_0_en],

}