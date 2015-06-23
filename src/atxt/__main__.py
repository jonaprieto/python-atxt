#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

from __future__ import print_function
import sys
import os

import logging
from log_conf import Logger
log = Logger.log

from docopt import docopt
from collections import defaultdict

from formats import supported_formats
import walking as wk

from utils import make_dir, extract_ext

from workers import run_file, run_path

from lib import aTXT

__version__ = "1.0.5"


def main():
    """aTXT for text extraction data mining tool

    Usage:
        aTXT
        aTXT [-ihv] [-l LOGPATH]
        aTXT <source>... [-ihv] [-d DEPTH] [-l LOGPATH] [-e ENC] [--from PATH] [--to PATH] [--format EXT]
        aTXT --file <files>... [-ihv] [-l LOGPATH] [-e ENC] [--from PATH] [--to PATH] [--format EXT]
        aTXT --path <path>...  [-d DEPTH] [-ihv] [-l LOGPATH] [-e ENC] [--to PATH] [--format EXT]

    Arguments:
        <source>...         It can be files, foldres or mix of them.
        <file>...           Just files paths
        <path>...           Just paths to directories

    Options:
        -i                  Launch the graphical interface
        -h                  Show help
        --format EXT        string separte with ',' of formats or extension to
                            consider when it will process the files
        -l LOGPATH          Specify a path to save the log [default: ./].
        -v                  Show the version. [default:False].
        -d, --depth DEPTH   Integer for depth for trasvering path using 
                            Depth-first-search on folders @int for path of files in <source>
                            [default: 0]
        -e ENC              Give a codification to open/save files. [default: utf-8].
        --from PATH         root path of the files [default: ./].
        --to PATH           root path of save the result files [default:./].
    Examples:

        $ atxt -i
        $ atxt prueba.html
        $ atxt --file ~/Documents/prueba.html
        $ atxt ~ -d 2
        $ atxt --path ~ -d 2
    """

    opts = docopt(main.__doc__, version=__version__)
    opts['<format>'] = []
    for ext in supported_formats:
        if opts['--format'] and opts['--format'].find(ext) > 0:
            opts['<format>'].append(ext)

    if opts['-v']:
        print(__version__)
        return
    if opts['-h']:
        print(usagedoc.__doc__)
        return

    opts['-i'] = opts.get('-i', True)
    if opts['-l']:
        try:
            log_path = os.path.abspath(opts['-l'])
            if not os.path.isfile(log_path):
                log_path = os.path.join(log_path, 'atxt-log.txt')
            log.info('log will be save in: %s' % log_path)
        except:
            log.error('LOGPATH error, it is not a valid path')
            print(main.__doc__)
            return
        opts['log_path'] = log_path
        logging.basicConfig(filename=log_path,
                            filemode='w',
                            level=logging.DEBUG
                            )
    manager = aTXT()
    manager.options = opts

    for k in manager.options:
        log.debug("%s: %s" % (k, manager.options[k]))

    if manager.options['-i']:
        log.info('Starting the graphical interface...')
        try:
            import gui
            gui.run(manager)
            return
        except Exception, e:
            log.critical(e)
            return
    res = None
    total, finished = 0, 0
    if manager.options['--file']:
        res = run_file(manager)
        if res and len(res) == 2:
            total += res[0]
            finished += res[1]
    if manager.options['--path']:
        res = run_path(manager)
        if res and len(res) == 2:
            total += res[0]
            finished += res[1]
    log.info('{0} end of aTXT {0}'.format('-' * 15))
    log.info('files: %d\tfinished: %d', total, finished)

    if total == 0:
        log.critical('No files to proceed or something was wrong.')
        return
    return

if __name__ == "__main__":
    main()
    sys.exit()
