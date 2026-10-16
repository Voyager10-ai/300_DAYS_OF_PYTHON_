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


# ─── 2. Binary Insertion Sort (O(n log n) Comparisons) ───────────────────────


def binary_search_insert_pos(
    arr: List[Any], val: Any, low: int, high: int, reverse: bool = False
) -> int:
    """
    Finds the insertion index for `val` in sorted subsegment `arr[low..high]` using binary search.
    Preserves stability by inserting after equal elements.

    Args:
        arr: List containing sorted elements in arr[low..high].
        val: Target value to place.
        low: Start index.
        high: End index (inclusive).
        reverse: If True, indicates subsegment is descending.

    Returns:
        Insertion index.
    """
    while low <= high:
        mid = (low + high) // 2
        if not reverse:
            if arr[mid] <= val:
                low = mid + 1
            else:
                high = mid - 1
        else:
            if arr[mid] >= val:
                low = mid + 1
            else:
                high = mid - 1
    return low


def binary_insertion_sort(arr: List[Any], reverse: bool = False) -> List[Any]:
    """
    Sorts a sequence using Binary Insertion Sort.
    Reduces total comparisons from O(n^2) to O(n log n) using binary search for placement.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    binary_insertion_sort_inplace(copied, reverse=reverse)
    return copied


def binary_insertion_sort_inplace(arr: List[Any], reverse: bool = False) -> None:
    """
    In-place Binary Insertion Sort.

    Args:
        arr: Mutable list.
        reverse: If True, sorts descending.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    for i in range(1, n):
        selected = arr[i]
        # Find position where selected should be inserted in arr[0..i-1]
        insert_idx = binary_search_insert_pos(arr, selected, 0, i - 1, reverse=reverse)

        # Shift elements from insert_idx to i - 1 one position right
        j = i - 1
        while j >= insert_idx:
            arr[j + 1] = arr[j]
            j -= 1

        arr[insert_idx] = selected


# ─── 3. Range-Bounded Slice Insertion Sort (Timsort Subroutine) ──────────────


def insertion_sort_range(
    arr: List[Any], left: int, right: int, reverse: bool = False
) -> None:
    """
    Sorts a designated subrange arr[left..right] in-place using Insertion Sort.
    This is the fundamental small-chunk optimization routine used in Timsort and Introsort.

    Args:
        arr: Mutable list.
        left: Left boundary index (inclusive).
        right: Right boundary index (inclusive).
        reverse: If True, sorts descending.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If indices are out of bounds or left > right.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")
    if not isinstance(left, int) or isinstance(left, bool):
        raise TypeError(f"Expected int for left, got {type(left).__name__}")
    if not isinstance(right, int) or isinstance(right, bool):
        raise TypeError(f"Expected int for right, got {type(right).__name__}")

    n = len(arr)
    if left < 0 or right >= n or left > right:
        raise ValueError(f"Invalid range [{left}, {right}] for array of length {n}")

    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1

        if not reverse:
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= left and arr[j] < key:
                arr[j + 1] = arr[j]
                j -= 1

        arr[j + 1] = key


def insertion_sort_blocks(arr: List[Any], block_size: int = 16) -> List[Any]:
    """
    Partitions an array into blocks of size `block_size` and sorts each block in-place.
    Serves as the preliminary run-creation step in hybrid algorithms like Timsort.

    Args:
        arr: Input sequence.
        block_size: Size of individual chunks to sort (must be >= 1).

    Returns:
        New list with internally sorted blocks.

    Raises:
        ValueError: If block_size < 1.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if block_size < 1:
        raise ValueError(f"block_size must be >= 1, got {block_size}")

    items = list(arr)
    n = len(items)
    for start in range(0, n, block_size):
        end = min(start + block_size - 1, n - 1)
        insertion_sort_range(items, start, end)

    return items


