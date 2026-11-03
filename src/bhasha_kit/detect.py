"""Lightweight Unicode-script language detection."""

from __future__ import annotations

import unicodedata


def detect_languages(text: str) -> dict[str, float]:
    """Return the share of countable Hindi, Bengali, and Latin letters.

    Example: ``detect_languages("नम hi")`` returns ``{"hi": 0.5, "en": 0.5}``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    counts = {"hi": 0, "bn": 0, "en": 0}
    for char in text:
        category = unicodedata.category(char)
        if not category.startswith(("L", "M")):
            continue
        codepoint = ord(char)
        if 0x0900 <= codepoint <= 0x097F:
            counts["hi"] += 1
        elif 0x0980 <= codepoint <= 0x09FF:
            counts["bn"] += 1
        elif category.startswith("L") and "LATIN" in unicodedata.name(char, ""):
            counts["en"] += 1

    total = sum(counts.values())
    if not total:
        return {}
    return {language: count / total for language, count in counts.items() if count}


def detect_language(text: str) -> str:
    """Return the dominant language code, or ``"unknown"`` if no letters exist.

    Example: ``detect_language("বাংলা text")`` returns ``"bn"``.
    """
    shares = detect_languages(text)
    if not shares:
        return "unknown"
    return max(shares, key=shares.get)


__all__ = ["detect_language", "detect_languages"]
