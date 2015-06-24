#!/usr/bin/env python
# -*- coding: utf-8 -*-
from atxt.log_conf import Logger
log = Logger.log

import subprocess as sub

from app.check import pdftotext as bpdftotext
from app.check import pdftopng as bpdftopng
from app.check import pdffonts as bpdffonts
from app.check import tesseract as btesseract


def pdftotext(filepath, txt_path):
    f = file(txt_path, 'wb')
    options = ' '.join([bpdftotext(), filepath, '-'])
    output = sub.call(options, stdout=f)
    if output == 0:
        log.debug('Everything ok. pdftotext.')
    elif output == 1:
        raise IOError('Error opening a PDF file: %s.' % from_path)
    elif output == 2:
        raise IOError('Error opening the output file.: %s.' % txt_path)
    elif output == 3:
        raise IOError('Error related to PDF permissions.')
    else:
        raise IOError('Unkwown Error.')
    f.close()


def pdffonts(filepath):
    cmd = bpdffonts() + ' ' + filepath
    return sub.check_output(cmd, shell=True)


def need_ocr(filepath):
    output = pdffonts(filepath)
    assert isinstance(output, unicode) or isinstance(output, str)
    if output.count('yes') or output.count('Type') or output.count('no'):
        log.info('ORC is not necessary with: %s' % filepath)
        return False
    return True


def pdftopng(filepath, to_path=None):
    if not to_path:
        to_path = os.path.dirname(filepath)
    options = ' '.join([bpdftopng(), filepath, to_path])
    sub.call(options, shell=True)


def tesseract(filepath, txt_path='', opts='-l spa'):
    if not txt_path:
        txt_path = os.path.join(os.path.dirname(filepath), 'output.txt')
    cmd = ' '.join([btesseract(), filepath, txt_path])
    if opts:
        cmd = cmd + ' ' + opts
    sub.call(cmd, shell=True)
