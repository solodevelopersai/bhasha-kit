"""Approximate, rule-based transliteration between Roman and Indic scripts.

Transliteration is rule-based and approximate; it is not linguistic conversion
and cannot resolve pronunciation or spelling ambiguities without context.
"""

from __future__ import annotations

import re

_DEVANAGARI_VOWELS = {
    "aa": ("आ", "ा"),
    "ii": ("ई", "ी"),
    "ee": ("ई", "ी"),
    "uu": ("ऊ", "ू"),
    "oo": ("ऊ", "ू"),
    "a": ("अ", ""),
    "i": ("इ", "ि"),
    "u": ("उ", "ु"),
    "e": ("ए", "े"),
    "o": ("ओ", "ो"),
    "ai": ("ऐ", "ै"),
    "au": ("औ", "ौ"),
}
_BENGALI_VOWELS = {
    "aa": ("আ", "া"),
    "ii": ("ঈ", "ী"),
    "ee": ("ঈ", "ী"),
    "uu": ("ঊ", "ূ"),
    "oo": ("ঊ", "ূ"),
    "a": ("অ", ""),
    "i": ("ই", "ি"),
    "u": ("উ", "ু"),
    "e": ("এ", "ে"),
    "o": ("ও", "ো"),
    "ai": ("ঐ", "ৈ"),
    "au": ("ঔ", "ৌ"),
}
_DEVANAGARI_CONSONANTS = {
    "k": "क", "kh": "ख", "g": "ग", "gh": "घ", "ng": "ङ",
    "ch": "च", "chh": "छ", "j": "ज", "jh": "झ", "ny": "ञ",
    "T": "ट", "Th": "ठ", "D": "ड", "Dh": "ढ", "N": "ण",
    "t": "त", "th": "थ", "d": "द", "dh": "ध", "n": "न",
    "p": "प", "ph": "फ", "b": "ब", "bh": "भ", "m": "म",
    "y": "य", "r": "र", "l": "ल", "v": "व", "w": "व",
    "sh": "श", "Sh": "ष", "s": "स", "h": "ह",
    "q": "क़", "x": "क्ष", "f": "फ़", "z": "ज़",
}
_BENGALI_CONSONANTS = {
    "k": "ক", "kh": "খ", "g": "গ", "gh": "ঘ", "ng": "ঙ",
    "ch": "চ", "chh": "ছ", "j": "জ", "jh": "ঝ", "ny": "ঞ",
    "T": "ট", "Th": "ঠ", "D": "ড", "Dh": "ঢ", "N": "ণ",
    "t": "ত", "th": "থ", "d": "দ", "dh": "ধ", "n": "ন",
    "p": "প", "ph": "ফ", "b": "ব", "bh": "ভ", "m": "ম",
    "y": "য", "r": "র", "l": "ল", "v": "ভ", "w": "ও",
    "sh": "শ", "Sh": "ষ", "s": "স", "h": "হ",
    "q": "ক", "x": "ক্ষ", "f": "ফ", "z": "জ",
}
_DEV_INDEPENDENT = {
    "अ": "a", "आ": "aa", "इ": "i", "ई": "ii", "उ": "u", "ऊ": "uu",
    "ऋ": "ri", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au",
}
_DEV_MATRA = {
    "ा": "aa", "ि": "i", "ी": "ii", "ु": "u", "ू": "uu",
    "ृ": "ri", "े": "e", "ै": "ai", "ो": "o", "ौ": "au",
}
_DEV_CONSONANT_ROMAN = {
    value: key.lower()
    for key, value in _DEVANAGARI_CONSONANTS.items()
    if key not in {"T", "Th", "D", "Dh", "N", "Sh"}
}
_DEV_CONSONANT_ROMAN.update(
    {"ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "ण": "n", "ष": "sh", "व": "v"}
)
_BN_INDEPENDENT = {
    "অ": "o", "আ": "aa", "ই": "i", "ঈ": "ii", "উ": "u", "ঊ": "uu",
    "ঋ": "ri", "এ": "e", "ঐ": "oi", "ও": "o", "ঔ": "ou",
}
_BN_MATRA = {
    "া": "aa", "ি": "i", "ী": "ii", "ু": "u", "ূ": "uu",
    "ৃ": "ri", "ে": "e", "ৈ": "oi", "ো": "o", "ৌ": "ou",
}
_BN_CONSONANT_ROMAN = {
    value: key.lower()
    for key, value in _BENGALI_CONSONANTS.items()
    if key not in {"T", "Th", "D", "Dh", "N", "Sh"}
}
_BN_CONSONANT_ROMAN.update(
    {
        "ক": "k", "ট": "t", "ঠ": "th", "ড": "d", "ঢ": "dh", "ণ": "n",
        "ষ": "sh", "ভ": "bh",
    }
)
_ROMAN_WORD_RE = re.compile(r"[A-Za-z]+")


def _phonemes(
    word: str,
    consonants: dict[str, str],
    vowels: dict[str, tuple[str, str]],
) -> list[tuple[str, str]]:
    keys = sorted(set(consonants) | set(vowels), key=len, reverse=True)
    result: list[tuple[str, str]] = []
    index = 0
    while index < len(word):
        match = next((key for key in keys if word.startswith(key, index)), None)
        if match is None:
            result.append(("unknown", word[index]))
            index += 1
        elif match in consonants:
            result.append(("consonant", consonants[match]))
            index += len(match)
        elif match in vowels:
            result.append(("vowel", match))
            index += len(match)
        else:
            result.append(("unknown", match))
            index += len(match)
    return result


def _roman_word_to_indic(
    word: str,
    consonants: dict[str, str],
    vowels: dict[str, tuple[str, str]],
    virama: str,
) -> str:
    units = _phonemes(word, consonants, vowels)
    output: list[str] = []
    index = 0
    while index < len(units):
        kind, value = units[index]
        if kind == "vowel":
            output.append(vowels[value][0])
        elif kind == "consonant":
            output.append(value)
            if index + 1 < len(units):
                next_kind, next_value = units[index + 1]
                if next_kind == "vowel":
                    sign = vowels[next_value][1]
                    if next_value == "a" and index + 1 == len(units) - 1:
                        sign = vowels["aa"][1]
                    output.append(sign)
                    index += 1
                elif next_kind == "consonant":
                    output.append(virama)
        else:
            output.append(value)
        index += 1
    return "".join(output)


def _to_indic(
    text: str,
    consonants: dict[str, str],
    vowels: dict[str, tuple[str, str]],
    virama: str,
) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return _ROMAN_WORD_RE.sub(
        lambda match: _roman_word_to_indic(match.group(0), consonants, vowels, virama), text
    )


def to_devanagari(text: str) -> str:
    """Transliterate Roman text approximately into Devanagari.

    Example: ``to_devanagari("namaste")`` returns ``"नमस्ते"``.
    """
    return _to_indic(text, _DEVANAGARI_CONSONANTS, _DEVANAGARI_VOWELS, "्")


def to_bengali(text: str) -> str:
    """Transliterate Roman text approximately into Bengali script.

    Example: ``to_bengali("aamaar naam rahim")`` returns ``"আমার নাম রহিম"``.
    """
    return _to_indic(text, _BENGALI_CONSONANTS, _BENGALI_VOWELS, "্")


def _indic_to_roman(
    text: str,
    independent: dict[str, str],
    matras: dict[str, str],
    consonants: dict[str, str],
    virama: str,
    anusvara: str,
    chandrabindu: str,
    visarga: str,
) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    output: list[str] = []
    for index, char in enumerate(text):
        supported = (
            char in consonants
            or char in independent
            or char in matras
            or char == virama
            or char in {anusvara, chandrabindu, visarga}
        )
        if char.isspace() or not supported:
            output.append(char)
            continue
        if char in consonants:
            output.append(consonants[char])
            next_char = text[index + 1] if index + 1 < len(text) else ""
            if next_char == virama or next_char in matras:
                continue
            if next_char in consonants or next_char in independent or next_char in {
                anusvara,
                chandrabindu,
                visarga,
            }:
                output.append("a")
            continue
        if char == virama:
            continue
        if char in independent:
            output.append(independent[char])
        elif char in matras:
            output.append(matras[char])
        elif char in {anusvara, chandrabindu}:
            output.append("n")
        elif char == visarga:
            output.append("h")
    return "".join(output)


def to_roman(text: str) -> str:
    """Transliterate Devanagari approximately into Roman characters.

    Example: ``to_roman("नमस्ते")`` returns ``"namaste"``.
    """
    return _indic_to_roman(
        text, _DEV_INDEPENDENT, _DEV_MATRA, _DEV_CONSONANT_ROMAN,
        "्", "ं", "ँ", "ः"
    )


def to_roman_bengali(text: str) -> str:
    """Transliterate Bengali script approximately into Roman characters.

    Example: ``to_roman_bengali("আমার")`` returns ``"aamaar"``.
    """
    return _indic_to_roman(
        text, _BN_INDEPENDENT, _BN_MATRA, _BN_CONSONANT_ROMAN,
        "্", "ং", "ঁ", "ঃ"
    )


__all__ = ["to_devanagari", "to_roman", "to_bengali", "to_roman_bengali"]
