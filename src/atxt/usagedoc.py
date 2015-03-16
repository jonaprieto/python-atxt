#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 17:13:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-15 20:53:47


"""
A Data Mining Tool For Extract Text From Files

Usage:
    aTXT
    aTXT -i [--log <log>]
    aTXT <file> [-uo] [--to <to>] [--verbose] [--log <log>]
    aTXT [--from <from>] [--to <to>] <file>... [-uo] [--verbose] [--log <log>]
    aTXT [--path <path>] [--depth <depth>] [--to <to>] [--all][<format>...] [-uo] [--log <log>]
    aTXT [-h|--help] 

Arguments:
    <file>            If <from> is none, file should be in current directory.
    --path            Process the folder with path <path> and all files inside. [default: ./]
    <format>          formats of files

General Options:
    -i                Launch the (GUI) Graphical Interface.
    --from <from>     Process files from path <from>. [default: ./]
    --to <to>         Save all (*.txt) files to path <to> if <file> appears. [default: ./]
    --depth <depth>   Integer for depth for trasvering path using depth-first-search
                      for --path option. [default: 1]
    --all             Convert all allowed supported formats.
    -u                Use uppercase for all text processed.
    -o                Overwrite if *.txt file version yet exists.
    -h, --help        Print this help.
    --log <log>       Save log file. 
    --version         Print current version installed.
    --verbose         Print error messages. [default: 1]
"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
