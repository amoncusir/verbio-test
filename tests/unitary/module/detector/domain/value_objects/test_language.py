import pytest

from src.module.detector.domain.value_objects import Language


def test_valid_language_initialization():
    lang = Language("en")

    assert lang.part_one == "en"
    assert str(lang) == "en"


@pytest.mark.parametrize(
    "code",
    (
        "eng",
        "e",
        "",
    ),
)
def test_invalid_language_initialization_raises(code):
    with pytest.raises(ValueError):
        Language(code)


def test_language_equality():
    lang1 = Language("es")
    lang2 = Language("es")
    lang3 = Language("fr")

    assert lang1 == lang2
    assert lang1 != lang3
    assert not (lang1 == "es")  # Should return NotImplemented → evaluated to False


def test_language_from_part_one():
    lang = Language.from_part_one("de")

    assert isinstance(lang, Language)
    assert lang.part_one == "de"
