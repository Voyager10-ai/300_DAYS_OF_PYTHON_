# Day 48: Convert to Int
#
# Problem:
#   Write a Python program to convert a string representation of a number to an integer.
#   Includes custom atoi implementation, arbitrary base conversion (2-36), word numbers ("forty-two"),
#   Roman numerals, formatted string cleaning, collection converters, unit tests, and Java practice.

import re
import math
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core String-to-Integer Parsing (custom atoi) ─────────────────────────


def custom_atoi(s: str) -> int:
    """
    Parses a string into an integer manually without using built-in int() for digit parsing.
    Handles leading/trailing whitespace, optional '+' or '-' sign, and stops at first non-digit.

    Args:
        s: Input string representation of an integer.

    Returns:
        Converted integer value.

    Raises:
        ValueError: If s contains no valid digit sequence.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    # 1. Strip leading and trailing whitespace
    s = s.strip()
    if not s:
        raise ValueError("Cannot convert empty or whitespace-only string to int")

    # 2. Extract sign
    sign = 1
    index = 0
    if s[0] == "-":
        sign = -1
        index += 1
    elif s[0] == "+":
        index += 1

    # 3. Iterate digits and accumulate
    digit_found = False
    result = 0

    while index < len(s):
        char = s[index]
        if "0" <= char <= "9":
            digit_found = True
            digit_val = ord(char) - ord("0")
            result = result * 10 + digit_val
            index += 1
        else:
            # Stop parsing at first invalid character
            break

    if not digit_found:
        raise ValueError(f"Invalid integer string: '{s}'")

    return sign * result


def safe_str_to_int(s: Any, default: Optional[int] = None) -> Optional[int]:
    """
    Safely converts input to an integer, returning default if conversion fails.

    Args:
        s: Input value (string, float, int, etc.).
        default: Fallback value if conversion fails (default None).

    Returns:
        Converted integer or default fallback.
    """
    if s is None:
        return default
    try:
        if isinstance(s, int):
            return s
        if isinstance(s, float):
            if math.isnan(s) or math.isinf(s):
                return default
            return int(s)
        if isinstance(s, str):
            return custom_atoi(s)
        return int(s)
    except (ValueError, TypeError):
        return default


# ─── 2. Arbitrary Base Conversion (Base 2-36) & Prefix Auto-Detection ─────────


def convert_base_to_int(s: str, base: int = 10) -> int:
    """
    Converts a string representation in any base from 2 to 36 into an integer.

    Args:
        s: Input number string.
        base: Base of the input string (2 <= base <= 36).

    Returns:
        Converted base-10 integer.

    Raises:
        ValueError: If base is invalid or string contains invalid characters for base.
    """
    if not (2 <= base <= 36):
        raise ValueError(f"Base must be between 2 and 36, got {base}")

    s = s.strip()
    if not s:
        raise ValueError("Cannot convert empty string")

    sign = 1
    if s[0] == "-":
        sign = -1
        s = s[1:]
    elif s[0] == "+":
        s = s[1:]

    # Remove optional standard prefixes if base matches
    s_lower = s.lower()
    if base == 2 and s_lower.startswith("0b"):
        s = s[2:]
    elif base == 8 and s_lower.startswith("0o"):
        s = s[2:]
    elif base == 16 and s_lower.startswith("0x"):
        s = s[2:]

    if not s:
        raise ValueError("No digits after sign/prefix")

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    char_map = {digits[i]: i for i in range(base)}

    result = 0
    for char in s.lower():
        if char not in char_map:
            raise ValueError(f"Invalid character '{char}' for base {base}")
        result = result * base + char_map[char]

    return sign * result


def auto_detect_base_convert(s: str) -> Tuple[int, int]:
    """
    Auto-detects base from prefix (0b/0o/0x) and converts to base-10 integer.

    Args:
        s: Input number string.

    Returns:
        Tuple of (integer_value, detected_base).
    """
    s_clean = s.strip()
    sign = 1
    if s_clean.startswith("-"):
        sign = -1
        raw = s_clean[1:]
    elif s_clean.startswith("+"):
        raw = s_clean[1:]
    else:
        raw = s_clean

    raw_lower = raw.lower()
    if raw_lower.startswith("0b"):
        base = 2
    elif raw_lower.startswith("0o"):
        base = 8
    elif raw_lower.startswith("0x"):
        base = 16
    else:
        base = 10

    val = convert_base_to_int(s_clean, base=base)
    return (val, base)

