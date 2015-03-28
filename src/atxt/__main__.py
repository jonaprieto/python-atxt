#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-13 13:45:43
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-28 00:32:09
from __future__ import print_function
import sys
import os

import logging
from log_conf import Logger
log = Logger.log

from docopt import docopt
from collections import defaultdict

import usagedoc
from formats import supported_formats
import walking as wk

from utils import make_dir, extract_ext

from workers import run_file, run_path

from lib import aTXT

__version__ = "1.0.5"


def main():
    
    opts = docopt(usagedoc.__doc__, version=__version__)

    if opts['--log']:
        log_path = os.path.abspath(opts['--log'])
        if not os.path.isfile(log_path):
            log_path = os.path.join(log_path, 'atxt-log.txt')
        logging.basicConfig(filename=log_path,
                            filemode='w',
                            level=logging.INFO,
                            format='%(log_color)s%(levelname)-1s%(reset)s | %(log_color)s%(message)s%(reset)s',
                            # datefmt='%m/%d/%y %I:%M:%S %p | '
                            )
    manager = aTXT()
    manager.options = opts
    for k in manager.options:
        log.debug("%s: %s" % (k, manager.options[k]))

    res = None
    if opts['--help']:
        print(usagedoc.__doc__)
    elif manager.options['-i']:
        log.info('Starting pretty graphical interface...')
        try:
            import gui
            gui.run(manager)
            return 1
        except Exception, e:
            log.critical(e)
            return 0
    res = None
    if manager.options['--file']:
        res = run_file(manager)
    if manager.options['--path']:
        res = run_path(manager)
    log.info('{0} process ended {0}'.format('-' * 15))
    if res:
        total, finished = res
    else:
        log.info('No files to proceed or something was wrong.')
        return 0
    if total:
        log.info('files: %d/%d', finished, total)
        return 1
    log.warning('No files to proceed')
    return 0

if __name__ == "__main__":
    main()
    sys.exit()
