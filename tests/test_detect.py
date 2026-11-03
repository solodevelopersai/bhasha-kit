import pytest

from bhasha_kit import detect_language, detect_languages


def test_detect_language_for_each_script_and_empty_text():
    assert detect_language("नमस्ते") == "hi"
    assert detect_language("বাংলা") == "bn"
    assert detect_language("English") == "en"
    assert detect_language("123 😀") == "unknown"
    assert detect_language("") == "unknown"


def test_detect_languages_returns_shares_for_mixed_text():
    assert detect_languages("नম") == {"hi": 0.5, "bn": 0.5}
    assert detect_languages("नम hi") == {"hi": 0.5, "en": 0.5}
    assert detect_languages("বাংলা English") == {
        "bn": 5 / 12,
        "en": 7 / 12,
    }


def test_detection_counts_indic_marks_and_ignores_uncountable_text():
    assert detect_languages("क्") == {"hi": 1.0}
    assert detect_languages("! 123 😀") == {}


@pytest.mark.parametrize("function", [detect_language, detect_languages])
def test_detection_rejects_non_string(function):
    with pytest.raises(TypeError):
        function(None)
