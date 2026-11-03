from decimal import Decimal

import pytest

from bhasha_kit import number_to_rupees, number_to_words
from bhasha_kit.numbers import _BN, _HI


def test_number_to_words_examples_and_language_outputs():
    assert number_to_words(1250, "hi") == "एक हज़ार दो सौ पचास"
    assert number_to_words(1250, "en") == "one thousand two hundred fifty"
    assert number_to_words(1250, "bn") == "এক হাজার দুই শত পঞ্চাশ"
    assert number_to_words(0, "hi") == "शून्य"
    assert number_to_words(-1, "bn") == "ঋণ এক"


def test_hindi_and_bengali_tables_cover_unique_entries_from_zero_to_ninety_nine():
    assert len(_HI) == len(set(_HI)) == 100
    assert len(_BN) == len(set(_BN)) == 100
    assert _HI[91:] == (
        "इक्यानवे", "बानवे", "तिरानवे", "चौरानवे", "पचानवे",
        "छियानवे", "सत्तानवे", "अट्ठानवे", "निन्यानवे",
    )
    assert all("\ufffd" not in word for word in _BN)
    for value in range(100):
        assert number_to_words(value, "hi") == _HI[value]
        assert number_to_words(value, "bn") == _BN[value]


def test_number_to_words_indian_boundaries():
    assert number_to_words(99_999_999) == "नौ करोड़ निन्यानवे लाख निन्यानवे हज़ार नौ सौ निन्यानवे"
    assert number_to_words(999_999_999, "en") == (
        "ninety nine crore ninety nine lakh ninety nine thousand "
        "nine hundred ninety nine"
    )
    assert number_to_words(-999_999_999, "hi").startswith("ऋण ")


@pytest.mark.parametrize("value", [1.5, "1", True, None])
def test_number_to_words_rejects_non_integer_values(value):
    with pytest.raises(TypeError):
        number_to_words(value)


def test_number_to_words_rejects_invalid_language_and_out_of_range_value():
    with pytest.raises(ValueError):
        number_to_words(1, "fr")
    with pytest.raises(ValueError):
        number_to_words(1_000_000_000)


def test_number_to_rupees_decimal_rounding_and_languages():
    assert number_to_rupees(Decimal("1250.50")) == (
        "एक हज़ार दो सौ पचास रुपये पचास पैसे"
    )
    assert number_to_rupees("12.345", "en") == "twelve rupees thirty five paise"
    assert number_to_rupees("12.344", "bn") == "বারো টাকা চৌত্রিশ পয়সা"
    assert number_to_rupees(0) == "शून्य रुपये"


def test_number_to_rupees_negative_and_rounding_across_zero():
    assert number_to_rupees("-0.01") == "ऋण शून्य रुपये एक पैसा"
    assert number_to_rupees("-1.50", "en") == "minus one rupee fifty paise"
    assert number_to_rupees("0.005") == "शून्य रुपये एक पैसा"
    assert number_to_rupees("-0.004") == "शून्य रुपये"


@pytest.mark.parametrize("value", [float("inf"), float("nan"), Decimal("Infinity"), "NaN"])
def test_number_to_rupees_rejects_non_finite_values(value):
    with pytest.raises(ValueError):
        number_to_rupees(value)


def test_number_to_rupees_rejects_invalid_input_and_currency_range():
    with pytest.raises(TypeError):
        number_to_rupees(True)
    with pytest.raises(ValueError):
        number_to_rupees("not money")
    with pytest.raises(ValueError):
        number_to_rupees("1000000000")
    with pytest.raises(ValueError):
        number_to_rupees("1", "fr")
