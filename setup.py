# Copyright 2017 LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.

import io
import venv
import sys

from pathlib import Path

from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

if sys.version_info < (3, 6):
    print('asciietch requires at least Python 3.6!')
    sys.exit(1)


description = 'A library for graphing charts using ascii characters.'
try:
    with io.open('README.md', encoding="utf-8") as fh:
            long_description = fh.read()
except IOError:
    long_description = description


class Tox(TestCommand):
    def run_tests(self):
        import tox

        errno = -1
        try:
            tox.session.main()
        except SystemExit as e:
            errno = e.code
        sys.exit(errno)


class PyTest(TestCommand):
    def run_tests(self):
        import pytest

        errno = pytest.main()
        sys.exit(errno)


class Venv(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        venv_path = Path(__file__).absolute().parent / 'venv' / 'asciietch'
        print(f'Creating virtual environment in {venv_path}')
        venv.main(args=[str(venv_path)])
        print(
            'Linking `activate` to top level of project.\n'
            'To activate, simply run `source activate`.'
        )
        activate = Path(venv_path, 'bin', 'activate')
        activate_link = Path(__file__).absolute().parent / 'activate'
        try:
            activate_link.symlink_to(activate)
        except FileExistsError:
            ...


setup(
    name='asciietch',
    version='1.0.4',
    description=description,
    long_description=description,
    url='https://github.com/linkedin/asciietch',
    author='Steven R. Callister',
    author_email='scallist@linkedin.com',
    cmdclass={'venv': Venv,
              'test': PyTest,
              'pytest': PyTest,
              'tox': Tox,
              },
    license='License :: OSI Approved :: BSD License',
    packages=find_packages(),
    install_requires=[
        'parsedatetime==2.4',
        'setuptools>=30',
    ],
    tests_require=[
        'flake8>=3.5.0',
        'pytest>=3.0.6',
        'tox',
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
    ],
)
