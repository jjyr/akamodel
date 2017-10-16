#!/usr/bin/env python
from __future__ import unicode_literals

import logging
import subprocess
import sys

from setuptools import Command
from setuptools import find_packages, setup

LOG = logging.getLogger(__name__)

description = "An ActiveRecord-like ORM in python world"


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(['tests'])
        sys.exit(errno)


setup(name='akamodel',
      version='0.0.0',
      license='Apache-2.0',
      description=description,
      long_description=open('README.md', encoding='utf-8').read(),
      author='Jiang Jinyang',
      author_email='hari.jiang@outlook.com',
      cmdclass={'test': TestCommand},
      platforms=['unix', 'linux', 'osx'],
      packages=find_packages(),
      install_requires=[
          'sqlalchemy'
      ],
      entry_points={
          'console_scripts': [
          ],
      },
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries',
      ],
      )
