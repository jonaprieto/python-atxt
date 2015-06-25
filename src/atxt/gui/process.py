#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:16:24
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-25 10:49:30
import os
from PySide import QtCore
from atxt.log_conf import Logger
log = Logger.log

from atxt.workers import run_files, run_paths, run_one_file
from atxt.lib import aTXT
import atxt.walking as wk
import shutil as sh


class Process(QtCore.QThread):
    # _end_process = QtCore.Signal(bool)
    _cursor_end = QtCore.Signal(bool)  # for the textbox

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

        manager = aTXT()
        manager.options = opts
        opts = manager.options

        for k in opts.keys():
            log.critical((k, opts[k]))

        res = 0
        total = 0
        finished = 0

        assert len(opts['<path>']) == 1

        if manager.options['--file']:
            res = run_files(manager)
            if res and len(res) == 2:
                total += res[0]
                finished += res[1]

        if manager.options['--path']:
            res = run_paths(manager, self)
            if res and len(res) == 2:
                total += res[0]
                finished += res[1]

        # for root, _, files in wk.walk(
        #         opts['<path>'][0],
        #         level=opts['--depth'],
        #         tfiles=opts['tfiles']):

        #     log.critical(root)
        #     if not self.FLAG:
        #         log.debug("Process stopped.")
        #         return

        #     log.debug("Process has been started on directory:")

        #     for f in files:
        #         file_path = os.path.join(root, f.name)
        #         log.critical(file_path)
        #         res = run_one_file(manager, file_path)
        #         if res and len(res) == 2:
        #             total += res[0]
        #             if res[1] == 1:
        #                 finished += 1

        log.debug("Process finished")
        log.info("Total Files: %s" % str(total))
        log.info("Files Finished: %s" % str(finished))
        log.info("Files Unfinished: %s" % str(total - finished))

        self._cursor_end.emit(True)
        self.window._btn_start.setEnabled(True)
        self.window._btn_scan.setEnabled(True)
        self.window._btn_stop.setEnabled(False)
        self.exit()
        return
