"""Number and currency spelling in Hindi, Bengali, and English."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

_HI = (
    "शून्य", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ",
    "दस", "ग्यारह", "बारह", "तेरह", "चौदह", "पंद्रह", "सोलह", "सत्रह", "अठारह", "उन्नीस",
    "बीस", "इक्कीस", "बाईस", "तेईस", "चौबीस", "पच्चीस", "छब्बीस", "सत्ताईस", "अट्ठाईस", "उनतीस",
    "तीस", "इकतीस", "बत्तीस", "तैंतीस", "चौंतीस", "पैंतीस", "छत्तीस", "सैंतीस", "अड़तीस", "उनतालीस",
    "चालीस", "इकतालीस", "बयालीस", "तैंतालीस", "चवालीस", "पैंतालीस", "छियालीस", "सैंतालीस", "अड़तालीस", "उनचास",
    "पचास", "इक्यावन", "बावन", "तिरपन", "चौवन", "पचपन", "छप्पन", "सत्तावन", "अट्ठावन", "उनसठ",
    "साठ", "इकसठ", "बासठ", "तिरसठ", "चौंसठ", "पैंसठ", "छियासठ", "सड़सठ", "अड़सठ", "उनहत्तर",
    "सत्तर", "इकहत्तर", "बहत्तर", "तिहत्तर", "चौहत्तर", "पचहत्तर", "छिहत्तर", "सतहत्तर", "अठहत्तर", "उन्नासी",
    "अस्सी", "इक्यासी", "बयासी", "तिरासी", "चौरासी", "पचासी", "छियासी", "सतासी", "अठासी", "नवासी",
    "नब्बे", "इक्यानवे", "बानवे", "तिरानवे", "चौरानवे", "पचानवे", "छियानवे", "सत्तानवे", "अट्ठानवे", "निन्यानवे",
)
_BN = (
    "শূন্য", "এক", "দুই", "তিন", "চার", "পাঁচ", "ছয়", "সাত", "আট", "নয়",
    "দশ", "এগারো", "বারো", "তেরো", "চৌদ্দ", "পনেরো", "ষোলো", "সতেরো", "আঠারো", "উনিশ",
    "কুড়ি", "একুশ", "বাইশ", "তেইশ", "চব্বিশ", "পঁচিশ", "ছাব্বিশ", "সাতাশ", "আটাশ", "ঊনত্রিশ",
    "ত্রিশ", "একত্রিশ", "বত্রিশ", "তেত্রিশ", "চৌত্রিশ", "পঁয়ত্রিশ", "ছত্রিশ", "সাঁইত্রিশ", "আটত্রিশ", "উনচল্লিশ",
    "চল্লিশ", "একচল্লিশ", "বিয়াল্লিশ", "তেতাল্লিশ", "চুয়াল্লিশ", "পঁয়তাল্লিশ", "ছেচল্লিশ", "সাতচল্লিশ", "আটচল্লিশ", "উনপঞ্চাশ",
    "পঞ্চাশ", "একান্ন", "বাহান্ন", "তিপ্পান্ন", "চুয়ান্ন", "পঞ্চান্ন", "ছাপ্পান্ন", "সাতান্ন", "আটান্ন", "ঊনষাট",
    "ষাট", "একষট্টি", "বাষট্টি", "তেষট্টি", "চৌষট্টি", "পঁয়ষট্টি", "ছেষট্টি", "সাতষট্টি", "আটষট্টি", "উনসত্তর",
    "সত্তর", "একাত্তর", "বাহাত্তর", "তিয়াত্তর", "চুয়াত্তর", "পঁচাত্তর", "ছিয়াত্তর", "সাতাত্তর", "আটাত্তর", "উনআশি",
    "আশি", "একাশি", "বিরাশি", "তিরাশি", "চুরাশি", "পঁচাশি", "ছিয়াশি", "সাতাশি", "আটাশি", "উননব্বই",
    "নব্বই", "একানব্বই", "বিরানব্বই", "তিরানব্বই", "চুরানব্বই", "পঁচানব্বই", "ছিয়ানব্বই", "সাতানব্বই", "আটানব্বই", "নিরানব্বই",
)
_EN_UNDER_TWENTY = (
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
)
_EN_TENS = (
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
)
_MAX_NUMBER = 999_999_999
_SCRIPT_DATA = {
    "hi": {
        "under_100": _HI,
        "hundred": "सौ",
        "thousand": "हज़ार",
        "lakh": "लाख",
        "crore": "करोड़",
        "negative": "ऋण",
        "rupees": "रुपये",
        "rupee_singular": "रुपया",
        "paise": "पैसे",
        "paise_singular": "पैसा",
    },
    "bn": {
        "under_100": _BN,
        "hundred": "শত",
        "thousand": "হাজার",
        "lakh": "লক্ষ",
        "crore": "কোটি",
        "negative": "ঋণ",
        "rupees": "টাকা",
        "rupee_singular": "টাকা",
        "paise": "পয়সা",
        "paise_singular": "পয়সা",
    },
    "en": {
        "under_100": _EN_UNDER_TWENTY,
        "hundred": "hundred",
        "thousand": "thousand",
        "lakh": "lakh",
        "crore": "crore",
        "negative": "minus",
        "rupees": "rupees",
        "rupee_singular": "rupee",
        "paise": "paise",
        "paise_singular": "paisa",
    },
}


def _under_hundred(number: int, lang: str) -> str:
    if lang != "en":
        return _SCRIPT_DATA[lang]["under_100"][number]
    if number < 20:
        return _EN_UNDER_TWENTY[number]
    tens, units = divmod(number, 10)
    return _EN_TENS[tens] + ((" " + _EN_UNDER_TWENTY[units]) if units else "")


def _under_thousand(number: int, lang: str) -> str:
    if number == 0:
        return _under_hundred(0, lang)
    parts: list[str] = []
    hundreds, remainder = divmod(number, 100)
    if hundreds:
        parts.append(_under_hundred(hundreds, lang))
        parts.append(_SCRIPT_DATA[lang]["hundred"])
    if remainder:
        parts.append(_under_hundred(remainder, lang))
    return " ".join(parts)


def _positive_number_to_words(number: int, lang: str) -> str:
    if number < 1000:
        return _under_thousand(number, lang)
    parts: list[str] = []
    for divisor, key in (
        (10_000_000, "crore"),
        (100_000, "lakh"),
        (1_000, "thousand"),
    ):
        count, number = divmod(number, divisor)
        if count:
            parts.append(_positive_number_to_words(count, lang))
            parts.append(_SCRIPT_DATA[lang][key])
    if number:
        parts.append(_under_thousand(number, lang))
    return " ".join(parts)


def number_to_words(n: int, lang: str = "hi") -> str:
    """Spell an integer using Indian number groups.

    Example: ``number_to_words(1250, "hi")`` returns ``"एक हज़ार दो सौ पचास"``.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if not isinstance(lang, str):
        raise TypeError("lang must be a string")
    if lang not in _SCRIPT_DATA:
        raise ValueError("lang must be 'hi', 'bn', or 'en'")
    if abs(n) > _MAX_NUMBER:
        raise ValueError("n must be between -999999999 and 999999999")

    prefix = ""
    if n < 0:
        prefix = _SCRIPT_DATA[lang]["negative"] + " "
    return prefix + _positive_number_to_words(abs(n), lang)


