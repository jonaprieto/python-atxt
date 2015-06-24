#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 02:38:43
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-24 01:29:01

from atxt.log_conf import Logger
log = Logger.log

import codecs
from atxt.infofile import InfoFile

try:
    import html2text
except:
    log.critical('html2text module not installed')
    log.critical('please: pip install html2text')
    raise Exception('html2text module not installed')

__all__ = ['html']


def html(from_file, to_txt, opts):
    log.debug('html2txt starting')
    assert isinstance(from_file, InfoFile)
    _file = from_file
    encoding = 'utf-8'
    if '-e' in opts:
        encoding = opts['-e'].strip()
        log.debug('using encoding: %s' % encoding)

    try:
        f = codecs.open(_file.path, 'r', encoding=encoding)
    except Exception, e:
        log.critical(e)
        return None

    s = ''
    for l in f:
        s += l
    h = html2text.HTML2Text()
    h.split_next_td = False
    h.td_count = 0
    h.table_start = False
    h.unicode_snob = 0
    h.escape_snob = 0
    h.links_each_paragraph = 0
    h.body_width = 78
    h.skip_internal_links = True
    h.inline_links = True
    h.protect_links = True
    h.ignore_links = True
    h.ignore_images = True
    h.images_to_alt = True
    h.ignore_emphasis = True
    h.bypass_tables = 1
    h.google_doc = False
    h.ul_item_mark = '*'
    h.emphasis_mark = '_'
    h.strong_mark = '**'
    h.single_line_break = True
    text = h.handle(s)
    f = codecs.open(to_txt.path, 'w', encoding=encoding)
    f.write(text)
    f.close()
    log.debug('txt finished: %s' % to_txt.path)
    return to_txt.path
