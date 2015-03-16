#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-13 13:45:43
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 04:13:38
from __future__ import print_function
import sys
import os

from log_conf import Logger
log = Logger.log

from docopt import docopt
from collections import defaultdict

import usagedoc
from formats import supported_formats
import walking as wk

from utils import make_dir, extract_ext

import logging


from to_txt import to_txt

__version__ = "1.0.5"


def main(argv=()):
    args = docopt(usagedoc.__doc__, version=__version__)
    if args['--log']:
        log_path = os.path.abspath(args['--log'])
        if not os.path.isfile(log_path):
            log_path = os.path.join(log_path, 'atxt-log.txt')
        logging.basicConfig(filename=log_path,
                            filemode='w',
                            level=logging.INFO,
                            format='%(levelname)s %(asctime)s\n\t%(message)s',
                            # datefmt='%m/%d/%y %I:%M:%S %p | '
                            )

    tfiles = set()
    files = defaultdict(set)
    total = 0
    finished = 0
    if args['-i']:
        log.info('Starting pretty graphical interface...')
        try:
            import gui
            gui.main()
        except Exception, e:
            log.critical(e)
            return 0
    elif args['<file>']:
        log.debug('with option --file')
        from_path = os.getcwd()
        if args['--from']:
            if not os.path.exists(args['--from']) or not os.path.isdir(args['--from']):
                log.error('%s is not a valid path for --from option' %
                          args['--from'])
                return 0
            from_path = args['--from']
        from_path = os.path.abspath(from_path)
        log.debug('from: %s' % from_path)
        to_path = from_path  # where you want to save txt files
        if args['--to']:
            if not os.path.exists(args['--to']) or not os.path.isdir(args['--to']):
                log.error(
                    '%s is not a valid path for --to_path option' % args['--to'])
                return 0
            to_path = args['--to']

        tfiles = set()
        for file_path in args['<file>']:
            if not os.path.isabs(file_path):
                file_path = os.path.join(from_path, file_path)
            ext = extract_ext(file_path)
            if ext in supported_formats:
                tfiles.add(ext)
                total += 1
                files[ext].add(file_path)

        log.info('supported formats: %s' % list(tfiles))

        # config settings...
        # if we need to process a lot MS office files is better
        # dispatching just once the program.

        for ext in supported_formats:
            for file_path in files[ext]:
                ext = extract_ext(file_path)
                status = to_txt(file_path, format=ext)
                if status:
                    log.info('successful conversion: %s' % file_path)
                    finished += 1
                else:
                    files[ext].remove(file_path)
                    log.error('unsucessful conversion: %s' % file_path)
    elif args['<path>']:
        from_path = args['<path>']
        from_path = os.path.abspath(from_path)
        log.info('--path: %s' % from_path)
        if not os.path.exists(from_path) or not os.path.isdir(from_path):
            log.error('%s is not a valid path for --path option' %
                      from_path)
            return 0
        try:
            depth = args['--depth']
            if depth < 0:
                raise ValueError
        except Exception, e:
            if verbose:
                log.error('arg <depth> needs to be a positive integer')
            return 0
        log.info('--depth: %s' % depth)
        to_path = args['--to'] or from_path
        if to_path == 'TXT':
            to_path = os.path.join(from_path, to_path)
            make_dir(to_path)
        elif not os.path.exists(to_path) or not os.path.isdir(to_path):
            log.error('%s is not a valid path for --to option' % to_path)
            return 0
        tfiles = set(supported_formats[:])
        if args['<format>']:
            tfiles = set()
            for format in args['<format>']:
                if format.startswith('.'):
                    format = format[1:]
                if format in supported_formats:
                    tfiles.add(format)
        log.info('searching for: %s' % tfiles)

        # config settings...
        # if we need to process a lot MS office files is better
        # dispatching just once the program.

        finished = 0
        total = 0
        for root_path, dirs, files_ in wk.walk(from_path, level=depth, tfiles=list(tfiles)):
            if files_:
                log.info('path=%s' % root_path)
                for f in files_:
                    total += 1
                    log.info('\tfile=%s' % f.name)
                    file_path = os.path.join(root_path, f.name)
                    ext = extract_ext(file_path)
                    log.info("to_txt(%s)" % file_path)
                    status = to_txt(file_path, format=ext)
                    if status:
                        log.info('successful conversion: %s' % file_path)
                        files[ext].add(file_path)
                        finished += 1
                    else:
                        log.error('unsucessful conversion: %s' % file_path)

    else:
        print(usagedoc.__doc__)
        return 0

    for ext in supported_formats:
        if len(files[ext]):
            log.info('%s %d' % (ext, len(files[ext])))
    if total:
        log.info('total: %d', total)
    else:
        log.warning('No files to proceed')
    return 0

if __name__ == "__main__":
    main()
    sys.exit()
