#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-04-25 14:07:56
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-04-25 18:50:02

from atxt.log_conf import Logger
log = Logger.log

__all__ = ['txt']

def txt(from_file, to_txt, opts):
    log.debug('txt2txt starting')
    if not isinstance(from_file, InfoFile):
        raise IOError
    encoding = 'utf-8'
    if 'encoding' in opts:
        encoding = opts['--enc'].strip()
        log.debug('using encoding from opts: %s' % encoding)
    try:
        f = codecs.open(from_file.path, 'r', encoding=encoding)
        text = f.read()
        f.close()
        f = codecs.open(to_txt.path, 'w', encoding=encoding)
        f.write(text)
        f.close()
    except Exception, e:
        log.critical(e)
        return None
    return to_txt.path