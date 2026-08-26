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


# ─── 3. English Word Number to Integer Converter ───────────────────────────────


WORD_NUMBER_MAP: Dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

WORD_MULTIPLIERS: Dict[str, int] = {
    "hundred": 100,
    "thousand": 1000,
    "million": 1000000,
    "billion": 1000000000,
}


def words_to_int(s: str) -> int:
    """
    Converts English word numbers (e.g. 'one hundred twenty-three') to integer.

    Args:
        s: String of word number tokens.

    Returns:
        Converted integer.

    Raises:
        ValueError: If words cannot be parsed into a valid number.
    """
    clean_str = s.lower().replace("-", " ").strip()
    if not clean_str:
        raise ValueError("Cannot convert empty word string")

    words = clean_str.split()
    sign = 1
    if words[0] in ("negative", "minus"):
        sign = -1
        words = words[1:]

    if not words:
        raise ValueError("No valid word tokens found after sign")

    total = 0
    current = 0

    for word in words:
        if word == "and":
            continue
        if word in WORD_NUMBER_MAP:
            current += WORD_NUMBER_MAP[word]
        elif word in WORD_MULTIPLIERS:
            scale = WORD_MULTIPLIERS[word]
            if scale == 100:
                current = (current if current != 0 else 1) * 100
            else:
                total += (current if current != 0 else 1) * scale
                current = 0
        else:
            raise ValueError(f"Unrecognized number word: '{word}'")

    return sign * (total + current)


# ─── 4. Roman Numeral to Integer Converter ────────────────────────────────────


ROMAN_VALUES: Dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def roman_to_int(s: str) -> int:
    """
    Converts a Roman numeral string (e.g. 'MCMXCIV') to integer.

    Args:
        s: Roman numeral string.

    Returns:
        Converted integer (1 to 3999).

    Raises:
        ValueError: If string is not a valid Roman numeral.
    """
    clean_s = s.strip().upper()
    if not clean_s:
        raise ValueError("Cannot convert empty Roman numeral string")

    # Basic regex validation for standard Roman numerals (1 - 3999)
    roman_pattern = r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    if not re.match(roman_pattern, clean_s):
        raise ValueError(f"Invalid Roman numeral string: '{s}'")

    total = 0
    prev_value = 0

    for char in reversed(clean_s):
        value = ROMAN_VALUES[char]
        if value < prev_value:
            total -= value
        else:
            total += value
            prev_value = value

    return total


# ─── 5. Collection & Dictionary Integer Conversion Utilities ──────────────────


def convert_list_to_ints(
    items: List[Any],
    ignore_errors: bool = False,
    default: Optional[int] = None,
) -> List[int]:
    """
    Converts a list of mixed element types (strings, floats, numbers) into integers.

    Args:
        items: Iterable list of items.
        ignore_errors: If True, skips items that fail to convert.
        default: Fallback value if item conversion fails and ignore_errors=False.

    Returns:
        List of converted integer values.
    """
    result: List[int] = []
    for item in items:
        converted = safe_str_to_int(item, default=default)
        if converted is not None:
            result.append(converted)
        elif not ignore_errors and default is None:
            raise ValueError(f"Could not convert item '{item}' to int")
    return result


def convert_dict_values_to_ints(
    d: Dict[Any, Any],
    ignore_errors: bool = False,
    default: Optional[int] = None,
) -> Dict[Any, int]:
    """
    Converts values of a dictionary to integers.

    Args:
        d: Input dictionary.
        ignore_errors: If True, omits keys whose values fail conversion.
        default: Default fallback value if conversion fails and ignore_errors=False.

    Returns:
        New dictionary with converted integer values.
    """
    result: Dict[Any, int] = {}
    for k, v in d.items():
        converted = safe_str_to_int(v, default=default)
        if converted is not None:
            result[k] = converted
        elif not ignore_errors and default is None:
            raise ValueError(f"Could not convert value '{v}' for key '{k}' to int")
    return result


# ─── 6. Formatted Numeric String Cleaning & Float Conversion ───────────────────


