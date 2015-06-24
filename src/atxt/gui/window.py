#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:17:55
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-23 12:24:15
import os
import sys
from PySide import QtGui, QtCore
from PySide.QtGui import (
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QCheckBox,
    QTextBrowser,
    QPushButton,
    QMessageBox
)
from walk_thread import WalkThread
import atxt.walking as wk
from atxt.formats import supported_formats
from constants import *

import logging
from atxt.log_conf import Logger
log = Logger.log
path_home = os.path.expanduser('~')


checked = QtCore.Qt.Checked
unchecked = QtCore.Qt.Unchecked


class QtHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('%s\n' % record)

handler = QtHandler()
log.addHandler(handler)
log.setLevel(logging.DEBUG)


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
            self.messageWritten.emit(msg)

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


class Window(QtGui.QWidget):
    layout = QGridLayout()
    _layout1 = QtGui.QVBoxLayout()
    _layout2 = QtGui.QVBoxLayout()
    run_type = "path"

    def __init__(self, manager=None):
        super(Window, self).__init__()
        log.debug('GUI aTXT')
        self._set_layout1()
        self._set_layout2()
        self._connect_acctions()
        box = QGroupBox(LABEL_BOX_LAYOUT1)
        box.setLayout(self._layout1)
        self.layout.addWidget(box, 0, 0)

        box = QGroupBox(LABEL_BOX_LAYOUT2)
        box.setLayout(self._layout2)
        self.layout.addWidget(box, 0, 1)
        self.setLayout(self.layout)

        XStream.stdout().messageWritten.connect(self._console.insertPlainText)
        XStream.stderr().messageWritten.connect(self._console.insertPlainText)

    def _set_layout1(self):
        self.setWindowTitle(TITLE_WINDOW)
        self.setFixedSize(850, 400)
        self.setContentsMargins(15, 15, 15, 15)
        self._layout1 = QtGui.QVBoxLayout()
        self._layout1.addStretch(1)

        self._btn_source = QtGui.QPushButton(BTN_BROWSER)
        self._edt_source = QtGui.QLineEdit()
        self._edt_source.setText(path_home)
        self._edt_source.setFixedSize(330, 20)
        self._edt_source.setAlignment(QtCore.Qt.AlignRight)

        self._depth = QtGui.QSpinBox()
        self._depth.setToolTip(TOOLTIP_DEPTH)
        self._depth.setMinimum(0)
        self._depth.setMaximum(100)
        self._depth.setFixedSize(50, 25)

        self._label1 = QtGui.QLabel()
        self._label1.setText(LABEL_DEPTH)

        box = QGroupBox(LABEL_BOX_DIRECTORY)
        ly = QGridLayout()
        ly.addWidget(self._btn_source, 0, 0)
        ly.addWidget(self._edt_source, 0, 1)
        ly.addWidget(self._label1, 0, 2)
        ly.addWidget(self._depth, 0, 3)
        box.setLayout(ly)
        self._layout1.addWidget(box)

        self._label_save = QtGui.QLabel(MSG_SAVE_IN)
        self._edt_save = QtGui.QLineEdit(NAME_FOLDER_TXT)
        self._edt_save.setFixedSize(200, 20)
        self._edt_save.setToolTip(TOOLTIP_SAVEIN)
        self._btn2 = QtGui.QPushButton(BTN_BROWSER)
        self._btn2.clicked.connect(self.set_directory_save_in)
        self._check_overwrite = QtGui.QCheckBox(LABEL_OVERWRITE)
        self._check_overwrite.setToolTip(TOOLTIP_OVERWRITE)
        self._check_overwrite.setCheckState(checked)

        self._check_use_temp = QtGui.QCheckBox(LABEL_USE_TEMP)
        self._check_use_temp.setToolTip(TOOLTIP_USE_TEMP)
        self._check_use_temp.setCheckState(checked)

        box = QGroupBox(LABEL_BOX_SAVE_IN)
        box.setToolTip(TOOLTIP_BOX_SAVEIN)
        ly = QGridLayout()
        ly.addWidget(self._btn2, 0, 0)
        ly.addWidget(self._edt_save, 0, 1)
        ly.addWidget(self._check_overwrite, 0, 2)
        ly.addWidget(self._check_use_temp, 0, 3)
        box.setLayout(ly)
        self._layout1.addWidget(box)

        self._console = QTextBrowser(self)
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self._console.setFrameStyle(frameStyle)

        # DETAILS

        self._progress_bar = QtGui.QProgressBar()
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(100)
        self._layout1.addWidget(self._console)
        self._layout1.addWidget(self._progress_bar)
        self._btn_save_log = QtGui.QPushButton(BTN_SAVE_LOG)
        self._btn_save_log.clicked.connect(self._save_log)
        self._layout1.addWidget(self._btn_save_log)

    def _save_log(self):
        save_log_dir = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text File (*.txt)")
        f = QtCore.QFile(str(save_log_dir[0]))
        try:
            if f.open(QtCore.QIODevice.ReadWrite):
                stream = QtCore.QTextStream(f)
                stream << self._console.toPlainText()
                f.flush()
                f.close()

        except Exception, e:
            log.critical(e)

    def _cursor_end(self, value=None):
        self._console.moveCursor(QtGui.QTextCursor.End)

    def _set_layout2(self):
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
        self._btn_scan = QPushButton("Scan")
        self._btn_stop = QPushButton("Stop")
        self._btn_start = QPushButton("Start")

        self._btn_scan.setEnabled(True)
        self._btn_scan.setToolTip(TOOLTIP_SCAN)

        self._btn_stop.setEnabled(False)
        self._btn_start.setEnabled(True)

        box = QGroupBox(LABEL_BOX_ACTIONS)
        ly = QGridLayout()
        ly.setColumnStretch(1, 1)
        ly.addWidget(self._btn_start,  0, 0)
        ly.addWidget(self._btn_stop,  1, 0)
        ly.addWidget(self._btn_scan,  2, 0)
        box.setLayout(ly)
        self._layout2.addWidget(box)

    def closeEvent(self, event):
        log.debug("Exit")
        event.accept()

    def on_show_info(self, value):
        QtGui.QMessageBox.information(self, "Information", value)

    def set_source(self):
        log.debug('set source for extraction')
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setDirectory(path_home)
        if dialog.exec_():
            paths = dialog.selectedFiles()
            for f in paths:
                if os.path.isdir(f):
                    log.info('set path: %s' % f)
                    run_type = "path"
                    self._btn_scan.setEnabled(True)

                elif os.path.isfile(f):
                    log.debug('--from %s' % os.path.dirname(f))
                    log.debug('file: %s' % os.path.basename(f))
                    run_type = "file"
                    self._btn_scan.setEnabled(False)
                log.debug('--depth: %s' % self._depth.text())
                self._edt_source.setText(f)

    def set_directory_save_in(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                                                     MSG_SAVE_IN,
                                                     self._edt_save.text(), options)
        if directory:
            self._edt_save.setText(directory)
            log.debug('--to: %s' % directory)

    def options(self):
        f = self._edt_source.text()
        if not os.path.exists(f):
            self.on_show_info('Choose a valid path for "from"')
            return None
        if os.path.isdir(f):
            self.run_type = "path"
        elif os.path.isfile(f):
            self.run_type = "file"

        tfiles = []
        for ext, widget in self.formats:
            if widget.isChecked():
                tfiles.append(ext)
        opt = {
            'run_type': self.run_type,
            'path': f,
            'savein': self._edt_save.text(),
            'overwrite': self._check_overwrite.isChecked(),
            'use_temp': self._check_use_temp.isChecked(),
            'depth': int(self._depth.text()),
            'tfiles': tfiles,
        }
        return opt

    def set_progress(self, value):
        if value > 100:
            value = 100
        self._progress_bar.setValue(value)

    def end_process(self):
        self._progress_bar.reset()

    def ready(self, value):
        self._ready = value

    def _connect_acctions(self):
        self._btn_source.clicked.connect(self.set_source)
        self._btn_scan.clicked.connect(self._scan)
        self._btn_stop.clicked.connect(self._stop)
        self._btn_start.clicked.connect(self._start)

    def _scan(self):
        opts = self.options()
        if not opts['tfiles']:
            QtGui.QMessageBox.information(
                self, "Information", NONE_EXT_CHOOSED)
            log.debug(NONE_EXT_CHOOSED)
            return
        flags = QMessageBox.StandardButton.Yes
        flags |= QMessageBox.StandardButton.No
        question = WARNING_LONG_PROCESS
        response = QMessageBox.question(self, "Question", question, flags)
        if response == QMessageBox.No:
            log.info("Scaning cancelled")
            return
        log.info("Starting process")
        log.warning(TOOLTIP_SCAN)
        log.debug(opts)

        self._btn_start.setEnabled(False)
        self._thread = WalkThread(self)
        self._thread._part.connect(self.set_progress)
        self._thread._end_process.connect(self.end_process)
        self._thread._ready.connect(self.ready)
        self._thread._cursor_end.connect(self._cursor_end)

        self._progress_bar.setValue(0)
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(100)
        self._thread.start()
        self._cursor_end()
        self._btn_start.setEnabled(True)

    def _stop(self):
        log.debug('_stop()')
        try:
            del self._thread
        except Exception, e:
            log.debug('it can delete thread')

    def _start(self):
        log.debug('_start()')
        flags = QMessageBox.StandardButton.Yes
        flags |= QMessageBox.StandardButton.No
        question = WARNING_LONG_PROCESS
        response = QMessageBox.question(self, "Question", question, flags)
        if response == QMessageBox.Yes:
            log.info("Starting process")
        elif QMessageBox.No:
            log.info("Starting cancelled")
