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
