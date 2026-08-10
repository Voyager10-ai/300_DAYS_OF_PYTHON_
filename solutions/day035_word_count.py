# Day 35: Word Count
#
# Problem:
#   Write a Python program to calculate word counts and word frequencies from a text string or stream.
#   - Basic Word Counting: Space-delimited token counting.
#   - Frequency Analysis: Frequency map creation using collections.Counter and dicts.

import sys
import re
import unittest
from collections import Counter
from typing import List, Set, Dict, Tuple, Optional, Iterable, Iterator, Any


def count_words_basic(text: str) -> int:
    """
    Calculates total word count based on whitespace separation.

    Args:
        text: Input string.

    Returns:
        Integer count of words.

    Time Complexity: O(N) where N is number of characters.
    Space Complexity: O(W) where W is number of words.

    Example:
        count_words_basic("Hello world! Python is great.") -> 5
        count_words_basic("") -> 0
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


def get_word_frequencies(text: str, case_sensitive: bool = False) -> Dict[str, int]:
    """
    Generates a frequency map of words in the given text.

    Args:
        text: Input text string.
        case_sensitive: Whether to maintain word casing when counting frequencies.

    Returns:
        Dictionary mapping each word to its occurrence count.

    Example:
        get_word_frequencies("apple Banana apple") -> {"apple": 2, "banana": 1}
    """
    if not text or not text.strip():
        return {}

    words = text.split()
    processed_words = words if case_sensitive else [w.lower() for w in words]
    return dict(Counter(processed_words))


def count_words_regex(text: str, strip_punctuation: bool = True) -> int:
    """
    Counts words using regex pattern matching, ignoring punctuation marks and special symbols.

    Args:
        text: Input string.
        strip_punctuation: If True, uses word boundaries \\b\\w+\\b to isolate alphanumeric tokens.

    Returns:
        Number of valid word tokens.

    Example:
        count_words_regex("Hello, world! 123... test-case") -> 4
    """
    if not text or not text.strip():
        return 0

    if strip_punctuation:
        tokens = re.findall(r'\b\w+\b', text)
    else:
        tokens = text.split()

    return len(tokens)


def count_words_case_insensitive(text: str) -> Dict[str, int]:
    """
    Counts word occurrences case-insensitively after stripping punctuation.

    Args:
        text: Input string.

    Returns:
        Dictionary of lowercased word frequencies.

    Example:
        count_words_case_insensitive("Python python PYTHON!") -> {"python": 3}
    """
    if not text or not text.strip():
        return {}

    tokens = [w.lower() for w in re.findall(r'\b\w+\b', text)]
    return dict(Counter(tokens))


DEFAULT_STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "what",
    "which", "this", "that", "these", "those", "then", "just", "so", "than",
    "such", "both", "through", "about", "for", "is", "of", "to", "in", "it"
}


def count_words_filter_stopwords(
    text: str,
    custom_stopwords: Optional[Set[str]] = None,
    min_length: int = 1
) -> Dict[str, int]:
    """
    Counts word frequencies excluding common stop-words and short noise tokens.

    Args:
        text: Input text string.
        custom_stopwords: Set of stop-words to exclude (uses DEFAULT_STOPWORDS if None).
        min_length: Minimum word length threshold to count.

    Returns:
        Filtered dictionary of word frequencies.

    Example:
        count_words_filter_stopwords("The quick brown fox is fast") -> {"quick": 1, "brown": 1, "fox": 1, "fast": 1}
    """
    if not text or not text.strip():
        return {}

    stopwords = custom_stopwords if custom_stopwords is not None else DEFAULT_STOPWORDS
    raw_tokens = re.findall(r'\b\w+\b', text.lower())

    filtered_tokens = [
        word for word in raw_tokens
        if word not in stopwords and len(word) >= min_length
    ]
    return dict(Counter(filtered_tokens))


def get_word_length_distribution(text: str) -> Dict[int, int]:
    """
    Calculates the frequency distribution of word lengths (e.g. how many 3-letter, 4-letter words).

    Args:
        text: Input string.

    Returns:
        Dictionary mapping word_length -> count_of_words_with_that_length.

    Example:
        get_word_length_distribution("cat dog elephant") -> {3: 2, 8: 1}
    """
    if not text or not text.strip():
        return {}

    tokens = re.findall(r'\b\w+\b', text)
    lengths = [len(token) for token in tokens]
    return dict(Counter(lengths))


