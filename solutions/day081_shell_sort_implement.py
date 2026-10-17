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

    gaps = get_gap_sequence(gap_sequence if gap_sequence is not None else "ciura", n)
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
        gap_sequence: Gap sequence to use ('ciura', 'knuth', 'shell', 'sedgewick', 'hibbard', or List[int]).

    Returns:
        Tuple of (sorted_list, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    if n <= 1:
        return (items, {"comparisons": 0, "shifts": 0, "gaps_applied": [], "gap_count": 0, "phase_breakdown": []})

    gaps = get_gap_sequence(gap_sequence if gap_sequence is not None else "ciura", n)
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


# ─── 2. Historical & Optimized Gap Sequence Generators ────────────────────────


def generate_shell_gaps(n: int) -> List[int]:
    """
    Donald Shell's original 1959 sequence: floor(n / 2^k).
    Worst-case time complexity: O(n^2).

    Args:
        n: Number of elements.

    Returns:
        Decreasing list of gaps ending in 1.
    """
    if n <= 1:
        return []
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    return gaps


def generate_knuth_gaps(n: int) -> List[int]:
    """
    Donald Knuth's 1973 sequence: h = 3*h + 1 => (3^k - 1) / 2.
    Gaps: 1, 4, 13, 40, 121, 364, 1093, ...
    Worst-case time complexity: O(n^(3/2)).

    Args:
        n: Number of elements.

    Returns:
        Decreasing list of gaps ending in 1.
    """
    if n <= 1:
        return []
    gaps = []
    h = 1
    while h < n:
        gaps.append(h)
        h = 3 * h + 1
    gaps.reverse()
    return gaps if gaps else [1]


def generate_hibbard_gaps(n: int) -> List[int]:
    """
    Hibbard's 1963 sequence: 2^k - 1.
    Gaps: 1, 3, 7, 15, 31, 63, 127, 255, ...
    Worst-case time complexity: O(n^(3/2)).

    Args:
        n: Number of elements.

    Returns:
        Decreasing list of gaps ending in 1.
    """
    if n <= 1:
        return []
    gaps = []
    k = 1
    while True:
        h = (1 << k) - 1
        if h >= n:
            break
        gaps.append(h)
        k += 1
    gaps.reverse()
    return gaps if gaps else [1]


def generate_sedgewick_gaps(n: int) -> List[int]:
    """
    Robert Sedgewick's 1982/1986 sequence interleaving:
    9 * (4^k - 2^k) + 1  and  4^(k+1) + 3 * 2^k + 1.
    Gaps: 1, 5, 19, 41, 109, 209, 505, 929, 2161, 3905, ...
    Worst-case time complexity: O(n^(4/3)).

    Args:
        n: Number of elements.

    Returns:
        Decreasing list of gaps ending in 1.
    """
    if n <= 1:
        return []
    gap_set = set()
    k = 0
    while True:
        term1 = 9 * (4**k - 2**k) + 1
        term2 = 4 ** (k + 1) + 3 * (2**k) + 1
        if term1 < n:
            gap_set.add(term1)
        if term2 < n:
            gap_set.add(term2)
        if term1 >= n and term2 >= n:
            break
        k += 1

    gaps = sorted(gap_set, reverse=True)
    return gaps if gaps else [1]


def generate_ciura_gaps(n: int) -> List[int]:
    """
    Marcin Ciura's 2001 empirical gap sequence, proven most efficient for practical inputs:
    [1, 4, 10, 23, 57, 132, 301, 701, 1750], extended by floor(gap * 2.25).
    Optimized for modern cache hierarchies.

    Args:
        n: Number of elements.

    Returns:
        Decreasing list of gaps ending in 1.
    """
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


def get_gap_sequence(strategy: Union[str, List[int]], n: int) -> List[int]:
    """
    Resolves a gap sequence by strategy name or validates a custom gap list.

    Args:
        strategy: 'ciura', 'knuth', 'sedgewick', 'hibbard', 'shell', or custom List[int].
        n: Number of elements.

    Returns:
        Sorted decreasing list of positive gaps ending with 1.
    """
    if isinstance(strategy, list):
        filtered = sorted([g for g in strategy if 0 < g < n], reverse=True)
        if not filtered or filtered[-1] != 1:
            filtered.append(1)
        return filtered

    strat = str(strategy).lower().strip()
    if strat == "shell":
        return generate_shell_gaps(n)
    elif strat == "knuth":
        return generate_knuth_gaps(n)
    elif strat == "hibbard":
        return generate_hibbard_gaps(n)
    elif strat == "sedgewick":
        return generate_sedgewick_gaps(n)
    elif strat == "ciura":
        return generate_ciura_gaps(n)
    else:
        raise ValueError(f"Unknown gap sequence strategy: {strategy}")

