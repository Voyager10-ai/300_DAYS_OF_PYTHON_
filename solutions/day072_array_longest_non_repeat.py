# Day 72: Array Longest Non Repeat
#
# Problem:
#   Write a Python program / module to find the longest contiguous subarray or substring without repeating elements/characters.
#   Includes core sliding window algorithms, multi-variant tie finders, subsegment slice extractors,
#   sequence analysis engine, collection batch processors, sequence transformation utilities, unit test suite, and Java practice.

import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Sliding Window Algorithms ───────────────────────────────────────


def longest_non_repeat_subarray(arr: List[Any]) -> Tuple[int, List[Any]]:
    """
    Finds the length and the contiguous subarray of maximum length without duplicate elements using sliding window.

    Args:
        arr: Input list of elements (hashable types).

    Returns:
        Tuple of (max_length, longest_subarray).

    Raises:
        TypeError: If arr is not a list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if not arr:
        return (0, [])

    seen_map: Dict[Any, int] = {}
    left = 0
    max_len = 0
    best_start = 0

    for right, item in enumerate(arr):
        if item in seen_map and seen_map[item] >= left:
            left = seen_map[item] + 1

        seen_map[item] = right
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len
            best_start = left

    return (max_len, list(arr[best_start : best_start + max_len]))


def longest_non_repeat_substring(text: str) -> Tuple[int, str]:
    """
    Finds the length and the substring of maximum length without duplicate characters.

    Args:
        text: Input string.

    Returns:
        Tuple of (max_length, longest_substring).

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str for text, got {type(text).__name__}")
    if not text:
        return (0, "")

    length, sub_list = longest_non_repeat_subarray(list(text))
    return (length, "".join(sub_list))
