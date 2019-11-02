#!/usr/bin/env python
from setuptools import setup, find_packages
import re
import os

# There is an issue with building python packages in a shared vagrant directory because of how setuptools works
# in python < 2.7.9. We solve this by deleting the filesystem hardlinking capability during build.
# See: http://stackoverflow.com/a/22147112/381010
del os.link

description = "Simple tool for inserting new entries in yaml files while keeping the original structure and formatting"
long_description = """
Simple tool for inserting new entries in yaml files while keeping the original structure and formatting.

Source code on `github.com/jorisroovers/yamlpal`_.

.. _github.com/jorisroovers/yamlpal: https://github.com/jorisroovers/yamlpal
"""


# shamelessly stolen from mkdocs' setup.py: https://github.com/mkdocs/mkdocs/blob/master/setup.py
def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="yamlpal",
    version=get_version("yamlpal"),
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        'Click==6.2',
        'PyYAML==5.1'
    ],
    keywords='yamlpal yaml',
    author='Joris Roovers',
    url='https://github.com/jorisroovers/yamlpal',
    license='MIT',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "yamlpal = yamlpal.cli:cli",
        ],
    },
)
