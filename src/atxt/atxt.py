#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 11:31:53
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 14:59:38

import os
import sys

from log_conf import Logger
log = Logger.log

from infofile import InfoFile
from config import Config, Office
from utils import extract_ext

import formats


class aTXT:

    @property
    def uppercase(self):
        return self._uppercase

    @uppercase.setter
    def uppercase(self, value):
        self._uppercase = value

    @property
    def overwrite(self):
        return self._overwrite

    @overwrite.setter
    def overwrite(self, value):
        self._overwrite = value

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

    @property
    def use_temp(self):
        return self._use_temp

    @use_temp.setter
    def use_temp(self, value):
        self._use_temp = value

    @property
    def savein(self):
        return self._savein

    @savein.setter
    def savein(self, value):
        if not os.path.isdir(value):
            log.debug('directory save in is not a directory')
            log.debug('savein option set by default: %s' % self._savein)
        else:
            # TODO consider value as TXT or a
            log.debug('trying to set savein')
            if not os.path.exists(value):
                try:
                    make_dir(value)
                except Exception, e:
                    log.warning(e)
                    return None
            self._savein = value
            log.debug('savein: %s' % value)
        return self._savein

    @property
    def hero_pdf(self):
        return self._hero_pdf

    @hero_pdf.setter
    def hero_pdf(self, value):
        self._foo = value

    @property
    def hero_docx(self):
        return self._hero_docx

    @hero_docx.setter
    def hero_docx(self, value):
        self._hero_docx = value

    @property
    def txt(self):
        return self._txt

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file_path):
        log.debug('set file')
        self._file = InfoFile(file_path)
        log.debug('txt file will be save in', self._savein)
        txt_path = os.path.join(self._savein,  self._file.name + '.txt')
        try:
            self._txt = InfoFile(txt_path)
        except Exception, e:
            log.critical('txt file creation fail: %e' % e)

    @property
    def msword(self):
        return self._msword

    @msword.setter
    def msword(self, msword=False):
        if msword:
            if isinstance(msword, bool):
                try:
                    self._msword = self._config.word()
                except ImportError, e:
                    log.error('word office doesnt run. %s' % e)
        self._msword = msword

    def __init__(self):

        log.debug('atxt configuring settings')

        self._config = Config()

        self._overwrite = 1
        self._uppercase = 0
        self._savein = 'TXT'
        self._hero_docx = 'xml'
        self._hero_pdf = 'xpdf'
        self._lang = 'spa'
        self._use_temp = 1

        log.debug('ready to start any conversion')

    def options(self):
        opt = {
            'overwrite': self._overwrite,
            'uppercase': self._uppercase,
            'savein': self._savein,
            'encoding': self.encoding,
            'hero_docx': self._hero_docx,
            'hero_pdf': self._hero_pdf,
            'lang': self._lang,
            'use_temp': self._use_temp
        }
        return opt

    def convert_to_txt(self, filepath=''):
        self.file = filepath
        if self._use_temp:
            try:
                self.file.create_temp()
            except Exception, e:
                log.warning(e)
                return None

        log.debug('starting conversion of file %s' % self.file.basename)
        formats.convert(self.file, self.txt, self.options())
        log.info('successful conversion %s' % self.txt.path)

        if self._use_temp:
            try:
                self.file.remove_temp()
            except Exception, e:
                log.warning(e)
                return None

        return self.txt.path
