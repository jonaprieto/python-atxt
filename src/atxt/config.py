#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:51:26
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 04:34:19

"""
    Check all dependencies of aTXT
"""

from log_conf import Logger
log = Logger.log

import os
import sys

from os.path import join

basedir_ = os.path.abspath(__file__)


class Config():

    LANG = 'es'
    USE_TEMP_FILES = True
    USE_MSWORD = False

    TESSERACT_VERSION = '3.02.02'
    XPDF_VERSION = '3.04'

    PATH_BIN = basedir_
    _XPDF_PATH = join(PATH_BIN, 'bin', 'win', 'bin32')

    @property
    def PATH_BIN(self):
        return self._PATH_BIN

    @PATH_BIN.setter
    def PATH_BIN(self, value):
        self._PATH_BIN = value

    @property
    def XPDF_PATH(self):
        return self._XPDF_PATH

    @XPDF_PATH.setter
    def XPDF_PATH(self, value):
        self._XPDF_PATH = value

    @property
    def pdftotext(self):
        if sys.platform in ['win32']:
            return join(self.XPDF_PATH, 'pdftotext.exe')
        return 'pdftotext'

    @property
    def pdftopng(self):
        if sys.platform in ['win32']:
            return join(self.XPDF_PATH, 'pdftopng.exe')
        return 'pdftotext'

    @property
    def pdffonts(self):
        if sys.platform in ['win32']:
            return join(self.XPDF_PATH, 'pdffonts.exe')
        return 'pdftotext'

    @staticmethod
    def word(self):
        try:
            log.debug('calling win32 package')
            from win32com import client
        except ImportError, e:
            log.error(e)
            raise e
        try:
            msword = client.DispatchEx('Word.Application')
            msword.Visible = False
        except Exception, e:
            log.critical('dispatching word appplication problems')
            raise e
        log.debug('successful dispatching of office word application')
        return msword

    @property
    def tesseract(self):
        if str(os.name) == 'nt': # windows 7 or later
            return 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
        return 'tesseract'
