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
