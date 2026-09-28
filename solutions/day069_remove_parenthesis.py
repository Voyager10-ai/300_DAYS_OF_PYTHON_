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


# ─── 2. Multi-Bracket Remover & Content Extractor ────────────────────────────

BRACKET_PAIRS = {
    "()": (r"\(", r"\)"),
    "[]": (r"\[", r"\]"),
    "{}": (r"\{", r"\}"),
    "<>": (r"<", r">"),
}


def remove_custom_brackets(
    text: str,
    brackets: Optional[List[str]] = None,
    remove_contents: bool = True,
) -> str:
    """
    Strips specified bracket types e.g. '()', '[]', '{}', '<>' and optionally their contents.

    Args:
        text: Input string.
        brackets: List of bracket pair strings e.g. ['()', '[]']. Defaults to all.
        remove_contents: If True, removes text enclosed inside brackets.

    Returns:
        Cleaned output string.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If invalid bracket type provided.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text:
        return ""

    target_brackets = brackets or ["()", "[]", "{}", "<>"]
    result = text

    for b in target_brackets:
        if b not in BRACKET_PAIRS:
            raise ValueError(f"Unsupported bracket pair '{b}'. Choose from '()', '[]', '{{}}', '<>'.")
        open_b, close_b = BRACKET_PAIRS[b]

        if remove_contents:
            pattern = f"{open_b}[^{open_b}{close_b}]*{close_b}"
            while re.search(pattern, result):
                result = re.sub(pattern, "", result)
        else:
            raw_open, raw_close = b[0], b[1]
            result = result.replace(raw_open, "").replace(raw_close, "")

    return re.sub(r" +", " ", result).strip()


def extract_parenthetical_contents(text: str) -> List[str]:
    """
    Extracts all substrings enclosed inside parentheses.

    Args:
        text: Source text string.

    Returns:
        List of extracted string contents.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if not text:
        return []

    return re.findall(r"\(([^()]*)\)", text)

