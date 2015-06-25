#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 18:23:55
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-25 12:12:12

import os
import re
import chardet
from atxt.log_conf import Logger
from atxt.infofile import InfoFile
log = Logger.log


basedir_ = os.path.dirname(os.path.abspath(__file__))
__all__ = ['convert', 'supported_formats']

supported_formats = []

regex = re.compile(r'[^(_|\.)+]\w+\.py$')
for root, dirs, files in os.walk(basedir_):
    files.sort()
    for f in files:
        if regex.match(f):
            extension = os.path.splitext(f)[0].lower()
            try:
                s = 'from {ext} import {ext}'.format(ext=extension)
                exec s
                log.info('%s is supported' % extension)
                supported_formats.append(extension)
            except Exception, e:
                log.warning(e)
                log.warning('%s is not supported' % extension)


def convert(from_file, to_txt, opts):
    if not isinstance(from_file, InfoFile):
        log.critical('the file should be instanced with InfoFile')
    f = from_file
    bot = lambda x: x  # dummy def before a real definition based on format
    exec 'bot = %s' % f.extension
    log.debug('calling bot = %s' % bot.__name__)
    return bot(from_file, to_txt, opts)

