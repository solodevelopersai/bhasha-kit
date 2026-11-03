"""Unicode-aware text cleaning utilities for Hindi, Bengali, and English."""

from __future__ import annotations

import re
import unicodedata

_URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
_KEYCAP_EMOJI_RE = re.compile(r"[#*0-9]\ufe0f?\u20e3")
_WHITESPACE_RE = re.compile(r"\s+")
_ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\ufeff"}
_DIGIT_MAPS = {
    "ascii": str.maketrans(
        "०१२३४५६७८९০১২৩৪৫৬৭৮৯",
        "01234567890123456789",
    ),
    "devanagari": str.maketrans(
        "0123456789০১২৩৪৫৬৭৮৯",
        "०१२३४५६७८९०१२३४५६७८९",
    ),
    "bengali": str.maketrans(
        "0123456789०१२३४५६७८९",
        "০১২৩৪৫৬৭৮৯০১২৩৪৫৬৭৮৯",
    ),
}


def _is_indic_character(char: str) -> bool:
    """Return whether a character belongs to either supported Indic block."""
    codepoint = ord(char)
    return 0x0900 <= codepoint <= 0x097F or 0x0980 <= codepoint <= 0x09FF


def _is_emoji(char: str) -> bool:
    """Detect common emoji and pictographic codepoint ranges."""
    codepoint = ord(char)
    return (
        0x1F000 <= codepoint <= 0x1FAFF
        or 0x2600 <= codepoint <= 0x27BF
        or 0x2300 <= codepoint <= 0x23FF
        or codepoint
        in {0x00A9, 0x00AE, 0x203C, 0x2049, 0x2122, 0x2139, 0x3030, 0x303D, 0x3297, 0x3299}
        or codepoint == 0xFE0F
    )


def clean_text(
    text: str,
    remove_emoji: bool = True,
    remove_urls: bool = False,
    lowercase: bool = False,
) -> str:
    """Normalize and clean text, retaining joiners inside Indic sequences.

    Example: ``clean_text("नमस्ते   😀 दोस्तों")`` returns ``"नमस्ते दोस्तों"``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    for name, value in (
        ("remove_emoji", remove_emoji),
        ("remove_urls", remove_urls),
        ("lowercase", lowercase),
    ):
        if not isinstance(value, bool):
            raise TypeError("{} must be a bool".format(name))

    text = unicodedata.normalize("NFC", text)
    if remove_urls:
        text = _URL_RE.sub(" ", text)
    if remove_emoji:
        text = _KEYCAP_EMOJI_RE.sub("", text)

    chars = list(text)
    cleaned: list[str] = []
    for index, char in enumerate(chars):
        if char in _ZERO_WIDTH:
            preserve = (
                char in {"\u200c", "\u200d"}
                and index > 0
                and index + 1 < len(chars)
                and _is_indic_character(chars[index - 1])
                and _is_indic_character(chars[index + 1])
            )
            if preserve:
                cleaned.append(char)
            continue
        if remove_emoji and _is_emoji(char):
            continue
        cleaned.append(char)

    result = _WHITESPACE_RE.sub(" ", "".join(cleaned)).strip()
    return result.lower() if lowercase else result


def normalize_digits(text: str, to: str = "ascii") -> str:
    """Convert supported-script digits to ASCII, Devanagari, or Bengali.

    Example: ``normalize_digits("১২৩")`` returns ``"123"``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(to, str):
        raise TypeError("to must be a string")
    if to not in _DIGIT_MAPS:
        raise ValueError("to must be 'ascii', 'devanagari', or 'bengali'")
    return text.translate(_DIGIT_MAPS[to])


__all__ = ["clean_text", "normalize_digits"]
