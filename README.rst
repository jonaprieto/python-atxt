aTXT
====

Extract the text from files. Text mining tool.

|PyPI Package latest release| |Code Quality Status| |Scrtinizer Status|
|PyPI Package monthly downloads| |GitHub issues for python-atxt|

Usage
-----

You can use aTXT with his name package or with 2txt in your console. For
example, if you want to show the help usage:

::

    aTXT -h

::

    2txt -h

Also, you can run the graphical interface (with PySide):

::

    aTXT -i

You should something like this:

|GUI|

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

Installation
------------

::

    pip install atxt

Check dependencies for avoiding surprises:

::

    aTXT --check

Requirements
------------

This software is available thanks to others open sources projects. The
following list itemizes some of those more hard to install:

-  PySide (GUI lib)
-  Tessaract OCR
-  Xpdf
-  scandir (trasversal folders fast)

Meta
----

-  Author: Jonathan S. Prieto C.
-  Email: prieto.jona@gmail.com
-  Notes: Have feedback? Please send me an email.
-  Free software: BSD license

Issues
======

Please be free to comment whatever issue or problem with the
installation. http://github.com/d555/python-atxt/issues

.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/atxt.png?style=flat
   :target: https://pypi.python.org/pypi/atxt
.. |Code Quality Status| image:: https://landscape.io/github/d555/python-atxt/master/landscape.svg?style=flat
   :target: https://landscape.io/github/d555/python-atxt/master
.. |Scrtinizer Status| image:: https://img.shields.io/scrutinizer/g/d555/python-atxt/master.png?style=flat
   :target: https://scrutinizer-ci.com/g/d555/python-atxt/
.. |PyPI Package monthly downloads| image:: http://img.shields.io/pypi/dm/atxt.png?style=flat
   :target: https://pypi.python.org/pypi/atxt
.. |GitHub issues for python-atxt| image:: https://img.shields.io/github/issues/d555/python-atxt.svg?style=flat-square
   :target: https://github.com/d555/python-atxt/issues
.. |GUI| image:: https://raw.githubusercontent.com/d555/python-atxt/master/gui.png
   :target: https://pypi.python.org/pypi/atxt
