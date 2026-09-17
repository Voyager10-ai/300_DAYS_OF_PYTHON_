# Day 65: Check String
#
# Problem:
#   Write a Python program / module to check various properties of a given string.
#   Includes core classification (alphanumeric, numeric, alpha, custom charsets), substring/prefix/suffix matching,
#   pattern validations (identifiers, hex color, email, IPv4), comprehensive string analysis metrics,
#   custom multi-condition rule validation, string sanitization/normalization, unit test suite, and Java practice.

import re
import string
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Classification & Character Set Checkers ─────────────────────────


def is_alphanumeric_str(s: str) -> bool:
    """
    Checks if non-empty string contains only alphanumeric characters (letters and digits).

    Args:
        s: Input string to check.

    Returns:
        True if s is non-empty and all characters are alphanumeric, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    return len(s) > 0 and s.isalnum()


def is_numeric_str(s: str, allow_negative: bool = False, allow_decimal: bool = False) -> bool:
    """
    Checks if string represents a valid integer or float numeric value.

    Args:
        s: Input string to check.
        allow_negative: If True, permits leading '-' or '+' sign.
        allow_decimal: If True, permits single decimal point '.'.

    Returns:
        True if s matches the numeric constraints, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    if not s:
        return False

    pattern = r"^"
    if allow_negative:
        pattern += r"[+-]?"
    if allow_decimal:
        pattern += r"\d+(\.\d+)?"
    else:
        pattern += r"\d+"
    pattern += r"$"

    return bool(re.match(pattern, s))


def is_alpha_str(s: str, allow_spaces: bool = False) -> bool:
    """
    Checks if string contains only alphabetic letters (a-z, A-Z), optionally allowing spaces.

    Args:
        s: Input string to check.
        allow_spaces: If True, space characters are permitted.

    Returns:
        True if s is non-empty and contains only letters (and spaces if allowed), else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    if not s:
        return False
    if allow_spaces:
        return bool(re.match(r"^[a-zA-Z\s]+$", s))
    return s.isalpha()


def contains_only_chars(s: str, allowed_chars: Union[str, Set[str], List[str]]) -> bool:
    """
    Checks if string consists solely of characters in allowed_chars set.

    Args:
        s: Input string to check.
        allowed_chars: String, set, or list of permitted characters.

    Returns:
        True if s is non-empty and every char in s is in allowed_chars, else False.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string for s, got {type(s).__name__}")
    if not s:
        return False

    allowed_set = set(allowed_chars)
    return all(char in allowed_set for char in s)


# ─── 2. Substring, Prefix & Suffix Matching Utilities ─────────────────────────


def check_substring(text: str, sub: str, case_sensitive: bool = True) -> bool:
    """
    Checks whether substring sub is present in text.

    Args:
        text: Main text string to search within.
        sub: Substring to search for.
        case_sensitive: If False, performs case-insensitive matching.

    Returns:
        True if sub is found in text, else False.

    Raises:
        TypeError: If text or sub is not a string.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("Both text and sub must be strings.")
    if not sub:
        return True

    if not case_sensitive:
        return sub.lower() in text.lower()
    return sub in text


def check_prefix_suffix(
    text: str,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    case_sensitive: bool = True,
) -> bool:
    """
    Checks if text starts with prefix and/or ends with suffix.

    Args:
        text: Main string to check.
        prefix: Required starting substring (or None to skip).
        suffix: Required ending substring (or None to skip).
        case_sensitive: If False, ignores letter case.

    Returns:
        True if text satisfies both prefix and suffix constraints (if provided), else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")

    t = text if case_sensitive else text.lower()

    if prefix is not None:
        p = prefix if case_sensitive else prefix.lower()
        if not t.startswith(p):
            return False

    if suffix is not None:
        s = suffix if case_sensitive else suffix.lower()
        if not t.endswith(s):
            return False

    return True


def count_substring_occurrences(text: str, sub: str, allow_overlap: bool = False) -> int:
    """
    Counts occurrences of sub within text.

    Args:
        text: Source string to search.
        sub: Pattern substring to count.
        allow_overlap: If True, counts overlapping occurrences.

    Returns:
        Number of matching occurrences.

    Raises:
        TypeError: If inputs are not strings.
        ValueError: If sub is an empty string.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("Both text and sub must be strings.")
    if not sub:
        raise ValueError("Search substring 'sub' cannot be empty.")

    if not allow_overlap:
        return text.count(sub)

    count = 0
    start = 0
    while True:
        pos = text.find(sub, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1
    return count

