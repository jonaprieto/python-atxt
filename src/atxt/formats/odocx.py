#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:53:06
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-27 02:14:33
from atxt.log_conf import Logger
log = Logger.log

from atxt.infofile import InfoFile
from atxt.encoding import latin2ascii

import codecs
import docx

from _utils import save_raw_data

__all__ = ['odocx']

def odocx(from_file, to_txt, opts):
    log.debug('docx2txt starting')
    try:
        doc = docx.opendocx(from_file.path)
    except Exception, e:
        log.critical(e)
    text = '\n'.join(line for line in docx.getdocumenttext(doc))
    return save_raw_data(to_txt.path, text, encoding='utf-8')