#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:52:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 14:04:43
from atxt.log_conf import Logger
log = Logger.log

def from_pdf( hero='xpdf'):
        log.debug('')
        log.debug('[new conversion]')
        log.debug('starting pdf to txt')

        if not overwrite and os.path.exists(txt.path):
            log.debug(txt.path, 'yet exists')
            return txt.path
        try:
            log.debug('from_pdf opening to read', file._path)
            doc_ = file(file._path, 'rb')
        except Exception, e:
            log.debug('* from_pdf', e)
            return ''
        try:
            log.debug('from_pdf creating to write', txt.path)
            f = file(txt.path, 'wb')
            log.debug('from_pdf created', txt.basename)
        except Exception, e:
            log.debug('* from_pdf', e)
            return ''

        log.debug('\thero:' + hero)

        if hero == 'pdfminer':
            try:
                log.debug('from_pdf', 'creating PDFResourceManager')
                resourceman = pdfinterp.PDFResourceManager()
                log.debug('from_pdf',  'using TextConverter')
                device = converter.TextConverter(
                    resourceman, f, laparams=layout.LAParams())
                log.debug('from_pdf',  'using PDFPageInterpreter')
                interpreter = pdfinterp.PDFPageInterpreter(resourceman, device)
                for page in pdfpage.PDFPage.get_pages(doc_):
                    interpreter.process_page(page)
                f.close()
                device.close()
            except Exception, e:
                log.debug('* from_pdf', e)
                return ''

        if hero == 'xpdf':
            try:
                log.debug('from_pdf', 'xpdf')
                options = [pdftotext, file._path, '-']

                log.debug('from_pdf', options)
                log.debug('from_pdf', 'starting subprocess')
                output = sub.call(options, stdout=f)
                log.debug('from_pdf', 'finished subprocess')
                if output == 0:
                    log.debug('from_pdf', 'No error.')
                elif output == 1:
                    log.debug('from_pdf', 'Error opening a PDF file.')
                elif output == 2:
                    log.debug('from_pdf', 'Error opening an output file.')
                elif output == 3:
                    log.debug(
                        'from_pdf', 'Error related to PDF permissions.')
                else:
                    log.debug('from_pdf', 'Other error.')
            except Exception, e:
                log.debug('*', 'from_pdf', e)
        f.close()
        doc_.close()
        return txt.path

def from_pdf_ocr( hero='xpdf'):

        log.debug('')
        log.debug('[new conversion]')
        log.debug('starting pdf_ocr to txt')

        if not overwrite and os.path.exists(txt.path):
            log.debug(txt.path, 'yet exists')
            return txt.path

        necessary_ocr, out_info = need_ocr()
        if not necessary_ocr:
            return from_pdf(hero)

        options = [pdftopng,
                   file._path,
                   os.path.join(file._tempdir, 'image')]

        options = ' '.join(options)
        log.debug('from_pdf_ocr', 'set options pdftopng:', options)
        try:
            log.debug('from_pdf_ocr', 'calling pdftopng')
            sub.call(options, shell=True)
            # sub.call(options)
        except Exception, e:
            log.debug('*', 'from_pdf_ocr', 'fail to use pdftopng')
            log.debug(e)
            return ''

        txt = open(txt.path, 'w')

        page = 1
        for root, dirs, files in wk.walk(file._tempdir, tfiles=['.png']):
            for f in files:
                p_ = os.path.join(root, f.name)
                o_ = os.path.join(root, 'output')
                cmd = [tesseract_binary, p_, o_, '-l', 'spa']
                cmd = ' '.join(cmd)
                try:
                    log.debug('from_pdf_ocr', 'processing page ' + str(page))
                    page += 1
                    sub.call(cmd, shell=True)
                except:
                    log.debug('* from_pdf_ocr', 'fail subprocess with', cmd)
                    return ''

                f_ = file(o_ + '.txt', 'r')
                for line in f_:
                    txt.write(line)
                f_.close()
        txt.close()
        return txt.path