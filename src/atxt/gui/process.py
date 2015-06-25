#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:16:24
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-25 00:58:24
import os
from PySide import QtCore
from atxt.log_conf import Logger
log = Logger.log

from atxt.workers import run_one_file
from atxt.lib import aTXT
from atxt.walking import walking as wk
import shutil as sh


class Process(QtCore.QThread):
    # _end_process = QtCore.Signal(bool)
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

        opts = self.window.options()
        try:
            if not os.path.exists(opts['path']):
                log.critical("Directory does not exist. Please give one.")
        except Exception, e:
            log.critical("Fail review directory of search: %s" % e)
            return

        manager = aTXT()
        manager.options = opts

        conta = 0
        sucessful_files = 0
        assert len(opts['<path>']) == 1

        for root, _, files in wk.walk(
                opts['<path>'][0],
                level=opts['--depth'],
                tfiles=opts['tfiles']):

            if not self.FLAG:
                log.debug("Process stopped.")
                return

            log.debug("Process has been started on directory:")

            for f in files:
                file_path = os.path.join(root, f.name)
                res = run_one_file(manager, file_path)
                if res and len(res) == 2:
                    conta += res[0]
                    if res[1] == 1:
                        sucessful_files += 1

        log.debug("Process finished")
        log.info("Total Files: %s" % str(conta))
        log.info("Files Finished: %s" % str(sucessful_files))
        log.info("Files Unfinished: %s" % str(conta - sucessful_files))

        self.window._btn_start.setEnabled(True)
        self.window._btn_scan.setEnabled(True)
        self.window._btn_stop.setEnabled(False)
        self.exit()
        return
