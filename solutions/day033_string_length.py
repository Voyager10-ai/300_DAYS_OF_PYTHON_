# Day 33: String Length
#
# Problem:
#   Write a Python program to calculate the length of a string using multiple algorithms and options.
#   - Iterative Character Count: Loop-based length counting without using len().
#   - Recursive Length: Divide-and-conquer recursive string length computation.
#   - Built-in Wrapper: Safe wrapper around standard len() with validation.

import sys
import io
import unicodedata
from typing import List, Dict, Tuple, Optional, Any, Callable


def calculate_length_iterative(s: str) -> int:
    """
    Calculates the length of a string by iterating through its characters without using len().

    Args:
        s: Input string.

    Returns:
        Integer count of characters in s.

    Time Complexity: O(N) where N is number of characters.
    Space Complexity: O(1).

    Example:
        calculate_length_iterative("Python") -> 6
        calculate_length_iterative("") -> 0
    """
    if not s:
        return 0
    count = 0
    for _ in s:
        count += 1
    return count


def calculate_length_recursive(s: str) -> int:
    """
    Recursively computes the length of a string.

    Args:
        s: Input string.

    Returns:
        Integer character count of s.

    Time Complexity: O(N) call depth.
    Space Complexity: O(N) call stack.

    Example:
        calculate_length_recursive("hello") -> 5
        calculate_length_recursive("") -> 0
    """
    if not s:
        return 0
    return 1 + calculate_length_recursive(s[1:])


def calculate_length_builtin(s: Optional[str]) -> int:
    """
    Safely retrieves the length of a string using Python's built-in len().

    Args:
        s: Input string or None.

    Returns:
        Length of s or 0 if s is None.
    """
    if s is None:
        return 0
    return len(s)


def calculate_byte_length(s: str, encoding: str = "utf-8") -> int:
    """
    Calculates the byte size of a string under a given text encoding format.

    Args:
        s: Input string.
        encoding: Character encoding format (e.g. 'utf-8', 'utf-16', 'ascii').

    Returns:
        Total number of encoded bytes.

    Example:
        calculate_byte_length("hello", "utf-8") -> 5
        calculate_byte_length("🚀", "utf-8") -> 4
    """
    if not s:
        return 0
    return len(s.encode(encoding, errors="replace"))


def calculate_unicode_code_points(s: str) -> int:
    """
    Calculates the total count of distinct Unicode code points in a string.

    Args:
        s: Input text string.

    Returns:
        Count of code points.
    """
    if not s:
        return 0
    return len([ord(c) for c in s])


def analyze_multi_byte_characters(s: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Analyzes character composition and identifies single-byte vs multi-byte characters.

    Args:
        s: Input string.
        encoding: Character encoding format.

    Returns:
        Dictionary containing character count, byte count, and multi-byte breakdown.
    """
    if not s:
        return {
            "char_count": 0,
            "byte_count": 0,
            "single_byte_chars": 0,
            "multi_byte_chars": 0,
            "expansion_ratio": 1.0,
        }

    char_count = len(s)
    byte_count = calculate_byte_length(s, encoding=encoding)

    single_byte = 0
    multi_byte = 0
    for char in s:
        b_len = len(char.encode(encoding, errors="replace"))
        if b_len == 1:
            single_byte += 1
        else:
            multi_byte += 1

    ratio = round(byte_count / char_count, 2) if char_count > 0 else 1.0

    return {
        "char_count": char_count,
        "byte_count": byte_count,
        "single_byte_chars": single_byte,
        "multi_byte_chars": multi_byte,
        "expansion_ratio": ratio,
    }

