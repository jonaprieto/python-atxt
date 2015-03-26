#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:17:55
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-26 02:02:52
import os
import sys
from PySide import QtGui, QtCore
from PySide.QtGui import QFileDialog, QGridLayout, QGroupBox
from PySide.QtGui import QCheckBox, QTextBrowser, QPushButton
from walksize import WalkSize
import atxt.walking as wk
from atxt.formats import supported_formats
from constants import *

import logging
from atxt.log_conf import Logger
log = Logger.log
path_home = os.path.expanduser('~')


class QtHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('%s\n' % record)

handler = QtHandler()
log.addHandler(handler)


class XStream(QtCore.QObject):

    """ http://stackoverflow.com/questions/24469662/
    how-to-redirect-logger-output-into-pyqt-text-widget"""

    _stdout = None
    _stderr = None
    messageWritten = QtCore.Signal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if (not self.signalsBlocked()):
            self.messageWritten.emit(unicode(msg))

    @staticmethod
    def stdout():
        if (not XStream._stdout):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if (not XStream._stderr):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


checked = QtCore.Qt.Checked
unchecked = QtCore.Qt.Unchecked


class Window(QtGui.QWidget):
    layout = QGridLayout()
    _layout1 = QtGui.QVBoxLayout()
    _layout2 = QtGui.QVBoxLayout()

    def __init__(self, manager=None):
        super(Window, self).__init__()
        log.debug('GUI aTXT')
        self.set_layout1()
        self.set_layout2()
        self.actions()
        box = QGroupBox(LABEL_BOX_LAYOUT1)
        box.setLayout(self._layout1)
        self.layout.addWidget(box, 0, 0)

        box = QGroupBox(LABEL_BOX_LAYOUT2)
        box.setLayout(self._layout2)
        self.layout.addWidget(box, 0, 1)
        self.setLayout(self.layout)

        XStream.stdout().messageWritten.connect(self._console.insertPlainText)
        XStream.stderr().messageWritten.connect(self._console.insertPlainText)

    def set_layout1(self):
        self.setWindowTitle(TITLE_WINDOW)
        self.setFixedSize(850, 400)
        self.setContentsMargins(15, 15, 15, 15)
        self._layout1 = QtGui.QVBoxLayout()
        self._layout1.addStretch(1)

        self._btn1 = QtGui.QPushButton(BTN_BROWSER)
        self._edt1 = QtGui.QLineEdit()
        self._edt1.setText(path_home)
        self._edt1.setFixedSize(330, 20)
        self._edt1.setAlignment(QtCore.Qt.AlignRight)

        self._depth = QtGui.QSpinBox()
        self._depth.setMinimum(0)
        self._depth.setMaximum(100)
        self._depth.setFixedSize(50, 25)

        self._label1 = QtGui.QLabel()
        self._label1.setText(LABEL_DEPTH)

        box = QGroupBox(LABEL_BOX_DIRECTORY)
        ly = QGridLayout()
        ly.addWidget(self._btn1, 0, 0)
        ly.addWidget(self._edt1, 0, 1)
        ly.addWidget(self._label1, 0, 2)
        ly.addWidget(self._depth, 0, 3)
        box.setLayout(ly)
        self._layout1.addWidget(box)

        self._label2 = QtGui.QLabel(MSG_SAVE_IN)
        self._edt2 = QtGui.QLineEdit(NAME_FOLDER_TXT)
        self._edt2.setFixedSize(330, 20)
        self._edt2.setToolTip(TOOLTIP_SAVEIN)
        self._btn2 = QtGui.QPushButton(BTN_BROWSER)
        self._btn2.clicked.connect(self.set_directory_save_in)
        self._check1 = QtGui.QCheckBox(LABEL_OVERWRITE)
        self._check1.setToolTip(TOOLTIP_OVERWRITE)
        self._check1.setCheckState(checked)

        box = QGroupBox(LABEL_BOX_SAVE_IN)
        ly = QGridLayout()
        ly.addWidget(self._btn2, 0, 0)
        ly.addWidget(self._edt2, 0, 1)
        ly.addWidget(self._check1, 0, 2)
        box.setLayout(ly)
        self._layout1.addWidget(box)

        self._console = QTextBrowser(self)
        # self._console.setPlainText(MSG_TEXT_BROWSER)
        self._layout1.addWidget(self._console)

    def set_layout2(self):
        self.formats = []
        for ext in supported_formats:
            self.formats.append((ext, QCheckBox(str(ext))))
        log.debug(self.formats)
        box = QGroupBox(LABEL_BOX_FORMATS)
        ly = QGridLayout()
        for ext, widget in self.formats:
            log.debug('render %s for gui' % ext)
            ly.addWidget(widget)
        box.setLayout(ly)
        self._layout2.addWidget(box)

        # ACTIONS
        self._btn_reset = QPushButton("Reset")
        self._btn_scan = QPushButton("Scan")
        self._btn_stop = QPushButton("Stop")
        self._btn_start = QPushButton("Execute")

        self._btn_scan.setEnabled(True)
        self._btn_scan.setToolTip(TOOLTIP_SCAN)

        self._btn_stop.setEnabled(False)
        self._btn_start.setEnabled(False)
        self._btn_reset.setEnabled(False)

        box = QGroupBox(LABEL_BOX_ACTIONS)
        ly = QGridLayout()
        ly.setColumnStretch(1, 1)
        ly.addWidget(self._btn_reset,  0, 0)
        ly.addWidget(self._btn_scan,  1, 0)
        ly.addWidget(self._btn_stop,  2, 0)
        ly.addWidget(self._btn_start,  3, 0)
        box.setLayout(ly)
        self._layout2.addWidget(box)

    def actions(self):
        self._btn1.clicked.connect(self.set_source)
        self._btn_reset.clicked.connect(self._reset)
        self._btn_scan.clicked.connect(self._scan)
        self._btn_stop.clicked.connect(self._stop)
        self._btn_start.clicked.connect(self._start)

    def _reset(self):
        log.debug('_reset()')

    def _scan(self):
        log.debug('_scan()')
        log.warning(TOOLTIP_SCAN)

    def _stop(self):
        log.debug('_stop()')

    def _start(self):
        log.debug('_start()')

    def closeEvent(self, event):
        log.debug("Exit")
        event.accept()

    def set_source(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setDirectory(path_home)
        if dialog.exec_():
            paths = dialog.selectedFiles()
            for f in paths:
                if os.path.isdir(f):
                    log.info('--path: %s' % f)
                elif os.path.isfile(f):
                    log.info('--from %s' % os.path.dirname(f))
                    log.info('file: %s' % os.path.basename(f))
                log.info('--depth: %s' % self._depth.text())
                self._edt1.setText(f)

    def set_directory_save_in(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                                                     MSG_SAVE_IN,
                                                     self._label2.text(), options)
        if directory:
            self._label2.setText(directory)
            log.info('--to: %s' % directory)
