# Day 68: Keep Alphanumeric Only
#
# Problem:
#   Write a Python program / module to strip non-alphanumeric characters from text inputs.
#   Includes core filtering, custom extra character retention, ASCII vs Unicode modes,
#   character removal breakdown analysis, batch list/dict sanitization, URL slugification,
#   unit test suite, and Java practice.

import re
import string
import unicodedata
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Alphanumeric Filtering Functions ─────────────────────────────────


def keep_alphanumeric_only(text: str, keep_spaces: bool = False) -> str:
    """
    Strips all non-alphanumeric characters (punctuation, symbols, emojis) from a string.

    Args:
        text: Target text string to filter.
        keep_spaces: If True, whitespace characters (spaces, tabs) are preserved.

    Returns:
        Filtered string containing only alphanumeric characters (and spaces if enabled).

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text:
        return ""

    if keep_spaces:
        return re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    return re.sub(r"[^\w]", "", text, flags=re.UNICODE).replace("_", "")


def is_pure_alphanumeric(text: str) -> bool:
    """
    Checks if a string consists strictly of alphanumeric characters without symbols or spaces.

    Args:
        text: Target text string.

    Returns:
        True if text is non-empty and contains only letters and digits, else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    return len(text) > 0 and text.isalnum()


# ─── 2. Custom Character Retention & Word Extraction ──────────────────────────


def sanitize_alphanumeric_custom(
    text: str,
    preserve_case: bool = True,
    allowed_extra_chars: Optional[str] = None,
) -> str:
    """
    Filters text to alphanumeric characters while permitting specified custom extra characters.

    Args:
        text: Target text string.
        preserve_case: If False, converts output to lowercase.
        allowed_extra_chars: String of extra allowed non-alphanumeric chars e.g. " -_@".

    Returns:
        Filtered string containing alphanumeric plus allowed extra characters.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")

    extra = allowed_extra_chars or ""
    escaped_extra = re.escape(extra)
    pattern = f"[^a-zA-Z0-9{escaped_extra}]"

    res = re.sub(pattern, "", text)
    return res if preserve_case else res.lower()


def extract_alphanumeric_words(text: str) -> List[str]:
    """
    Extracts words containing strictly alphanumeric characters from a body of text.

    Args:
        text: Source text paragraph.

    Returns:
        List of alphanumeric word strings.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if not text.strip():
        return []

    tokens = text.split()
    words = []

    for token in tokens:
        cleaned = re.sub(r"[^\w]", "", token).replace("_", "")
        if cleaned:
            words.append(cleaned)

    return words


# ─── 3. ASCII vs Unicode Alphanumeric Filtering Modes ─────────────────────────


def keep_ascii_alphanumeric(text: str, keep_spaces: bool = False) -> str:
    """
    Filters text strictly to ASCII alphanumeric characters (A-Z, a-z, 0-9).

    Args:
        text: Target text string.
        keep_spaces: If True, preserves space characters.

    Returns:
        Filtered ASCII string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    if keep_spaces:
        return re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return re.sub(r"[^a-zA-Z0-9]", "", text)


def keep_unicode_alphanumeric(text: str, keep_spaces: bool = False) -> str:
    """
    Filters text using Unicode character category inspection (retains letters and numbers across all languages).

    Args:
        text: Target text string.
        keep_spaces: If True, preserves space characters.

    Returns:
        Filtered Unicode string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    retained = []
    for char in text:
        # Category check: 'L' (Letter), 'N' (Number)
        cat = unicodedata.category(char)
        if cat.startswith("L") or cat.startswith("N"):
            retained.append(char)
        elif keep_spaces and char.isspace():
            retained.append(char)

    return "".join(retained)


# ─── 4. Character Removal Breakdown & Analysis Engine ─────────────────────────


def analyze_alphanumeric_filtration(text: str) -> Dict[str, Any]:
    """
    Analyzes character composition and calculates filtration metrics for a text.

    Args:
        text: Input string to analyze.

    Returns:
        Dict containing total_chars, retained_alphanumeric_count, removed_special_count,
        removed_characters_list, retention_ratio_percentage, and category_breakdown.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    total_len = len(text)
    retained_chars = []
    removed_chars = []

    cat_breakdown = {
        "letters": 0,
        "digits": 0,
        "punctuation": 0,
        "whitespace": 0,
        "symbols_other": 0,
    }

    for c in text:
        if c.isalnum():
            retained_chars.append(c)
            if c.isalpha():
                cat_breakdown["letters"] += 1
            else:
                cat_breakdown["digits"] += 1
        else:
            removed_chars.append(c)
            if c in string.punctuation:
                cat_breakdown["punctuation"] += 1
            elif c.isspace():
                cat_breakdown["whitespace"] += 1
            else:
                cat_breakdown["symbols_other"] += 1

    ret_count = len(retained_chars)
    rem_count = len(removed_chars)
    ratio = (ret_count / total_len * 100.0) if total_len > 0 else 0.0

    return {
        "total_length": total_len,
        "retained_alphanumeric_count": ret_count,
        "removed_special_count": rem_count,
        "retained_text": "".join(retained_chars),
        "removed_characters": removed_chars,
        "retention_ratio_percentage": round(ratio, 2),
        "category_breakdown": cat_breakdown,
    }


# ─── 5. Collection Batch Sanitizers ───────────────────────────────────────────


def sanitize_string_list(
    text_list: List[str],
    keep_spaces: bool = False,
) -> List[str]:
    """
    Sanitizes a list of strings, keeping only alphanumeric characters in each item.

    Args:
        text_list: List of input string items.
        keep_spaces: If True, preserves whitespace characters.

    Returns:
        New list of sanitized strings.

    Raises:
        TypeError: If text_list is not a list.
    """
    if not isinstance(text_list, list):
        raise TypeError(f"Expected list for text_list, got {type(text_list).__name__}")

    sanitized = []
    for item in text_list:
        if not isinstance(item, str):
            raise TypeError(f"All list items must be strings, got {type(item).__name__}")
        sanitized.append(keep_alphanumeric_only(item, keep_spaces=keep_spaces))

    return sanitized


def sanitize_dictionary_keys_values(
    data: Dict[str, Any],
    sanitize_keys: bool = True,
    sanitize_values: bool = True,
) -> Dict[str, Any]:
    """
    Sanitizes dictionary keys and/or string values to contain only alphanumeric characters.

    Args:
        data: Target dictionary.
        sanitize_keys: If True, strips non-alphanumeric chars from string keys.
        sanitize_values: If True, strips non-alphanumeric chars from string values.

    Returns:
        New dictionary with sanitized keys/values.

    Raises:
        TypeError: If data is not a dict.
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict for data, got {type(data).__name__}")

    new_dict: Dict[str, Any] = {}

    for k, v in data.items():
        new_key = keep_alphanumeric_only(str(k)) if sanitize_keys else k
        new_val = v
        if sanitize_values and isinstance(v, str):
            new_val = keep_alphanumeric_only(v)

        new_dict[new_key] = new_val

    return new_dict


