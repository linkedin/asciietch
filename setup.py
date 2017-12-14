# Copyright 2017 LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.

import io

from setuptools import setup, find_packages


description = 'A library for graphing charts using ascii characters.'
try:
    with io.open('README.md', encoding="utf-8") as fh:
            long_description = fh.read()
except IOError:
    long_description = description

setup(
    name='asciietch',
    version='1.0.1',
    description=description,
    long_description=description,
    url='https://github.com/linkedin/asciietch',
    author='Steven R. Callister',
    author_email='scallist@linkedin.com',
    license='License :: OSI Approved :: BSD License',
    packages=find_packages(),
    install_requires=[
        'parsedatetime==2.4'
    ],
    tests_require=[
        'flake8>=3.5.0',
        'mock>=2.0.0',
        'pytest>=3.0.6'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: POSIX :: Linux'
    ]
)
