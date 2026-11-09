import pytest

from bhasha_kit import extract_keywords


def test_extract_keywords_removes_stopwords_numbers_and_single_characters():
    assert extract_keywords("The quick fox and the fox 123 a") == [
        ("fox", 2), ("quick", 1),
    ]


def test_extract_keywords_top_n_order_and_first_appearance_ties():
    text = "apple banana apple cherry banana date"
    assert extract_keywords(text, top_n=3, lang="en") == [
        ("apple", 2), ("banana", 2), ("cherry", 1),
    ]
    assert extract_keywords("apple banana", top_n=1, lang="en") == [
        ("apple", 1),
    ]


def test_extract_keywords_supports_hindi_bengali_and_empty_text():
    assert extract_keywords(
        "यह फिल्म और फिल्म", lang="hi"
    ) == [("फिल्म", 2)]
    assert extract_keywords(
        "এই বাংলা এবং বাংলা", lang="bn"
    ) == [("বাংলা", 2)]
    assert extract_keywords("") == []


def test_extract_keywords_errors():
    with pytest.raises(ValueError):
        extract_keywords("text", top_n=0)
    with pytest.raises(ValueError):
        extract_keywords("text", lang="fr")
    with pytest.raises(TypeError):
        extract_keywords("text", top_n=1.5)
