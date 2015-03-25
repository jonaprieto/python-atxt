#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:17:19
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-20 23:34:23
import os
from atxt.log_conf import Logger
log = Logger.log
from PySide import QtCore


class WalkSize(QtCore.QThread):
    procDone = QtCore.Signal(bool)
    partDone = QtCore.Signal(int)
    message = QtCore.Signal(str)
    fileCount = QtCore.Signal(int)
    sizeCount = QtCore.Signal(str)
    pathCount = QtCore.Signal(str)
    Ready = QtCore.Signal(bool)

    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):

        log.debug('created QThread for WalkSize')

        self.window.buttonStart.setEnabled(False)
        self.window.buttonStop.setEnabled(True)

        log.debug('Trasversing directory')

        self.partDone.emit(0)

        try:
            if not os.path.exists(self.window.directory):
                log.debug("Directory does not exist")
            else:
                log.debug('Directory is valid')
        except:
            log.debug("Fail review directory of search")
            return

        dir = enconding_path(self.window.directory)
        sdirs = []
        level = self.window.level
        tfiles = self.window.tfiles

        self.sizeCount.emit(0)
        self.fileCount.emit(0)

        conta = 0
        tsize = 0
        factor = 0.1 if level != 0 else 0.01 * level
        log.debug("wk.walk starting")
        for root, dirs, files in wk.walk(dir, sdirs=sdirs, level=level, tfiles=tfiles):
            if not self.FLAG:
                log.debug("Process stopped.")
                self.partDone(0)
                self.procDone(True)
                return

            for f in files:
                conta += 1
                self.partDone.emit(conta * factor)
                log.debug("File #" + str(conta))

                filepath = os.path.join(root, f.name)
                filepath = enconding_path(filepath)
                tsize += os.path.getsize(filepath)
                self.pathCount.emit(filepath)

                log.debug("path: " + filepath)

        log.debug("wk.walk Finish")

        self.partDone.emit(100)
        self.fileCount.emit(conta)
        self.sizeCount.emit(str(tsize))

        self.procDone.emit(True)
        self.Ready.emit(True)
        self.exit()
        return
