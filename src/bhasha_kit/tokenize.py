"""Unicode-aware tokenization for Hindi, Bengali, and English text."""

from __future__ import annotations

import unicodedata


def _is_indic_character(char: str) -> bool:
    codepoint = ord(char)
    return 0x0900 <= codepoint <= 0x097F or 0x0980 <= codepoint <= 0x09FF


def tokenize(text: str) -> list[str]:
    """Split text on whitespace and punctuation while retaining Indic marks."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    tokens = []
    current = []
    for index, char in enumerate(text):
        category = unicodedata.category(char)
        is_joiner = (
            char in {"\u200c", "\u200d"}
            and current
            and index + 1 < len(text)
            and _is_indic_character(text[index - 1])
            and _is_indic_character(text[index + 1])
        )
        if (
            category[0] in {"L", "N"}
            or (category[0] == "M" and current)
            or is_joiner
        ):
            current.append(char)
        else:
            if current:
                tokens.append("".join(current).lower())
                current = []
    if current:
        tokens.append("".join(current).lower())
    return tokens


__all__ = ["tokenize"]
