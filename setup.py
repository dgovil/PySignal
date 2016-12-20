from setuptools import setup
import PySignal




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
    version=PySignal.__version__,
    description="Python Signal Library to mimic the Qt Signal system for event driven connections",
    author=PySignal.__author__,
    author_email=PySignal.__email__,
    url="https://github.com/dgovil/PySignal",
    license="MIT",
    zip_safe=False,
    py_modules=["PySignal"],
    classifiers=classifiers,
    keywords=['signals', 'qt', 'events']
)