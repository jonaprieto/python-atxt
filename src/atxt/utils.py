#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import os

from log_conf import Logger
log = Logger.log

from encoding import encoding_path
import shutil as sh


def make_dir(path):
    try:
        log.debug('creating directory: %s' % path)
        os.makedirs(path)
        if not os.access(path, os.W_OK):
            log.debug('directory without permissions: %s' % path)
    except OSError, e:
        if os.path.exists(path):
            log.warning('directory exists')
        else:
            log.error(e)


def remove_dir(path):
    if os.path.isdir(path) and os.path.exists(path):
        try:
            log.debug('removing entire folder: %s' % path)
            sh.rmtree(path)
            log.debug('directory removed: %s' % path)
        except IOError, e:
            if os.path.exists(path):
                log.warning('fail to remove directory: %s' % e)
            else:
                log.error(e)
    else:
        log.warning('%s is not a directory' % path)


def remove(file_path):
    if os.path.isfile(file_path):
        log.debug('removing file %s' % file_path)
        try:
            sh.remove(file_path)
        except IOError, e:
            log.warning(e)
            raise e
    else:
        log.warning('remove file, %s is not a file' % file_path)


def move_to(file_path, to_path):
    if os.path.isfile(file_path):
        try:
            log.debug('moving from %s to %s' % (file_path, to_path))
            if not os.path.exists(to_path):
                make_dir(to_path)
            sh.copy2(file_path, to_path)
        except Exception, e:
            log.warning(e)
            raise e


def copy_to(file_path, to_path):
    try:
        log.debug('copying %s to %s' % (file_path, to_path))
        sh.copy2(file_path, to_path)
    except IOError, e:
        log.error(e)
        raise e


def size(file_path):
    if not os.path.isfile(file_path):
        log.warning('%s isnot a file' % os.path.basename(file_path))
        return
    try:
        size = os.path.getsize(file_path)
        return size
    except Exception, e:
        log.warning(e)
    return


def extract_ext(filepath):
    assert isinstance(filepath, str) or isinstance(filepate, unicode)
    ext = os.path.splitext(filepath)[1].lower()
    if ext.startswith('.'):
        ext = ext[1:]
    return ext


def parser_opts(opts):
    assert isinstance(opts, dict)
    if '--from' in opts:
        if opts['--from']:
            opts['--from'] = encoding_path(opts['--from'])
            if os.path.isdir(opts['--from']):
                opts['--from'] = os.path.abspath(opts['--from'])
    if '<source>' in opts:
        if isinstance(opts['<source>'], list):
            opts['<source>'] = list(set(opts['<source>']))
        opts['<file>'] = []
        opts['<path>'] = []
        for s in opts['<source>']:
            s = encoding_path(s)
            if os.path.isdir(s):
                opts['<path>'].append(s)
            elif os.path.isfile(s):
                opts['<file>'].append(s)
            else:
                log.debug('else: %s' % s)
                try:
                    if '--from' in opts and os.path.isdir(opts['--from']):
                        s = os.path.join(opts['--from'], s)
                        if os.path.isfile(s):
                            opts['<file>'].append(s)
                except Exception, e:
                    log.critical("options: %s " % e)
        if len(opts['<file>']) > 0:
            opts['--file'] = True
        if len(opts['<path>']) > 0:
            opts['--path'] = True
            opts['<path>'] = map(encoding_path, opts['<path>'])
            opts['<path>'] = map(os.path.abspath, opts['<path>'])
    opts['--depth'] = int(opts['--depth'])
    return opts.copy()
