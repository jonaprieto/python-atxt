#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

from __future__ import print_function

from collections import defaultdict
import logging
import os
import sys

from check import check
from docopt import docopt
from formats import supported_formats
from lib import aTXT
from log_conf import Logger
from utils import make_dir, extract_ext
import walking as wk
from workers import run_files, run_paths


log = Logger.log

__version__ = "1.0.5"


def main():
    """aTXT for text extraction data mining tool

    Usage:
        aTXT [--check] [--log PATH]
        aTXT [-ihvo] [--log PATH] [--use-temp] [-l LANG]
        aTXT <source>... [-hvo] [-d DEPTH] [--log PATH] [--from PATH] [--to PATH] [--format EXT] [--use-temp] [-l LANG]
        aTXT --file <file>... [-hvo] [--log PATH] [--from PATH] [--to PATH] [--format EXT] [--use-temp] [-l LANG]
        aTXT --path <path>... [-d DEPTH] [-hvuo] [--log PATH] [--to PATH] [--format EXT] [--use-temp] [-l LANG]

    Arguments:
        <source>...         It can be files, foldres or mix of them.
        <file>...           Just files paths
        <path>...           Just paths to directories

    Options:
        -i                  Launch the graphical interface 
        -h                  Show help
        -o                  Overwrite result files. [default: False].
        --format EXT        string \"...\" separte with ',' of formats or extension to
                            consider when it will process the files
        --log PATH          Specify a path to save the log [default: ./].
        -v                  Show the version. [default:False].
        -d, --depth DEPTH   Integer for depth for trasvering path using 
                            Depth-first-search on folders @int for path of files in <source>
                            [default: 0]
        --from PATH         root path of the files [default: ./].
        --to PATH           root path of save the result files [default: ./].
        --check             check the system for requirements: Xpdf, Tesseract
        --ocr               Use OCR for extract text from hard pdf, if you have a language package
                            installed, you could use option -l LANGSPEC [default: False].
        --use-temp          use the generation of temporary files for avoid problems with filepaths
        -l LANG             option of a language for tesseract OCR, please be sure that 
                            thes package is installed. [default: spa].

    Examples:

        $ atxt -i
        $ atxt prueba.html
        $ atxt --file ~/Documents/prueba.html
        $ atxt ~ -d 2
        $ atxt --path ~ -d 2 --format 'txt,html'
    """

    opts = docopt(main.__doc__, version=__version__)
    opts['<format>'] = []

    for ext in supported_formats[:]:
        if opts['--format'] and opts['--format'].find(ext) >= 0:
            opts['<format>'].append(ext)
            if 'tfiles' in opts:
                opts['tfiles'].append(ext)
            else:
                opts['tfiles'] = [ext]
    if 'tfiles' not in opts or not opts['tfiles']:
        opts['tfiles'] = supported_formats[:]

    if opts['-v']:
        print(__version__)
        return
    if opts['-h']:
        print(usagedoc.__doc__)
        return

    # for k,v in opts.iteritems():
    #     log.critical((k,v))

    opts['-i'] = opts.get('-i', True)
    if opts['--log']:
        try:
            log_path = os.path.abspath(opts['--log'])
            if not os.path.isfile(log_path):
                log_path = os.path.join(log_path, 'log.txt')
            log.info('log will be save in: %s' % log_path)
        except:
            log.error('LOGPATH error, it is not a valid path')
            print(main.__doc__)
            return
        opts['log_path'] = log_path
        f = open(log_path, 'wb')
        f.close()
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(levelname)-1s| %(message)s::%(filename)s:%(lineno)s")
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if opts['--check']:
        check()
        return

    manager = aTXT()
    manager.options = opts

    # for k in manager.options:
    #     log.debug("%s: %s" % (k, manager.options[k]))

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
        res = run_files(manager)
        if res and len(res) == 2:
            total += res[0]
            finished += res[1]
    if manager.options['--path']:
        res = run_paths(manager)
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
