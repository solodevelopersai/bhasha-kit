"""Frequency-based keyword extraction."""

from __future__ import annotations

from .detect import detect_language
from .lexicons import STOPWORDS
from .tokenize import tokenize

_SUPPORTED_LANGUAGES = frozenset(STOPWORDS)


def extract_keywords(
    text: str, top_n: int = 5, lang: str | None = None
) -> list[tuple[str, int]]:
    """Return frequent non-stopword tokens, preserving order for ties."""
    if not isinstance(top_n, int) or isinstance(top_n, bool):
        raise TypeError("top_n must be an integer")
    if top_n < 1:
        raise ValueError("top_n must be at least 1")
    if lang is None:
        lang = detect_language(text)
        if lang == "unknown":
            return []
    elif not isinstance(lang, str) or lang not in _SUPPORTED_LANGUAGES:
        raise ValueError("lang must be 'hi', 'bn', or 'en'")

    frequencies = {}
    stopwords = STOPWORDS[lang]
    for word in tokenize(text):
        if word in stopwords or word.isnumeric() or len(word) == 1:
            continue
        frequencies[word] = frequencies.get(word, 0) + 1

    return sorted(frequencies.items(), key=lambda item: -item[1])[:top_n]


__all__ = ["extract_keywords"]
