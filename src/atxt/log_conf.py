#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import logging
from logging import StreamHandler, DEBUG, getLogger as realGetLogger, Formatter


from colorama import Fore, Back, Style, init
init()


class ColourStreamHandler(StreamHandler):

    """ A colorized output SteamHandler """

    # Some basic colour scheme defaults
    colours = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARN': Fore.YELLOW,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRIT': Back.RED + Fore.WHITE,
        'CRITICAL': Back.RED + Fore.WHITE
    }

    def emit(self, record):
        try:
            message = self.format(record)
            line = self.colours[
                record.levelname] + '{: <5} | '.format(record.levelname)

            if record.levelname not in ['CRITICAL', 'CRIT']:
                line += Style.RESET_ALL

            line += message
            if record.levelname in ['DEBUG','CRITICAL', 'CRIT']:
                line += ' :: {filename} : {lineno}'.format(
                    filename=record.filename, lineno=record.lineno)
            line += Style.RESET_ALL
            self.stream.write(line)
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def getLogger(name=None, fmt='%(message)s'):
    log = realGetLogger(name)
    handler = ColourStreamHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(fmt))
    log.addHandler(handler)
    log.setLevel(DEBUG)
    log.propagate = 0  # Don't bubble up to the root logger
    return log


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()


@singleton
class Logger(object):

    def __init__(self, level=logging.INFO):
        # LOG_LEVEL = level
        # logging.root.setLevel(LOG_LEVEL)
        # stream = logging.StreamHandler()
        # stream.setLevel(LOG_LEVEL)

        # LOGFORMAT = "%(levelname)-1s | %(message)s ::%(filename)s:%(lineno)s"
        # try:
        # LOGFORMAT = "%(log_color)s%(levelname)-1s%(reset)s | %(log_color)s%(message)s%(reset)s ::%(filename)s:%(lineno)s"
        #     from colorlog import ColoredFormatter
        #     formatter = ColoredFormatter(LOGFORMAT)
        #     stream.setFormatter(formatter)
        # except Exception:
        #     formatter = logging.Formatter(LOGFORMAT)
        self.log = getLogger('root')
        # self.log.setLevel(LOG_LEVEL)
        # self.log.addHandler(stream)
