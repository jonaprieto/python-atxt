#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='aTXT',
    version='1.0.5.9',
    license='BSD',
    description='data mining tool for extract text for files',
    long_description='%s\n%s' % (
        read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author='Jonathan Steven Prieto C.',
    author_email='prieto.jona@gmail.com',
    url='https://github.com/d555/python-atxt',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    keywords=[
        'text', 'extraction', 'mining', 'tool', 'data', 'pdf2txt', 'csv2txt',
        'text', 'txt', 'doc', 'docx', 'pdf', 'csv', 'png', 'jpg', 'doc2txt', 'docx2txt', 'convert'
    ],
    install_requires=map(
        lambda x: x.strip(), open('requirements.txt').readlines()),
    extra_require={
        'gui': ['PySide']
    },
    entry_points={
        'console_scripts': [
            'atxt = atxt.__main__:main',
            '2txt = atxt.__main__:main',
        ]
    },
)


# pandoc --from=rst --to=rst --output=README.rst README.rst
# Pasos para subir a pypi
# git tag v...
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
