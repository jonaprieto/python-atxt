#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:53:25
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-27 00:56:23

from atxt.log_conf import Logger
from atxt.infofile import InfoFile
from _utils import save_raw_data, find_encoding
import codecs

import csv
log = Logger.log


__all__ = ['ocsv']


def ocsv(from_file, to_txt, opts):
    log.debug('csv2txt starting')
    text = None
    reader = None
    try:
        f = open(from_file.path, 'rb')
        reader = csv.reader(f)
    except Exception, e:
        log.critical(e)
    log.info('processing csv')
    text = '\n'.join('\t'.join(row) for row in reader)
    return save_raw_data(to_txt.path, text)
