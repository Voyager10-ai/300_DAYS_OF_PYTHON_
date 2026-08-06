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


def reverse_words_custom_delimiter(text: str, delimiter: str = ",") -> str:
    """
    Reverses sequence of tokens delimited by a custom separator string.

    Args:
        text: Input string with custom delimiters.
        delimiter: Separator string between tokens.

    Returns:
        Delimited string with token order reversed.
    """
    if not text:
        return ""
    tokens = [t.strip() for t in text.split(delimiter)]
    return delimiter.join(reversed(tokens))


def reverse_words_preserve_whitespace(text: str) -> str:
    """
    Reverses word sequence while keeping original spacing/whitespace layout intact.

    Args:
        text: Input text containing spaces, tabs, or newlines.

    Returns:
        Reversed word order string matching identical whitespace slot locations.
    """
    if not text:
        return ""
    # Extract words and whitespace gaps using regex split
    tokens = re.split(r'(\s+)', text)
    words = [t for t in tokens if not t.isspace() and t != '']
    reversed_words = list(reversed(words))

    result = []
    word_idx = 0
    for t in tokens:
        if t == '':
            continue
        if t.isspace():
            result.append(t)
        else:
            result.append(reversed_words[word_idx])
            word_idx += 1
    return "".join(result)


def reverse_each_word_preserve_case(text: str) -> str:
    """
    Reverses characters of each word while maintaining capital letter positions.

    Args:
        text: Input string.

    Returns:
        Character-reversed string with original casing template preserved.

    Example:
        reverse_each_word_preserve_case("Hello World") -> "Olleh Dlrow"
    """
    def transform_word(w: str) -> str:
        casing_mask = [c.isupper() for c in w]
        raw_reversed = list(w[::-1].lower())
        for i, is_upper in enumerate(casing_mask):
            if is_upper:
                raw_reversed[i] = raw_reversed[i].upper()
        return "".join(raw_reversed)

    if not text:
        return ""
    words = text.split()
    return " ".join(transform_word(w) for w in words)

