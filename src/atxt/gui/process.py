#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:16:24
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-24 01:10:38
import os
from PySide import QtCore
from atxt.log_conf import Logger
log = Logger.log

from atxt.lib import aTXT
from atxt.walking import walking as wk
import shutil as sh


class Process(QtCore.QThread):
    _end_process = QtCore.Signal(bool)
    _part = QtCore.Signal(int)
    _ready = QtCore.Signal(bool)
    _cursor_end = QtCore.Signal(bool)  # for the textbox
    _message = QtCore.Signal(str)
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):

        log.debug('created QThread for Process')

        self.window._btn_start.setEnabled(False)
        self.window._btn_scan.setEnabled(False)
        self.window._btn_stop.setEnabled(True)

        self._ready.emit(0)
        opts = self.window.options()
        try:
            if not os.path.exists(opts['path']):
                log.critical("Directory does not exist")
        except Exception, e:
            log.critical("Fail review directory of search: %s" % e)
            return None

        manager = aTXT()

        conta = 0
        sucessful_files = 0
        unsucessful_files = []

        for root, _, files in wk.walk(
                opts['path'],
                level=opts['depth'],
                tfiles=opts['tfiles']):

            if not self.FLAG:
                log.debug("Process stopped.")
                self._ready(0)
                self._part(True)
                return

            log.debug("Starting process over files in directory:")

            for f in files:
                conta += 1
                try:
                    porc = conta * 100.0
                    porc /= self.window.totalfiles
                except Exception, e:
                    log.debug(e)
                    porc = 0

                file_path = os.path.join(root, f.name)
                log.debug("File #" + str(conta))
                log.debug("Filepath: " + file_path)

                self._ready.emit(porc)
                log.debug("File finished")

        log.debug("Process finished")
        self._ready.emit(100)

        log.info("Total Files: %s" % str(conta))
        log.info("Files Finished: %s" % str(sucessful_files))
        log.info("Files Unfinished: %s" % str(conta - sucessful_files))

        try:
            manager.close()
        except Exception, e:
            log.debug(e)
        self._part.emit(True)
        self.window._btn_start.setEnabled(True)
        self.window._btn_scan.setEnabled(True)
        self.window._btn_stop.setEnabled(False)
        self.exit()
        return None
