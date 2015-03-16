#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 22:29:02
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 04:10:28

import os
import sys

from log_conf import Logger
log = Logger.log

import tempfile as tmp
from encoding import encoding_path
import utils



class InfoFile():

    """
        Handle file

        .path
        .basename
        .name
        .extension
        .dirname

    """
    @property
    def path(self):
        return self._path

    @property
    def dirname(self):
        return self._dirname

    @property
    def basename(self):
        return self._basename

    @property
    def name(self):
        return self._name

    @property
    def extension(self):
        return self._extension

    def __init__(self, file_path):
        log.debug('extracting data file from %s' % file_path)
        self._path = os.path.abspath(encoding_path(file_path))
        try:
            self._basename = os.path.basename(self._path)
            self._extension = utils.extract_ext(self._basename)
            name, ext = os.path.splitext(self._basename)
            self._name = name
            self._dirname = os.path.dirname(self._path)
        except Exception, e:
            log.error(e)

    def remove(self):
        utils.remove(self.path)
        # TODO remove entire object

    def size(self):
        return utils.size(self.path)

    def move(self, to_path=None):
        utils.move_to(self.path, to_path)

    def __repr__(self):
        return encoding_path(self.path)

    @property
    def temp(self):
        try:
            self._temp_path
        except:
            return self.create_temp()

    def create_temp(self, value=None):
        self._temp_dir = value
        if not value or not os.path.exists(self._temp_dir):
            try:
                log.debug('creating a temporary directory')
                self._temp_dir = tmp.mkdtemp()
                log.debug('tempdir: %s' % self._temp_dir)
            except Exception, e:
                log.error(e)
                return None
        utils.copy_to(self._path, self._temp_dir)

        self._temp_basename = self._basename
        self._temp_path = os.path.join(self._temp_dir, self._temp_basename)

        log.debug('temp path: %s' % self._temp_path)
        return self._temp_path

    def remove_temp(self):
        try:
            utils.remove_dir(self._temp_dir)
            del self._temp_basename
            del self._temp_path
            del self._temp_dir
        except AttributeError,e:
            log.warning('%s file has not temporal version'%self._basename)
