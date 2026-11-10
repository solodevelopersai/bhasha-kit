# bhasha-kit

Offline Python utilities for cleaning, detecting, transliterating, spelling, and analyzing Hindi, Bengali, and English text.

[![PyPI version](https://img.shields.io/pypi/v/bhasha-kit)](https://pypi.org/project/bhasha-kit/)
[![PyPI downloads](https://img.shields.io/pypi/dm/bhasha-kit)](https://pypi.org/project/bhasha-kit/)
[![Tests](https://github.com/solodevelopersai/bhasha-kit/actions/workflows/tests.yml/badge.svg)](https://github.com/solodevelopersai/bhasha-kit/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

`bhasha-kit` runs locally, uses only the Python standard library at runtime, and makes no external API calls.

## Features

- Unicode NFC text cleaning, optional URL and emoji removal, and script-aware digit conversion.
- Lightweight Hindi (`hi`), Bengali (`bn`), and English (`en`) script detection with language shares.
- Rule-based Roman ↔ Devanagari and Roman ↔ Bengali transliteration.
- Integer-to-words and rupee/paise amount conversion using Indian number groups.
- **Level 4 (done):** offline lexicon-based sentiment analysis and frequency-based keyword extraction.
- Python 3.9+ support with no third-party runtime dependencies.

## Installation

Install from PyPI:

```shell
python -m pip install bhasha-kit
```

Or install directly from GitHub:

```shell
python -m pip install git+https://github.com/solodevelopersai/bhasha-kit.git
```

For local development:

```shell
git clone https://github.com/solodevelopersai/bhasha-kit.git
cd bhasha-kit
python -m pip install -e ".[dev]"
```

## Quick start

```python
from bhasha_kit import clean_text, number_to_words, analyze_sentiment

clean_text("नमस्ते   😀 दोस्तों")
# 'नमस्ते दोस्तों'

number_to_words(1250, "hi")
# 'एक हज़ार दो सौ पचास'

analyze_sentiment("यह फिल्म बहुत अच्छी है")
# {'label': 'positive', 'score': 1.0, 'lang': 'hi'}
```

## Usage

Every function is available from the `bhasha_kit` package:

```python
from bhasha_kit import (
    clean_text, normalize_digits, detect_language, detect_languages,
    to_devanagari, to_roman, to_bengali, to_roman_bengali,
    number_to_words, number_to_rupees,
    tokenize, analyze_sentiment, extract_keywords,
)

clean_text("नमस्ते   😀 दोस्तों")
# 'नमस्ते दोस्तों'

normalize_digits("১২৩")
# '123'

detect_language("বাংলা")
# 'bn'

detect_languages("नম hi")
# {'hi': 0.25, 'bn': 0.25, 'en': 0.5}

to_devanagari("namaste")
# 'नमस्ते'

to_roman("नमस्ते")
# 'namaste'

to_bengali("aamaar naam rahim")
# 'আমার নাম রহিম'

to_roman_bengali("আমার")
# 'aamaar'

number_to_words(1250, "hi")
# 'एक हज़ार दो सौ पचास'

number_to_rupees("1250.50")
# 'एक हज़ार दो सौ पचास रुपये पचास पैसे'

analyze_sentiment("यह फिल्म बहुत अच्छी है")
# {'label': 'positive', 'score': 1.0, 'lang': 'hi'}

analyze_sentiment("this is not good")
# {'label': 'negative', 'score': -1.0, 'lang': 'en'}

extract_keywords("The film was good and the story was excellent.")
# [('film', 1), ('good', 1), ('story', 1), ('excellent', 1)]
```

`clean_text` normalizes whitespace and Unicode by default; set `remove_urls=True`
or `lowercase=True` to enable those options. `normalize_digits` accepts
`to="ascii"`, `to="devanagari"`, or `to="bengali"`. The language detector returns
shares only for scripts found in the input, and returns an empty dictionary for
text with no countable letters. Sentiment and keyword functions detect the
dominant script unless a language code (`"hi"`, `"bn"`, or `"en"`) is supplied.

## Known limitations

Transliteration is deliberately rule-based and approximate. It uses simple Roman
spelling conventions, cannot infer pronunciation or resolve all ambiguities, and
is not a substitute for a full language-specific transliteration system.
Language detection is based on Unicode script ranges, not linguistic semantics.
Sentiment is lexicon-based, uses a small word list, and does not understand
sarcasm or context.

## Roadmap

- **Level 5:** REST API and a web demo.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing, and pull
request guidance.

## License

Released under the MIT License. See [LICENSE](LICENSE).
