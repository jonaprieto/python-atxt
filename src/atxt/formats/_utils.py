#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 13:09:59
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-16 13:15:18

from atxt.log_conf import Logger
log = Logger.log

 def upper():
        if not os.path.exists(txt.path):
            log.debug(txt.path, 'Not Found')
            return txt.path

        # FIXME: maybe it's enough with file._path
        temp = tmp.NamedTemporaryFile(mode='w', delete=False)

        with open(txt.path, 'r') as f:
            for line in f:
                try:
                    line = remove_accents(line)
                except:
                    # log.debug('from upper', 'fail remove_accents')
                    pass
                try:
                    line = enconding_path(line)
                except:
                    pass
                # try:
                #     line = latin2ascii(line)
                # except:
                #     log.debug('from upper', 'fail latin2ascii')
                try:
                    line = line.encode('utf-8', 'replace')
                except:
                    # log.debug('from upper', 'fail encode(ascii)')
                    pass
                try:
                    line = line.upper()
                except:
                    # log.debug('*', 'from upper', 'fail .upper()')
                    pass
                temp.write(line)
            temp.close()

            txt.remove()

            try:
                log.debug('moving tempfile', temp.name)
                sh.copy2(temp.name, txt.path)
            except:
                try:
                    sh.remove(temp.name)
                except Exception, e:
                    log.debug('*', 'fail to move tempfile', temp.name)
                    log.debug(e)
                return ''
        return txt.path