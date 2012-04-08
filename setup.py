#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import virtbox
from distutils.core import setup

# publish package
#if sys.argv[-1] == 'publish':
#    os.system('python setup.py sdist upload')
#    sys.exit()
#
## run tests
#if sys.argv[-1] == 'test':
#    os.system('python test_requests.py')
#    sys.exit()


setup(
    name='py-virtbox',
    version=virtbox.__version__,
    description='Python Package for Managing Virtualbox.',
    long_description=open('README.rst').read(),
    author='Sean Plaice',
    url='http://github.com/splaice/virtbox',
    package_data={'': ['LICENSE', 'NOTICE']},
    license=virtbox.__license__,
    #packages=find_packages()
    packages=['virtbox']
)
