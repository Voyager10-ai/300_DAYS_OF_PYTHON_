# Day 34: Unique Word
#
# Problem:
#   Write a Python program to extract and analyze unique words from a string or text corpus.
#   - Core Set-Based Extraction: Fast unordered unique word retrieval using set().
#   - Order-Preserving Unique Words: Retain word appearance sequence using dict.fromkeys() or set tracking.
#   - Case-Insensitive Extraction: Standardize text casing to find distinct semantic words.

import sys
import re
import unittest
from typing import List, Set, Dict, Tuple, Optional, Iterable, Iterator


def get_unique_words_set(text: str) -> Set[str]:
    """
    Extracts unique words from text using an unordered set.

    Args:
        text: Input string.

    Returns:
        Set of unique space-delimited words.

    Time Complexity: O(N) where N is number of characters in text.
    Space Complexity: O(U) where U is number of unique words.

    Example:
        get_unique_words_set("apple banana apple cherry") -> {"apple", "banana", "cherry"}
    """
    if not text:
        return set()
    return set(text.split())


def get_unique_words_ordered(text: str) -> List[str]:
    """
    Extracts unique words from text while preserving their initial order of appearance.

    Args:
        text: Input string.

    Returns:
        List of unique words in first-seen order.

    Time Complexity: O(N).
    Space Complexity: O(U).

    Example:
        get_unique_words_ordered("apple banana apple cherry banana") -> ["apple", "banana", "cherry"]
    """
    if not text:
        return []
    words = text.split()
    return list(dict.fromkeys(words))


def get_unique_words_case_insensitive(text: str, preserve_first_case: bool = False) -> List[str]:
    """
    Extracts unique words ignoring case sensitivity.

    Args:
        text: Input string.
        preserve_first_case: If True, keeps the case of the word's first occurrence;
                             if False, returns all words in lowercase.

    Returns:
        List of unique words with normalized case matching.

    Example:
        get_unique_words_case_insensitive("Python python PYTHON") -> ["python"]
        get_unique_words_case_insensitive("Python python PYTHON", preserve_first_case=True) -> ["Python"]
    """
    if not text:
        return []
    
    words = text.split()
    seen: Set[str] = set()
    result: List[str] = []

    for word in words:
        lowered = word.lower()
        if lowered not in seen:
            seen.add(lowered)
            result.append(word if preserve_first_case else lowered)

    return result
