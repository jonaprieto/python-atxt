#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:17:19
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-26 19:59:37
import os

import logging
from atxt.log_conf import Logger
log = Logger.log

from PySide import QtCore

from atxt.encoding import encoding_path
import atxt.walking as wk


class WalkThread(QtCore.QThread):
    _end_process = QtCore.Signal(bool)
    _part = QtCore.Signal(int)
    _ready = QtCore.Signal(bool)

    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        log.debug('created QThread for WalkThread')
        opts = self.window.options()

        self.window._btn_start.setEnabled(False)
        self.window._btn_stop.setEnabled(True)

        self._part.emit(0)

        conta, tsize = 0, 0
        factor = 0.1 if opts['depth'] != 0 else 0.01 * opts['depth']

        log.debug("\n")
        for root, _, files in wk.walk(encoding_path(opts['path']),
                                      sdirs=[],
                                      level=opts['depth'],
                                      tfiles=['*']):
            if not self.FLAG:
                self._part(0)
                self._end_process(True)
                return

            for f in files:
                conta += 1
                self._part.emit(conta * factor)
                file_path = os.path.join(root, f.name)
                file_path = encoding_path(file_path)
                log.info("(%d): %s" % (conta, file_path))
                tsize += os.path.getsize(file_path)

        log.info('[number of files]: %d' % conta)
        log.info('[size on disk]: %s' % wk.size_str(tsize))

        self._part.emit(100)
        self._ready.emit(True)
        self._end_process.emit(True)
        self.exit()
