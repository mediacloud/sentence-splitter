Text to Sentence Splitter
=========================

.. image:: https://travis-ci.org/pypt/mediacloud-sentence-splitter.svg?branch=develop
    :target: https://travis-ci.org/pypt/mediacloud-sentence-splitter

.. image:: https://coveralls.io/repos/github/pypt/mediacloud-sentence-splitter/badge.svg?branch=develop
    :target: https://coveralls.io/github/pypt/mediacloud-sentence-splitter?branch=develop

Text to sentence splitter using heuristic algorithm by Philipp Koehn and Josh Schroeder.

This module allows splitting of text paragraphs into sentences. It is based on scripts developed by Philipp Koehn and
Josh Schroeder for processing the `Europarl corpus <http://www.statmt.org/europarl/>`_.

The module is a port of `Lingua::Sentence Perl module <http://search.cpan.org/perldoc?Lingua::Sentence>`_ with some
extra additions (improved non-breaking prefix lists for some languages and added support for Danish, Finnish,
Lithuanian, Norwegian (Bokmål), Romanian, and Turkish).


Usage
-----

The module uses punctuation and capitalization clues to split plain text into a list of sentences:

.. code-block:: python

    from sentence_splitter import SentenceSplitter, split_text_into_sentences

    #
    # Object interface
    #
    splitter = SentenceSplitter(language='en')
    print(splitter.split(text='This is a paragraph. It contains several sentences. "But why," you ask?'))
    # ['This is a paragraph.', 'It contains several sentences.', '"But why," you ask?']

    #
    # Functional interface
    #
    print(split_text_into_sentences(
        text='This is a paragraph. It contains several sentences. "But why," you ask?',
        language='en'
    ))
    # ['This is a paragraph.', 'It contains several sentences.', '"But why," you ask?']

You can provide your own non-breaking prefix file to add support for new Latin languages or improve sentence
tokenization of the currently supported ones:

.. code-block:: python

    from sentence_splitter import SentenceSplitter, split_text_into_sentences

    # Object interface
    splitter = SentenceSplitter(language='en', non_breaking_prefix_file='custom_english_non_breaking_prefixes.txt')
    print(splitter.split(text='This is a paragraph. It contains several sentences. "But why," you ask?'))

    # Functional interface
    print(split_text_into_sentences(
        text='This is a paragraph. It contains several sentences. "But why," you ask?',
        language='en',
        non_breaking_prefix_file='custom_english_non_breaking_prefixes.txt'
    ))


Languages
---------

Currently supported languages are:

- Catalan (``ca``)
- Czech (``cs``)
- Danish (``da``)
- Dutch (``nl``)
- English (``en``)
- Finnish (``fi``)
- French (``fr``)
- German (``de``)
- Greek (``el``)
- Hungarian (``hu``)
- Icelandic (``is``)
- Italian (``it``)
- Latvian (``lv``)
- Lithuanian (``lt``)
- Norwegian (Bokmål) (``no``)
- Polish (``pl``)
- Portuguese (``pt``)
- Romanian (``ro``)
- Russian (``ru``)
- Slovak (``sk``)
- Slovene (``sl``)
- Spanish (``es``)
- Swedish (``sv``)
- Turkish (``tr``)


License
-------

Copyright (C) 2010 by Digital Silk Road, 2017 Linas Valiukas.

Portions Copyright (C) 2005 by Philip Koehn and Josh Schroeder (used with permission).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along with this program. If not, see
<http://www.gnu.org/licenses/>.