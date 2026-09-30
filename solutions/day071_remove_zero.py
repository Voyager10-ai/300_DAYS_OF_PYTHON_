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


# ─── 4. Zero Occurrence Analyzer & Distribution Metrics Engine ───────────────


def analyze_zero_distribution(text: str) -> Dict[str, Any]:
    """
    Analyzes zero frequency, positioning (leading, trailing, interior), and percentages in text.

    Args:
        text: Input target string.

    Returns:
        Dictionary containing metric counts and distribution figures.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str for text, got {type(text).__name__}")

    total_chars = len(text)
    if total_chars == 0:
        return {
            "total_chars": 0,
            "zero_count": 0,
            "zero_percentage": 0.0,
            "leading_zero_count": 0,
            "trailing_zero_count": 0,
            "interior_zero_count": 0,
            "cleaned_text": "",
        }

    zero_count = text.count("0")
    zero_percentage = round((zero_count / total_chars) * 100, 2)

    # Calculate leading zeros
    leading_zero_count = 0
    for char in text:
        if char == "0":
            leading_zero_count += 1
        else:
            break

    # Calculate trailing zeros
    trailing_zero_count = 0
    for char in reversed(text):
        if char == "0":
            trailing_zero_count += 1
        else:
            break

    # Handle edge case where entire string is zeros
    if leading_zero_count == total_chars:
        interior_zero_count = 0
        trailing_zero_count = 0
    else:
        interior_zero_count = max(0, zero_count - leading_zero_count - trailing_zero_count)

    return {
        "total_chars": total_chars,
        "zero_count": zero_count,
        "zero_percentage": zero_percentage,
        "leading_zero_count": leading_zero_count,
        "trailing_zero_count": trailing_zero_count,
        "interior_zero_count": interior_zero_count,
        "cleaned_text": text.replace("0", ""),
    }


# ─── 5. Collection Zero Sanitizers ───────────────────────────────────────────


def sanitize_zeros_from_collection(data: Any, mode: str = "all") -> Any:
    """
    Recursively strips or removes zeros from data collections (lists, tuples, dicts, sets, strings).

    Args:
        data: Collection or item to sanitize.
        mode: Trimming mode applied to string elements ('all', 'leading', 'trailing').

    Returns:
        Sanitized collection of the same structure.

    Raises:
        ValueError: If mode is invalid.
    """
    m = mode.lower().strip()
    if m not in ("all", "leading", "trailing"):
        raise ValueError(f"Invalid mode '{mode}'. Choose from 'all', 'leading', 'trailing'.")

    if isinstance(data, str):
        if m == "all":
            return data.replace("0", "")
        elif m == "leading":
            return data.lstrip("0")
        elif m == "trailing":
            return data.rstrip("0")
    elif isinstance(data, (int, float)):
        if data == 0:
            return None
        return data
    elif isinstance(data, list):
        cleaned = [sanitize_zeros_from_collection(item, mode=mode) for item in data]
        return [item for item in cleaned if item is not None and item != ""]
    elif isinstance(data, tuple):
        cleaned = [sanitize_zeros_from_collection(item, mode=mode) for item in data]
        return tuple(item for item in cleaned if item is not None and item != "")
    elif isinstance(data, set):
        cleaned = {sanitize_zeros_from_collection(item, mode=mode) for item in data}
        return {item for item in cleaned if item is not None and item != ""}
    elif isinstance(data, dict):
        res = {}
        for k, v in data.items():
            cleaned_val = sanitize_zeros_from_collection(v, mode=mode)
            if cleaned_val is not None and cleaned_val != "":
                res[k] = cleaned_val
        return res

    return data


def filter_zero_values_dict(d: Dict[Any, Any], remove_zero_strings: bool = True) -> Dict[Any, Any]:
    """
    Filters out key-value pairs from a dictionary where the value is zero (0, 0.0, or string zeros).

    Args:
        d: Input dictionary.
        remove_zero_strings: If True, treats strings like "0", "0.0", "00" as zero values to filter out.

    Returns:
        Filtered dictionary without zero entries.

    Raises:
        TypeError: If d is not a dictionary.
    """
    if not isinstance(d, dict):
        raise TypeError(f"Expected dict for d, got {type(d).__name__}")

    result = {}
    for k, v in d.items():
        if v == 0 or v == 0.0:
            continue
        if remove_zero_strings and isinstance(v, str):
            stripped = v.strip()
            if stripped and re.match(r"^0+(\.0+)?$", stripped):
                continue
        result[k] = v
    return result


# ─── 6. Zero Masking & Replacement Helpers ────────────────────────────────────


def replace_zeros(text: str, replacement: str = "X") -> str:
    """
    Replaces all '0' characters in a string with a designated replacement token.

    Args:
        text: Input string.
        replacement: String token to replace zeros with (default "X").

    Returns:
        String with zeros substituted.

    Raises:
        TypeError: If text or replacement is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str for text, got {type(text).__name__}")
    if not isinstance(replacement, str):
        raise TypeError(f"Expected str for replacement, got {type(replacement).__name__}")

    return text.replace("0", replacement)


def mask_zeros(text: str, mask_char: str = "*", leading_only: bool = False) -> str:
    """
    Masks zeros with a specified character.

    Args:
        text: Input string.
        mask_char: Masking character (default "*").
        leading_only: If True, masks only leading zeros.

    Returns:
        Masked string.

    Raises:
        TypeError: If text is not a string or mask_char is invalid.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str for text, got {type(text).__name__}")
    if not isinstance(mask_char, str) or len(mask_char) != 1:
        raise TypeError("mask_char must be a single character string.")

    if leading_only:
        leading_count = 0
        for char in text:
            if char == "0":
                leading_count += 1
            else:
                break
        return (mask_char * leading_count) + text[leading_count:]

    return text.replace("0", mask_char)





