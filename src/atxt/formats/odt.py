#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-15 10:03:09
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-15 10:26:40
from __future__ import print_function

import zipfile
import xml.etree.ElementTree as ET
import StringIO

from _utils import raw_data, find_encoding, save_raw_data
from atxt.log_conf import Logger

# this format is bring to us thanks to:
# https://github.com/deanmalmgren/textract/blob/master/textract/parsers/odt_parser.py


def text_to_string(element):
    buff = u""
    if element.text is not None:
        buff += element.text
    for child in element:
        if child.tag == qn('text:tab'):
            buff += "\t"
            if child.tail is not None:
                buff += child.tail
        elif child.tag == qn('text:s'):
            buff += u" "
            if child.get(qn('text:c')) is not None:
                buff += u" " * (int(child.get(qn('text:c'))) - 1)
            if child.tail is not None:
                buff += child.tail
        else:
            buff += text_to_string(child)
    if element.tail is not None:
        buff += element.tail
    return buff


def qn(namespace):
    """Connect tag prefix to longer namespace"""
    nsmap = {
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    }
    spl = namespace.split(':')
    return '{{{}}}{}'.format(nsmap[spl[0]], spl[1])


def odt(from_file, to_txt, opts):
    content = None
    with open(from_file.path) as stream:
        zip_stream = zipfile.ZipFile(stream)
        content = ET.fromstring(zip_stream.read("content.xml"))

    buff = u""
    for child in content.iter():
        if child.tag in [qn('text:p'), qn('text:h')]:
            buff += text_to_string(child) + "\n"
    if buff:
        buff = buff[:-1]
    return save_raw_data(to_txt.path, buff)
