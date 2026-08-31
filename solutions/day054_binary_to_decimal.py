# Day 54: Binary to Decimal
#
# Problem:
#   Write a Python program / module to convert a binary string to a decimal integer.
#   Includes manual positional powers, fractional float binary conversion, two's complement,
#   reverse decimal to binary, bitwise binary operations, base conversion (2-36), bit buffer stream, unit tests, and Java practice.

import re
import math
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Binary to Decimal Conversion ──────────────────────────────────────


def binary_to_decimal(binary_str: str) -> int:
    """
    Converts a binary string (e.g., '1010') to a decimal integer using positional powers of 2.

    Args:
        binary_str: Binary string containing only '0' and '1' digits (with optional '0b' prefix).

    Returns:
        Decimal integer value.

    Raises:
        TypeError: If input is not a string.
        ValueError: If input contains invalid non-binary characters or is empty.
    """
    if not isinstance(binary_str, str):
        raise TypeError(f"Expected string input, got {type(binary_str).__name__}")

    clean_str = binary_str.strip().lower()
    if clean_str.startswith("0b"):
        clean_str = clean_str[2:]

    if not clean_str:
        raise ValueError("Binary string cannot be empty")

    if not all(char in "01" for char in clean_str):
        raise ValueError(f"Invalid binary string '{binary_str}': contains non-binary characters")

    # Manual positional power calculation: sum(digit * 2^(length - 1 - i))
    decimal_val = 0
    length = len(clean_str)
    for i, char in enumerate(clean_str):
        bit = int(char)
        power = length - 1 - i
        decimal_val += bit * (2 ** power)

    return decimal_val


def safe_binary_to_decimal(binary_str: str, default: int = 0) -> int:
    """
    Safely converts a binary string to decimal integer, returning a default fallback on error.

    Args:
        binary_str: Binary string.
        default: Fallback value if conversion fails.

    Returns:
        Converted integer or default fallback.
    """
    try:
        return binary_to_decimal(binary_str)
    except (ValueError, TypeError):
        return default


# ─── 2. Fractional Floating-Point Binary to Decimal Converter ─────────────────


def binary_float_to_decimal(binary_str: str) -> float:
    """
    Converts a floating-point binary string (e.g. '101.101') to its decimal float equivalent (e.g. 5.625).
    Evaluates fractional bits using negative powers of 2 (2^-1, 2^-2, 2^-3, ...).

    Args:
        binary_str: Binary string with optional radix point '.'.

    Returns:
        Converted decimal float value.

    Raises:
        ValueError: If input is invalid.
    """
    if not isinstance(binary_str, str):
        raise TypeError(f"Expected string input, got {type(binary_str).__name__}")

    clean_str = binary_str.strip().lower()
    if clean_str.startswith("0b"):
        clean_str = clean_str[2:]

    parts = clean_str.split(".")
    if len(parts) > 2:
        raise ValueError(f"Invalid binary float string '{binary_str}': multiple radix points found")

    int_part_str = parts[0] if parts[0] else "0"
    frac_part_str = parts[1] if len(parts) == 2 else ""

    int_val = binary_to_decimal(int_part_str)

    frac_val = 0.0
    if frac_part_str:
        if not all(char in "01" for char in frac_part_str):
            raise ValueError(f"Invalid fractional binary string '{frac_part_str}'")

        for i, char in enumerate(frac_part_str, start=1):
            if char == "1":
                frac_val += 2.0 ** (-i)

    return int_val + frac_val

