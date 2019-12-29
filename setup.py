# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup

setup(name='MySQLslow',
      version='0.1',
      description='Analyze MySQL slow queries',
      url='https://github.com/mohtork/mysql-slow-query',
      author='Torkey',
      author_email='',
      setup_requires='setuptools',
      package_dir={'': 'mysqlslow'},
      packages=find_packages(where='mysqlslow'),
      license='Apache 2.0',
      zip_safe=False)
