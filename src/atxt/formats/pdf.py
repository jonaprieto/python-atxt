#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:52:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-28 01:38:53
import codecs
import os

from _utils import raw_data, save_raw_data
from atxt.log_conf import Logger
from atxt.utils import remove
from atxt.vendors import (
    pdftopng,
    pdftotext,
    tesseract,
    need_ocr
)
import atxt.walking as wk
from pdfminer import layout, pdfinterp, converter, pdfpage


log = Logger.log


def pdf_miner(from_file, to_txt, opts, thread=None):
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


def pdf(from_file, to_txt, opts, thread=None):
    opts['--ocr'] = opts.get('--ocr', False)
    ocr = need_ocr(from_file.path)
    if opts['--ocr']:
        log.info('Extraction with OCR technology')
        if not ocr:
            log.info('it could be more better if you dont use OCR')
        return pdf_ocr(from_file, to_txt, opts)
    log.info('Extraction with Xpdf technology')

    if thread:
        thread._cursor_end.emit(True)
    if ocr:
        log.warning('it would be better if you use OCR options')
    return pdftotext(from_file.path, to_txt.path)


def pdf_ocr(from_file, to_txt, opts, thread=None):
    pdftopng(from_file.path, to_txt.path)
    text = ''
    outputpath = os.path.join(to_txt.dirname, 'output.txt')
    for root, _, files in wk.walk(to_txt.dirname, tfiles=['png']):
        for f in files:
            if (f.name).startswith(to_txt.basename):
                filepath = os.path.join(root, f.name)
                log.info('tesseract is processing: {}'.format(filepath))
                tesseract(filepath, None, opts)
                if thread:
                    thread._cursor_end.emit(True)
                try:
                    raw = raw_data(outputpath)
                    text = text + '\n' + raw
                except Exception, e:
                    log.critical(e)
                remove(os.path.join(root, f.name))
    remove(outputpath)
    if thread:
        thread._cursor_end.emit(True)
    return save_raw_data(to_txt.path, text)

# def from_pdf_ocr(hero='xpdf'):

#     log.debug('')
#     log.debug('[new conversion]')
#     log.debug('starting pdf_ocr to txt')

#     if not overwrite and os.path.exists(txt.path):
#         log.debug(txt.path, 'yet exists')
#         return txt.path

#     necessary_ocr, out_info = need_ocr()
#     if not necessary_ocr:
#         return from_pdf(hero)

#     options = [pdftopng,
#                file._path,
#                os.path.join(file._tempdir, 'image')]

#     options = ' '.join(options)
#     log.debug('from_pdf_ocr', 'set options pdftopng:', options)
#     try:
#         log.debug('from_pdf_ocr', 'calling pdftopng')
#         sub.call(options, shell=True)
# sub.call(options)
#     except Exception, e:
#         log.debug('*', 'from_pdf_ocr', 'fail to use pdftopng')
#         log.debug(e)
#         return ''

#     txt = open(txt.path, 'w')

#     page = 1
#     for root, dirs, files in wk.walk(file._tempdir, tfiles=['.png']):
#         for f in files:
#             p_ = os.path.join(root, f.name)
#             o_ = os.path.join(root, 'output')
#             cmd = [tesseract_binary, p_, o_, '-l', 'spa']
#             cmd = ' '.join(cmd)
#             try:
#                 log.debug('from_pdf_ocr', 'processing page ' + str(page))
#                 page += 1
#                 sub.call(cmd, shell=True)
#             except:
#                 log.debug('* from_pdf_ocr', 'fail subprocess with', cmd)
#                 return ''

#             f_ = file(o_ + '.txt', 'r')
#             for line in f_:
#                 txt.write(line)
#             f_.close()
#     txt.close()
#     return txt.path
