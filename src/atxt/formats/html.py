#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 02:38:43
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 13:15:15

from atxt.log_conf import Logger
log = Logger.log

def from_html():
        log.debug('')
        log.debug('[new conversion html]')
        log.debug('\tfrom_html starting')

        if not overwrite and os.path.exists(txt.path):
            return txt.path

        try:
            import codecs
            f = codecs.open(file._path, 'r', encoding='utf-8')
            s = ''
            for l in f:
                s += l
            import html2text
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
            h.bypass_tables = False
            h.google_doc = False
            h.ul_item_mark = '*'
            h.emphasis_mark = '_'
            h.strong_mark = '**'
            h.single_line_break = True
            text = h.handle(s)
            f = codecs.open(txt.path, 'w', encoding='utf-8')
            f.write(text)
            f.close()
        except Exception, e:
            print e