#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 03:49:40
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-19 15:56:02
import colorlog
import logging

def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class Logger():
    def __init__(self):
        LOG_LEVEL = logging.DEBUG
        # LOG_LEVEL = logging.INFO
        LOGFORMAT = "%(log_color)s%(levelname)-1s%(reset)s | %(log_color)s%(message)s%(reset)s [%(filename)s:%(lineno)s - %(funcName)s() ] "
        from colorlog import ColoredFormatter
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger('root')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)