# ─── 6. Text Masking & URL Slugification Helpers ──────────────────────────────


def replace_non_alphanumeric(text: str, replacement_char: str = "_") -> str:
    """
    Replaces all non-alphanumeric characters with a designated replacement character.

    Args:
        text: Source text string.
        replacement_char: Character to substitute for special symbols/whitespace (default '_').

    Returns:
        Transformed output string.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(text, str) or not isinstance(replacement_char, str):
        raise TypeError("text and replacement_char must be strings.")

    return re.sub(r"[^\w]", replacement_char, text, flags=re.UNICODE)


def slugify_alphanumeric(text: str, separator: str = "-") -> str:
    """
    Generates a clean, URL-friendly slug by retaining alphanumeric words separated by separator.

    Args:
        text: Source title or headline string.
        separator: Delimiter string connecting words (default '-').

    Returns:
        URL slug string.

    Raises:
        TypeError: If inputs are not strings.
    """
    if not isinstance(text, str) or not isinstance(separator, str):
        raise TypeError("text and separator must be strings.")
    if not text.strip():
        return ""

    words = extract_alphanumeric_words(text)
    return separator.join(w.lower() for w in words)


# ─── 7. Unit Test Suite ───────────────────────────────────────────────────────


class TestKeepAlphanumericOnly(unittest.TestCase):
    """Test suite for alphanumeric filtering, custom retention, analysis, and batch operations."""

    def test_keep_alphanumeric_only(self):
        self.assertEqual(keep_alphanumeric_only("Hello, World! 123"), "HelloWorld123")
        self.assertEqual(keep_alphanumeric_only("Hello, World! 123", keep_spaces=True), "Hello World 123")
        self.assertEqual(keep_alphanumeric_only(""), "")
        self.assertTrue(is_pure_alphanumeric("Python300"))
        self.assertFalse(is_pure_alphanumeric("Python 300!"))

        with self.assertRaises(TypeError):
            keep_alphanumeric_only(12345)

    def test_sanitize_custom_and_word_extraction(self):
        self.assertEqual(sanitize_alphanumeric_custom("User@Domain.com!", preserve_case=True, allowed_extra_chars="@."), "User@Domain.com")
        self.assertEqual(sanitize_alphanumeric_custom("User@Domain.com!", preserve_case=False, allowed_extra_chars="@."), "user@domain.com")
        self.assertEqual(extract_alphanumeric_words("The quick, brown-fox!"), ["The", "quick", "brownfox"])

    def test_ascii_and_unicode_modes(self):
        self.assertEqual(keep_ascii_alphanumeric("Café#123!"), "Caf123")
        self.assertEqual(keep_unicode_alphanumeric("Café#123!"), "Café123")

    def test_analyze_alphanumeric_filtration(self):
        res = analyze_alphanumeric_filtration("Py#300!")
        self.assertEqual(res["total_length"], 7)
        self.assertEqual(res["retained_alphanumeric_count"], 5)
        self.assertEqual(res["removed_special_count"], 2)
        self.assertEqual(res["retained_text"], "Py300")
        self.assertEqual(res["category_breakdown"]["letters"], 2)
        self.assertEqual(res["category_breakdown"]["digits"], 3)

    def test_batch_sanitizers(self):
        lst = ["Item #1!", "User @Home!"]
        self.assertEqual(sanitize_string_list(lst), ["Item1", "UserHome"])

        d = {"user_name!": "John Doe#1", "age": 30}
        san_d = sanitize_dictionary_keys_values(d)
        self.assertIn("username", san_d)
        self.assertEqual(san_d["username"], "JohnDoe1")

    def test_replace_and_slugify(self):
        self.assertEqual(replace_non_alphanumeric("Hello World!", "_"), "Hello_World_")
        self.assertEqual(slugify_alphanumeric("300 Days of Python! Day #68"), "300-days-of-python-day-68")






