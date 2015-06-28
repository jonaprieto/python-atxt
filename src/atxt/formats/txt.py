#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-04-25 14:07:56
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-28 00:49:27
from __future__ import print_function

import codecs

from _utils import raw_data, find_encoding, save_raw_data
from atxt.log_conf import Logger
import chardet


log = Logger.log
__all__ = ['txt']


def txt(from_file, to_txt, opts, thread=None):
    """This function serves as example
    """
    log.debug('txt2txt starting')
    _encoding = find_encoding(from_file.path)
    text = raw_data(from_file.path, _encoding)
    return save_raw_data(to_txt.path, text, _encoding)
