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


# ─── 4. Sequence Metrics & Complexity Analysis Engine ───────────────────────


def analyze_non_repeat_sequence(sequence: Union[str, List[Any]]) -> Dict[str, Any]:
    """
    Analyzes sequence composition, unique elements, max non-repeat window metrics, and ratios.

    Args:
        sequence: Input string or list.

    Returns:
        Dictionary containing detailed composition metrics and ratios.

    Raises:
        TypeError: If sequence is not str/list/tuple.
    """
    if not isinstance(sequence, (str, list, tuple)):
        raise TypeError(f"Expected str, list, or tuple, got {type(sequence).__name__}")

    total_len = len(sequence)
    if total_len == 0:
        empty_sub = "" if isinstance(sequence, str) else []
        return {
            "total_length": 0,
            "unique_element_count": 0,
            "duplicate_element_count": 0,
            "longest_non_repeat_length": 0,
            "non_repeat_ratio": 0.0,
            "unique_ratio": 0.0,
            "longest_subsegment": empty_sub,
            "all_longest_subsegments": [],
        }

    items = list(sequence)
    unique_set = set(items)
    unique_count = len(unique_set)
    duplicate_count = total_len - unique_count

    all_longest = all_longest_non_repeat_subsegments(sequence)
    longest_sub = all_longest[0] if all_longest else sequence[0:0]
    longest_len = len(longest_sub)

    non_repeat_ratio = round((longest_len / total_len) * 100, 2)
    unique_ratio = round((unique_count / total_len) * 100, 2)

    return {
        "total_length": total_len,
        "unique_element_count": unique_count,
        "duplicate_element_count": duplicate_count,
        "longest_non_repeat_length": longest_len,
        "non_repeat_ratio": non_repeat_ratio,
        "unique_ratio": unique_ratio,
        "longest_subsegment": longest_sub,
        "all_longest_subsegments": all_longest,
    }


# ─── 5. Batch Collection Processors ──────────────────────────────────────────


def batch_longest_non_repeat(sequences: List[Union[str, List[Any]]]) -> List[Dict[str, Any]]:
    """
    Processes a collection of sequences and generates analytical summaries for each.

    Args:
        sequences: List of input strings or lists.

    Returns:
        List of analytical summary dictionaries for each sequence.

    Raises:
        TypeError: If sequences is not a list/tuple.
    """
    if not isinstance(sequences, (list, tuple)):
        raise TypeError(f"Expected list or tuple of sequences, got {type(sequences).__name__}")

    return [analyze_non_repeat_sequence(seq) for seq in sequences]


def filter_sequences_by_non_repeat_threshold(
    sequences: List[Union[str, List[Any]]], min_non_repeat_len: int
) -> List[Union[str, List[Any]]]:
    """
    Filters sequences that have a longest non-repeating subsegment length >= min_non_repeat_len.

    Args:
        sequences: List of input sequences (strings or lists).
        min_non_repeat_len: Minimum required non-repeating length threshold.

    Returns:
        Filtered list of qualifying sequences.

    Raises:
        TypeError: If sequences is not a list or min_non_repeat_len is not an int.
        ValueError: If min_non_repeat_len < 0.
    """
    if not isinstance(sequences, (list, tuple)):
        raise TypeError(f"Expected list or tuple for sequences, got {type(sequences).__name__}")
    if not isinstance(min_non_repeat_len, int):
        raise TypeError(f"Expected int for min_non_repeat_len, got {type(min_non_repeat_len).__name__}")
    if min_non_repeat_len < 0:
        raise ValueError("min_non_repeat_len must be >= 0.")

    result = []
    for seq in sequences:
        if isinstance(seq, (str, list, tuple)):
            stats = analyze_non_repeat_sequence(seq)
            if stats["longest_non_repeat_length"] >= min_non_repeat_len:
                result.append(seq)
    return result


# ─── 6. Sequence Transformation & Formatting Helpers ───────────────────────


def collapse_repeats_in_sequence(sequence: Union[str, List[Any]]) -> Union[str, List[Any]]:
    """
    Removes duplicate elements while preserving original order of first occurrence.

    Args:
        sequence: Input string or list.

    Returns:
        Deduplicated string or list of same type.

    Raises:
        TypeError: If sequence is not str/list/tuple.
    """
    if not isinstance(sequence, (str, list, tuple)):
        raise TypeError(f"Expected str, list, or tuple, got {type(sequence).__name__}")

    seen: Set[Any] = set()
    deduped = []
    for item in sequence:
        if item not in seen:
            seen.add(item)
            deduped.append(item)

    if isinstance(sequence, str):
        return "".join(deduped)
    return deduped


def highlight_longest_non_repeat(text: str, marker: str = "***") -> str:
    """
    Highlights the longest non-repeating substring by enclosing it with marker tokens.

    Args:
        text: Input string.
        marker: Surrounding marker string (default '***').

    Returns:
        String with highlighted non-repeating segment.

    Raises:
        TypeError: If text or marker is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str for text, got {type(text).__name__}")
    if not isinstance(marker, str):
        raise TypeError(f"Expected str for marker, got {type(marker).__name__}")
    if not text:
        return ""

    start, end, max_len = get_non_repeat_subsegment_indices(text)
    if max_len == 0:
        return text

    prefix = text[:start]
    target = text[start : end + 1]
    suffix = text[end + 1 :]
    return f"{prefix}{marker}{target}{marker}{suffix}"





