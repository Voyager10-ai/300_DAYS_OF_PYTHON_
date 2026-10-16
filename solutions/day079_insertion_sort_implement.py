# Day 79: Insertion Sort Implement
#
# Problem:
#   Write a Python program / module implementing Insertion Sort and its advanced algorithmic variations.
#   Includes core pure and in-place insertion sort, binary insertion sort, range-bounded slice sorting (Timsort building block),
#   recursive insertion sort, online streaming sorter, step-by-step trace visualizer, shift counter & efficiency analytics,
#   stability verification engine, comprehensive unit test suite, and Java practice.

import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Core Insertion Sort Implementations ───────────────────────────────────


def insertion_sort(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> List[Any]:
    """
    Sorts a sequence using Insertion Sort and returns a new sorted list (pure function).

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
    insertion_sort_inplace(copied, reverse=reverse, key=key)
    return copied


def insertion_sort_inplace(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> None:
    """
    Sorts a list in-place using Insertion Sort (O(n^2) worst/average, O(n) best-case).
    Uses shifting rather than element swaps to minimize write overhead.

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

    for i in range(1, n):
        current_item = arr[i]
        current_key = key_func(current_item)
        j = i - 1

        # Shift elements of arr[0..i-1] that are greater (or smaller if reverse) than current_key
        if not reverse:
            while j >= 0 and key_func(arr[j]) > current_key:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= 0 and key_func(arr[j]) < current_key:
                arr[j + 1] = arr[j]
                j -= 1

        arr[j + 1] = current_item


def insertion_sort_metrics(
    arr: List[Any], reverse: bool = False
) -> Tuple[List[Any], Dict[str, int]]:
    """
    Executes Insertion Sort while recording exact comparisons, shifts, and insertions executed.

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
    shifts = 0
    passes = 0

    for i in range(1, n):
        passes += 1
        key = items[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            condition = (items[j] < key) if reverse else (items[j] > key)
            if condition:
                items[j + 1] = items[j]
                shifts += 1
                j -= 1
            else:
                break

        items[j + 1] = key

    metrics = {
        "comparisons": comparisons,
        "shifts": shifts,
        "passes_executed": passes,
        "total_elements": n,
    }
    return (items, metrics)
