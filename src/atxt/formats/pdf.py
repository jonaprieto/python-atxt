#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:52:42
# @Last Modified by:   d555
# @Last Modified time: 2015-11-11 00:22:10
import codecs
import os
import re

from _utils import raw_data, save_raw_data
from atxt.log_conf import Logger
from atxt.utils import remove
from atxt.vendors import (
    pdftopng,
    pdftotext,
    tesseract,
    need_ocr
)
from atxt.walking import walk
from pdfminer import layout, pdfinterp, converter, pdfpage


log = Logger.log


def pdf_miner(from_file, to_txt):
    log.debug('trying with pdfminer')
    pdf = codecs.open(from_file.path, mode='rb')
    output = codecs.open(to_txt.path, mode='wb')
    try:
        resourceman = pdfinterp.PDFResourceManager()
        device = converter.TextConverter(
            resourceman, output, laparams=layout.LAParams())
        interpreter = pdfinterp.PDFPageInterpreter(resourceman, device)
        for page in pdfpage.PDFPage.get_pages(pdf):
            interpreter.process_page(page)
        output.close()
        device.close()
        pdf.close()
    except Exception, e:
        log.critical(e)
        return
    return to_txt.path


def pdf(from_file, to_txt, opts):
    path = None
    try:
        ocr_required = need_ocr(from_file.path)
        opts['--ocr'] = opts['--ocr'] or (ocr_required and opts['--ocr-necessary'])
        if not opts['--ocr']:
            try:
                path = pdftotext(from_file.path, to_txt.path)
            except:
                path = pdf_miner(from_file, to_txt)
        else:
            path = pdf_ocr(from_file, to_txt, opts)
    except Exception, e:
        log.critical(e)
        log.critical('IGNORED')
    try:
        if path and to_txt.size() <= 1000:
            if not opts['--ocr'] and not opts['--without-ocr']:
                log.info('OCR running. The last output text file is suspicious and almost empty') 
                path = pdf_ocr(from_file, to_txt, opts)
    except: 
        log.critical('IGNORED')


def pdf_ocr(from_file, to_txt, opts):
    pdftopng(from_file.path, to_txt.path)
    text = []
    outputpath = os.path.join(to_txt.dirname, 'output.txt')
    regex = re.compile('.*png$')
    raw = None
    for _, _, files in walk(to_txt.dirname, regex=regex):
        for f in files:
            if (f.name).startswith(to_txt.basename):
                log.info('tesseract is processing:')
                log.info(f.path)
                tesseract(f.path, None, opts)
                try:
                    raw = raw_data(outputpath)
                except Exception, e:
                    log.critical('pdf_ocr: %s' % e)
                text.append(raw)
                remove(f.path)
    remove(outputpath)
    if text:
        return save_raw_data(to_txt.path, text)