def number_to_rupees(amount: Decimal | int | float | str, lang: str = "hi") -> str:
    """Spell a currency amount rounded to two decimal places.

    Example: ``number_to_rupees("1250.50")`` returns
    ``"एक हज़ार दो सौ पचास रुपये पचास पैसे"``.
    """
    if isinstance(lang, str) and lang not in _SCRIPT_DATA:
        raise ValueError("lang must be 'hi', 'bn', or 'en'")
    if not isinstance(lang, str):
        raise TypeError("lang must be a string")
    if isinstance(amount, bool) or not isinstance(amount, (Decimal, int, float, str)):
        raise TypeError("amount must be a Decimal, integer, float, or numeric string")
    try:
        value = amount if isinstance(amount, Decimal) else Decimal(str(amount))
    except InvalidOperation as error:
        raise ValueError("amount must be a valid finite number") from error
    if not value.is_finite():
        raise ValueError("amount must be finite")
    try:
        rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation as error:
        raise ValueError("amount is outside the supported numeric range") from error
    is_negative = rounded < 0
    absolute = abs(rounded)
    rupees = int(absolute)
    paise = int((absolute - Decimal(rupees)) * 100)
    if rupees > _MAX_NUMBER:
        raise ValueError("rupee amount exceeds the supported number range")

    words = _positive_number_to_words(rupees, lang)
    units = _SCRIPT_DATA[lang]
    rupee_unit = units["rupee_singular"] if rupees == 1 else units["rupees"]
    result = "{} {}".format(words, rupee_unit)
    if paise:
        paise_unit = units["paise_singular"] if paise == 1 else units["paise"]
        result += " {} {}".format(_positive_number_to_words(paise, lang), paise_unit)
    if is_negative:
        result = units["negative"] + " " + result
    return result


__all__ = ["number_to_words", "number_to_rupees"]
