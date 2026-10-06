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


# ─── 2. Multiple Missing Elements & Shuffled Array Comparison ────────────────


def find_all_missing_elements(arr: List[int], start: int = 1, end: Optional[int] = None) -> List[int]:
    """
    Finds all missing numbers in an array within a given inclusive range [start, end].

    Args:
        arr: List of integers.
        start: Start of inclusive target range (default 1).
        end: End of inclusive target range. If None, defaults to max(arr) or start.

    Returns:
        Sorted list of all missing integers in the range.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If start > end.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    if not isinstance(start, int):
        raise TypeError(f"Expected int for start, got {type(start).__name__}")

    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    if end is None:
        end = max(arr) if arr else start

    if not isinstance(end, int):
        raise TypeError(f"Expected int for end, got {type(end).__name__}")
    if start > end:
        raise ValueError(f"Invalid range: start {start} > end {end}")

    present_set = set(arr)
    missing_list = [num for num in range(start, end + 1) if num not in present_set]
    return missing_list


def find_missing_element_shuffled(arr1: List[Any], arr2: List[Any]) -> Any:
    """
    Finds the single element present in arr1 but missing in shuffled arr2 (handles duplicates).

    Args:
        arr1: Original list of elements.
        arr2: Shuffled list with one element missing.

    Returns:
        The missing element.

    Raises:
        TypeError: If inputs are not lists/tuples.
        ValueError: If len(arr1) != len(arr2) + 1 or no missing element found.
    """
    if not isinstance(arr1, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr1, got {type(arr1).__name__}")
    if not isinstance(arr2, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr2, got {type(arr2).__name__}")

    if len(arr1) != len(arr2) + 1:
        raise ValueError(f"arr1 length ({len(arr1)}) must be exactly 1 greater than arr2 length ({len(arr2)})")

    counts: Dict[Any, int] = {}
    for item in arr1:
        counts[item] = counts.get(item, 0) + 1

    for item in arr2:
        if item in counts:
            counts[item] -= 1
            if counts[item] == 0:
                del counts[item]
        else:
            raise ValueError(f"Element {item} in arr2 was not present in arr1.")

    if len(counts) == 1:
        return next(iter(counts.keys()))

    raise ValueError("Failed to find unique missing element between arrays.")

