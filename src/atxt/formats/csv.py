#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:53:25
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 14:26:43

from atxt.log_conf import Logger
log = Logger.log

def from_csv(info_file, info_txt, encoding='utf-8'):
    return info_txt