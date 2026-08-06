# Day 32: Reverse Word in String
#
# Problem:
#   Write a Python program to reverse the words in a given string, sentence, or text block.
#   - Reverse Word Order: Reverses the sequence of words in a sentence.
#   - Reverse Each Word: Reverses the characters within each word while maintaining word order.

import re
import string
import sys
import io
from typing import List, Dict, Tuple, Optional, Any, Callable


def reverse_words(text: str) -> str:
    """
    Reverses the sequence of words in a given string.

    Args:
        text: Input sentence or paragraph.

    Returns:
        String with words in reverse order, joined by single spaces.

    Time Complexity: O(N) where N is string length.
    Space Complexity: O(N) for storing word tokens.

    Example:
        reverse_words("the sky is blue") -> "blue is sky"
        reverse_words("  hello world  ") -> "world hello"
    """
    if not text:
        return ""
    words = text.strip().split()
    return " ".join(reversed(words))


def reverse_each_word(text: str) -> str:
    """
    Reverses the characters of each word in a string while preserving original word placement.

    Args:
        text: Input string.

    Returns:
        String with every individual word character-reversed.

    Time Complexity: O(N) where N is string length.
    Space Complexity: O(N) for word token storage.

    Example:
        reverse_each_word("hello world") -> "olleh dlrow"
        reverse_each_word("Python Programming") -> "nohtyP gnimmargorP"
    """
    if not text:
        return ""
    words = text.split()
    reversed_words = [w[::-1] for w in words]
    return " ".join(reversed_words)
