import tempfile

import pytest

from sentence_splitter import (
    SentenceSplitter,
    split_text_into_sentences,
    SentenceSplitterWarning,
    SentenceSplitterException
)


def test_invalid_language_code():
    """Invalid language code."""
    with pytest.raises(SentenceSplitterException):
        SentenceSplitter(language='/etc/passwd')


def test_unsupported_language():
    """Unsupported language (and no prefix file provided)."""
    with pytest.raises(SentenceSplitterException):
        SentenceSplitter(language='xx')


def test_text_none():
    """Text is None."""
    with pytest.warns(SentenceSplitterWarning):
        splitter = SentenceSplitter(language='en')
        # noinspection PyTypeChecker
        sentences = splitter.split(text=None)
        assert sentences == []


def test_text_empty():
    """Text is empty."""
    splitter = SentenceSplitter(language='en')
    assert splitter.split(text='') == []


def test_en():
    splitter = SentenceSplitter(language='en')

    input_text = 'This is a paragraph. It contains several sentences. "But why," you ask?'
    expected_sentences = ['This is a paragraph.', 'It contains several sentences.', '"But why," you ask?']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences

    input_text = 'Hey! Now.'
    expected_sentences = ['Hey!', 'Now.']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences

    input_text = 'Hey... Now.'
    expected_sentences = ['Hey...', 'Now.']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences

    input_text = 'Hey. Now.'
    expected_sentences = ['Hey.', 'Now.']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences

    input_text = 'Hey.  Now.'
    expected_sentences = ['Hey.', 'Now.']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_en_numeric_only():
    splitter = SentenceSplitter(language='en')

    input_text = 'Hello. No. 1. No. 2. Prefix. 1. Prefix. 2. Good bye.'
    expected_sentences = ['Hello.', 'No. 1.', 'No. 2.', 'Prefix.', '1.', 'Prefix.', '2.', 'Good bye.']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_en_uppercase_acronym():
    splitter = SentenceSplitter(language='en')

    input_text = 'Hello. .NATO. Good bye.'
    expected_sentences = ['Hello. .NATO. Good bye.']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_en_sentence_within_brackets():
    splitter = SentenceSplitter(language='en')

    input_text = 'Foo bar. (Baz foo.) Bar baz.'
    expected_sentences = ['Foo bar.', '(Baz foo.)', 'Bar baz.']
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_de():
    splitter = SentenceSplitter(language='de')

    input_text = 'Nie hätte das passieren sollen. Dr. Soltan sagte: "Der Fluxcompensator war doch kalibriert!".'
    expected_sentences = [
        'Nie hätte das passieren sollen.',
        'Dr. Soltan sagte: "Der Fluxcompensator war doch kalibriert!".',
    ]
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_fr():
    splitter = SentenceSplitter(language='fr')

    input_text = 'Brookfield Office Properties Inc. (« BOPI »), dont les actifs liés aux immeubles directement...'
    expected_sentences = [
        input_text,
    ]
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_el():
    splitter = SentenceSplitter(language='el')

    input_text = (
        'Όλα τα συστήματα ανώτατης εκπαίδευσης σχεδιάζονται σε εθνικό επίπεδο. Η ΕΕ αναλαμβάνει κυρίως να συμβάλει '
        'στη βελτίωση της συγκρισιμότητας μεταξύ των διάφορων συστημάτων και να βοηθά φοιτητές και καθηγητές να '
        'μετακινούνται με ευκολία μεταξύ των συστημάτων των κρατών μελών.'
    )
    expected_sentences = [
        'Όλα τα συστήματα ανώτατης εκπαίδευσης σχεδιάζονται σε εθνικό επίπεδο.',
        (
            'Η ΕΕ αναλαμβάνει κυρίως να συμβάλει στη βελτίωση της συγκρισιμότητας μεταξύ των διάφορων συστημάτων '
            'και να βοηθά φοιτητές και καθηγητές να μετακινούνται με ευκολία μεταξύ των συστημάτων των κρατών '
            'μελών.'
        ),
    ]
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_pt():
    splitter = SentenceSplitter(language='pt')

    input_text = 'Isto é um parágrafo. Contém várias frases. «Mas porquê,» perguntas tu?'
    expected_sentences = [
        "Isto é um parágrafo.",
        "Contém várias frases.",
        "«Mas porquê,» perguntas tu?",
    ]
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_es():
    splitter = SentenceSplitter(language='es')

    input_text = (
        'La UE ofrece una gran variedad de empleos en un entorno multinacional y multilingüe. La Oficina Europea de '
        'Selección de Personal (EPSO) se ocupa de la contratación, sobre todo mediante oposiciones generales.'
    )
    expected_sentences = [
        'La UE ofrece una gran variedad de empleos en un entorno multinacional y multilingüe.',
        (
            'La Oficina Europea de Selección de Personal (EPSO) se ocupa de la contratación, sobre todo mediante '
            'oposiciones generales.'
        ),
    ]
    actual_sentences = splitter.split(text=input_text)
    assert expected_sentences == actual_sentences


def test_custom_non_breaking_prefixes():
    with tempfile.NamedTemporaryFile(mode='w+') as f:
        f.write((
            "# \n"
            "# Temporary prefix file\n"
            "# \n"
            "\n"
            "Prefix1\n"
            "Prefix2\n"
        ))
        f.flush()

        splitter = SentenceSplitter(language='xx', non_breaking_prefix_file=f.name)
        input_text = "Hello. Prefix1. Prefix2. Hello again. Good bye."
        expected_sentences = [
            'Hello.',
            'Prefix1. Prefix2. Hello again.',
            'Good bye.',
        ]
        actual_sentences = splitter.split(text=input_text)
        assert expected_sentences == actual_sentences


def test_split_text_into_sentences():
    input_text = 'This is a paragraph. It contains several sentences. "But why," you ask?'
    expected_sentences = ['This is a paragraph.', 'It contains several sentences.', '"But why," you ask?']
    actual_sentences = split_text_into_sentences(text=input_text, language='en')
    assert expected_sentences == actual_sentences
