#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
from __future__ import print_function

import os
import shutil as sh
import subprocess
import sys

from distutils.spawn import find_executable
from log_conf import Logger
from osinfo import osinfo


log = Logger.log

vendors = os.path.dirname(os.path.abspath(__file__))
vendors = os.path.join(vendors, 'vendors')


def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False or len(which(name)) > 0
    return True


def check_os():
    info = osinfo.OSInfo()
    return info.system


def check_office():
    system = check_os()
    if system != 'Windows':
        return False
    try:
        from win32com import client
        self.msword = client.DispatchEx('Word.Application')
        self.msword.Visible = False
        self.msword.Quit()
        log.debug('Successful Dispatching of Word.Application')
    except Exception, e:
        log.debug(e)
    return False


def path_program(name):
    system = check_os()
    path = vendors
    if system == 'Windows':
        name = name + '.exe' if not name.endswith('.exe') else name
        path = os.path.join(vendors, system)
    else:
        path = os.path.join(vendors, 'Unix')
    p = find_executable(name)
    return p if p else find_executable(name, path=path)


def path_pdftotext():
    return path_program('pdftotext')


def path_pdftopng():
    return path_program('pdftopng')


def path_pdffonts():
    return path_program('pdffonts')


def path_tesseract():
    return path_program('tesseract')


def check():
    p = path_pdftotext()
    if p:
        log.debug(p)
    else:
        log.warning('Xpdf: pdftotext is not available')

    p = path_pdftopng()
    if p:
        log.debug(p)
    else:
        log.warning('Xpdf: pdftopng is not available')

    p = path_pdffonts()
    if p:
        log.debug(p)
    else:
        log.warning('Xpdf: pdffonts is not available')
    p = path_tesseract()
    if p:
        log.debug(p)
    else:
        log.warning('Xpdf: pdffonts is not available')
    if not check_office() and check_os == 'Windows':
        log.warning(
            'PyWin32 or Microsoft Office Suite is not installed or not available.')
