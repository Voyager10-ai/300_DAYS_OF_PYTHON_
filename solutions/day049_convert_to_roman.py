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


# ─── 2. Additive Roman Numeral Variant ─────────────────────────────────────────


ADDITIVE_ROMAN_TABLE: List[Tuple[int, str]] = [
    (1000, "M"),
    (500, "D"),
    (100, "C"),
    (50, "L"),
    (10, "X"),
    (5, "V"),
    (1, "I"),
]


def int_to_roman_additive(num: int) -> str:
    """
    Converts an integer to an additive Roman numeral string (without subtractive pairs like IV or IX).
    For example: 4 -> 'IIII', 9 -> 'VIIII', 40 -> 'XXXX'.

    Args:
        num: Integer between 1 and 3999.

    Returns:
        Additive Roman numeral string.

    Raises:
        ValueError: If num is outside range 1 to 3999.
    """
    if not isinstance(num, int) or isinstance(num, bool):
        raise TypeError(f"Expected integer input, got {type(num).__name__}")

    if not (1 <= num <= 3999):
        raise ValueError(f"Additive Roman conversion requires 1 <= num <= 3999, got {num}")

    result: List[str] = []
    remaining = num

    for val, symbol in ADDITIVE_ROMAN_TABLE:
        count = remaining // val
        if count > 0:
            result.append(symbol * count)
            remaining %= val

    return "".join(result)


# ─── 3. Extended Roman Numerals for Large Numbers (up to 1,000,000) ───────────


EXTENDED_ROMAN_TABLE: List[Tuple[int, str]] = [
    (1000000, "(M)"),
    (900000, "(CM)"),
    (500000, "(D)"),
    (400000, "(CD)"),
    (100000, "(C)"),
    (90000, "(XC)"),
    (50000, "(L)"),
    (40000, "(XL)"),
    (10000, "(X)"),
    (9000, "(IX)"),
    (5000, "(V)"),
    (4000, "(IV)"),
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


def int_to_extended_roman(num: int) -> str:
    """
    Converts numbers up to 1,000,000 to Extended Roman numerals using bracket Vinculum notation.
    For example: 5000 -> '(V)', 10500 -> '(X)D', 1000000 -> '(M)'.

    Args:
        num: Integer between 1 and 1,000,000.

    Returns:
        Extended Roman numeral string.

    Raises:
        ValueError: If num is outside range 1 to 1,000,000.
    """
    if not isinstance(num, int) or isinstance(num, bool):
        raise TypeError(f"Expected integer input, got {type(num).__name__}")

    if not (1 <= num <= 1000000):
        raise ValueError(f"Extended Roman conversion requires 1 <= num <= 1,000,000, got {num}")

    result: List[str] = []
    remaining = num

    for val, symbol in EXTENDED_ROMAN_TABLE:
        while remaining >= val:
            result.append(symbol)
            remaining -= val

    return "".join(result)


# ─── 4. Roman Numeral Validator & Round-Trip Verifier ─────────────────────────


ROMAN_PARSER_VALUES: Dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def is_valid_roman(s: str) -> bool:
    """
    Validates if a string is a syntactically correct standard Roman numeral (1 to 3999).

    Args:
        s: Input string.

    Returns:
        True if valid standard Roman numeral, False otherwise.
    """
    if not isinstance(s, str):
        return False
    clean_s = s.strip().upper()
    pattern = r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    return bool(re.match(pattern, clean_s)) and len(clean_s) > 0


def roman_to_int(s: str) -> int:
    """
    Converts a standard Roman numeral string to integer (1 to 3999).

    Args:
        s: Roman numeral string.

    Returns:
        Converted integer.

    Raises:
        ValueError: If string is invalid.
    """
    if not is_valid_roman(s):
        raise ValueError(f"Invalid Roman numeral string: '{s}'")

    clean_s = s.strip().upper()
    total = 0
    prev_val = 0

    for char in reversed(clean_s):
        val = ROMAN_PARSER_VALUES[char]
        if val < prev_val:
            total -= val
        else:
            total += val
            prev_val = val

    return total


def round_trip_verify(num: int) -> bool:
    """
    Verifies that converting num to Roman and back to integer yields the original number.

    Args:
        num: Integer (1 to 3999).

    Returns:
        True if round-trip conversion is loss-less and accurate.
    """
    try:
        roman_str = int_to_roman(num)
        reconstructed = roman_to_int(roman_str)
        return reconstructed == num
    except Exception:
        return False


# ─── 5. Roman Numeral Arithmetic Operations ───────────────────────────────────


def roman_add(r1: str, r2: str) -> str:
    """
    Adds two Roman numeral strings and returns the result as a Roman numeral.

    Args:
        r1: First Roman numeral.
        r2: Second Roman numeral.

    Returns:
        Sum represented as a Roman numeral string.
    """
    v1 = roman_to_int(r1)
    v2 = roman_to_int(r2)
    return int_to_roman(v1 + v2)


def roman_subtract(r1: str, r2: str) -> str:
    """
    Subtracts second Roman numeral from the first (r1 - r2).

    Args:
        r1: Minuend Roman numeral.
        r2: Subtrahend Roman numeral.

    Returns:
        Difference represented as a Roman numeral string.

    Raises:
        ValueError: If difference <= 0 (Roman numerals have no zero or negative values).
    """
    v1 = roman_to_int(r1)
    v2 = roman_to_int(r2)
    diff = v1 - v2
    if diff <= 0:
        raise ValueError(f"Roman arithmetic subtraction resulted in non-positive value ({diff})")
    return int_to_roman(diff)


def roman_multiply(r1: str, r2: str) -> str:
    """
    Multiplies two Roman numeral strings (r1 * r2).

    Args:
        r1: First Roman numeral.
        r2: Second Roman numeral.

    Returns:
        Product represented as a Roman numeral string.
    """
    v1 = roman_to_int(r1)
    v2 = roman_to_int(r2)
    product = v1 * v2
    if product > 3999:
        return int_to_extended_roman(product)
    return int_to_roman(product)




