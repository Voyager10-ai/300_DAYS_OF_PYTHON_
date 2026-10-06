# Day 74: Array Missing Element Challenge
#
# Problem:
#   Write a Python program / module to solve missing element challenges in arrays.
#   Includes core single missing element solvers (Sum & XOR methods), multiple missing elements finder,
#   shuffled array comparison, duplicate & missing finder, first missing positive integer solver,
#   completeness metrics engine, batch dataset processors, array reconstruction helpers, unit test suite, and Java practice code.

import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Single Missing Element Solvers (Sum & XOR Methods) ──────────────


def find_missing_element_sum(arr: List[int], n: Optional[int] = None) -> int:
    """
    Finds a single missing number in an array containing numbers from 1 to N using the Gauss sum formula.

    Args:
        arr: List of integers from 1 to N with exactly one element missing.
        n: Expected upper limit N. If None, inferred as len(arr) + 1.

    Returns:
        The missing integer.

    Raises:
        TypeError: If arr is not a list or elements are not ints.
        ValueError: If array contains invalid range elements or more/fewer missing items.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    
    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    if n is None:
        n = len(arr) + 1

    if n <= 0:
        raise ValueError("Range limit N must be greater than 0.")

    expected_sum = (n * (n + 1)) // 2
    actual_sum = sum(arr)
    missing = expected_sum - actual_sum

    if missing <= 0 or missing > n:
        raise ValueError(f"Calculated missing element {missing} is out of expected range [1, {n}]. Check input array.")

    return missing


def find_missing_element_xor(arr: List[int], n: Optional[int] = None) -> int:
    """
    Finds a single missing number in an array containing numbers from 1 to N using bitwise XOR.

    Args:
        arr: List of integers from 1 to N with exactly one element missing.
        n: Expected upper limit N. If None, inferred as len(arr) + 1.

    Returns:
        The missing integer.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If n <= 0.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    if n is None:
        n = len(arr) + 1

    if n <= 0:
        raise ValueError("Range limit N must be greater than 0.")

    xor_all = 0
    for i in range(1, n + 1):
        xor_all ^= i

    xor_arr = 0
    for x in arr:
        xor_arr ^= x

    return xor_all ^ xor_arr
