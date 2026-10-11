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


# ─── 2. Bidirectional Cocktail Shaker Sort & Comb Sort ────────────────────────


def cocktail_shaker_sort(arr: List[Any], reverse: bool = False) -> List[Any]:
    """
    Sorts a sequence using bidirectional bubble sort (Cocktail Shaker / Ripple Sort).
    Eliminates the 'turtles' problem (small values at the end of the list).

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    copied = list(arr)
    cocktail_shaker_sort_inplace(copied, reverse=reverse)
    return copied


def cocktail_shaker_sort_inplace(arr: List[Any], reverse: bool = False) -> None:
    """
    In-place bidirectional cocktail shaker sort.

    Args:
        arr: Mutable list.
        reverse: If True, sorts descending.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected list for in-place sorting, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    start = 0
    end = n - 1
    swapped = True

    while swapped:
        swapped = False

        # Forward pass (left to right)
        for i in range(start, end):
            condition = (arr[i] < arr[i + 1]) if reverse else (arr[i] > arr[i + 1])
            if condition:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        # Backward pass (right to left)
        for i in range(end - 1, start - 1, -1):
            condition = (arr[i] < arr[i + 1]) if reverse else (arr[i] > arr[i + 1])
            if condition:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        start += 1


def comb_sort(arr: List[Any], reverse: bool = False, shrink_factor: float = 1.3) -> List[Any]:
    """
    Sorts an array using Comb Sort, an optimization over Bubble Sort with gap shrinking.
    Reduces time complexity towards O(n log n) by eliminating distant inversions early.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        shrink_factor: Factor to reduce gap on each pass (ideally 1.3).

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if shrink_factor <= 1.0:
        raise ValueError(f"shrink_factor must be > 1.0, got {shrink_factor}")

    items = list(arr)
    n = len(items)
    gap = n
    swapped = True

    while gap > 1 or swapped:
        gap = int(gap / shrink_factor)
        if gap < 1:
            gap = 1

        swapped = False
        for i in range(0, n - gap):
            condition = (items[i] < items[i + gap]) if reverse else (items[i] > items[i + gap])
            if condition:
                items[i], items[i + gap] = items[i + gap], items[i]
                swapped = True

    return items


# ─── 3. Odd-Even Transposition Sort & Recursive Bubble Sort ──────────────────


def odd_even_sort(arr: List[Any], reverse: bool = False) -> List[Any]:
    """
    Sorts a sequence using Odd-Even Transposition Sort (Brick Sort).
    Alternates between comparing odd-indexed pairs and even-indexed pairs.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    odd_even_sort_inplace(copied, reverse=reverse)
    return copied


def odd_even_sort_inplace(arr: List[Any], reverse: bool = False) -> None:
    """
    In-place odd-even transposition sort.

    Args:
        arr: Mutable list.
        reverse: If True, sorts descending.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected list for in-place sorting, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    is_sorted = False
    while not is_sorted:
        is_sorted = True

        # Odd phase: compare elements at odd indices (1, 3, 5, ...)
        for i in range(1, n - 1, 2):
            condition = (arr[i] < arr[i + 1]) if reverse else (arr[i] > arr[i + 1])
            if condition:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False

        # Even phase: compare elements at even indices (0, 2, 4, ...)
        for i in range(0, n - 1, 2):
            condition = (arr[i] < arr[i + 1]) if reverse else (arr[i] > arr[i + 1])
            if condition:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False


def bubble_sort_recursive(
    arr: List[Any], n: Optional[int] = None, reverse: bool = False
) -> List[Any]:
    """
    Recursive implementation of Bubble Sort.

    Base case: n == 1 (array of 1 element is sorted).
    Recursive step: Execute 1 pass to move maximum element to end, then recurse on n - 1 elements.

    Args:
        arr: Input list.
        n: Length of subarray to consider (defaults to len(arr)).
        reverse: If True, sorts descending.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    _bubble_sort_recursive_helper(copied, len(copied) if n is None else n, reverse=reverse)
    return copied


def _bubble_sort_recursive_helper(arr: List[Any], n: int, reverse: bool = False) -> None:
    """Helper mutating arr recursively."""
    if n <= 1:
        return

    swapped = False
    for i in range(n - 1):
        condition = (arr[i] < arr[i + 1]) if reverse else (arr[i] > arr[i + 1])
        if condition:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
            swapped = True

    # If no swap occurred in this pass, array is already sorted
    if not swapped:
        return

    _bubble_sort_recursive_helper(arr, n - 1, reverse=reverse)


