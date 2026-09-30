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
