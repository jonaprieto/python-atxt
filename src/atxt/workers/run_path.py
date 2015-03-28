#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:48
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-27 17:21:20
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
from atxt.encoding import encoding_path

__all__ = ['run_path']


def run_path(manager):
    assert isinstance(manager, aTXT)
    opts = manager.options
    log.info('<path>: %s' % opts['<path>'])
    if opts['--depth'] < 0:
        opts['--depth'] = 0
    log.info('--depth: %s' % opts['--depth'])

    opts['--to'] = opts['--to'] or opts['--from']
    opts['--to'] = encoding_path(opts['--to'])
    if opts['--to'] == 'TXT':
        opts['--to'] = os.path.join(opts['--from'], opts['--to'])
        make_dir(opts['--to'])
    tfiles = set(supported_formats[:])
    log.critical(tfiles)
    # if opts['<format>']:
    #     tfiles = set()
    #     for f in opts['<format>']:
    #         f = f[1:] if f.startswith('.') else f
    #         if f in supported_formats:
    #             tfiles.add(f)
    opts['tfiles'] = list(tfiles)
    manager.options = opts
    log.critical(manager.options)
    return None
    total, finished = 0, 0
    for path in opts['--path']:
        res = run_one_path(manager, path)
        if res:
            total += res[0]
            finished += res[1]
        else:
            log.warning('errors in path: %s'%path)
    return total, finished


def run_one_path(manager, path=None):
    assert isinstance(manager, aTXT)
    opts = manager.options
    if not path:
        if len(opts['--path']) > 1:
            return run_path(manager)
        if not len(opts['--path']):
            raise ValueError('not path to proceed')
        path = opts['--path'][0]
    log.info('processing: %s' % path)
    assert isinstance(path, str)
    if not os.path.isdir(path):
        log.error('%s is not a valid path for --path option' % path)
        return None
    # the part below can be omitted for a second time (tfiles->opts)
    if 'tfiles' not in opts:
        log.critical('no entro')
        tfiles = set(supported_formats[:])
        if opts['<format>']:
            tfiles = set()
            for f in opts['<format>']:
                f = f[1:] if f.startswith('.') else f
                if f in supported_formats:
                    tfiles.add(f)
        opts['tfiles'] = list(tfiles)
    log.info('searching for: %s' % opts['tfiles'])
    # manager.word()
    total = 0
    successful_files = defaultdict(str)

    for _root, _, _files in wk.walk(path,
                                    level=opts['--depth'],
                                    tfiles=opts['tfiles']):
        if not _files:
            continue
        log.info('path=%s' % _root)
        for f in _files:
            total += 1
            log.info('-' * 50)
            log.info('file: %s' % f.name)
            file_path = os.path.join(_root, f.name)
            ext = extract_ext(file_path)
            new_path = None
            try:
                new_path = manager.convert_to_txt(filepath=file_path)
            except Exception, e:
                log.critical(e)
            if new_path:
                log.info('successful conversion: %s' % file_path)
                successful_files[new_path] = file_path
            else:
                log.error('unsucessful conversion: %s' % file_path)
    finished = len(successful_files)
    return total, finished
