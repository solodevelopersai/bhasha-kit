import pytest

from bhasha_kit import to_bengali, to_devanagari, to_roman, to_roman_bengali


def test_required_roman_to_indic_examples():
    assert to_devanagari("namaste") == "नमस्ते"
    assert to_devanagari("bhaarat") == "भारत"
    assert to_devanagari("mera naam raaj hai") == "मेरा नाम राज है"
    assert to_bengali("aamaar naam rahim") == "আমার নাম রহিম"


def test_required_indic_to_roman_examples():
    assert to_roman("नमस्ते") == "namaste"
    assert to_roman_bengali("আমার") == "aamaar"


def test_transliteration_preserves_boundaries_and_supports_independent_vowels():
    assert to_devanagari("a aa, namaste!") == "अ आ, नमस्ते!"
    assert to_bengali("a aamaar.") == "অ আমার."
    assert to_devanagari("नमस्ते") == "नमस्ते"
    assert to_roman("नमस्ते, भारत!") == "namaste, bhaarat!"
    assert to_roman("कि क") == "ki k"
    assert to_roman_bengali("কি ক") == "ki k"


def test_transliteration_empty_strings_and_invalid_inputs():
    for function in (to_devanagari, to_roman, to_bengali, to_roman_bengali):
        assert function("") == ""
        with pytest.raises(TypeError):
            function(None)
