#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:21
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-27 00:30:21
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

__all__ = ['run_file']


def run_file(manager):
    assert isinstance(manager, aTXT)
    opts = manager.options
    log.debug('with option --file')

    #     to_path = opts['--from']  # where you want to save txt files
    # if opts['--to']:
    #     if not os.path.exists(opts['--to']) or not os.path.isdir(opts['--to']):
    #         log.error(
    #             '%s is not a valid path for --to_path option' % opts['--to'])
    #         return 0
    #     to_path = opts['--to']
    tfiles = set()
    files = defaultdict(list)
    total, finished = 0, 0

    for file_path in set(opts['<file>']):
        log.debug('-> %s' % file_path)
        if not os.path.isabs(file_path):
            file_path = os.path.join(opts['--from'], file_path)
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
                log.info('successful conversion for: %s' % file_path)
                finished += 1
            else:
                unsuccessful_files[ext].add(file_path)
                log.error('unsucessful conversion: %s' % file_path)
    return total, finished
