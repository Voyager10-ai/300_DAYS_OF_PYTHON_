# Day 78: Bubble Sort Implement
#
# Problem:
#   Write a Python program / module implementing Bubble Sort and its advanced algorithmic variations.
#   Includes core in-place and pure bubble sort, early-exit optimization, bidirectional cocktail shaker sort,
#   comb sort, odd-even brick sort, recursive bubble sort, k-pass partial sorters, inversion counter,
#   sortedness metrics engine, step-by-step trace visualizer, unit test suite, and Java practice.

import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Core Bubble Sort Implementations ──────────────────────────────────────


def bubble_sort(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> List[Any]:
    """
    Sorts a sequence using standard Bubble Sort and returns a new sorted list (pure function).

    Args:
        arr: Input list or tuple of comparable items.
        reverse: If True, sorts in descending order.
        key: Optional function of one argument to extract a comparison key.

    Returns:
        New sorted list.

    Raises:
        TypeError: If arr is not a list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    copied = list(arr)
    bubble_sort_inplace(copied, reverse=reverse, key=key)
    return copied


def bubble_sort_inplace(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> None:
    """
    Sorts a list in-place using Bubble Sort with early-exit optimization (O(n^2) worst, O(n) best).

    Args:
        arr: Mutable list to sort in-place.
        reverse: If True, sorts in descending order.
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

    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - 1 - i):
            val_a = key_func(arr[j])
            val_b = key_func(arr[j + 1])

            condition = (val_a < val_b) if reverse else (val_a > val_b)
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # If no two elements were swapped by inner loop, array is sorted
        if not swapped:
            break


def bubble_sort_optimized(
    arr: List[Any], reverse: bool = False
) -> Tuple[List[Any], Dict[str, int]]:
    """
    Executes Bubble Sort while tracking comparative execution metrics (comparisons, swaps, passes).

    Args:
        arr: Input list.
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
    passes = 0

    for i in range(n):
        swapped = False
        passes += 1
        for j in range(0, n - 1 - i):
            comparisons += 1
            condition = (items[j] < items[j + 1]) if reverse else (items[j] > items[j + 1])
            if condition:
                items[j], items[j + 1] = items[j + 1], items[j]
                swaps += 1
                swapped = True

        if not swapped:
            break

    metrics = {
        "comparisons": comparisons,
        "swaps": swaps,
        "passes_executed": passes,
        "total_elements": n,
    }
    return (items, metrics)
