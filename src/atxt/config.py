#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:51:26
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-25 16:49:19


from log_conf import Logger
log = Logger.log

import os
import sys

from os.path import join

basedir_ = os.path.abspath(__file__)


class Office(object):

    @property
    def msword(self):
        return self._msword

    def __init__(self, msword=None):
        if isinstance(msword, bool):
            try:
                self._msword = self.open()
            except ImportError, e:
                log.error('word office doesnt run. %s' % e)
        else:
            self._msword = msword

    def open(self):
        try:
            log.debug('calling win32 package')
            from win32com import client
        except ImportError, e:
            log.error(e)
            raise e
        try:
            self._msword = client.DispatchEx('Word.Application')
            self._msword.Visible = False
        except Exception, e:
            log.critical('impossible dispatching msword')
            raise e
        log.debug('successful dispatching of msword')
        return self._msword

    def close(self):
        log.debug('closing msword')
        try:
            self._msword.Quit()
        except Exception, e:
            log.debug('fail to close msword: %s'%e)

class Config(object):

    @property
    def HOME_PATH(self):
        return os.path.expanduser('~')

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
            return join(self._XPDF_PATH, 'pdftotext.exe')
        return 'pdftotext'

    @property
    def pdftopng(self):
        if sys.platform in ['win32']:
            return join(self._XPDF_PATH, 'pdftopng.exe')
        return 'pdftotext'

    @property
    def pdffonts(self):
        if sys.platform in ['win32']:
            return join(self._XPDF_PATH, 'pdffonts.exe')
        return 'pdftotext'


    @property
    def tesseract(self):
        if str(os.name) == 'nt':  # windows 7 or later
            return 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
        return 'tesseract'

    @property
    def antiword(self):
        return 'antiword'

    def __init__(self, path_bin=None):
        self._LANG = 'es'
        self._USE_TEMP_FILES = True
        self._USE_MSWORD = False

        self._TESSERACT_VERSION = '3.02.02'
        self._XPDF_VERSION = '3.04'
        if not path_bin:
            self._PATH_BIN = basedir_
        self.__XPDF_PATH = join(self._PATH_BIN, 'bin', 'win', 'bin32')
