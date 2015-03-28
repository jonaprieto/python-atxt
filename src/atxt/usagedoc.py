#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 17:13:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-27 23:52:53


"""
aTXT tool

Usage:
  aTXT <source>... [--ext <ext>...]

Options:
    --ext       message

"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
