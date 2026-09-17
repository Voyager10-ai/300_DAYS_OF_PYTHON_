# Day 65: Check String
#
# Problem:
#   Write a Python program / module to check various properties of a given string.
#   Includes core classification (alphanumeric, numeric, alpha, custom charsets), substring/prefix/suffix matching,
#   pattern validations (identifiers, hex color, email, IPv4), comprehensive string analysis metrics,
#   custom multi-condition rule validation, string sanitization/normalization, unit test suite, and Java practice.

import re
import string
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Classification & Character Set Checkers ─────────────────────────


def is_alphanumeric_str(s: str) -> bool:
    """
    Checks if non-empty string contains only alphanumeric characters (letters and digits).

    Args:
        s: Input string to check.

    Returns:
        True if s is non-empty and all characters are alphanumeric, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    return len(s) > 0 and s.isalnum()


def is_numeric_str(s: str, allow_negative: bool = False, allow_decimal: bool = False) -> bool:
    """
    Checks if string represents a valid integer or float numeric value.

    Args:
        s: Input string to check.
        allow_negative: If True, permits leading '-' or '+' sign.
        allow_decimal: If True, permits single decimal point '.'.

    Returns:
        True if s matches the numeric constraints, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    if not s:
        return False

    pattern = r"^"
    if allow_negative:
        pattern += r"[+-]?"
    if allow_decimal:
        pattern += r"\d+(\.\d+)?"
    else:
        pattern += r"\d+"
    pattern += r"$"

    return bool(re.match(pattern, s))


def is_alpha_str(s: str, allow_spaces: bool = False) -> bool:
    """
    Checks if string contains only alphabetic letters (a-z, A-Z), optionally allowing spaces.

    Args:
        s: Input string to check.
        allow_spaces: If True, space characters are permitted.

    Returns:
        True if s is non-empty and contains only letters (and spaces if allowed), else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    if not s:
        return False
    if allow_spaces:
        return bool(re.match(r"^[a-zA-Z\s]+$", s))
    return s.isalpha()


def contains_only_chars(s: str, allowed_chars: Union[str, Set[str], List[str]]) -> bool:
    """
    Checks if string consists solely of characters in allowed_chars set.

    Args:
        s: Input string to check.
        allowed_chars: String, set, or list of permitted characters.

    Returns:
        True if s is non-empty and every char in s is in allowed_chars, else False.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string for s, got {type(s).__name__}")
    if not s:
        return False

    allowed_set = set(allowed_chars)
    return all(char in allowed_set for char in s)


# ─── 2. Substring, Prefix & Suffix Matching Utilities ─────────────────────────


def check_substring(text: str, sub: str, case_sensitive: bool = True) -> bool:
    """
    Checks whether substring sub is present in text.

    Args:
        text: Main text string to search within.
        sub: Substring to search for.
        case_sensitive: If False, performs case-insensitive matching.

    Returns:
        True if sub is found in text, else False.

    Raises:
        TypeError: If text or sub is not a string.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("Both text and sub must be strings.")
    if not sub:
        return True

    if not case_sensitive:
        return sub.lower() in text.lower()
    return sub in text


def check_prefix_suffix(
    text: str,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    case_sensitive: bool = True,
) -> bool:
    """
    Checks if text starts with prefix and/or ends with suffix.

    Args:
        text: Main string to check.
        prefix: Required starting substring (or None to skip).
        suffix: Required ending substring (or None to skip).
        case_sensitive: If False, ignores letter case.

    Returns:
        True if text satisfies both prefix and suffix constraints (if provided), else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")

    t = text if case_sensitive else text.lower()

    if prefix is not None:
        p = prefix if case_sensitive else prefix.lower()
        if not t.startswith(p):
            return False

    if suffix is not None:
        s = suffix if case_sensitive else suffix.lower()
        if not t.endswith(s):
            return False

    return True


def count_substring_occurrences(text: str, sub: str, allow_overlap: bool = False) -> int:
    """
    Counts occurrences of sub within text.

    Args:
        text: Source string to search.
        sub: Pattern substring to count.
        allow_overlap: If True, counts overlapping occurrences.

    Returns:
        Number of matching occurrences.

    Raises:
        TypeError: If inputs are not strings.
        ValueError: If sub is an empty string.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("Both text and sub must be strings.")
    if not sub:
        raise ValueError("Search substring 'sub' cannot be empty.")

    if not allow_overlap:
        return text.count(sub)

    count = 0
    start = 0
    while True:
        pos = text.find(sub, start)
        if pos == -1:
            break
        count += 1
        start = pos + 1
    return count


# ─── 3. Pattern Validation Engine ────────────────────────────────────────────


def is_valid_identifier(s: str) -> bool:
    """
    Checks if string is a valid Python/Java variable identifier.

    Args:
        s: Input string to check.

    Returns:
        True if s is a valid identifier name, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    return s.isidentifier()


def is_hex_color(s: str) -> bool:
    """
    Checks if string is a valid 3-digit or 6-digit hex color code (e.g., '#FFF', '#1a2b3c').

    Args:
        s: Input color string.

    Returns:
        True if s is a valid hex color string, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    pattern = r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"
    return bool(re.match(pattern, s.strip()))


def is_valid_email_basic(s: str) -> bool:
    """
    Performs basic email format validation.

    Args:
        s: Input email string to test.

    Returns:
        True if s matches standard email format, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, s.strip()))


