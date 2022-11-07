from enum import Enum
import os
from typing import List, Tuple, Iterator
import warnings

import regex

__all__ = (
    'SentenceSplitter',
    'split_text_into_sentences',
    'SentenceSplitterException',
    'SentenceSplitterWarning'
)


class SentenceSplitterException(Exception):
    """Sentence splitter exception."""
    pass


class SentenceSplitterWarning(Warning):
    """Sentence splitter warning."""
    pass


class SentenceSplitter(object):
    """Text to sentence splitter using heuristic algorithm by Philipp Koehn and Josh Schroeder.."""

    class PrefixType(Enum):
        DEFAULT = 1
        NUMERIC_ONLY = 2

    __slots__ = [
        # Dictionary of non-breaking prefixes; keys are string prefixes, values are PrefixType enums
        '__non_breaking_prefixes',
    ]

    def __init__(self, language: str, non_breaking_prefix_file: str = None):
        """Create sentence splitter object.

        :param language: ISO 639-1 language code
        :param non_breaking_prefix_file: path to non-breaking prefix file
        """
        if not regex.match(pattern=r'^[a-z][a-z]$', string=language, flags=regex.UNICODE):
            raise SentenceSplitterException("Invalid language code: {}".format(language))

        if non_breaking_prefix_file is None:
            pwd = os.path.dirname(os.path.abspath(__file__))
            prefix_dir = os.path.join(pwd, 'non_breaking_prefixes')
            non_breaking_prefix_file = os.path.join(prefix_dir, '{}.txt'.format(language))

        if not os.path.isfile(non_breaking_prefix_file):
            raise SentenceSplitterException(
                "Non-breaking prefix file for language '{}' was not found at path '{}'".format(
                    language,
                    non_breaking_prefix_file,
                ))

        self.__non_breaking_prefixes = dict()
        with open(non_breaking_prefix_file, mode='r', encoding='utf-8') as prefix_file:
            for line in prefix_file.readlines():

                if '#NUMERIC_ONLY#' in line:
                    prefix_type = SentenceSplitter.PrefixType.NUMERIC_ONLY
                else:
                    prefix_type = SentenceSplitter.PrefixType.DEFAULT

                # Remove comments
                line = regex.sub(pattern=r'#.*', repl='', string=line, flags=regex.DOTALL | regex.UNICODE)

                line = line.strip()

                if not line:
                    continue

                self.__non_breaking_prefixes[line] = prefix_type

    def split(self, text: str, strip_whitespace: bool = True) -> List[str]:
        """Split text into sentences.

        :param text: Text to be split into individual sentences
        :param strip_whitespace: strip leading, trailing and duplicated
        whitespace from every sentence
        :return: List of string sentences
        """
        if text is None:
            warnings.warn("Text is None.", SentenceSplitterWarning)
            return []

        if not text:
            return []

        boundaries = [None, *self.boundaries(text), None]
        spans = zip(boundaries, boundaries[1:])
        sentences = [text[start:end] for start, end in spans]

        if strip_whitespace:
            sentences = [regex.sub(r'\s\s+', ' ', s.strip()) for s in sentences]

        return sentences


    def boundaries(self, text: str) -> List[int]:
        """Find sentence boundaries.

        :param text: Text to be split into individual sentences
        :return: List of int sentence-boundary offsets
        """
        boundaries = []

        for pattern in (
            # Non-period end of sentence markers (?!) followed by sentence starters
            r'([?!]) +'
            r'([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\p{Uppercase_Letter}\p{Other_Letter}])',

            # Multi-dots followed by sentence starters
            r'(\.\.+) +'
            r'([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\p{Uppercase_Letter}\p{Other_Letter}])',

            # Add breaks for sentences that end with some sort of punctuation inside a quote or parenthetical and are
            # followed by a possible sentence starter punctuation and upper case
            r'([?!\.][ ]*[\'")\]\p{Final_Punctuation}]+) +'
            r'([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[ ]*[\p{Uppercase_Letter}\p{Other_Letter}])',

            # Add breaks for sentences that end with some sort of punctuation and are followed by a sentence starter punctuation
            # and upper case
            r'([?!\.]) +'
            r'([\'"[\u00bf\u00A1\p{Initial_Punctuation}]+[ ]*[\p{Uppercase_Letter}\p{Other_Letter}])',
        ):
            for match in regex.finditer(pattern, text):
                match_range = range(match.start(), match.end())
                if any(found_boundary in match_range for found_boundary in boundaries):
                    # Skip matches that overlap with a previously found sentence boundary.
                    # In the original implementation, overlaps are prevented through inserting
                    # newline characters in the input string.
                    continue
                boundaries.append(match.start(2))  # Group #2 starts the new sentence.

        # Special punctuation cases are covered. Check all remaining periods
        for left, right, offset in self._bigram_walk(r'\S+', text):
            if offset in boundaries:
                continue

            match = regex.search(pattern=r'([\w\.\-]*)([\'\"\)\]\%\p{Final_Punctuation}]*)(\.+)$',
                                 string=left)
            if not match:
                continue

            prefix, starting_punct, _ = match.groups()

            if self.is_prefix_honorific(prefix, starting_punct):
                # Not breaking
                pass

            elif regex.search(pattern=r'(\.)[\p{Uppercase_Letter}\p{Other_Letter}\-]+(\.+)$',
                              string=left):
                # Not breaking - upper case acronym
                pass

            elif regex.search(
                    pattern=(
                        r'^([ ]*[\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[ ]*[\p{Uppercase_Letter}'
                        r'\p{Other_Letter}0-9])'
                    ),
                    string=right):

                if not self.is_numeric(prefix, starting_punct, next_word=right):
                    boundaries.append(offset)

                # We always add a return for these unless we have a numeric non-breaker and a number start

        boundaries.sort()
        return boundaries

    @staticmethod
    def _bigram_walk(pattern, text: str) -> Iterator[Tuple[str, str, int]]:
        last_word = None
        for match in regex.finditer(pattern, text):
            new_word = match.group()
            if last_word is not None:
                yield last_word, new_word, match.start()
            last_word = new_word

    def is_prefix_honorific(self, prefix: str, starting_punct: str) -> bool:
        """Check if prefix is a known honorific and starting_punct is empty."""
        return (
            bool(prefix)
            and self.__non_breaking_prefixes.get(prefix) == SentenceSplitter.PrefixType.DEFAULT
            and not starting_punct
        )

    def is_numeric(self, prefix: str, starting_punct: str, next_word: str):
        """The next word has a bunch of initial quotes, maybe a space, then either upper case or a
        number."""
        return (
            bool(prefix)
            and self.__non_breaking_prefixes.get(prefix) == SentenceSplitter.PrefixType.NUMERIC_ONLY
            and not starting_punct
            and bool(regex.match(r'[0-9]', next_word))
        )


def split_text_into_sentences(text: str, language: str, non_breaking_prefix_file: str = None) -> List[str]:
    """Split text into sentences.

    For better performance, use SentenceSplitter class directly to avoid reloading non-breaking prefix file on every
    call.

    :param text: Text to be split into individual sentences
    :param language: ISO 639-1 language code
    :param non_breaking_prefix_file: path to non-breaking prefix file
    :return: List of string sentences
    """
    splitter = SentenceSplitter(language=language, non_breaking_prefix_file=non_breaking_prefix_file)
    return splitter.split(text=text)
