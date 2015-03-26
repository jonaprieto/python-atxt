#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 17:12:37
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-25 17:31:22
import sys
from PySide import QtGui
from window import Window

from atxt.log_conf import Logger
log = Logger.log

__all__ = ['run']


def run(manager=None):
    app = QtGui.QApplication(sys.argv)
    wds = Window(manager)
    wds.show()
    sys.exit(app.exec_())
    del wds


if __name__ == '__main__':
    run()
