#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:16:24
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-22 18:12:39
import os
from PySide import QtCore
from atxt.log_conf import Logger
log = Logger.log

from atxt.lib import aTXT
from atxt.walking import walking as wk
import shutil as sh

homeDirectory = os.path.expanduser('~')


class ProcessLib(QtCore.QThread):
    procDone = QtCore.Signal(bool)
    partDone = QtCore.Signal(int)
    message = QtCore.Signal(str)
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):

        log.debug('created QThread for ProcessLib')

        self.window.buttonStart.setEnabled(False)
        self.window.buttonStop.setEnabled(True)

        self.partDone.emit(0)
        opts = self.window.options()
        try:
            if not os.path.exists(opst['path']):
                log.debug("Directory does not exist")
        except Exception, e:
            log.debug("Fail review directory of search")
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
                self.partDone(0)
                self.procDone(True)
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

                self.partDone.emit(porc)
                log.debug("File finished")

        log.debug("Process finished")
        self.partDone.emit(100)

        log.info("Total Files: %s" % str(conta))
        log.info("Files Finished: %s" % str(sucessful_files))
        log.info("Files Unfinished: %s" % str(conta - sucessful_files))

        try:
            manager.close()
        except Exception, e:
            log.debug(e)
        self.procDone.emit(True)
        self.exit()
        return None
