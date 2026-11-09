"""Offline text utilities for Hindi, Bengali, and English."""

from .cleaner import clean_text, normalize_digits
from .detect import detect_language, detect_languages
from .keywords import extract_keywords
from .numbers import number_to_rupees, number_to_words
from .sentiment import analyze_sentiment
from .tokenize import tokenize
from .translit import to_bengali, to_devanagari, to_roman, to_roman_bengali

__version__ = "0.2.0"

__all__ = [
    "clean_text",
    "normalize_digits",
    "detect_language",
    "detect_languages",
    "to_devanagari",
    "to_roman",
    "to_bengali",
    "to_roman_bengali",
    "number_to_words",
    "number_to_rupees",
    "tokenize",
    "analyze_sentiment",
    "extract_keywords",
]
