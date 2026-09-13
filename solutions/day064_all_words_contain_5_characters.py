# Day 64: All Words Contain 5 Characters
#
# Problem:
#   Write a Python program / module to check if all words in a given string or list contain exactly 5 characters.
#   Includes robust word tokenization, punctuation removal, length filtering, comprehensive analysis metrics,
#   5-letter word validation, custom length range constraints, unit tests, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Tokenization & Length Verification ──────────────────────────────


def tokenize_words(text: str, remove_punct: bool = True) -> List[str]:
    """
    Extracts words from a string input.

    Args:
        text: Input string to tokenize.
        remove_punct: If True, strips punctuation around words.

    Returns:
        List of extracted word strings.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")

    if not text.strip():
        return []

    if remove_punct:
        # Match sequences of word characters (alphanumeric + underscore)
        words = re.findall(r"\b\w+\b", text)
    else:
        words = text.strip().split()

    return words


def all_words_have_length(
    text_or_list: Union[str, List[str]],
    target_length: int = 5,
    clean_punctuation: bool = True,
) -> bool:
    """
    Checks if all words in a string or list have exactly target_length characters.

    Args:
        text_or_list: A string sentence or list of word strings.
        target_length: Required length for all words (default: 5).
        clean_punctuation: If True, strips punctuation from string input words.

    Returns:
        True if input is non-empty and ALL words have length == target_length, else False.

    Raises:
        TypeError: If input is invalid type or target_length is not an int.
        ValueError: If target_length < 1.
    """
    if not isinstance(target_length, int) or isinstance(target_length, bool):
        raise TypeError(f"target_length must be an integer, got {type(target_length).__name__}")
    if target_length < 1:
        raise ValueError(f"target_length must be positive, got {target_length}")

    if isinstance(text_or_list, str):
        words = tokenize_words(text_or_list, remove_punct=clean_punctuation)
    elif isinstance(text_or_list, list):
        words = text_or_list
    else:
        raise TypeError(f"Expected str or list of str, got {type(text_or_list).__name__}")

    if not words:
        return False

    for word in words:
        if not isinstance(word, str):
            raise TypeError(f"All list elements must be strings, got {type(word).__name__}")
        w = word.strip()
        if clean_punctuation and isinstance(text_or_list, list):
            w = re.sub(r"^\W+|\W+$", "", w)
        if len(w) != target_length:
            return False

    return True