def is_valid_ipv4(s: str) -> bool:
    """
    Validates if string represents a correct IPv4 address (4 octets, 0 to 255).

    Args:
        s: IP address string.

    Returns:
        True if s is a valid IPv4 address, else False.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")

    parts = s.strip().split(".")
    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False
        # Disallow leading zeroes unless single zero
        if len(part) > 1 and part.startswith("0"):
            return False
        val = int(part)
        if val < 0 or val > 255:
            return False

    return True


# ─── 4. Detailed String Analysis Engine ──────────────────────────────────────


def analyze_string_properties(s: str) -> Dict[str, Any]:
    """
    Analyzes character breakdown, casing, palindrome status, and metrics of a string.

    Args:
        s: Input string to analyze.

    Returns:
        Dict containing total_length, char_counts (digits, letters, uppercase, lowercase,
        whitespace, punctuation/special), casing_format, is_palindrome, is_ascii,
        and char_frequencies.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")

    total_len = len(s)
    digit_cnt = sum(1 for c in s if c.isdigit())
    alpha_cnt = sum(1 for c in s if c.isalpha())
    upper_cnt = sum(1 for c in s if c.isupper())
    lower_cnt = sum(1 for c in s if c.islower())
    space_cnt = sum(1 for c in s if c.isspace())
    punct_cnt = sum(1 for c in s if c in string.punctuation)
    other_cnt = total_len - (digit_cnt + alpha_cnt + space_cnt + punct_cnt)

    casing = "empty"
    if s:
        if s.isupper():
            casing = "uppercase"
        elif s.islower():
            casing = "lowercase"
        elif s.istitle():
            casing = "titlecase"
        else:
            casing = "mixedcase"

    # Palindrome check (ignoring case and non-alphanumeric chars)
    clean_chars = [c.lower() for c in s if c.isalnum()]
    is_pal = len(clean_chars) > 0 and clean_chars == clean_chars[::-1]

    # Frequency breakdown
    freq: Dict[str, int] = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1

    return {
        "total_length": total_len,
        "digits_count": digit_cnt,
        "letters_count": alpha_cnt,
        "uppercase_count": upper_cnt,
        "lowercase_count": lower_cnt,
        "whitespace_count": space_cnt,
        "punctuation_count": punct_cnt,
        "other_count": max(0, other_cnt),
        "casing_format": casing,
        "is_palindrome": is_pal,
        "is_ascii": s.isascii(),
        "char_frequencies": freq,
    }


# ─── 5. Custom Rule-Based Multi-Condition Validator ──────────────────────────


def validate_string_rules(
    s: str,
    min_len: Optional[int] = None,
    max_len: Optional[int] = None,
    require_upper: bool = False,
    require_lower: bool = False,
    require_digit: bool = False,
    require_special: bool = False,
    forbidden_chars: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validates string against custom configurable criteria (length, character classes, forbidden chars).

    Args:
        s: Target string to validate.
        min_len: Minimum allowed length (or None).
        max_len: Maximum allowed length (or None).
        require_upper: If True, must contain at least 1 uppercase letter.
        require_lower: If True, must contain at least 1 lowercase letter.
        require_digit: If True, must contain at least 1 numeric digit.
        require_special: If True, must contain at least 1 punctuation/special char.
        forbidden_chars: String of disallowed characters.

    Returns:
        Dict with 'is_valid', 'passed_rules', 'failed_rules', and 'score_percentage'.

    Raises:
        TypeError: If s is not a string.
        ValueError: If min_len > max_len or negative limits provided.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string, got {type(s).__name__}")

    if min_len is not None and min_len < 0:
        raise ValueError("min_len cannot be negative.")
    if max_len is not None and max_len < 0:
        raise ValueError("max_len cannot be negative.")
    if min_len is not None and max_len is not None and min_len > max_len:
        raise ValueError(f"min_len ({min_len}) cannot be greater than max_len ({max_len}).")

    passed_rules = []
    failed_rules = []

    # Rule 1: min_len
    if min_len is not None:
        if len(s) >= min_len:
            passed_rules.append(f"min_length_satisfied ({len(s)} >= {min_len})")
        else:
            failed_rules.append(f"min_length_failed ({len(s)} < {min_len})")

    # Rule 2: max_len
    if max_len is not None:
        if len(s) <= max_len:
            passed_rules.append(f"max_length_satisfied ({len(s)} <= {max_len})")
        else:
            failed_rules.append(f"max_length_failed ({len(s)} > {max_len})")

    # Rule 3: require_upper
    if require_upper:
        if any(c.isupper() for c in s):
            passed_rules.append("require_uppercase_satisfied")
        else:
            failed_rules.append("require_uppercase_failed")

    # Rule 4: require_lower
    if require_lower:
        if any(c.islower() for c in s):
            passed_rules.append("require_lowercase_satisfied")
        else:
            failed_rules.append("require_lowercase_failed")

    # Rule 5: require_digit
    if require_digit:
        if any(c.isdigit() for c in s):
            passed_rules.append("require_digit_satisfied")
        else:
            failed_rules.append("require_digit_failed")

    # Rule 6: require_special
    if require_special:
        if any(c in string.punctuation for c in s):
            passed_rules.append("require_special_satisfied")
        else:
            failed_rules.append("require_special_failed")

    # Rule 7: forbidden_chars
    if forbidden_chars:
        found_forbidden = [c for c in s if c in forbidden_chars]
        if not found_forbidden:
            passed_rules.append("forbidden_chars_satisfied")
        else:
            failed_rules.append(f"forbidden_chars_failed (found: {''.join(set(found_forbidden))})")

    total_rules = len(passed_rules) + len(failed_rules)
    score = (len(passed_rules) / total_rules * 100.0) if total_rules > 0 else 100.0

    return {
        "is_valid": len(failed_rules) == 0,
        "passed_rules": passed_rules,
        "failed_rules": failed_rules,
        "score_percentage": round(score, 2),
    }




