# Day 30: Longest Word
#
# Problem:
#   Write a Python program to find the longest word in a string, sentence, or list of words.
#   - Core Longest Word Search: Extract the single longest word from input text.
#   - Punctuation Sanitization: Clean leading/trailing punctuation and symbols.

import string
from typing import Optional, List, Dict, Any, Callable, Tuple


def clean_word(word: str) -> str:
    """
    Strips leading and trailing punctuation characters from a word token.

    Args:
        word: Single word token string.

    Returns:
        Cleaned word string with punctuation removed from boundaries.

    Example:
        clean_word("hello,") -> "hello"
        clean_word("...world!") -> "world"
    """
    return word.strip(string.punctuation)


def find_longest_word(text: str, strip_punctuation: bool = True) -> str:
    """
    Finds the first longest word in a given text string.

    Args:
        text: Input string or sentence.
        strip_punctuation: Whether to remove surrounding punctuation.

    Returns:
        The longest word found, or an empty string if input contains no valid words.

    Time Complexity: O(N) where N is number of characters.
    Space Complexity: O(W) where W is number of words.

    Example:
        find_longest_word("The quick brown fox jumps over the lazy dog") -> "jumps"
        find_longest_word("Comprehensive Python programming guide!") -> "Comprehensive"
    """
    if not text or not text.strip():
        return ""

    tokens = text.split()
    if strip_punctuation:
        cleaned_words = [clean_word(t) for t in tokens]
        words = [w for w in cleaned_words if w]
    else:
        words = tokens

    if not words:
        return ""

    return max(words, key=len)


def find_all_longest_words(text: str, strip_punctuation: bool = True) -> List[str]:
    """
    Finds all words in text that share the maximum word length.

    Args:
        text: Input text string.
        strip_punctuation: Whether to strip surrounding punctuation.

    Returns:
        List of distinct longest words in order of appearance.

    Example:
        find_all_longest_words("cat dog elephant dinosaur") -> ["elephant", "dinosaur"]
    """
    if not text or not text.strip():
        return []

    tokens = text.split()
    if strip_punctuation:
        cleaned_words = [clean_word(t) for t in tokens]
        words = [w for w in cleaned_words if w]
    else:
        words = tokens

    if not words:
        return []

    max_len = max(len(w) for w in words)
    longest_words = []
    seen = set()

    for w in words:
        if len(w) == max_len and w not in seen:
            longest_words.append(w)
            seen.add(w)

    return longest_words

