#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 11:31:53
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-20 12:15:15

import os
import sys

from log_conf import Logger
log = Logger.log

from infofile import InfoFile
from config import Config
from utils import extract_ext, make_dir

from formats import convert, supported_formats


class aTXT(object):

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
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        self._encoding = value

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
                    utils.make_dir(value)
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
        self._encoding = 'utf-8'
        self._tempfile = None

        log.debug('ready to start atxt conversion')

    def options(self):
        opt = {
            'overwrite': self._overwrite,
            'uppercase': self._uppercase,
            'savein': self._savein,
            'encoding': self._encoding,
            'lang': self._lang,
            'hero_docx': self._hero_docx,
            'hero_pdf': self._hero_pdf,
            'lang': self._lang,
            'use_temp': self._use_temp
        }
        return opt

    def convert_to_txt(self, filepath='', opts=None):
        log.info("processing %s" % filepath)
        _file = InfoFile(filepath, check=True)
        if _file.extension not in supported_formats:
            log.warning('%s is not supported yet.')
            return None
        _txt = None
        try:
            _txt = InfoFile(
                os.path.join(self._savein,  _file.name + '.txt'), check=False)
        except OSError, e:
            log.critical('extraction metadata fails: %e' % e)
            raise e

        if not self._overwrite and os.path.exists(_txt.path):
            return _txt.path

        opts = opts or self.options()
        if self._use_temp:
            _file.create_temp()
            _tempfile = InfoFile(_file.temp)
            try:
                convert(from_file=_tempfile, to_txt=_txt, opts=opts)
            except Exception, e:
                log.critical(e)
            _file.remove_temp()
        else:
            try:
                convert(from_file=_file, to_txt=_txt, opts=opts)
            except Exception, e:
                log.critical(e)
        return _txt.path
