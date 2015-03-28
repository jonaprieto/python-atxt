#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 17:13:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-28 00:28:41


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


# Arguments:
#     <source>          origin of data, it can be file(s) or folder(s) with files
# Options:
#     -h, --help        Show this message and exit
#     --version         Print current version installed.
#     -i                Launch the (GUI) Graphical Interface.
#     --from <from>     path to relative <sources> ./ [default: ./]
#     --to <to>         folder destination for outcomes files.
#                       [default: ./]
#     --enc ENCODING    Encoding for input file, or files
#                       [default: utf-8]
#     --depth DEPTH   Integer for depth for trasvering path using 
#                       depth-first-search on folders @int for --path option. 
#                       [default: 0]
#     -o                Overwrite if *.txt file version exists yet.
#     --all             Convert all allowed supported extensions.
#     --use_temp        No use temp generation file by each file
#     --lang LANG     Specific language for OCR tasks.
#     --log  LOG       Save log file. [default: ./]
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
