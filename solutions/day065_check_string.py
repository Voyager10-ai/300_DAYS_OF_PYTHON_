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
