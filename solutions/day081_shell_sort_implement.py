# Day 81: Shell Sort Implement
#
# Problem:
#   Write a Python program / module implementing Shell Sort (Diminishing Increment Sort)
#   and its advanced algorithmic variations.
#   Includes core pure and in-place shell sort, historical and empirical gap sequence generators
#   (Shell, Knuth, Hibbard, Sedgewick, Ciura), comparative gap efficiency analytics,
#   range-bounded slice sorting, step-by-step gap phase trace visualizer, batch processor,
#   multi-attribute record sorter, instability verification engine, comprehensive unit test suite,
#   and Java practice code.

import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Core Shell Sort Implementations ───────────────────────────────────────


def shell_sort(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
    gap_sequence: Optional[Union[str, List[int]]] = None,
) -> List[Any]:
    """
    Sorts a sequence using Shell Sort and returns a new sorted list (pure function).

    Shell Sort is a diminishing increment sort that sorts elements at decreasing gap distances h,
    converting the array into an h-sorted state at each stage until h = 1 (insertion sort).

    Args:
        arr: Input sequence (list or tuple).
        reverse: If True, sorts descending.
        key: Optional function of one argument to extract a comparison key.
        gap_sequence: Optional custom gap sequence or strategy name ('ciura', 'knuth', 'shell', etc.).

    Returns:
        New sorted list.

    Raises:
        TypeError: If arr is not a list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    copied = list(arr)
    shell_sort_inplace(copied, reverse=reverse, key=key, gap_sequence=gap_sequence)
    return copied


def _default_gaps(n: int) -> List[int]:
    """Generates standard Ciura gaps extended by 2.25x for n elements."""
    if n <= 1:
        return []
    base_ciura = [1, 4, 10, 23, 57, 132, 301, 701, 1750]
    gaps = [g for g in base_ciura if g < n]
    if not gaps:
        gaps = [1]
    last = gaps[-1]
    while int(last * 2.25) < n:
        last = int(last * 2.25)
        gaps.append(last)
    gaps.reverse()
    return gaps


def shell_sort_inplace(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
    gap_sequence: Optional[Union[str, List[int]]] = None,
) -> None:
    """
    Sorts a list in-place using Shell Sort.
    Eliminates inversions between widely separated elements before fine-grained passes,
    avoiding the O(n^2) worst-case of basic insertion sort.

    Args:
        arr: Mutable list to sort in-place.
        reverse: If True, sorts descending.
        key: Optional key projection function.
        gap_sequence: Explicit list of decreasing gaps or strategy name.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list for in-place sorting, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    # Determine gaps
    if gap_sequence is None or gap_sequence == "ciura":
        gaps = _default_gaps(n)
    elif isinstance(gap_sequence, list):
        gaps = [g for g in gap_sequence if 0 < g < n]
        if not gaps or gaps[-1] != 1:
            gaps.append(1)
    else:
        gaps = _default_gaps(n)

    key_func = key if key is not None else (lambda x: x)

    for gap in gaps:
        for i in range(gap, n):
            temp_item = arr[i]
            temp_key = key_func(temp_item)
            j = i

            while j >= gap:
                prev_key = key_func(arr[j - gap])
                condition = (prev_key < temp_key) if reverse else (prev_key > temp_key)
                if condition:
                    arr[j] = arr[j - gap]
                    j -= gap
                else:
                    break

            arr[j] = temp_item


def shell_sort_metrics(
    arr: List[Any],
    reverse: bool = False,
    gap_sequence: Optional[Union[str, List[int]]] = None,
) -> Tuple[List[Any], Dict[str, Any]]:
    """
    Sorts a copy of arr while profiling comparisons, element shifts, and gap phases.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        gap_sequence: Gap sequence to use.

    Returns:
        Tuple of (sorted_list, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    if n <= 1:
        return (items, {"comparisons": 0, "shifts": 0, "gaps_applied": [], "gap_count": 0})

    if gap_sequence is None or gap_sequence == "ciura":
        gaps = _default_gaps(n)
    elif isinstance(gap_sequence, list):
        gaps = [g for g in gap_sequence if 0 < g < n]
        if not gaps or gaps[-1] != 1:
            gaps.append(1)
    else:
        gaps = _default_gaps(n)

    comparisons = 0
    shifts = 0
    phase_stats = []

    for gap in gaps:
        phase_comp = 0
        phase_shifts = 0

        for i in range(gap, n):
            temp_item = items[i]
            j = i

            while j >= gap:
                phase_comp += 1
                condition = (items[j - gap] < temp_item) if reverse else (items[j - gap] > temp_item)
                if condition:
                    items[j] = items[j - gap]
                    phase_shifts += 1
                    j -= gap
                else:
                    break

            items[j] = temp_item

        comparisons += phase_comp
        shifts += phase_shifts
        phase_stats.append({
            "gap": gap,
            "comparisons": phase_comp,
            "shifts": phase_shifts,
        })

    metrics = {
        "comparisons": comparisons,
        "shifts": shifts,
        "gaps_applied": gaps,
        "gap_count": len(gaps),
        "phase_breakdown": phase_stats,
    }
    return (items, metrics)
