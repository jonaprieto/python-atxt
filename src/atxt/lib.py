#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import os
import sys

from log_conf import Logger
log = Logger.log

from infofile import InfoFile
from config import Config
from utils import extract_ext, make_dir, parser_opts
from encoding import encoding_path
from formats import convert, supported_formats


class aTXT(object):
    opts = dict()

    @property
    def uppercase(self):
        return self.opts['-u']

    @uppercase.setter
    def uppercase(self, value):
        self.opts['-u'] = value

    @property
    def overwrite(self):
        return self.opts['-o']

    @overwrite.setter
    def overwrite(self, value):
        self.opts['-o'] = value

    @property
    def lang(self):
        return self.opts['--lang']

    @lang.setter
    def lang(self, value):
        self.opts['--lang'] = True

    @property
    def use_temp(self):
        return self.opts['--use-temp']

    @use_temp.setter
    def use_temp(self, value):
        self.opts['--use-temp'] = value

    @property
    def encoding(self):
        return self.opts['--enc']

    @encoding.setter
    def encoding(self, value):
        self.opts['--enc'] = value

    @property
    def to(self):
        return self.opts['--to']

    @to.setter
    def to(self, value):
        if not os.path.isdir(value):
            log.debug('directory save in is not a directory')
            log.debug('--to option set by default: %s' % self.opts['--to'])
        else:
            log.debug('trying to set --to')
            if not os.path.exists(value):
                try:
                    utils.make_dir(value)
                except Exception, e:
                    log.warning(e)
                    return
            self.opts['--to'] = value
            log.debug('--to: %s' % value)
        return self.opts['--to']

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
        self.opts['msword'] = msword

    def __init__(self):

        log.debug('atxt is setting')
        self._config = Config()
        self.opts = {
            '-u': False,
            '-o': True,
            '--to': 'TXT',
            '--lang': 'spa',
            '--use-temp': True,
            '--enc': 'utf-8',
            '--file': False,
            '<file>': None,
            '--path': False,
            '<path>': None,
            '<source>': None
        }
        self._hero_docx = 'xml'
        self._hero_pdf = 'xpdf'
        self._tempfile = None
        log.debug('ready to start atxt conversion')

    @property
    def options(self):
        extra_opts = {
            'hero_docx': self._hero_docx,
            'hero_pdf': self._hero_pdf,
        }
        x = self.opts.copy()
        x.update(extra_opts)
        return x

    @options.setter
    def options(self, opts):
        self.opts.update(parser_opts(opts))

    def convert_to_txt(self, filepath='', opts=None):
        opts = opts or self.options

        _file = InfoFile(filepath, check=True)
        log.debug("file name: %s" % _file)
        if _file.extension not in supported_formats:
            log.warning('%s is not supported yet.' % _file.extension)
            return
        _txt = None
        try:
            _txt = InfoFile(
                os.path.join(self.opts['--to'], _file.name + '.txt'))
        except OSError, e:
            log.critical('extraction metadata fails: %e' % e)
            raise e
            log.critical(opts)

        if not self.opts['-o'] and os.path.exists(_txt.path):
            return _txt.path

        res = None
        if self.opts['--use-temp']:
            try:
                _file.create_temp()
            except Exception, e:
                log.critical(e)
            try:
                _tempfile = InfoFile(_file.temp)
            except Exception, e:
                log.critical(e)
            try:
                res = convert(from_file=_tempfile, to_txt=_txt, opts=opts)
            except Exception, e:
                log.critical('conversion fails (--use-temp): %e' % e)
            try:
                _file.remove_temp()
            except Exception, e:
                log.critical(e)
        else:
            try:
                res = convert(from_file=_file, to_txt=_txt, opts=opts)
            except Exception, e:
                log.critical('conversion fails: %e' % e)
        if not res:
            raise IOError('problems with I/O reading file')
            return None
        return _txt.path
