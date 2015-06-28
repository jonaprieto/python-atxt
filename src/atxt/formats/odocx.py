#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:53:06
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-28 00:49:20
import codecs

from _utils import save_raw_data
from atxt.encoding import latin2ascii
from atxt.log_conf import Logger
import docx


log = Logger.log



__all__ = ['odocx']

def odocx(from_file, to_txt, opts, thread=None):
    log.debug('docx2txt starting')
    try:
        doc = docx.opendocx(from_file.path)
    except Exception, e:
        log.critical(e)
    text = '\n'.join(line for line in docx.getdocumenttext(doc))
    return save_raw_data(to_txt.path, text, encoding='utf-8')