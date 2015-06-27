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

    def __init__(self):

        log.debug('atxt is setting')
        self._config = Config()
        self.opts = {
            '-u': False,
            '-o': True,
            '--to': './',
            '--lang': 'spa',
            '--use-temp': True,
            '--file': False,
            '<file>': None,
            '--path': False,
            '<path>': None,
            '<source>': None,
            'hero-docx': 'xml',
            'hero-pdf': 'xpdf'
        }
        self._tempfile = None
        log.debug('ready to start atxt conversion')

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

    @property
    def options(self):
        return self.opts

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
