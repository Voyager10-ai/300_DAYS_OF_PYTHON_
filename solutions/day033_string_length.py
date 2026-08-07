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
