#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 13:08:14
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 13:15:16
from atxt.log_conf import Logger
log = Logger.log

 def need_ocr():
        try:
            if not file._path:
                file.create_temp()
            cmd = pdffonts + ' ' + file._path
        except:
            cmd = pdffonts + ' ' + file.path
            log.debug('cmd', cmd)

        o_ = ''
        try:
            log.debug('OCR?')
            o_ = sub.check_output(cmd, shell=True)

            log.debug('using pdffonts')
            log.debug('\n' + o_)
            if o_.count('yes') or o_.count('Type') or o_.count('no'):
                log.debug('ORC is not necessary!')
                return False, o_

        except Exception, e:
            log.debug('* from_pdf_ocr', 'looks like OCR is necessary')
            log.debug(e)
        return True, o_