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


# ─── 2. Multi-Variant & Custom Constraint Search Algorithms ─────────────────


def all_longest_non_repeat_subsegments(sequence: Union[str, List[Any]]) -> List[Union[str, List[Any]]]:
    """
    Finds all unique subsegments that achieve the maximum non-repeating length (including ties).

    Args:
        sequence: Input string or list.

    Returns:
        List of all non-repeating subsegments of maximum length.

    Raises:
        TypeError: If sequence is neither a string nor a list/tuple.
    """
    if not isinstance(sequence, (str, list, tuple)):
        raise TypeError(f"Expected str, list, or tuple, got {type(sequence).__name__}")
    if not sequence:
        return []

    is_str = isinstance(sequence, str)
    items = list(sequence)

    seen_map: Dict[Any, int] = {}
    left = 0
    max_len = 0
    results: List[Union[str, List[Any]]] = []

    for right, item in enumerate(items):
        if item in seen_map and seen_map[item] >= left:
            left = seen_map[item] + 1

        seen_map[item] = right
        current_len = right - left + 1
        subsegment = sequence[left : right + 1]

        if current_len > max_len:
            max_len = current_len
            results = [subsegment]
        elif current_len == max_len:
            if subsegment not in results:
                results.append(subsegment)

    return results


def longest_k_unique_subsegment(sequence: Union[str, List[Any]], k: int) -> Tuple[int, Union[str, List[Any]]]:
    """
    Finds the length and subsegment containing at most k distinct elements/characters.

    Args:
        sequence: Input string or list.
        k: Maximum number of distinct elements allowed.

    Returns:
        Tuple of (max_length, longest_subsegment).

    Raises:
        TypeError: If sequence is not str/list/tuple or k is not int.
        ValueError: If k < 1.
    """
    if not isinstance(sequence, (str, list, tuple)):
        raise TypeError(f"Expected str, list, or tuple, got {type(sequence).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")
    if k < 1:
        raise ValueError("k must be at least 1.")

    if not sequence:
        return (0, "" if isinstance(sequence, str) else [])

    items = list(sequence)
    left = 0
    freq_map: Dict[Any, int] = {}
    max_len = 0
    best_start = 0

    for right, item in enumerate(items):
        freq_map[item] = freq_map.get(item, 0) + 1

        while len(freq_map) > k:
            left_item = items[left]
            freq_map[left_item] -= 1
            if freq_map[left_item] == 0:
                del freq_map[left_item]
            left += 1

        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len
            best_start = left

    return (max_len, sequence[best_start : best_start + max_len])


# ─── 3. Subsegment Slice Extractors & Indexing Utilities ────────────────────


def get_non_repeat_subsegment_indices(sequence: Union[str, List[Any]]) -> Tuple[int, int, int]:
    """
    Returns start index, end index (inclusive), and length of the longest non-repeating subsegment.

    Args:
        sequence: Input string or list.

    Returns:
        Tuple of (start_index, end_index, max_length). If empty, returns (-1, -1, 0).

    Raises:
        TypeError: If sequence is not str/list/tuple.
    """
    if not isinstance(sequence, (str, list, tuple)):
        raise TypeError(f"Expected str, list, or tuple, got {type(sequence).__name__}")
    if not sequence:
        return (-1, -1, 0)

    items = list(sequence)
    seen_map: Dict[Any, int] = {}
    left = 0
    max_len = 0
    best_start = 0
    best_end = 0

    for right, item in enumerate(items):
        if item in seen_map and seen_map[item] >= left:
            left = seen_map[item] + 1

        seen_map[item] = right
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len
            best_start = left
            best_end = right

    return (best_start, best_end, max_len)


def slice_non_repeat_windows(
    sequence: Union[str, List[Any]], min_length: int = 1
) -> List[Tuple[int, int, Union[str, List[Any]]]]:
    """
    Extracts all maximal non-repeating contiguous windows of length >= min_length.

    Args:
        sequence: Input string or list.
        min_length: Minimum window length to include.

    Returns:
        List of tuples (start_idx, end_idx_inclusive, subsegment).

    Raises:
        TypeError: If sequence is not str/list/tuple.
        ValueError: If min_length < 1.
    """
    if not isinstance(sequence, (str, list, tuple)):
        raise TypeError(f"Expected str, list, or tuple, got {type(sequence).__name__}")
    if min_length < 1:
        raise ValueError("min_length must be at least 1.")

    if not sequence:
        return []

    items = list(sequence)
    n = len(items)
    windows: List[Tuple[int, int, Union[str, List[Any]]]] = []

    for start in range(n):
        seen: Set[Any] = set()
        for end in range(start, n):
            if items[end] in seen:
                break
            seen.add(items[end])
            win_len = end - start + 1
            if win_len >= min_length:
                windows.append((start, end, sequence[start : end + 1]))

    return windows


