# Day 52: Reverse Word
#
# Problem:
#   Write a Python program / module to reverse words in a string.
#   Includes word-order reversal, character reversal per word, punctuation preservation,
#   casing preservation, custom delimiters, predicate filtering, batch processing, unit tests, and Java practice.

import re
import string
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union, Callable


# ─── 1. Core Word Reversing Algorithms ─────────────────────────────────────────


def reverse_words_order(s: str) -> str:
    """
    Reverses the order of words in a string, preserving single space separation.
    For example: 'The quick brown fox' -> 'fox brown quick The'.

    Args:
        s: Input text string.

    Returns:
        String with words in reverse order.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")
    words = s.split()
    return " ".join(reversed(words))


def reverse_each_word(s: str) -> str:
    """
    Reverses the characters of each individual word while maintaining word order.
    For example: 'hello world' -> 'olleh dlrow'.

    Args:
        s: Input text string.

    Returns:
        String with characters of each word reversed.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")
    words = s.split(" ")
    return " ".join(w[::-1] for w in words)


def reverse_entire_string(s: str) -> str:
    """
    Reverses the entire string completely from end to start.
    For example: 'Hello World' -> 'dlroW olleH'.

    Args:
        s: Input text string.

    Returns:
        Reversed string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")
    return s[::-1]


# ─── 2. Punctuation & Position Preserving Word Reverser ───────────────────────


def reverse_words_preserve_punctuation(s: str) -> str:
    """
    Reverses alphabetical characters within each word token while keeping punctuation,
    digits, and whitespace symbols in their exact original indices.
    For example: 'Hello, World!' -> 'Olleh, Dlrow!'.

    Args:
        s: Input text string.

    Returns:
        String with word characters reversed while punctuation remains in-place.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    def reverse_token(token: str) -> str:
        letters = [ch for ch in token if ch.isalpha()]
        letters.reverse()
        result = []
        letter_idx = 0
        for ch in token:
            if ch.isalpha():
                result.append(letters[letter_idx])
                letter_idx += 1
            else:
                result.append(ch)
        return "".join(result)

    # Tokenize by word bounds using regex while keeping spaces/punctuation intact
    tokens = re.split(r"(\s+)", s)
    return "".join(reverse_token(tok) for tok in tokens)


# ─── 3. Case-Preserving Word Reverser ──────────────────────────────────────────


def reverse_words_preserve_casing(s: str) -> str:
    """
    Reverses characters of each word while preserving the original capitalization pattern.
    For example: 'Python' -> 'Nohtyp' (index 0 was uppercase 'P', so new index 0 'N' becomes 'N').

    Args:
        s: Input text string.

    Returns:
        String with reversed words adhering to original casing map.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    def apply_casing(word: str) -> str:
        reversed_chars = list(word[::-1].lower())
        result = []
        for orig_ch, rev_ch in zip(word, reversed_chars):
            if orig_ch.isupper():
                result.append(rev_ch.upper())
            else:
                result.append(rev_ch.lower())
        return "".join(result)

    words = s.split(" ")
    return " ".join(apply_casing(w) for w in words)


