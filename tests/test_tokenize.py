import pytest

from bhasha_kit import tokenize


def test_tokenize_splits_punctuation_and_lowercases_latin():
    assert tokenize("Hello, WORLD! Good-day.") == [
        "hello", "world", "good", "day",
    ]


def test_tokenize_preserves_devanagari_and_bengali_marks():
    assert tokenize("नमस्ते। বাংলা—ভাষা") == ["नमस्ते", "বাংলা", "ভাষা"]
    assert tokenize("क्‍ष") == ["क्‍ष"]


def test_tokenize_handles_empty_and_mixed_text():
    assert tokenize("") == []
    assert tokenize("Hi नमस्ते বাংলা 123!") == ["hi", "नमस्ते", "বাংলা", "123"]


def test_tokenize_rejects_non_string():
    with pytest.raises(TypeError):
        tokenize(None)
