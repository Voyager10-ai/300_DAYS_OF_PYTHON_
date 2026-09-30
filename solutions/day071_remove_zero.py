# Day 71: Remove Zero
#
# Problem:
#   Write a Python program / module to strip, trim, replace, and analyze zero characters and zero values.
#   Includes core removal (leading, trailing, all zeros), numeric zero stripping, float normalization,
#   alignment/padding helpers, zero distribution analysis, collection sanitizers, zero masking/replacement,
#   unit test suite, and Java practice code.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Zero Removal Utilities ──────────────────────────────────────────


def remove_all_zeros(val: Union[str, int, float, List]) -> str:
    """
    Removes all '0' characters from a string representation of a value or list element.

    Args:
        val: Input value (string, int, float, or sequence).

    Returns:
        String with all zero characters removed.

    Raises:
        TypeError: If input cannot be converted to a string representation cleanly.
    """
    if val is None:
        raise TypeError("Input value cannot be None.")
    
    text = str(val)
    return text.replace("0", "")


def remove_leading_zeros(val: str, keep_single_zero: bool = False) -> str:
    """
    Removes leading zeros from a string representation of numbers or text.

    Args:
        val: Input string.
        keep_single_zero: If True and the string consists solely of zeros, retains a single '0'.

    Returns:
        String stripped of leading zeros.

    Raises:
        TypeError: If val is not a string.
    """
    if not isinstance(val, str):
        raise TypeError(f"Expected str for val, got {type(val).__name__}")
    if not val:
        return ""

    stripped = val.lstrip("0")
    if keep_single_zero and not stripped and "0" in val:
        return "0"
    return stripped


def remove_trailing_zeros(val: str) -> str:
    """
    Removes trailing zeros from a string representation.

    Args:
        val: Input string.

    Returns:
        String stripped of trailing zeros.

    Raises:
        TypeError: If val is not a string.
    """
    if not isinstance(val, str):
        raise TypeError(f"Expected str for val, got {type(val).__name__}")
    return val.rstrip("0")


# ─── 2. Numeric Zero Stripping & Float Format Normalizers ────────────────────


def strip_decimal_zeros(val: Union[str, float, int]) -> str:
    """
    Strips redundant trailing zeros after a decimal point, converting numbers like '12.3400' to '12.34' and '5.00' to '5'.

    Args:
        val: Input string, float, or integer.

    Returns:
        Cleaned numeric string without trailing fractional zeros.

    Raises:
        TypeError: If input is None.
    """
    if val is None:
        raise TypeError("Input value cannot be None.")

    text = str(val).strip()
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def normalize_numeric_zeros(val: str) -> str:
    """
    Normalizes a numeric string by removing excess leading/trailing zeros, preserving sign (+/-).

    Examples:
        "-00042.500" -> "-42.5"
        "+000.050"   -> "0.05"
        "0000"       -> "0"

    Args:
        val: Numeric string input.

    Returns:
        Normalized numeric string.

    Raises:
        TypeError: If val is not a string.
        ValueError: If val is not a valid representation of a number.
    """
    if not isinstance(val, str):
        raise TypeError(f"Expected str for val, got {type(val).__name__}")

    s = val.strip()
    if not s:
        raise ValueError("Input numeric string cannot be empty.")

    sign = ""
    if s[0] in ("+", "-"):
        sign = "-" if s[0] == "-" else ""
        s = s[1:]

    if not s or not re.match(r"^\d*\.?\d*$", s) or s == ".":
        raise ValueError(f"Invalid numeric string format: '{val}'")

    if "." in s:
        integer_part, decimal_part = s.split(".", 1)
        integer_part = integer_part.lstrip("0") or "0"
        decimal_part = decimal_part.rstrip("0")
        if decimal_part:
            res = f"{integer_part}.{decimal_part}"
        else:
            res = integer_part
    else:
        res = s.lstrip("0") or "0"

    if res == "0":
        return "0"

    return f"{sign}{res}"


# ─── 3. Non-Zero Padding & Alignment Helpers ─────────────────────────────────


def pad_non_zeros(text: str, length: int, fillchar: str = " ") -> str:
    """
    Removes leading zeros from a string and pads the result on the left with fillchar.

    Args:
        text: Input string.
        length: Target total width.
        fillchar: Character used for padding (default is space).

    Returns:
        Padded string after stripping leading zeros.

    Raises:
        TypeError: If text is not a string or fillchar length != 1.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str for text, got {type(text).__name__}")
    if not isinstance(fillchar, str) or len(fillchar) != 1:
        raise TypeError("fillchar must be a single character string.")

    unpadded = text.lstrip("0")
    return unpadded.rjust(length, fillchar)


def align_numeric_string(val: str, min_digits: int = 1) -> str:
    """
    Ensures a numeric string has leading zeros removed, but guarantees at least min_digits.

    Args:
        val: Numeric input string.
        min_digits: Minimum required integer digits (default 1).

    Returns:
        Formatted numeric string with exact minimum leading zero padding.

    Raises:
        TypeError: If input is not a string.
        ValueError: If min_digits < 1.
    """
    if not isinstance(val, str):
        raise TypeError(f"Expected str for val, got {type(val).__name__}")
    if min_digits < 1:
        raise ValueError("min_digits must be at least 1.")

    normalized = normalize_numeric_zeros(val)
    parts = normalized.split(".", 1)
    integer_part = parts[0]
    
    # Handle negative sign if present
    is_neg = integer_part.startswith("-")
    if is_neg:
        integer_part = integer_part[1:]
        
    padded_int = integer_part.zfill(min_digits)
    if is_neg:
        padded_int = f"-{padded_int}"

    if len(parts) > 1:
        return f"{padded_int}.{parts[1]}"
    return padded_int


