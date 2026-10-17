# Day 80: Selection Sort Implement
#
# Problem:
#   Write a Python program / module implementing Selection Sort and its advanced algorithmic variations.
#   Includes core pure and in-place selection sort, bidirectional min-max double selection sort,
#   stable shift-based selection sort, k-pass partial sorters, kth order statistics, recursive selection sort,
#   range-bounded slice sorting, step-by-step trace visualizer, write-minimization memory analytics,
#   comprehensive unit test suite, and Java practice.

import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Core Selection Sort Implementations ───────────────────────────────────


def selection_sort(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> List[Any]:
    """
    Sorts a sequence using Selection Sort and returns a new sorted list (pure function).

    Repeatedly finds the minimum (or maximum) element from the unsorted segment
    and puts it at the beginning of the unsorted segment.

    Args:
        arr: Input sequence (list or tuple).
        reverse: If True, sorts descending.
        key: Optional function of one argument to extract a comparison key.

    Returns:
        New sorted list.

    Raises:
        TypeError: If arr is not a list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    copied = list(arr)
    selection_sort_inplace(copied, reverse=reverse, key=key)
    return copied


def selection_sort_inplace(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> None:
    """
    Sorts a list in-place using standard Selection Sort (O(n^2) comparisons, O(n) swaps).
    Guarantees at most n - 1 write/swap operations, ideal when memory writes are costly.

    Args:
        arr: Mutable list to sort in-place.
        reverse: If True, sorts descending.
        key: Optional key function.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list for in-place sorting, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    key_func = key if key is not None else (lambda x: x)

    for i in range(n - 1):
        target_idx = i
        target_val = key_func(arr[i])

        for j in range(i + 1, n):
            val_j = key_func(arr[j])
            condition = (val_j > target_val) if reverse else (val_j < target_val)
            if condition:
                target_idx = j
                target_val = val_j

        if target_idx != i:
            arr[i], arr[target_idx] = arr[target_idx], arr[i]


def selection_sort_metrics(
    arr: List[Any], reverse: bool = False
) -> Tuple[List[Any], Dict[str, int]]:
    """
    Executes Selection Sort while tracking comparisons, swaps, and redundant passes.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        Tuple of (sorted_list, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        target_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            condition = (items[j] > items[target_idx]) if reverse else (items[j] < items[target_idx])
            if condition:
                target_idx = j

        if target_idx != i:
            items[i], items[target_idx] = items[target_idx], items[i]
            swaps += 1

    metrics = {
        "comparisons": comparisons,
        "swaps": swaps,
        "passes_executed": max(0, n - 1),
        "total_elements": n,
        "max_possible_swaps": max(0, n - 1),
    }
    return (items, metrics)
