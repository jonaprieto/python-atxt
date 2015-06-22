#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 03:49:40
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-05-25 11:50:53
import logging

def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class Logger(object):
    def __init__(self):
        LOG_LEVEL = logging.DEBUG
        # LOG_LEVEL = logging.INFO
        LOGFORMAT = "%(log_color)s%(levelname)-1s%(reset)s | %(log_color)s%(message)s%(reset)s [%(filename)s:%(lineno)s - %(funcName)s() ] "
        logging.root.setLevel(LOG_LEVEL)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        try:
            from colorlog import ColoredFormatter
            formatter = ColoredFormatter(LOGFORMAT)
            stream.setFormatter(formatter)
        except:
            pass
        self.log = logging.getLogger('root')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)