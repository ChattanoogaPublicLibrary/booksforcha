#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='booksforcha',
    version='0.1.0',
    description="Twitter bot for Chattanooga Public Library.",
    long_description=readme + '\n\n' + history,
    author="Sean Brewer",
    author_email='sbrewer@lib.chattanooga.gov',
    url='https://github.com/ChattanoogaPublicLibrary/booksforcha',
    packages=[
        'booksforcha',
    ],
    package_dir={'booksforcha':
                 'booksforcha'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='booksforcha',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
