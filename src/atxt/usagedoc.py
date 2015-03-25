#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 17:13:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-20 23:26:10


"""
A Data Mining Tool For Extract Text From Files

Usage:
    aTXT
    aTXT -i [--log <log>] [--enc <enc>] [-uo]
    aTXT <file> [-uo] [--to <to>] [-uo] [--verbose] [--log <log>] [--lang <lang>] [--use-temp] [--enc <enc>]
    aTXT [--from <from>] [--to <to>] <file>... [-uo] [--verbose] [--log <log>] [--lang <lang>] [--use-temp] [--enc <enc>]
    aTXT [--path <path>] [--depth <depth>] [--to <to>] [--all] [<format>...] [-uo] [--log <log>] [--lang <lang>] [--use-temp] [--enc <enc>]
    aTXT [-h|--help] 

Arguments:
    <file>            If <from> is none, file should be in current directory.
    --path            Process the folder with path <path> and all files inside. [default: ./]
    <format>          formats of files

General Options:
    -i                Launch the (GUI) Graphical Interface.
    --from <from>     Process files from path <from>. [default: ./]
    --to <to>         Save all (*.txt) files to path <to> if <file> appears. [default: ./]
    --depth <depth>   Integer for depth for trasvering path using depth-first-search  @int
                      for --path option. [default: 1]
    --all             Convert all allowed supported formats.
    --use_temp        No use temp generation file by each file
    --enc <enc>       Encoding for input file, or files [default: utf-8]
    -u                Use uppercase for all text processed.
    -o                Overwrite if *.txt file version yet exists.
    --lang <lang>     Specific language of the input file
    -h, --help        Print this help.
    --log <log>       Save log file. 
    --version         Print current version installed.
    --verbose         Print error messages. [default: 1]
"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
