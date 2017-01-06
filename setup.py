import os
import re
import ast
from setuptools import setup
import PySignal

with open('PySignal.py', 'rb') as f:
    contents = f.read().decode('utf-8')


def parse(pattern):
    return re.search(pattern, contents).group(1).replace('"', '').strip()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = parse(r'__version__\s+=\s+(.*)')
author = parse(r'__author__\s+=\s+(.*)')
email = parse(r'__email__\s+=\s+(.*)')

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.5",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]



setup(
    name="PySignal",
    version=version,
    description="Python Signal Library to mimic the Qt Signal system for event driven connections",
    author=author,
    author_email=email,
    url="https://github.com/dgovil/PySignal",
    license="MIT",
    zip_safe=False,
    py_modules=["PySignal"],
    classifiers=classifiers,
    keywords=['signals', 'qt', 'events']
)