# ─── 4. K-Pass Partial Sorters & Top-K Extraction ────────────────────────────


def bubble_sort_k_passes(arr: List[Any], k: int, reverse: bool = False) -> List[Any]:
    """
    Executes exactly k passes of Bubble Sort.
    After k passes, the k extreme elements are guaranteed to be in their final sorted positions.

    Args:
        arr: Input sequence.
        k: Number of passes to execute (0 <= k <= len(arr)).
        reverse: If True, sorts descending.

    Returns:
        Partially sorted list.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If k < 0.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")
    if k < 0:
        raise ValueError(f"k must be non-negative, got {k}")

    items = list(arr)
    n = len(items)
    effective_k = min(k, n)

    for i in range(effective_k):
        swapped = False
        for j in range(0, n - 1 - i):
            condition = (items[j] < items[j + 1]) if reverse else (items[j] > items[j + 1])
            if condition:
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        if not swapped:
            break

    return items


def find_k_largest_via_bubble(arr: List[Any], k: int) -> List[Any]:
    """
    Finds the k largest elements in O(k * n) time using k passes of standard bubble sort.
    Efficient when k << n without full O(n log n) overhead.

    Args:
        arr: Input list.
        k: Number of largest elements to find.

    Returns:
        List of k largest elements sorted in descending order.

    Raises:
        ValueError: If k < 0 or k > len(arr).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")
    if k < 0 or k > len(arr):
        raise ValueError(f"k must be in range [0, {len(arr)}], got {k}")

    if k == 0:
        return []

    partially_sorted = bubble_sort_k_passes(arr, k, reverse=False)
    # The k largest elements are at the end: partially_sorted[-k:]
    # Return them in descending order
    return list(reversed(partially_sorted[-k:]))


def find_k_smallest_via_bubble(arr: List[Any], k: int) -> List[Any]:
    """
    Finds the k smallest elements in O(k * n) time using k passes of reverse bubble sort.

    Args:
        arr: Input list.
        k: Number of smallest elements to find.

    Returns:
        List of k smallest elements sorted in ascending order.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")
    if k < 0 or k > len(arr):
        raise ValueError(f"k must be in range [0, {len(arr)}], got {k}")

    if k == 0:
        return []

    partially_sorted = bubble_sort_k_passes(arr, k, reverse=True)
    # The k smallest elements are at the end in descending order; reverse to ascending
    return list(reversed(partially_sorted[-k:]))


# ─── 5. Step-by-Step Trace & ASCII Visualizer ─────────────────────────────────


def trace_bubble_sort(arr: List[Any], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Generates a step-by-step pedagogical trace of Bubble Sort comparisons and swaps.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        List of trace event dictionaries.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    trace: List[Dict[str, Any]] = []
    step_num = 1

    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            condition = (items[j] < items[j + 1]) if reverse else (items[j] > items[j + 1])
            swap_done = False
            val_a, val_b = items[j], items[j + 1]

            if condition:
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
                swap_done = True

            trace.append({
                "step": step_num,
                "pass": i + 1,
                "indices": (j, j + 1),
                "compared_values": (val_a, val_b),
                "swapped": swap_done,
                "snapshot": list(items),
            })
            step_num += 1

        if not swapped:
            break

    return trace


def render_ascii_trace(trace: List[Dict[str, Any]], max_events: int = 10) -> str:
    """
    Renders trace events as a clean ASCII diagram.

    Args:
        trace: List of trace events.
        max_events: Maximum events to render.

    Returns:
        Formatted multi-line ASCII string.
    """
    lines: List[str] = []
    lines.append(f"{'Step':<6} | {'Pass':<5} | {'Indices':<9} | {'Action':<10} | {'Array Snapshot'}")
    lines.append("-" * 65)

    displayed = trace[:max_events]
    for ev in displayed:
        action = "SWAP" if ev["swapped"] else "keep"
        idx_str = f"({ev['indices'][0]},{ev['indices'][1]})"
        lines.append(
            f"{ev['step']:<6} | {ev['pass']:<5} | {idx_str:<9} | {action:<10} | {ev['snapshot']}"
        )

    if len(trace) > max_events:
        lines.append(f"... ({len(trace) - max_events} more comparison steps omitted) ...")

    return "\n".join(lines)




