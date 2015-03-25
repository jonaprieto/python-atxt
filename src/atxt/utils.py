#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 20:28:40
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-20 12:08:19
import os
import sys

from log_conf import Logger
log = Logger.log

import shutil as sh


def make_dir(path):
    try:
        log.info('creating directory: %s' % path)
        os.makedirs(path)
        if not os.access(path, os.W_OK):
            log.info('directory without permissions: %s' % path)
    except OSError, e:
        if os.path.exists(path):
            log.warning('directory exists')
        else:
            log.error(e)


def remove_dir(path):
    if os.path.isdir(path) and os.path.exists(path):
        try:
            log.info('removing entire folder: %s' % path)
            sh.rmtree(path)
            log.info('directory removed: %s' % path)
        except IOError, e:
            if os.path.exists(path):
                log.warning('fail to remove directory: %s' % e)
            else:
                log.error(e)
    else:
        log.info('%s is not a directory' % path)


def remove(file_path):
    if os.path.isfile(file_path):
        log.info('removing file %s' % file_path)
        try:
            sh.remove(file_path)
        except IOError, e:
            log.warning(e)
            raise e
    else:
        log.info('remove file, %s is not a file' % file_path)


def move_to(file_path, to_path):
    if os.path.isfile(file_path):
        try:
            log.info('moving from %s to %s' % (file_path, to_path))
            if not os.path.exists(to_path):
                make_dir(to_path)
            sh.copy2(file_path, to_path)
        except Exception, e:
            log.warning(e)
            raise e


def copy_to(file_path, to_path):
    try:
        log.info('copying %s to %s' % (file_path, to_path))
        sh.copy2(file_path, to_path)
    except IOError, e:
        log.error(e)
        raise e


def size(file_path):
    if not os.path.isfile(file_path):
        log.warning('%s isnot a file' % os.path.basename(file_path))
        return None
    try:
        size = os.path.getsize(file_path)
        return size
    except Exception, e:
        log.warning(e)
    return None


def extract_ext(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext.startswith('.'):
        ext = ext[1:]
    return ext
