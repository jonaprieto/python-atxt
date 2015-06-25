#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:53:25
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-25 11:46:26

from atxt.log_conf import Logger
from atxt.infofile import InfoFile
import codecs

log = Logger.log

import csv as _csv

__all__ = ['csv']


def csv(from_file, to_txt, opts):
    log.debug('csv2txt starting')
    if not isinstance(from_file, InfoFile):
        raise IOError
    encoding = 'utf-8'
    if 'encoding' in opts:
        encoding = opts['--enc'].strip()
        log.debug('using encoding: %s' % encoding)
    try:
        f = codecs.open(from_file.path, 'r', encoding=encoding)
        reader = _csv.reader(f)
        f.close()
        f = codecs.open(to_txt.path, 'w', encoding=encoding)
        text = '\n'.join(['\t'.join(row) for row in reader])
        f.write(text)
        f.close()
    except Exception, e:
        log.critical(e)
        return
    return to_txt.path
