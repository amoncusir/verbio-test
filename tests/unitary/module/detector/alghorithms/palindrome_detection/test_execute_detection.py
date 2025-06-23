import random

import pytest

from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithm
from src.module.detector.domain.value_objects import Language

SIMPLE_PALINDROME = (
    ("asdffdsa", Language.from_part_one('na'), 1),
    ("abcdefgh", Language.from_part_one('na'), 0),
    # Spanish (es)
    ("aníta laval atína", Language.from_part_one('es'), 1),
    ("állí veselasovev íllá", Language.from_part_one('es'), 0),
    ("reconocer", Language.from_part_one('es'), 1),
    ("lenguaje", Language.from_part_one('es'), 0),
    # English (en)
    ("madam", Language.from_part_one('en'), 1),
    ("racecar", Language.from_part_one('en'), 1),
    ("rotator", Language.from_part_one('en'), 1),
    ("world", Language.from_part_one('en'), 0),
    # French (fr)
    ("ressasser", Language.from_part_one('fr'), 1),
    ("été", Language.from_part_one('fr'), 1),
    ("kayak", Language.from_part_one('fr'), 1),
    ("bonjour", Language.from_part_one('fr'), 0),
    # Italian (it)
    ("aiuola", Language.from_part_one('it'), 0),
    ("osse", Language.from_part_one('it'), 0),
    ("anna", Language.from_part_one('it'), 1),
    ("amore", Language.from_part_one('it'), 0),
    # German (de)
    ("reliefpfeiler", Language.from_part_one('de'), 1),
    ("lagerregal", Language.from_part_one('de'), 1),
    ("tretet", Language.from_part_one('de'), 0),
    ("schreiben", Language.from_part_one('de'), 0),
    # Portuguese (pt)
    ("arara", Language.from_part_one('pt'), 1),
    ("radar", Language.from_part_one('pt'), 1),
    ("reviver", Language.from_part_one('pt'), 1),
    ("português", Language.from_part_one('pt'), 0),
)


@pytest.mark.asyncio
@pytest.mark.parametrize("text, lang, match_len", SIMPLE_PALINDROME)
async def test_execute_detection_without_ignore(
    algorithm: TextDetectionAlgorithm,
    text,
    lang,
    match_len,
):
    result = await algorithm.execute_detection(
        text,
        lang,
        ignore_case=False,
        ignore_spaces=False,
        ignore_punctuation=False,
        ignore_orthographic_symbols=False,
    )

    assert len(result) == match_len


@pytest.mark.asyncio
@pytest.mark.parametrize("text, lang, match_len", SIMPLE_PALINDROME)
async def test_execute_detection_ignore_case(
    algorithm: TextDetectionAlgorithm,
    text,
    lang,
    match_len,
):
    def randomize_case(i) -> str:
        return ''.join(char.upper() if random.choice([True, False]) else char.lower() for char in i)

    result = await algorithm.execute_detection(
        randomize_case(text),
        lang,
        ignore_case=True,
        ignore_spaces=False,
        ignore_punctuation=False,
        ignore_orthographic_symbols=False,
    )

    assert len(result) == match_len


@pytest.mark.asyncio
@pytest.mark.parametrize("text, lang, match_len", SIMPLE_PALINDROME)
async def test_execute_detection_ignore_spaces(
    algorithm: TextDetectionAlgorithm,
    text,
    lang,
    match_len,
):
    def add_random_spaces(i) -> str:
        return ''.join(f" {char} " if random.choice([True, False]) else char for char in i)

    result = await algorithm.execute_detection(
        add_random_spaces(text),
        lang,
        ignore_case=False,
        ignore_spaces=True,
        ignore_punctuation=False,
        ignore_orthographic_symbols=False,
    )

    assert len(result) == match_len


@pytest.mark.asyncio
@pytest.mark.parametrize("text, lang, match_len", SIMPLE_PALINDROME)
async def test_execute_detection_ignore_punctuation(
    algorithm: TextDetectionAlgorithm,
    text,
    lang,
    match_len,
):
    def add_random_symbols(t: str) -> str:
        chars = ".,:;!¡¿?-_'"
        combined = []
        max_len = max(len(t), len(chars))
        for i in range(max_len):
            if i < len(t):
                combined.append(t[i])
            if i < len(chars):
                combined.append(chars[i])
        return ''.join(combined)

    result = await algorithm.execute_detection(
        add_random_symbols(text),
        lang,
        ignore_case=False,
        ignore_spaces=False,
        ignore_punctuation=True,
        ignore_orthographic_symbols=False,
    )

    assert len(result) == match_len


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, lang, match_len",
    (
        ("asdffdsa", Language.from_part_one('na'), 1),
        ("abcdefgh", Language.from_part_one('na'), 0),
        # Spanish (es)
        ("aníta laval atina", Language.from_part_one('es'), 1),
        ("allí vesel lesev illá", Language.from_part_one('es'), 1),
        ("reconocér", Language.from_part_one('es'), 1),
        ("lenguaje", Language.from_part_one('es'), 0),
        # English (en)
        ("madam", Language.from_part_one('en'), 1),
        ("racecar", Language.from_part_one('en'), 1),
        ("rotator", Language.from_part_one('en'), 1),
        ("world", Language.from_part_one('en'), 0),
        # French (fr)
        ("ressasser", Language.from_part_one('fr'), 1),
        ("éte", Language.from_part_one('fr'), 1),
        ("kayak", Language.from_part_one('fr'), 1),
        ("bonjoür", Language.from_part_one('fr'), 0),
        # Italian (it)
        ("aiuola", Language.from_part_one('it'), 0),
        ("osse", Language.from_part_one('it'), 0),
        ("änna", Language.from_part_one('it'), 1),
        ("amore", Language.from_part_one('it'), 0),
        # German (de)
        ("reliefpfeiler", Language.from_part_one('de'), 1),
        ("lägerregal", Language.from_part_one('de'), 1),
        ("tretet", Language.from_part_one('de'), 0),
        ("schreiben", Language.from_part_one('de'), 0),
        # Portuguese (pt)
        ("arara", Language.from_part_one('pt'), 1),
        ("radar", Language.from_part_one('pt'), 1),
        ("revivêr", Language.from_part_one('pt'), 1),
        ("português", Language.from_part_one('pt'), 0),
    ),
)
async def test_execute_detection_ignore_orthographic_symbols(
    algorithm: TextDetectionAlgorithm,
    text,
    lang,
    match_len,
):
    result = await algorithm.execute_detection(
        text,
        lang,
        ignore_case=False,
        ignore_spaces=False,
        ignore_punctuation=False,
        ignore_orthographic_symbols=True,
    )

    assert len(result) == match_len
