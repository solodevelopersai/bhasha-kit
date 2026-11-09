import pytest

from bhasha_kit import analyze_sentiment


@pytest.mark.parametrize(
    ("text", "lang"),
    [
        ("यह फिल्म बहुत अच्छी है", "hi"),
        ("খুব ভালো", "bn"),
        ("This movie is great", "en"),
    ],
)
def test_positive_sentiment_in_each_language(text, lang):
    assert analyze_sentiment(text) == {
        "label": "positive", "score": 1.0, "lang": lang,
    }


@pytest.mark.parametrize(
    ("text", "lang"),
    [
        ("यह फिल्म खराब है", "hi"),
        ("সিনেমাটি খারাপ", "bn"),
        ("This movie is terrible", "en"),
    ],
)
def test_negative_sentiment_in_each_language(text, lang):
    result = analyze_sentiment(text)
    assert result["label"] == "negative"
    assert result["score"] == -1.0
    assert result["lang"] == lang


@pytest.mark.parametrize(
    ("text", "lang"),
    [
        ("यह फिल्म अच्छी नहीं है", "hi"),
        ("সিনেমাটি ভালো না", "bn"),
        ("this is not good", "en"),
    ],
)
def test_negation_flips_sentiment_in_each_language(text, lang):
    result = analyze_sentiment(text)
    assert result == {"label": "negative", "score": -1.0, "lang": lang}


def test_neutral_empty_and_mixed_language_sentiment():
    assert analyze_sentiment("यह एक फिल्म है") == {
        "label": "neutral", "score": 0.0, "lang": "hi",
    }
    assert analyze_sentiment("") == {
        "label": "neutral", "score": 0.0, "lang": "unknown",
    }
    assert analyze_sentiment("good खराब", lang="en") == {
        "label": "positive", "score": 1.0, "lang": "en",
    }


def test_explicit_language_and_input_errors():
    with pytest.raises(ValueError):
        analyze_sentiment("good", lang="fr")
    with pytest.raises(TypeError):
        analyze_sentiment(None)
