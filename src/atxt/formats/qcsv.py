#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:53:25
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-15 10:14:13

import csv

from _utils import save_raw_data
from atxt.log_conf import Logger


log = Logger.log

__all__ = ['qcsv']


def qcsv(from_file, to_txt, opts):
    log.debug('csv2txt starting')
    text = None
    reader = None
    try:
        f = open(from_file.path, 'rb')
        reader = csv.reader(f)
    except Exception, e:
        log.critical(e)
    log.info('processing csv: %s' % from_file.basename)
    text = '\n'.join('\t'.join(row) for row in reader)
    return save_raw_data(to_txt.path, text)
