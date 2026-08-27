# Day 49: Convert to Roman
#
# Problem:
#   Write a Python program to convert an integer to a Roman numeral.
#   Includes standard subtractive notation (1-3999), additive notation (IIII),
#   extended Roman notation for large numbers, bidirectional validation/round-trip,
#   Roman arithmetic operations, text extractions, unit tests, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Integer to Roman Numeral Conversion ──────────────────────────────


ROMAN_NUMERAL_TABLE: List[Tuple[int, str]] = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def int_to_roman(num: int) -> str:
    """
    Converts an integer (1 to 3999) to a standard subtractive Roman numeral string.

    Args:
        num: Integer between 1 and 3999.

    Returns:
        Roman numeral string representation (e.g. 1994 -> 'MCMXCIV').

    Raises:
        TypeError: If num is not an integer.
        ValueError: If num is outside the valid range 1 <= num <= 3999.
    """
    if not isinstance(num, int) or isinstance(num, bool):
        raise TypeError(f"Expected integer input, got {type(num).__name__}")

    if not (1 <= num <= 3999):
        raise ValueError(f"Standard Roman numeral conversion requires 1 <= num <= 3999, got {num}")

    result: List[str] = []
    remaining = num

    for val, symbol in ROMAN_NUMERAL_TABLE:
        while remaining >= val:
            result.append(symbol)
            remaining -= val

    return "".join(result)
