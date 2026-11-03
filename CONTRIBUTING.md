# Contributing

Thank you for helping improve bhasha-kit. The project is intentionally
dependency-free at runtime and supports Python 3.9 and newer.

## Development setup

```shell
git clone https://github.com/solodevelopersai/bhasha-kit.git
cd bhasha-kit
python -m pip install -e ".[dev]"
```

## Tests and changes

Run the test suite with:

```shell
python -m pytest
```

Please include tests for behavior changes, keep the implementation offline, and
avoid adding third-party runtime dependencies. For language data, favor explicit
tables and document any transliteration limitations. Open a pull request with a
short explanation of the change and its test results.

## Code of conduct

Be respectful, constructive, and welcoming in discussions and reviews.
