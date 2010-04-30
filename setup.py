#! /usr/bin/env python

from distutils.core import setup
from table_fu import __doc__, __version__, __author__

long_description = open('README.markdown').read()

setup(
    name = "python-tablefu",
    version = __version__,
    author = "Chris Amico",
    author_email = "eyeseast@gmail.com",
    description = "A tool for manipulating spreadsheets and tables in Python, based on ProPublica's TableFu",
    long_description = long_description,
    packages = ['table_fu'],
    url = "http://github.com/eyeseast/python-tablefu",
    platforms = ['any'],
    classifiers = ["Development Status :: 1 - Alpha",
                   "Intended Audience :: Developers",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
)
