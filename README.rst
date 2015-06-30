===============================
aTXT
===============================

| A Data Mining Tool For Extract Text From Files.

| |version| |landscape| |scrutinizer| |downloads|

.. |version| image:: http://img.shields.io/pypi/v/atxt.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/atxt

.. |landscape| image:: https://landscape.io/github/d555/python-atxt/master/landscape.svg?style=flat
    :target: https://landscape.io/github/d555/python-atxt/master
    :alt: Code Quality Status


.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/d555/python-atxt/master.png?style=flat
    :alt: Scrtinizer Status
    :target: https://scrutinizer-ci.com/g/d555/python-atxt/

.. |downloads| image:: http://img.shields.io/pypi/dm/atxt.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/atxt



Meta
============

-  Author: Jonathan S. Prieto C.
-  Email: prieto.jona@gmail.com
-  Notes: Have feedback? Please send me an email. 
* Free software: BSD license

Requirements
============

This software is available thanks to others open sources projects.
The following list itemizes some of those:

- PySide (GUI lib)
- Tessaract OCR 
- Xpdf
- lxml (doc files)
- scandir (trasversal folders fast) 
- docx

Installation
============

::

    pip install atxt

Check dependencies for avoiding surprises:

::

    atxt --check

Show help for command line:
::

    atxt -h

Usage
============
You can use the graphical interface (if you have installed PySide):

::

    atxt -i

Note: aTXT will always generate a FILE for each file path.

Examples:
::

    $ atxt prueba.html
    $ atxt prueba.html -o
    $ atxt --file ~/Documents/prueba.html
    $ atxt --file ~/Documents/prueba.html --to ~/htmls

Searching all textable files in a level-2 of depth over ~:
::

    $ atxt ~ -d 2
    $ atxt --path ~ -d 2 --format 'txt,html'
