#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 22:23:20
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 12:28:37

from formats import supported_formats
from utils import extract_ext


from log_conf import Logger
log = Logger.log

from infofile import InfoFile


def to_txt(filepath, format=None):
    ext = format
    if not ext:
        ext = extract_ext(filepath)
    f = InfoFile(filepath)
    f.create_temp()
    log.info('working with: %s' % f.basename)

    return True
