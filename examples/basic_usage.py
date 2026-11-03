"""Examples of the offline bhasha-kit public API."""

import sys

from bhasha_kit import (
    clean_text,
    detect_language,
    detect_languages,
    normalize_digits,
    number_to_rupees,
    number_to_words,
    to_bengali,
    to_devanagari,
    to_roman,
    to_roman_bengali,
)

sys.stdout.reconfigure(encoding="utf-8")

print(clean_text("नमस्ते   😀 दोस्तों"))
print(normalize_digits("১২৩"))
print(detect_language("नमस्ते"))
print(detect_languages("नम hi"))
print(to_devanagari("namaste"))
print(to_roman("नमस्ते"))
print(to_bengali("aamaar naam rahim"))
print(to_roman_bengali("আমার"))
print(number_to_words(1250, "hi"))
print(number_to_rupees("1250.50"))
