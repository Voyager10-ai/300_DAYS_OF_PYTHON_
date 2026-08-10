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
