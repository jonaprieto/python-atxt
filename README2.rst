aTXT
====

A Data Mining Tool For Extract Text From Files.

|PyPI Package latest release| |Code Quality Status| |Scrtinizer Status|
|PyPI Package monthly downloads|

Meta
----

-  Author: Jonathan S. Prieto C.
-  Email: prieto.jona@gmail.com
-  Notes: Have feedback? Please send me an email.
-  Free software: BSD license

Requirements
------------

This software is available thanks to others open sources projects. The
following list itemizes some of those:

-  PySide (GUI lib)
-  Tessaract OCR
-  Xpdf
-  lxml (doc files)
-  scandir (trasversal folders fast)
-  docx

Installation
------------

::

    pip install atxt

Check dependencies for avoiding surprises:

::

    aTXT --check

Show help for command line: :

::

    aTXT -h

Usage
-----

In every case, you can use aTXT with his name package or more easy: :

::

    2txt -h

You can use the graphical interface (if you have installed PySide):

::

    aTXT -i

You should something like this:

image:: http://github.com/d555/python-atxt/gui.png

Note: aTXT will always generate a FILE for each file path.

Examples: :

::

    $ 2txt prueba.html
    $ 2txt prueba.html -o
    $ 2txt --file ~/Documents/prueba.html
    $ 2txt --file ~/Documents/prueba.html --to ~/htmls

Searching all textable files in a level-2 of depth over ~: :

::

    $ 2txt ~ -d 2
    $ 2txt --path ~ -d 2 --format 'txt,html'

.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/atxt.png?style=flat
   :target: https://pypi.python.org/pypi/atxt
.. |Code Quality Status| image:: https://landscape.io/github/d555/python-atxt/master/landscape.svg?style=flat
   :target: https://landscape.io/github/d555/python-atxt/master
.. |Scrtinizer Status| image:: https://img.shields.io/scrutinizer/g/d555/python-atxt/master.png?style=flat
   :target: https://scrutinizer-ci.com/g/d555/python-atxt/
.. |PyPI Package monthly downloads| image:: http://img.shields.io/pypi/dm/atxt.png?style=flat
   :target: https://pypi.python.org/pypi/atxt
