#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:21
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-27 15:28:00
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

    to_path = opts['--from']  # where you want to save txt files
    if opts['--to']:
        if not os.path.isdir(opts['--to']):
            log.error('%s is not a valid path for --to_path option' %
                      opts['--to'])
            return None
    tfiles = set()
    files = defaultdict(list)
    for file_path in set(opts['<file>']):
        log.debug('-> %s' % file_path)
        if not os.path.isabs(file_path):
            file_path = os.path.join(opts['--from'], file_path)
        if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            log.info('either file is missing or is not readable')
            # if file_path correspond to a folder path,(user omitted --path flag)
            # it shoudl be process with run_path(manager) --path=True
            # and before that: manager.opts.update({'<path>': [file_path]})
            continue
        ext = extract_ext(file_path)
        if ext in supported_formats:
            tfiles.add(ext)
            files[ext].append(file_path)
        else:
            log.warning('%s ignored (%s is not supported yet)' %
                        (file_path, ext))
    total = sum(len(v) for _, v in files.items())
    #  manager.word()
    successful_files = defaultdict(str)
    for _ext in supported_formats:
        for file_path in files[_ext]:
            ext = extract_ext(file_path)
            new_path = None
            try:
                new_path = manager.convert_to_txt(filepath=file_path)
            except Exception, e:
                log.critical('convert_to_txt: %s'%e)
            if new_path:
                successful_files[file_path] = new_path
                log.info('successful conversion for: %s' % file_path)
            else:
                log.error('unsucessful conversion: %s' % file_path)
    finished = len(successful_files)
    return total, finished
