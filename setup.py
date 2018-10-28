# -*- coding: utf-8 -*-

"""A setuptools-based setup module.

See:
https://github.com/renweizhukov/txt2mobi3
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='txt2mobi3',
    version='0.2.5',
    description='Convert Chinese novel txt files into Kindle mobi files.',
    long_description=long_description,
    url='https://github.com/renweizhukov/txt2mobi3',
    author='Wei Ren',
    author_email='renwei2004@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Text Processing :: General',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        ],
    keywords='txt mobi python3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'chardet',
        'setuptools',
        ],
    # This project depends on a built-in module `secrets` only available
    # in Python 3.6 and later,
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'txt2mobi3_clt=txt2mobi3.txt2mobi3_clt:txt2mobi3_clt'
        ],
        },
    project_urls={
        'Bug Reports': 'https://github.com/renweizhukov/txt2mobi3/issues',
        'Documentation': 'https://github.com/renweizhukov/txt2mobi3',
        'Source': 'https://github.com/renweizhukov/txt2mobi3',
        },
    )