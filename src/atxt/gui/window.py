#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:17:55
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-21 14:16:52

import sys
from atxt.log_conf import Logger
log = Logger.log

from PySide import QtGui, QtCore


class Window(QtGui.QWidget):
    checked = QtCore.Qt.Checked
    unchecked = QtCore.Qt.Unchecked
    debug = True
    totalfiles = 0
    totalsize = 0

    def __init__(self, manager=None):
        super(Window, self).__init__()
        log.debug('GUI aTXT')
        self.config()
        self.putBoxDirectory()
        self.putBoxOptions()
        self.setLayout(self.layout)

    def config(self):
        self.setWindowTitle("aTXT: Data Mining Tool to Extract Text")
        self.setFixedSize(650, 600)
        self.setContentsMargins(15, 15, 15, 15)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addStretch(1)

    def putBoxDirectory(self):
        self.buttonDirectory = QtGui.QPushButton("Browser")
        self.buttonDirectory.clicked.connect(self.findDirectory)
        self.directoryLabel = QtGui.QLineEdit()
        self.directoryLabel.setText(homeDirectory)

        self.directoryLabel.setFixedSize(280, 20)
        self.directoryLabel.setAlignment(QtCore.Qt.AlignRight)

        self.boxDirectoryLayout = QtGui.QGridLayout()
        self.boxDirectoryLayout.addWidget(self.directoryLabel, 0, 1)
        self.boxDirectoryLayout.addWidget(self.buttonDirectory, 0, 0)

        label = QtGui.QLabel()
        label.setText("Level:")

        self.depth_search = QtGui.QSpinBox()
        self.depth_search.setMinimum(0)
        self.depth_search.setMaximum(100)
        # self.depth_search.setValue(1)
        self.depth_search.setFixedSize(50, 25)

        self.boxDirectoryLayout.addWidget(label, 0, 4)
        self.boxDirectoryLayout.addWidget(self.depth_search, 0, 5)

        self.boxDirectory = QtGui.QGroupBox("Directory")
        self.boxDirectory.setLayout(self.boxDirectoryLayout)
        self.layout.addWidget(self.boxDirectory)

    def closeEvent(self, event):
        self.debug("Exit")
        event.accept()

    def findDirectory(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                                                           "Select Root Directory",
                                                           self.directoryLabel.text(), options)
        if directory:
            self.directoryLabel.setText(directory)

    def setDirectorySaveIn(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                                                           "Save In",
                                                           self.saveinLabel.text(), options)
        if directory:
            self.saveinLabel.setText(directory)

    def putBoxOptions(self):
        # TYPE FILES
        self.checkPDF = QtGui.QCheckBox(".pdf")
        self.checkPDF.setCheckState(self.checked)

        self.heroPDF = QtGui.QComboBox()
        self.heroPDF.addItems(['xpdf', 'pdfminer'])

        self.checkDOCX = QtGui.QCheckBox(".docx")
        self.checkDOCX.setCheckState(self.checked)

        self.checkDAT = QtGui.QCheckBox(".dat")
        self.checkDAT.setCheckState(self.checked)

        self.checkHTML = QtGui.QCheckBox(".html")
        self.checkHTML.setCheckState(self.checked)

        self.heroDOCX = QtGui.QComboBox()
        self.heroDOCX.addItems(['xml', 'python-docx'])
        self.checkDOC = QtGui.QCheckBox(".doc")
        self.checkDOC.setCheckState(self.checked)

        if sys.platform not in ["win32"]:
            self.checkDOC.setCheckState(self.unchecked)
            self.checkDOC.setEnabled(False)

        layout = QtGui.QGridLayout()

        layout.addWidget(QtGui.QLabel("Type"), 0, 0)
        layout.addWidget(QtGui.QLabel("Library"), 0, 1)
        layout.addWidget(self.checkPDF, 1, 0)
        layout.addWidget(self.heroPDF, 1, 1)
        layout.addWidget(self.checkDOCX, 2, 0)
        layout.addWidget(self.heroDOCX, 2, 1)
        layout.addWidget(self.checkDOC, 3, 0)
        layout.addWidget(self.checkDAT, 4, 0)
        layout.addWidget(self.checkHTML, 5, 0)

        self.boxTypeFiles = QtGui.QGroupBox("Types Files")
        self.boxTypeFiles.setLayout(layout)

        self.gridSettings = QtGui.QGridLayout()
        self.gridSettings.addWidget(self.boxTypeFiles, 0, 0)

        # SETTINGS
        self.checkUPPER_CASE = QtGui.QCheckBox("Content in Upper Case")

        self.saveinL = QtGui.QLabel("Save In:")
        self.saveinLabel = QtGui.QLineEdit("TXT")
        self.saveinLabel.setFixedSize(100, 20)
        self.saveinLabel.setToolTip("aTXT creates new folder\
            for each one that contains files of the search.")
        self.saveinBrowser = QtGui.QPushButton("...")
        self.saveinBrowser.clicked.connect(self.setDirectorySaveIn)

        self.checkOverwrite = QtGui.QCheckBox("Overwrite Files")
        self.checkOverwrite.setToolTip(
            "Dont process file if txt version exists")
        self.checkOverwrite.setCheckState(self.checked)
        # debug
        self.checkClean = QtGui.QCheckBox("Clean Directory")
        self.checkClean.setToolTip("Remove Directories with name above enter")
        self.checkClean.setCheckState(self.unchecked)
        self.checkClean.setVisible(False)

        self.checkDebug = QtGui.QCheckBox("Debug")
        self.checkDebug.setCheckState(self.checked)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.checkOverwrite, 0, 0)
        layout.addWidget(self.checkUPPER_CASE, 1, 0)
        layout.addWidget(self.saveinL, 3, 0)
        layout.addWidget(self.saveinLabel, 3, 1)
        layout.addWidget(self.saveinBrowser, 3, 2)
        layout.addWidget(self.checkDebug, 5, 0)
        layout.addWidget(self.checkClean, 5, 1)

        self.boxSettings = QtGui.QGroupBox("Settings")
        self.boxSettings.setLayout(layout)

        self.gridSettings.addWidget(self.boxSettings, 0, 1)
        self.layout.addLayout(self.gridSettings)

        # DETAILS

        self.progress_bar = QtGui.QProgressBar()
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self.current_process = QtGui.QTextEdit()
        self.current_process.setFrameStyle(frameStyle)

        self.boxDetails = QtGui.QGroupBox("Details")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.current_process)
        self.boxDetails.setLayout(layout)
        self.layout.addWidget(self.boxDetails)

        # ACTIONS
        self.buttonReset = QtGui.QPushButton("Reset")
        self.buttonReset.clicked.connect(self.resetOptions)

        self.buttonScan = QtGui.QPushButton("Scan")
        self.buttonScan.clicked.connect(self.scanDir)

        self.buttonStop = QtGui.QPushButton("Stop")
        self.buttonStop.setEnabled(False)
        self.buttonStop.clicked.connect(self.stopProcess)

        self.buttonStart = QtGui.QPushButton("Execute")
        self.buttonStart.setEnabled(False)
        self.buttonStart.clicked.connect(self.startProcess)

        box = QtGui.QGroupBox("Actions")
        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.addWidget(self.buttonReset, 0, 0)
        layout.addWidget(self.buttonScan, 0, 1)
        layout.addWidget(self.buttonStop, 0, 5)
        layout.addWidget(self.buttonStart, 0, 6)
        box.setLayout(layout)
        self.layout.addWidget(box)

    def resetOptions(self):
        self.setEnabled(True)
        self.depth_search.setValue(0)
        self.setProgress(0)
        self.checkPDF.setCheckState(self.checked)
        self.checkDOCX.setCheckState(self.checked)
        self.checkDAT.setCheckState(self.checked)

        self.checkDOC.setCheckState(self.checked)
        if sys.platform not in ["win32"]:
            self.checkDOC.setCheckState(self.unchecked)
            self.checkDOC.setEnabled(False)

        self.checkOverwrite.setCheckState(self.checked)
        # self.saveinLabel.setText("TXT")
        self.checkClean.setCheckState(self.unchecked)
        self.checkDebug.setCheckState(self.checked)
        self.checkUPPER_CASE.setCheckState(self.unchecked)
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)
        self.buttonScan.setEnabled(True)
        self.current_process.setText("")

    def fileCount(self, value):
        self.totalfiles = value

    def sizeCount(self, value):
        self.totalsize = value

    def pathCount(self, s):
        try:
            self.listfiles.append(s)
        except:
            self.listfiles = []
            self.listfiles.append(s)

    def scanDir(self):
        log.debug("\nfrom scanDir", "starting scanning")
        self.progress_bar.setValue(0)

        self.directory = self.directoryLabel.text()

        log.debug("directory:" + self.directory)

        self.level = self.depth_search.text()
        try:
            self.level = int(self.level)
        except:
            log.debug('Fail casting for number level')

        log.debug("level:" + str(self.level))

        self.tfiles = []
        if self.checkPDF.isChecked():
            self.tfiles.append('.pdf')
        if self.checkDOCX.isChecked():
            self.tfiles.append('.docx')
        if self.checkDOC.isChecked():
            self.tfiles.append('.doc')
        if self.checkDAT.isChecked():
            self.tfiles.append('.dat')
        if self.checkHTML.isChecked():
            self.tfiles.append('.html')

        log.debug("tfiles:", self.tfiles)

        self.setStatus('Calculating the total size of files ...')
        self.totalfiles, self.totalsize = [0] * 2
        self.listfiles = []

        if len(self.tfiles) > 0:
            log.debug('Starting Walking over Directory')
            self.thread = WalkSize(self)
            self.thread.partDone.connect(self.setProgress)
            self.thread.procDone.connect(self.fin)
            self.thread.Ready.connect(self.Ready)

            self.thread.message.connect(self.setStatus)
            self.thread.fileCount.connect(self.fileCount)
            self.thread.sizeCount.connect(self.sizeCount)
            self.thread.pathCount.connect(self.pathCount)

            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(100)
            self.thread.start()

        log.debug("Options:")
        self.savein = self.saveinLabel.text()

        log.debug('savein:' + self.savein)

        self.heroes = [self.heroPDF.currentText(), self.heroDOCX.currentText()]
        log.debug('heroes: ' + str(self.heroes))

        log.debug('debug: ' + str(self.debug))

        self.clean = self.checkClean.isChecked()
        log.debug('clean: ' + str(self.clean))

        self.uppercase = self.checkUPPER_CASE.isChecked()
        log.debug("uppercase: " + str(self.uppercase))

        self.overwrite = self.checkOverwrite.isChecked()
        log.debug('overwrite: ' + str(self.overwrite))
        return

    def Ready(self):

        self.debug("Ready")
        self.debug("Total Files: " + str(self.totalfiles))
        self.debug("Total Size: " + wk.size_str(self.totalsize))
        self.debug("Type Files: " + str(self.tfiles))

        try:
            self.stopProcess()
        except:
            pass
        try:
            del self.thread
        except:
            pass

        if self.totalfiles > 0:
            self.buttonStop.setEnabled(False)
            self.buttonScan.setEnabled(False)
            self.buttonStart.setEnabled(True)
        else:
            self.buttonScan.setEnabled(True)
            self.buttonReset.setEnabled(True)
        return

    def stopProcess(self):
        try:
            self.thread.FLAG = False
            self.thread.terminate()
            if self.thread.isRunning():
                self.stopProcess()
                return
            self.buttonStop.setEnabled(False)
            self.buttonScan.setEnabled(True)
            self.buttonReset.setEnabled(True)
            self.boxDetails.setEnabled(True)
            self.progress_bar.reset()
            # self.progress_bar.setEnabled(False)
        except:
            pass
        self.setEnabled(True)
        return

    def startProcess(self):
        if len(self.listfiles) == 0:
            self.debug("There's not nothing to convert.")
            self.buttonStart.setEnabled(False)
            return
        try:
            del self.thread
        except:
            pass

        self.thread = ProcessLib(self)
        self.thread.partDone.connect(self.setProgress)
        self.thread.procDone.connect(self.fin)
        self.thread.message.connect(self.setStatus)
        self.buttonStop.setEnabled(True)
        self.buttonScan.setEnabled(False)
        self.buttonReset.setEnabled(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.thread.start()
        self.setEnabled(False)
        return

    def setEnabled(self, value):
        self.boxDirectory.setEnabled(value)
        self.boxSettings.setEnabled(value)
        self.boxTypeFiles.setEnabled(value)
        return

    def setStatus(self, menssage):
        if self.checkDebug.isChecked():
            self.current_process.append(menssage)
        else:
            self.current_process.setText(menssage)
        self.current_process.moveCursor(QtGui.QTextCursor.End)

    def setProgress(self, value):
        if value > 100:
            value = 100
        self.progress_bar.setValue(value)

    def fin(self):
        self.progress_bar.reset()
        self.stopProcess()
