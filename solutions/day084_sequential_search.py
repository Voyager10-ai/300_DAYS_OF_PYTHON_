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


# ─── 2. Self-Organizing Linear Search Algorithms ──────────────────────────────


def move_to_front_search(
    arr: List[Any],
    target: Any,
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Self-organizing search using the Move-To-Front (MTF) heuristic.
    When target is found at index i, moves it directly to index 0.

    Optimizes for non-uniform access distributions (e.g. 80-20 rule / Zipfian workloads),
    converging frequently accessed items towards O(1) retrieval time.

    Args:
        arr: Mutable list.
        target: Target value to search for.
        key: Optional comparison projection.

    Returns:
        Original index where item was found (or -1 if missing).
        Mutates arr in-place moving target to index 0 if found.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list for MTF search, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    for idx in range(len(arr)):
        if key_func(arr[idx]) == target_key:
            # Move item to front
            if idx > 0:
                item = arr.pop(idx)
                arr.insert(0, item)
            return idx

    return -1


def transpose_search(
    arr: List[Any],
    target: Any,
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Self-organizing search using the Transpose heuristic.
    When target is found at index i > 0, swaps it with its immediate predecessor arr[i - 1].

    More conservative than Move-To-Front; prevents one-off outlier queries from displacing
    frequently accessed elements from the front of the list.

    Args:
        arr: Mutable list.
        target: Target value.
        key: Optional comparison projection.

    Returns:
        Original index where item was found (or -1 if missing).
        Mutates arr by swapping with predecessor if found.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list for transpose search, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    for idx in range(len(arr)):
        if key_func(arr[idx]) == target_key:
            if idx > 0:
                arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]
            return idx

    return -1


def frequency_count_search(
    records: List[Dict[str, Any]],
    target_id: Any,
    id_field: str = "id",
    count_field: str = "access_count",
) -> Tuple[int, int]:
    """
    Self-organizing search using explicit Frequency Counts.
    Increments access_count of the target record and shifts it leftward
    to maintain descending order of popularity.

    Args:
        records: List of dictionary records.
        target_id: Identifier value to find.
        id_field: Key name for record identifier.
        count_field: Key name for access frequency counter.

    Returns:
        Tuple of (original_index, updated_frequency). Returns (-1, 0) if missing.
    """
    if not isinstance(records, list):
        raise TypeError(f"Expected list of records, got {type(records).__name__}")

    for idx, rec in enumerate(records):
        if rec.get(id_field) == target_id:
            # Increment count
            rec[count_field] = rec.get(count_field, 0) + 1
            updated_count = rec[count_field]

            # Shift leftward while access_count is greater than predecessor
            curr = idx
            while curr > 0 and records[curr - 1].get(count_field, 0) < updated_count:
                records[curr], records[curr - 1] = records[curr - 1], records[curr]
                curr -= 1

            return (idx, updated_count)

    return (-1, 0)


# ─── 3. Sentinel Linear Search (Knuth's Boundary Check Elimination) ───────────


def sentinel_linear_search(arr: List[Any], target: Any) -> int:
    """
    Executes Sentinel Linear Search (Donald Knuth's optimization).
    Eliminates the array boundary check (i < n) from the inner loop by appending
    target as a guaranteed terminator at the end of a working copy.

    Halves the number of conditional branches evaluated per loop iteration.

    Args:
        arr: Sequence of elements.
        target: Value to search for.

    Returns:
        Index of first occurrence of target, or -1 if missing.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    n = len(arr)
    if n == 0:
        return -1

    # Check last element first so sentinel doesn't mask it
    if arr[n - 1] == target:
        # Check if an earlier occurrence exists
        for i in range(n - 1):
            if arr[i] == target:
                return i
        return n - 1

    # Append sentinel to temporary list copy
    work_list = list(arr)
    work_list.append(target)

    i = 0
    while work_list[i] != target:
        i += 1

    return i if i < n else -1


def sentinel_linear_search_inplace(arr: List[Any], target: Any) -> int:
    """
    In-place Sentinel Linear Search avoiding list reallocation.
    Temporarily replaces the last element arr[n - 1] with the sentinel target,
    executes the boundary-free loop, and restores the original value before returning.

    Args:
        arr: Mutable list.
        target: Value to find.

    Returns:
        Index of target, or -1 if missing.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    if n == 0:
        return -1

    last = arr[n - 1]
    # Place sentinel at the last position
    arr[n - 1] = target

    i = 0
    while arr[i] != target:
        i += 1

    # Restore original last element
    arr[n - 1] = last

    if i < n - 1 or last == target:
        return i
    return -1


def sentinel_search_metrics(
    arr: List[Any], target: Any
) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluates Sentinel Linear Search and calculates boundary conditions saved.

    Args:
        arr: Input sequence.
        target: Target item.

    Returns:
        Tuple of (found_index, metrics_dict).
    """
    n = len(arr)
    idx = sentinel_linear_search(arr, target)
    steps_executed = (idx + 1) if idx != -1 else n

    metrics = {
        "found_index": idx,
        "element_comparisons": steps_executed,
        "boundary_checks_saved": steps_executed,  # Standard search executes steps_executed boundary checks
        "total_checks_standard": steps_executed * 2,
        "total_checks_sentinel": steps_executed + 1,
        "branch_reduction_percent": round(
            ((steps_executed - 1) / max(1, steps_executed * 2)) * 100, 2
        ),
    }
    return (idx, metrics)


