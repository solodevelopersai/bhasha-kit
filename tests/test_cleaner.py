import pytest

from bhasha_kit import clean_text, normalize_digits


def test_clean_text_removes_emoji_and_collapses_whitespace():
    assert clean_text("नमस्ते   😀 दोस्तों") == "नमस्ते दोस्तों"


def test_clean_text_options_and_unicode_normalization():
    assert clean_text("  CAFE\u0301  ", remove_emoji=False, lowercase=True) == "café"
    assert clean_text("देखें https://example.com अब", remove_urls=True) == "देखें अब"
    assert clean_text("a\u200bb") == "ab"


def test_clean_text_preserves_indic_joiners_and_non_emoji_when_disabled():
    assert clean_text("क्\u200dष") == "क्\u200dष"
    assert clean_text("A😀B", remove_emoji=False) == "A😀B"
    assert clean_text("❤\ufe0f 1\ufe0f\u20e3 done") == "done"


def test_clean_text_empty_and_invalid_inputs():
    assert clean_text("") == ""
    with pytest.raises(TypeError):
        clean_text(None)
    with pytest.raises(TypeError):
        clean_text("text", lowercase="yes")


def test_normalize_digits_between_all_supported_scripts():
    assert normalize_digits("०१२৩৪৫৬৭৮৯") == "0123456789"
    assert normalize_digits("0123456789", to="devanagari") == "०१२३४५६७८९"
    assert normalize_digits("१२3০", to="bengali") == "১২৩০"
    assert normalize_digits("", to="bengali") == ""


def test_normalize_digits_rejects_invalid_target_and_input():
    with pytest.raises(ValueError):
        normalize_digits("1", to="arabic")
    with pytest.raises(TypeError):
        normalize_digits(123)
