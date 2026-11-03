"""Text cleaning and Unicode normalization utilities."""

from __future__ import annotations

import re
import unicodedata

_URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
_WHITESPACE_RE = re.compile(r"\s+")
_ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\ufeff"}


def _is_indic_character(char: str) -> bool:
    """Return True for Devanagari or Bengali characters."""
    codepoint = ord(char)
    return 0x0900 <= codepoint <= 0x097F or 0x0980 <= codepoint <= 0x09FF


def _is_emoji(char: str) -> bool:
    """Detect common emoji and pictographic characters."""
    codepoint = ord(char)
    return (
        0x1F000 <= codepoint <= 0x1FAFF
        or 0x2600 <= codepoint <= 0x27BF
        or 0x2300 <= codepoint <= 0x23FF
        or codepoint in {0x00A9, 0x00AE, 0x203C, 0x2049, 0x2122, 0x2139, 0x3030, 0x303D, 0x3297, 0x3299}
        or 0x1F1E6 <= codepoint <= 0x1F1FF
    )


def clean_text(
    text: str,
    remove_emoji: bool = True,
    remove_urls: bool = False,
    lowercase: bool = False,
) -> str:
    """Normalize Unicode and clean text while preserving Indic conjuncts.

    Example: ``clean_text("नमस्ते   😀 दोस्तों")`` returns ``"नमस्ते दोस्तों"``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    text = unicodedata.normalize("NFC", text)
    if remove_urls:
        text = _URL_RE.sub(" ", text)

    chars = list(text)
    cleaned: list[str] = []
    for index, char in enumerate(chars):
        if char in _ZERO_WIDTH:
            keep_joiner = (
                char in {"\u200c", "\u200d"}
                and index > 0
                and index + 1 < len(chars)
                and _is_indic_character(chars[index - 1])
                and _is_indic_character(chars[index + 1])
            )
            if keep_joiner:
                cleaned.append(char)
            continue
        if remove_emoji and _is_emoji(char):
            continue
        cleaned.append(char)

    result = _WHITESPACE_RE.sub(" ", "".join(cleaned)).strip()
    return result.lower() if lowercase else result


def normalize_digits(text: str, to: str = "ascii") -> str:
    """Convert Devanagari or Bengali digits to ASCII or another script.

    Example: ``normalize_digits("১২৩")`` returns ``"123"``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    mappings = {
        "ascii": {"०": "0", "१": "1", "२": "2", "३": "3", "४": "4", "५": "5", "६": "6", "७": "7", "८": "8", "९": "9", "০": "0", "১": "1", "২": "2", "৩": "3", "৪": "4", "৫": "5", "৬": "6", "৭": "7", "৮": "8", "৯": "9"},
        "devanagari": {"0": "०", "1": "१", "2": "२", "3": "३", "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९"},
        "bengali": {"0": "০", "1": "১", "2": "২", "3": "৩", "4": "৪", "5": "৫", "6": "৬", "7": "৭", "8": "৮", "9": "৯"},
    }
    if to not in mappings:
        raise ValueError("to must be 'ascii', 'devanagari', or 'bengali'")

    if to == "ascii":
        return "".join(mappings["ascii"].get(ch, ch) for ch in text)

    result: list[str] = []
    for ch in text:
        if ch in mappings["devanagari"]:
            result.append(mappings[to][ch])
        elif ch.isdigit() and ch in mappings["devanagari"]:
            result.append(mappings[to][ch])
        else:
            result.append(ch)
    return "".join(result)


__all__ = ["clean_text", "normalize_digits"]
