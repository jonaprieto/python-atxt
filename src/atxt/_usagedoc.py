#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 17:13:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-04-25 14:11:19


"""
A Data Mining Tool For Extract Text From Files

Usage:
    aTXT
    aTXT -i [options] 
    aTXT <source>... [--] [<ext>]...

Options:
    -h, --help              Show this message and exit
    -v, --version               Print current version installed.
    -i                      Launch the (GUI) Graphical Interface.
    -l, --log               folder destination for log file.
    -d, --depth DEPTH       Integer for depth for trasvering path using 
                            Depth-first-search on folders @int for --path option.
                            [default: 0]
    -f, --from FROM         path to relative <sources> ./ [default: ./]
    -t, --to TO             folder destination for outcomes files.
                            [default: ./]
    -e, --enc ENCODING      Encoding for input file, or files
                            [default: utf-8]
"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
