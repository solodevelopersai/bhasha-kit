"""Offline lexicon-based sentiment analysis."""

from __future__ import annotations

from .detect import detect_language
from .lexicons import NEGATIONS, NEGATIVE_WORDS, POSITIVE_WORDS
from .tokenize import tokenize

_SUPPORTED_LANGUAGES = frozenset(POSITIVE_WORDS)


def analyze_sentiment(text: str, lang: str | None = None) -> dict[str, object]:
    """Analyze sentiment using a small language-specific word lexicon."""
    words = tokenize(text)
    if lang is None:
        lang = detect_language(text)
        if lang == "unknown":
            return {"label": "neutral", "score": 0.0, "lang": lang}
    elif not isinstance(lang, str) or lang not in _SUPPORTED_LANGUAGES:
        raise ValueError("lang must be 'hi', 'bn', or 'en'")

    positive = POSITIVE_WORDS[lang]
    negative = NEGATIVE_WORDS[lang]
    negations = NEGATIONS[lang]
    positive_count = 0
    negative_count = 0

    for index, word in enumerate(words):
        if word not in positive and word not in negative:
            continue
        is_negated = (
            (index > 0 and words[index - 1] in negations)
            or (index + 1 < len(words) and words[index + 1] in negations)
        )
        is_positive = word in positive
        if is_negated:
            is_positive = not is_positive
        if is_positive:
            positive_count += 1
        else:
            negative_count += 1

    sentiment_count = positive_count + negative_count
    score = (positive_count - negative_count) / max(1, sentiment_count)
    if not sentiment_count or -0.1 <= score <= 0.1:
        label = "neutral"
    elif score > 0:
        label = "positive"
    else:
        label = "negative"
    return {"label": label, "score": score, "lang": lang}


__all__ = ["analyze_sentiment"]
