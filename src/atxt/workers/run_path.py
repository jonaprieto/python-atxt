#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:48
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-26 21:01:11
from __future__ import print_function
import sys
import os
from collections import defaultdict

import logging
from atxt.log_conf import Logger
log = Logger.log


from atxt.formats import supported_formats
import atxt.walking as wk
from atxt.utils import make_dir, extract_ext
from atxt.lib import aTXT

__all__ = ['run_path']


def run_path(manager):
    assert isinstance(manager, aTXT)
    opts = manager.options
    from_path = opts['<path>']
    from_path = os.path.abspath(from_path)
    log.info('--path: %s' % from_path)
    if not os.path.exists(from_path) or not os.path.isdir(from_path):
        log.error('%s is not a valid path for --path option' % from_path)
        return 0
    try:
        depth = int(opts['--depth'])
        if depth < 0:
            raise ValueError
    except Exception, e:
        log.error('arg <depth> needs to be a positive integer')
        return 0
    log.info('--depth: %s' % depth)
    to_path = opts['--to'] or from_path
    if to_path == 'TXT':
        to_path = os.path.join(from_path, to_path)
        make_dir(to_path)
    elif not os.path.exists(to_path) or not os.path.isdir(to_path):
        log.error('%s is not a valid path for --to option' % to_path)
        return 0

    tfiles = set(supported_formats[:])
    if opts['<format>']:
        tfiles = set()
        for f in opts['<format>']:
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
