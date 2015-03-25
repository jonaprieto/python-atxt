#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:16:24
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-25 16:35:35
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

        try:
            if not os.path.exists(self.window.directory):
                log.debug("Directory does not exist")
        except Exception, e:
            log.debug("Fail review directory of search")
            return None

        manager = aTXT()
        conta = 0
        sucessful_files = 0
        unsucessful_files = []

        for root, dirs, files in wk.walk(
                self.window.directory,
                level=self.window.level,
                tfiles=self.window.tfiles):

            if not self.FLAG:
                log.debug("Process stopped.")
                self.partDone(0)
                self.procDone(True)
                return

            log.debug('Directory: ' + root)

            try:
                if os.path.isdir(self.window.savein):
                    savein = os.path.join(root, self.window.savein)
                else:
                    savein = self.window.savein
            except Exception, e:

                log.debug("Something wrong with `savein` path: ")
                log.debug(savein)
                log.debug(e)

            try:
                if self.window.clean and os.path.exists(savein):
                    log.debug("Cleaning directory of " + savein)
                    sh.rmtree(savein)
                    log.debug("Remove " + savein + " DONE")
            except Exception, e:
                log.debug("Fail remove " + savein)

            if self.window.clean:
                continue

            log.debug("Starting process over files in Directory:")

            for f in files:
                conta += 1
                try:
                    porc = conta * 100.0
                    porc /= self.window.totalfiles
                except Exception, e:
                    log.debug(e)
                    porc = 0

                filepath = os.path.join(root, f.name)
                log.debug("File #" + str(conta))
                log.debug("Filepath: " + filepath)

                try:
                    log.debug('Converting File ... ')

                    if filepath.lower().endswith('.pdf'):
                        log.debug(
                            'It\'ll take few seconds or minutes (OCR)')
                        log.debug('Please Wait')

                    newpath = manager.convert(
                        filepath=filepath,
                        uppercase=self.window.uppercase,
                        overwrite=self.window.overwrite,
                        savein=self.window.savein
                    )
                    if newpath != '':
                        sucessful_files += 1
                    else:
                        unsucessful_files.append(filepath)
                        self.message.emit(
                            "Impossible process: " + str(filepath))

                except Exception, e:
                    log.debug('Fail conversion aTXT calling from GUI.py')
                    log.debug(e)
                    log.debug("*" * 50)
                self.partDone.emit(porc)
                log.debug("File finished")

        log.debug("Process finished")
        self.partDone.emit(100)

        self.message.emit("Total Files: " + str(conta))
        self.message.emit("Files Finished: " + str(sucessful_files))
        self.message.emit("Files Unfinished: " + str(conta - sucessful_files))

        try:
            manager.close()
        except Exception, e:
            log.debug(e)
        self.procDone.emit(True)
        self.exit()
        return None
