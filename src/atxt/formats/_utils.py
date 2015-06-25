#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 13:09:59
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-25 13:39:39
import os
import chardet
import codecs

from atxt.log_conf import Logger
log = Logger.log

__all__ = ['rawdata', 'find_encoding']


def raw_data(filepath, opts=None, encoding=None):
    raw_data = None
    if not encoding:
        encoding = find_encoding(filepath)
    try:
        f = codecs.open(filepath, 'r', encoding=opts.get('-e', None))
        rawdata = f.read()
        f.close()
    except Exception, e:
        try:
            log.warning('trying to read file with encoding: %s' % encoding)
            if not os.access(filepath, os.R_OK):
                log.warning('file has not read permission')
            f = codecs.open(filepath, mode='r', encoding=encoding)
            rawdata = f.read()
            f.close()
        except Exception, e:
            log.warning('trying to read without encoding:%s' % e)
            try:
                f = codecs.open(filepath, mode='r')
                rawdata = f.read()
                f.close()
            except Exception, e:
                log.critical(e)
            return rawdata

    # log.warning(rawdata)
    return rawdata


def find_encoding(filepath):
    log.debug('find out the correct encoding')
    rawdata = codecs.open(filepath, mode="r").read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    return encoding


def save_raw_data(filepath, text, encoding=None):
    try:
        if encoding:
            f = codecs.open(filepath, mode='w', encoding=encoding)
            if text:
                f.write(text)
            f.close()
            return filepath
    except Exception, e:
        try:
            f = codecs.open(filepath, mode='w')
            if text:
                f.write(text)
            f.close()
            return filepath
        except Exception, ee:
            log.critical(e)
            log.critical(ee)
            return

# def upper():
#     if not os.path.exists(txt.path):
#         log.debug(txt.path, 'Not Found')
#         return txt.path

# FIXME: maybe it's enough with file._path
#     temp = tmp.NamedTemporaryFile(mode='w', delete=False)

#     with open(txt.path, 'r') as f:
#         for line in f:
#             try:
#                 line = remove_accents(line)
#             except Exception, e:
#                 log.debug('from upper', 'fail remove_accents')
#             try:
#                 line = enconding_path(line)
#             except Exception, e:
#                 log.debug(e)
# try:
# line = latin2ascii(line)
# except:
# log.debug('from upper', 'fail latin2ascii')
#             try:
#                 line = line.encode('utf-8', 'replace')
#             except Exception, e:
#                 log.debug('from upper', 'fail encode(ascii)')
#             try:
#                 line = line.upper()
#             except Exception, e:
#                 log.debug('*', 'from upper', 'fail .upper()')
#             temp.write(line)
#         temp.close()

#         txt.remove()

#         try:
#             log.debug('moving tempfile', temp.name)
#             sh.copy2(temp.name, txt.path)
#         except Exception, e:
#             log.debug(e)
#             try:
#                 sh.remove(temp.name)
#             except Exception, e:
#                 log.debug('*', 'fail to move tempfile', temp.name)
#                 log.debug(e)
#             return ''
#     return txt.path
