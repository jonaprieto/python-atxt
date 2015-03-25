#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-13 13:45:43
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-25 16:51:55
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

from lib import aTXT

__version__ = "1.0.5"


def main():
    args = docopt(usagedoc.__doc__, version=__version__)
    if args['--log']:
        log_path = os.path.abspath(args['--log'])
        if not os.path.isfile(log_path):
            log_path = os.path.join(log_path, 'atxt-log.txt')
        logging.basicConfig(filename=log_path,
                            filemode='w',
                            level=logging.INFO,
                            format='%(log_color)s%(levelname)-1s%(reset)s | %(log_color)s%(message)s%(reset)s',
                            # datefmt='%m/%d/%y %I:%M:%S %p | '
                            )

    manager = aTXT()
    manager.uppercase = args['-u']
    manager.overwrite = args['-o']
    manager.savein = args['--to']
    manager.lang = args['--lang']
    manager.use_temp = args['--use-temp']
    manager.encoding = args['--enc']

    options = manager.options()
    for k in options:
        log.debug("%s: %s" % (k, options[k]))
    total = 0
    if args['-i']:
        log.info('Starting pretty graphical interface...')
        try:
            import gui
            gui.run(manager)
            return 1
        except Exception, e:
            log.critical(e)
            return 0
    elif args['<file>']:
        total, finished = run_file(args, manager)
    elif args['<path>']:
        total, finished = run_path(args, manager)
    else:
        print(usagedoc.__doc__)
        return 0

    if total:
        log.info('%d/%d', finished, total)
        return 1
    log.warning('No files to proceed')
    return 0


def run_file(args, manager):
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
    files = defaultdict(list)
    total, finished = 0, 0

    for file_path in set(args['<file>']):
        log.debug('-> %s' % file_path)
        if not os.path.isabs(file_path):
            file_path = os.path.join(from_path, file_path)
        ext = extract_ext(file_path)
        if ext in supported_formats:
            tfiles.add(ext)
            total += 1
            files[ext].append(file_path)
        else:
            log.warning('%s ignored (%s is not supported yet)' %
                        (file_path, ext))
    #  manager.word()
    successful_files = defaultdict(str)
    unsuccessful_files = defaultdict(set)

    for _ext in supported_formats:
        for file_path in files[_ext]:
            ext = extract_ext(file_path)
            new_path = None
            try:
                new_path = manager.convert_to_txt(filepath=file_path)
            except Exception, e:
                log.critical(e)
            if new_path:
                successful_files[file_path] = new_path
                log.info('successful conversion: %s' % file_path)
                finished += 1
            else:
                unsuccessful_files[ext].add(file_path)
                log.error('unsucessful conversion: %s' % file_path)
    return total, finished


def run_path(args, manager):
    from_path = args['<path>']
    from_path = os.path.abspath(from_path)
    log.info('--path: %s' % from_path)
    if not os.path.exists(from_path) or not os.path.isdir(from_path):
        log.error('%s is not a valid path for --path option' % from_path)
        return 0
    try:
        depth = int(args['--depth'])
        if depth < 0:
            raise ValueError
    except Exception, e:
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
        for f in args['<format>']:
            f = f[1:] if f.startswith('.') else f
            if f in supported_formats:
                tfiles.add(f)
    log.info('searching for: %s' % tfiles)
    # manager.word()
    total, finished = 0, 0
    successful_files = defaultdict(str)
    unsuccessful_files = defaultdict(set)

    for _root, _, _files in wk.walk(from_path, level=depth, tfiles=list(tfiles)):
        if not _files:
            continue
        log.info('path=%s' % _root)
        for f in _files:
            total += 1
            log.info('file: %s' % f.name)
            file_path = os.path.join(_root, f.name)
            ext = extract_ext(file_path)
            new_path = None
            try:
                new_path = manager.convert_to_txt(filepath=file_path)
            except Exception, e:
                log.critical(e)
                # raise e
            if new_path:
                log.info('successful conversion: %s' % file_path)
                successful_files[new_path] = file_path
                finished += 1
            else:
                unsuccessful_files[ext].add(file_path)
                log.error('unsucessful conversion: %s' % file_path)
    return total, finished

if __name__ == "__main__":
    main()
    sys.exit()