def clean_numeric_str_to_int(s: str, rounding_mode: str = "trunc") -> int:
    """
    Cleans formatted currency/number strings (e.g. '$1,234,567.89', '  1e5  ') and converts to int.

    Args:
        s: Raw input string containing digits, commas, currency symbols, floats, or sci notation.
        rounding_mode: How float components are rounded: 'trunc', 'round', 'floor', 'ceil'.

    Returns:
        Converted integer.

    Raises:
        ValueError: If cleaning fails to yield a valid number.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")

    # Remove commas, currency symbols, spaces
    cleaned = re.sub(r"[$,\s]", "", s.strip())

    # Handle scientific notation or float strings
    try:
        val_float = float(cleaned)
    except ValueError:
        raise ValueError(f"Unable to parse formatted numeric string: '{s}'")

    if math.isnan(val_float) or math.isinf(val_float):
        raise ValueError(f"Cannot convert non-finite float value '{val_float}' to integer")

    if rounding_mode == "trunc":
        return int(val_float)
    elif rounding_mode == "round":
        return round(val_float)
    elif rounding_mode == "floor":
        return math.floor(val_float)
    elif rounding_mode == "ceil":
        return math.ceil(val_float)
    else:
        raise ValueError(f"Unknown rounding mode: '{rounding_mode}'")


# ─── 7. Range-Bounded Integer Conversion & Clamping ───────────────────────────


def bounded_str_to_int(
    s: str,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    clamp: bool = False,
) -> int:
    """
    Converts a string to integer and enforces minimum and maximum boundary bounds.

    Args:
        s: Input string representation of an integer.
        min_val: Optional lower bound (inclusive).
        max_val: Optional upper bound (inclusive).
        clamp: If True, clamps out-of-bound values to min_val/max_val instead of raising error.

    Returns:
        Bounded or clamped integer value.

    Raises:
        ValueError: If value is out of bounds and clamp=False.
    """
    val = custom_atoi(s)

    if min_val is not None and val < min_val:
        if clamp:
            return min_val
        raise ValueError(f"Value {val} is below minimum allowed bound {min_val}")

    if max_val is not None and val > max_val:
        if clamp:
            return max_val
        raise ValueError(f"Value {val} exceeds maximum allowed bound {max_val}")

    return val


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestConvertToIntOperations(unittest.TestCase):
    def test_custom_atoi(self):
        self.assertEqual(custom_atoi("42"), 42)
        self.assertEqual(custom_atoi("   -12345extra"), -12345)
        self.assertEqual(custom_atoi("+99"), 99)
        with self.assertRaises(ValueError):
            custom_atoi("words")
        with self.assertRaises(ValueError):
            custom_atoi("")

    def test_safe_str_to_int(self):
        self.assertEqual(safe_str_to_int("100"), 100)
        self.assertEqual(safe_str_to_int(12.7), 12)
        self.assertIsNone(safe_str_to_int("invalid"))
        self.assertEqual(safe_str_to_int("invalid", default=-1), -1)

    def test_convert_base_to_int(self):
        self.assertEqual(convert_base_to_int("1010", base=2), 10)
        self.assertEqual(convert_base_to_int("0b1010", base=2), 10)
        self.assertEqual(convert_base_to_int("0x1A", base=16), 26)
        self.assertEqual(convert_base_to_int("z", base=36), 35)

        val, base = auto_detect_base_convert("0x3E8")
        self.assertEqual(val, 1000)
        self.assertEqual(base, 16)

    def test_words_to_int(self):
        self.assertEqual(words_to_int("forty-two"), 42)
        self.assertEqual(words_to_int("one hundred twenty-three"), 123)
        self.assertEqual(words_to_int("minus five thousand four hundred six"), -5406)

    def test_roman_to_int(self):
        self.assertEqual(roman_to_int("IV"), 4)
        self.assertEqual(roman_to_int("MCMXCIV"), 1994)
        with self.assertRaises(ValueError):
            roman_to_int("IIII")

    def test_collection_conversions(self):
        items = ["10", "20.5", "invalid", "30"]
        self.assertEqual(convert_list_to_ints(items, ignore_errors=True), [10, 20, 30])

        d = {"a": "1", "b": "$2.5", "c": "3"}
        self.assertEqual(convert_dict_values_to_ints({"a": "1", "c": "3"}), {"a": 1, "c": 3})

    def test_clean_numeric_str_to_int(self):
        self.assertEqual(clean_numeric_str_to_int("$1,234,567.89"), 1234567)
        self.assertEqual(clean_numeric_str_to_int("1e4"), 10000)
        self.assertEqual(clean_numeric_str_to_int("  4.9  ", rounding_mode="round"), 5)

    def test_bounded_str_to_int(self):
        self.assertEqual(bounded_str_to_int("50", min_val=0, max_val=100), 50)
        with self.assertRaises(ValueError):
            bounded_str_to_int("150", max_val=100)
        self.assertEqual(bounded_str_to_int("150", max_val=100, clamp=True), 100)


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" 🔢 Day 48: Convert String to Int Utilities - Interactive Demo")
    print("=" * 60)

    # 1. Custom atoi
    sample_str = "   -42999 extra trailing text"
    converted_atoi = custom_atoi(sample_str)
    print(f"\n1. Custom atoi Parsing:")
    print(f"   Input String : '{sample_str}'")
    print(f"   Parsed Int   : {converted_atoi}")

    # 2. Base Conversions
    hex_str = "0x7E4"
    hex_val, detected_base = auto_detect_base_convert(hex_str)
    bin_val = convert_base_to_int("110101", base=2)
    print(f"\n2. Arbitrary Base Conversions:")
    print(f"   '{hex_str}' (auto-detected base {detected_base}) -> {hex_val}")
    print(f"   '110101' (base 2) -> {bin_val}")

    # 3. English Words & Roman Numerals
    words = "two million five hundred thousand three hundred forty-five"
    word_val = words_to_int(words)
    roman_str = "MCMXCIV"
    roman_val = roman_to_int(roman_str)
    print(f"\n3. Textual & Roman Numeral Conversion:")
    print(f"   Words: '{words}' -> {word_val:,}")
    print(f"   Roman: '{roman_str}' -> {roman_val}")

    # 4. Formatted Currency Cleaning
    currency_str = "  $ 1,234,567.89  "
    clean_val = clean_numeric_str_to_int(currency_str, rounding_mode="round")
    print(f"\n4. Currency & Formatted String Cleaning:")
    print(f"   Formatted Input : '{currency_str}'")
    print(f"   Cleaned Int     : {clean_val:,}")

    # 5. Unit Test Suite Execution
    print("\n5. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvertToIntOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








