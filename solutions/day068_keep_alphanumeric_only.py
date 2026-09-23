# Day 68: Keep Alphanumeric Only
#
# Problem:
#   Write a Python program / module to strip non-alphanumeric characters from text inputs.
#   Includes core filtering, custom extra character retention, ASCII vs Unicode modes,
#   character removal breakdown analysis, batch list/dict sanitization, URL slugification,
#   unit test suite, and Java practice.

import re
import string
import unicodedata
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Alphanumeric Filtering Functions ─────────────────────────────────


def keep_alphanumeric_only(text: str, keep_spaces: bool = False) -> str:
    """
    Strips all non-alphanumeric characters (punctuation, symbols, emojis) from a string.

    Args:
        text: Target text string to filter.
        keep_spaces: If True, whitespace characters (spaces, tabs) are preserved.

    Returns:
        Filtered string containing only alphanumeric characters (and spaces if enabled).

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text:
        return ""

    if keep_spaces:
        return re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    return re.sub(r"[^\w]", "", text, flags=re.UNICODE).replace("_", "")


def is_pure_alphanumeric(text: str) -> bool:
    """
    Checks if a string consists strictly of alphanumeric characters without symbols or spaces.

    Args:
        text: Target text string.

    Returns:
        True if text is non-empty and contains only letters and digits, else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    return len(text) > 0 and text.isalnum()


# ─── 2. Custom Character Retention & Word Extraction ──────────────────────────


def sanitize_alphanumeric_custom(
    text: str,
    preserve_case: bool = True,
    allowed_extra_chars: Optional[str] = None,
) -> str:
    """
    Filters text to alphanumeric characters while permitting specified custom extra characters.

    Args:
        text: Target text string.
        preserve_case: If False, converts output to lowercase.
        allowed_extra_chars: String of extra allowed non-alphanumeric chars e.g. " -_@".

    Returns:
        Filtered string containing alphanumeric plus allowed extra characters.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")

    extra = allowed_extra_chars or ""
    escaped_extra = re.escape(extra)
    pattern = f"[^a-zA-Z0-9{escaped_extra}]"

    res = re.sub(pattern, "", text)
    return res if preserve_case else res.lower()


def extract_alphanumeric_words(text: str) -> List[str]:
    """
    Extracts words containing strictly alphanumeric characters from a body of text.

    Args:
        text: Source text paragraph.

    Returns:
        List of alphanumeric word strings.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if not text.strip():
        return []

    tokens = text.split()
    words = []

    for token in tokens:
        cleaned = re.sub(r"[^\w]", "", token).replace("_", "")
        if cleaned:
            words.append(cleaned)

    return words

