# Day 84: Sequential Search
#
# Problem:
#   Write a Python program / module implementing Sequential Search (Linear Search)
#   and its advanced algorithmic variations.
#   Includes core pure sequential search (first, last, all occurrences), metrics profiling,
#   self-organizing search (Move-to-Front and Transpose heuristics), Knuth's sentinel search,
#   ordered sequential search with early exit, predicate-based matching, step-by-step
#   ASCII traversal visualizer, self-organizing benchmark engine, exhaustive unit test suite,
#   and Java practice code.

import time
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Core Sequential Search Implementations ────────────────────────────────


def sequential_search(
    arr: List[Any],
    target: Any,
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Finds the first index of target in arr using standard Linear / Sequential Search.

    Time Complexity:
      - Best Case: O(1) (target is at index 0)
      - Average Case: O(n / 2) = O(n)
      - Worst Case: O(n) (target is at the end or not present)
    Space Complexity: O(1) auxiliary.

    Args:
        arr: Sequence of elements (list or tuple).
        target: Target value to find.
        key: Optional projection function applied to each element before comparison.

    Returns:
        0-based index of the first occurrence of target, or -1 if not found.

    Raises:
        TypeError: If arr is not a list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    for idx, item in enumerate(arr):
        if key_func(item) == target_key:
            return idx

    return -1


def sequential_search_last(
    arr: List[Any],
    target: Any,
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Finds the last occurrence of target by scanning backwards from the end.

    Args:
        arr: Sequence of elements.
        target: Target value to search for.
        key: Optional comparison projection.

    Returns:
        Index of the last occurrence of target, or -1 if not found.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    for idx in range(len(arr) - 1, -1, -1):
        if key_func(arr[idx]) == target_key:
            return idx

    return -1


def sequential_search_all(
    arr: List[Any],
    target: Any,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[int]:
    """
    Finds all 0-based indices where target occurs in arr.

    Args:
        arr: Sequence of elements.
        target: Target value.
        key: Optional comparison projection.

    Returns:
        List of matching indices (empty list if not found).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    matches = []
    for idx, item in enumerate(arr):
        if key_func(item) == target_key:
            matches.append(idx)

    return matches


def sequential_search_metrics(
    arr: List[Any],
    target: Any,
    key: Optional[Callable[[Any], Any]] = None,
) -> Tuple[int, Dict[str, Any]]:
    """
    Searches for target while profiling comparisons executed and array traversal coverage.

    Args:
        arr: Sequence of elements.
        target: Target item.
        key: Optional comparison projection.

    Returns:
        Tuple of (found_index, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    comparisons = 0
    found_idx = -1
    n = len(arr)

    for idx, item in enumerate(arr):
        comparisons += 1
        if key_func(item) == target_key:
            found_idx = idx
            break

    traversal_ratio = round((comparisons / n) * 100, 2) if n > 0 else 0.0

    metrics = {
        "found": (found_idx != -1),
        "index": found_idx,
        "comparisons": comparisons,
        "total_elements": n,
        "traversal_percent": traversal_ratio,
        "efficiency": "Best Case (O(1))" if comparisons == 1 and found_idx == 0 else (
            "Worst Case (O(n))" if comparisons == n else "Average Case (O(n))"
        ),
    }
    return (found_idx, metrics)
