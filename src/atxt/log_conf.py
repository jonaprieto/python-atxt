#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

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
        LOGFORMAT = "%(log_color)s%(levelname)-1s%(reset)s | %(log_color)s%(message)s%(reset)s ::%(filename)s:%(lineno)s"
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