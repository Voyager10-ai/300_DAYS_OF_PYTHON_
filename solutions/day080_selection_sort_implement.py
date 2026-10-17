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


# ─── 2. Bidirectional Double Selection Sort (Min-Max) ─────────────────────────


def double_selection_sort(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> List[Any]:
    """
    Pure bidirectional selection sort placing min and max in each pass.
    Reduces total passes from n - 1 to floor(n / 2).

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        key: Optional comparison key function.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    double_selection_sort_inplace(copied, reverse=reverse, key=key)
    return copied


def double_selection_sort_inplace(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> None:
    """
    In-place bidirectional selection sort (cocktail / min-max selection sort).
    Carefully handles the edge case where the max element resides at the left boundary
    before the min element is swapped.

    Args:
        arr: Mutable list.
        reverse: If True, sorts descending.
        key: Key projection function.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    key_func = key if key is not None else (lambda x: x)
    left = 0
    right = n - 1

    while left < right:
        min_idx = left
        max_idx = left
        min_val = key_func(arr[left])
        max_val = min_val

        for i in range(left + 1, right + 1):
            val = key_func(arr[i])
            if val < min_val:
                min_idx = i
                min_val = val
            elif val > max_val:
                max_idx = i
                max_val = val

        # If all elements in range are identical, subarray is already sorted
        if min_val == max_val:
            break

        if not reverse:
            # Ascending: place min at left, max at right
            if min_idx != left:
                arr[left], arr[min_idx] = arr[min_idx], arr[left]
                # If maximum was at left, it was swapped to min_idx
                if max_idx == left:
                    max_idx = min_idx

            if max_idx != right:
                arr[right], arr[max_idx] = arr[max_idx], arr[right]
        else:
            # Descending: place max at left, min at right
            if max_idx != left:
                arr[left], arr[max_idx] = arr[max_idx], arr[left]
                # If minimum was at left, it was swapped to max_idx
                if min_idx == left:
                    min_idx = max_idx

            if min_idx != right:
                arr[right], arr[min_idx] = arr[min_idx], arr[right]

        left += 1
        right -= 1

