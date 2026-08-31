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


# ─── 3. Two's Complement Signed Binary Converter ───────────────────────────────


def twos_complement_to_decimal(binary_str: str, bits: Optional[int] = None) -> int:
    """
    Converts a Two's Complement signed binary string to a signed decimal integer.
    If MSB (most significant bit) is 1, returns negative integer value.

    Args:
        binary_str: Signed binary string (e.g. '11111111' -> -1 for 8 bits).
        bits: Explicit bit width (defaults to len(binary_str)).

    Returns:
        Signed decimal integer.
    """
    val = binary_to_decimal(binary_str)
    num_bits = bits if bits is not None else len(binary_str.strip().lower().replace("0b", ""))

    if val & (1 << (num_bits - 1)):
        val -= 1 << num_bits
    return val


def decimal_to_twos_complement(val: int, bits: int = 8) -> str:
    """
    Converts a signed decimal integer to its N-bit Two's Complement binary string representation.

    Args:
        val: Signed integer.
        bits: Bit width integer (e.g. 8, 16, 32).

    Returns:
        N-bit binary string.

    Raises:
        ValueError: If val is out of bounds for the given bit width.
    """
    min_val = -(1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1
    if not (min_val <= val <= max_val):
        raise ValueError(f"Value {val} out of bounds for {bits}-bit Two's Complement [{min_val}, {max_val}]")

    if val < 0:
        val = (1 << bits) + val

    return format(val, f"0{bits}b")


# ─── 4. Reverse Decimal to Binary Converters ───────────────────────────────────


def decimal_to_binary(n: int, min_bits: Optional[int] = None, prefix: bool = False) -> str:
    """
    Converts a non-negative decimal integer to binary string.

    Args:
        n: Non-negative integer.
        min_bits: Minimum padded bit length.
        prefix: If True, includes '0b' prefix.

    Returns:
        Binary string.

    Raises:
        ValueError: If n < 0.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"Expected integer input, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"decimal_to_binary expects non-negative integer, got {n}")

    bin_str = bin(n)[2:]
    if min_bits is not None and len(bin_str) < min_bits:
        bin_str = bin_str.zfill(min_bits)

    return f"0b{bin_str}" if prefix else bin_str


def decimal_float_to_binary(val: float, precision: int = 8) -> str:
    """
    Converts a decimal float to a binary string representation with specified fractional precision.
    For example: 5.625 -> '101.101'.

    Args:
        val: Non-negative float value.
        precision: Maximum number of fractional binary digits.

    Returns:
        Binary float string.
    """
    if val < 0:
        raise ValueError("Non-negative float required")

    int_part = int(val)
    frac_part = val - int_part

    int_bin = decimal_to_binary(int_part)
    if frac_part == 0:
        return int_bin

    frac_bits = []
    curr = frac_part
    for _ in range(precision):
        if curr == 0:
            break
        curr *= 2
        bit = int(curr)
        frac_bits.append(str(bit))
        curr -= bit

    return f"{int_bin}.{''.join(frac_bits)}"



