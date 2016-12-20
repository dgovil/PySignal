import re
import ast
from setuptools import setup
import PySignal


_version_re = re.compile(r'__version__\s+=\s+(.*)')
_author_re = re.compile(r'__author__\s+=\s+(.*)')
_email_re = re.compile(r'__email__\s+=\s+(.*)')


with open('PySignal.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))
    author = str(ast.literal_eval(_author_re.search(
        f.read().decode('utf-8')).group(1)))
    email = str(ast.literal_eval(_email_re.search(
        f.read().decode('utf-8')).group(1)))


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
