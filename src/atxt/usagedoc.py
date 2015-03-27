#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 17:13:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-26 22:07:49


"""
A Data Mining Tool For Extract Text From Files

Usage:
    aTXT
    aTXT -i [--log] [--enc <enc>] [-uo]
    aTXT <file> [-uo] [--to <to>] [-uo] [--verbose] [--log] [--lang <lang>] [--use-temp] [--enc <enc>]
    aTXT [--from <from>] [--to <to>] <file>... [-uo] [--verbose] [--log] [--lang <lang>] [--use-temp] [--enc <enc>]
    aTXT [--path <path>] [--depth <depth>] [--to <to>] [--all] [<format>...] [-uo] [--log] [--lang <lang>] [--use-temp] [--enc <enc>]
    aTXT [-h|--help] 

Options:
    -h, --help        Show this message and exit
    --version         Print current version installed.
    -i                Launch the (GUI) Graphical Interface.
    --from <from>     Process files from path <from>. [default: ./]
    --path <path>     source folder.    
    --to <to>         folder destination.
                      [default: ./]    
    --enc <enc>       Encoding for input file, or files
                      [default: utf-8]
    --depth <depth>   Integer for depth for trasvering path using 
                      depth-first-search  @int for --path option. 
                      [default: 0]
    --all             Convert all allowed supported formats.
    --use_temp        No use temp generation file by each file
    -u                Use uppercase for all text processed.
    -o                Overwrite if *.txt file version yet exists.
    --lang <lang>     Specific language for OCR tasks.
    --log  <log>      Save log file. [default: ./]
    --verbose         Print error messages. [default: 1]
"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
