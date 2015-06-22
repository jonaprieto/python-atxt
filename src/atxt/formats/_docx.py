#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:53:06
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-04-25 14:54:12
from atxt.log_conf import Logger
log = Logger.log

from atxt.infofile import InfoFile
from atxt.encoding import latin2ascii

import codecs
import docx as libDOCX



def docx(from_file, to_txt, opts):
    log.debug('from_docx processing using %s' % hero)
    if not isinstance(info_file, InfoFile):
        _file = InfoFile(info_file)
    if not isinstance(info_txt, InfoFile):
        _txt = InfoFile(info_txt)

    try:
        _txt.content = codecs.open(txt.path, encoding=encoding)
    except Exception, e:
        log.critical('fail to create txt: %s' % _txt.basename)
        log.critical(e)
        return None

    if hero == 'python-docx':
        _doc = docx.opendocx(_file.path)
        for line in docx.getdocumenttext(_doc):
            line = latin2ascii(unicode(line, 'utf-8', 'ignore'))
            line = line.encode('utf-8', 'replace')
            _txt.content.write(line + '\n')
        _txt.content.close()
        log.debug('finish work with .docx')
        return _txt
    elif hero == 'xml':
        try:
            _content = from_docx_(info_file, info_txt, encoding)
            _txt.content.write(_content)
        except Exception, e:
            log.critical(e)
            return None
    return _txt


def from_docx_xml(info_file, info_txt,  encoding='utf-8'):
    """
     http://stackoverflow.com/questions/42482/best-way-to-extract-text-from-a-word-doc-
     without-using-com-automation
    """

    try:
        from xml.etree.cElementTree import XML
    except:
        from xml.etree.ElementTree import XML
        log.warning('*', 'from_docx_ failed XML')

    if not isinstance(info_file, InfoFile):
        _file = InfoFile(info_file)
    if not isinstance(info_txt, InfoFile):
        _txt = InfoFile(info_txt)

    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'

    document = zp.ZipFile(_file.path)

    log.debug('from_docx_ zipfile open document')
    xml_content = document.read('word/document.xml')
    document.close()

    log.debug('from_docx_ XML(xml_content)')
    tree = XML(xml_content)
    paragraphs = []

    log.debug('from_docx_ tree.iterator')
    for paragraph in tree.getiterator(PARA):
        line = [n.text for n in paragraph.getiterator(TEXT) if n.text]
        line = ''.join(line)
        line = latin2ascii(unicode(line, encoding, 'ignore'))
        try:
            line = line.encode(encoding, 'replace')
        except:
            pass
        if line:
            paragraphs.append(line)
    return '\n\n'.join(paragraphs)