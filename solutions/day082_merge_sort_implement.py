# Day 82: Merge Sort Implement
#
# Problem:
#   Write a Python program / module implementing Merge Sort (Divide and Conquer)
#   and its advanced algorithmic variations.
#   Includes core pure and in-place recursive merge sort, bottom-up iterative merge sort,
#   hybrid merge sort with insertion cutoff and skip-merge optimization, heap-based k-way merge,
#   O(n log n) inversion counting engine, step-by-step divide-and-conquer trace visualizer,
#   stability verification engine, performance analytics benchmark, exhaustive unit test suite,
#   and Java practice code.

import time
import heapq
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union, Iterator


# ─── 1. Core Top-Down Recursive Merge Sort ───────────────────────────────────


def merge(
    left: List[Any],
    right: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Merges two sorted lists into a single sorted list while maintaining stability.

    Uses '<=' (or '>=' if reverse) to preserve the relative order of equal keys,
    guaranteeing algorithmic stability.

    Args:
        left: First pre-sorted list.
        right: Second pre-sorted list.
        reverse: If True, merges in descending order.
        key: Optional projection function for comparisons.

    Returns:
        New merged sorted list of length len(left) + len(right).
    """
    key_func = key if key is not None else (lambda x: x)
    merged = []
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        k_left = key_func(left[i])
        k_right = key_func(right[j])

        # Using <= for ascending preserves left-before-right stability on ties
        condition = (k_left >= k_right) if reverse else (k_left <= k_right)
        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements
    if i < len_left:
        merged.extend(left[i:])
    if j < len_right:
        merged.extend(right[j:])

    return merged


def merge_sort(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Sorts a sequence using standard Top-Down Divide-and-Conquer Merge Sort (pure function).

    Guarantees O(n log n) comparisons in all cases (worst, average, and best).
    Space Complexity: O(n) auxiliary.

    Args:
        arr: Input sequence (list or tuple).
        reverse: If True, sorts descending.
        key: Optional comparison key projection.

    Returns:
        New sorted list.

    Raises:
        TypeError: If arr is not a list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return list(arr)

    mid = n // 2
    left_sorted = merge_sort(arr[:mid], reverse=reverse, key=key)
    right_sorted = merge_sort(arr[mid:], reverse=reverse, key=key)

    return merge(left_sorted, right_sorted, reverse=reverse, key=key)


def merge_sort_inplace(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> None:
    """
    Sorts a mutable list in-place using standard Merge Sort with an auxiliary buffer.

    Args:
        arr: Mutable list to sort in-place.
        reverse: If True, sorts descending.
        key: Key projection function.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    sorted_copy = merge_sort(arr, reverse=reverse, key=key)
    for idx, val in enumerate(sorted_copy):
        arr[idx] = val


def merge_sort_metrics(
    arr: List[Any],
    reverse: bool = False,
) -> Tuple[List[Any], Dict[str, Any]]:
    """
    Sorts a sequence using Merge Sort while tracking comparisons, merge operations,
    and maximum recursion depth.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        Tuple of (sorted_list, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    comparisons = 0
    merge_ops = 0
    max_depth = 0

    def _sort_with_profiling(sub: List[Any], depth: int) -> List[Any]:
        nonlocal comparisons, merge_ops, max_depth
        max_depth = max(max_depth, depth)

        m = len(sub)
        if m <= 1:
            return list(sub)

        mid = m // 2
        left = _sort_with_profiling(sub[:mid], depth + 1)
        right = _sort_with_profiling(sub[mid:], depth + 1)

        # Profiled merge
        merged = []
        i = 0
        j = 0
        len_l = len(left)
        len_r = len(right)
        merge_ops += 1

        while i < len_l and j < len_r:
            comparisons += 1
            cond = (left[i] >= right[j]) if reverse else (left[i] <= right[j])
            if cond:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        if i < len_l:
            merged.extend(left[i:])
        if j < len_r:
            merged.extend(right[j:])

        return merged

    sorted_result = _sort_with_profiling(list(arr), depth=1)
    metrics = {
        "comparisons": comparisons,
        "merge_operations": merge_ops,
        "max_recursion_depth": max_depth,
        "input_length": len(arr),
    }
    return (sorted_result, metrics)
