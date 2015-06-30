#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _utils import raw_data, save_raw_data
from atxt.log_conf import Logger
from atxt.utils import remove
from jpg import imagen


__all__ = ['png']
log = Logger.log

def png(from_file, to_txt, opts):
    return imagen(from_file, to_txt, opts)
