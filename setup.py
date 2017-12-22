#!/usr/bin/env python
import os
from setuptools import setup
from sentence_splitter.__about__ import __version__

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, 'requirements.txt')

with open(REQUIREMENTS_FILE) as requirements:
    install_requirements = requirements.read().splitlines()

setup(
    name='sentence_splitter',
    version=__version__,
    description='Text to sentence splitter using heuristic algorithm by Philipp Koehn and Josh Schroeder',
    long_description="""
Text to sentence splitter using heuristic algorithm by Philipp Koehn and Josh Schroeder.

This module allows splitting of text paragraphs into sentences. It is based on scripts developed by Philipp
Koehn and Josh Schroeder for processing the `Europarl corpus <http://www.statmt.org/europarl/>`_.

The module is a port of `Lingua::Sentence Perl module <http://search.cpan.org/perldoc?Lingua::Sentence>`_ with
some extra additions (improved non-breaking prefix lists for some languages and added support for Danish,
Finnish, Lithuanian, Norwegian (Bokmål), Romanian, and Turkish).
    """,
    author='Philip Koehn, Josh Schroeder, Digital Silk Road, Linas Valiukas',
    author_email='lvaliukas@cyber.law.harvard.edu',
    url='https://github.com/berkmancenter/mediacloud-sentence-splitter',
    keywords="sentence splitter tokenization tokenizer tokenize",
    license="LGPLv3",
    install_requires=install_requirements,
    packages=['sentence_splitter'],
    package_dir={'sentence_splitter': 'sentence_splitter'},
    package_data={'sentence_splitter': [
        'non_breaking_prefixes/*.txt',
    ]},
    include_package_data=True,
    platforms='any',
    python_requires=">=3.5",
    test_suite='pytest-runner',
    tests_require=['pytest', 'pytest-runner'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Natural Language :: Catalan',
        'Natural Language :: Czech',
        'Natural Language :: Danish',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: Finnish',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Greek',
        'Natural Language :: Hungarian',
        'Natural Language :: Icelandic',
        'Natural Language :: Italian',
        'Natural Language :: Latvian',
        # No 'Natural Language :: Lithuanian' available
        'Natural Language :: Norwegian',
        'Natural Language :: Polish',
        'Natural Language :: Portuguese',
        'Natural Language :: Portuguese (Brazilian)',
        'Natural Language :: Romanian',
        'Natural Language :: Russian',
        'Natural Language :: Slovak',
        'Natural Language :: Slovenian',
        'Natural Language :: Spanish',
        'Natural Language :: Swedish',
        'Natural Language :: Turkish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
    ]
)
