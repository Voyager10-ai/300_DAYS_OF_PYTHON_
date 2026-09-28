# Day 69: Remove Parenthesis
#
# Problem:
#   Write a Python program / module to strip or extract parentheses and enclosed text from strings.
#   Includes core removal, multi-bracket support ((), [], {}, <>), nested stack-based parsers,
#   expression simplifiers, structure analysis metrics, collection batch cleaners,
#   redaction masking, unit test suite, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Parenthesis Removal & Content Stripping ─────────────────────────


def remove_parentheses(text: str, remove_contents: bool = True) -> str:
    """
    Removes parentheses '()' from a string, optionally stripping the enclosed contents.

    Args:
        text: Target text string.
        remove_contents: If True, removes text inside parentheses e.g. "Hello (world)" -> "Hello ".
                         If False, removes only the parenthesis characters '(' and ')'.

    Returns:
        Cleaned string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text:
        return ""

    if remove_contents:
        # Regex to strip non-nested parentheses and their contents, repeated for simple multi-pair
        result = text
        while re.search(r"\([^()]*\)", result):
            result = re.sub(r"\([^()]*\)", "", result)
        # Collapse multiple spaces leftover into single space if needed
        return re.sub(r" +", " ", result).strip()

    return text.replace("(", "").replace(")", "")


def has_parentheses(text: str) -> bool:
    """
    Checks if a string contains any parenthesis characters '(' or ')'.

    Args:
        text: Target text string.

    Returns:
        True if text contains '(' or ')', else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    return "(" in text or ")" in text
