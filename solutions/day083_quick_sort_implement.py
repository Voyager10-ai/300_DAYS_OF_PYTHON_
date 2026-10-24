# Day 83: Quick Sort Implement
#
# Problem:
#   Write a Python program / module implementing Quick Sort (Divide and Conquer Partitioning)
#   and its advanced algorithmic variations.
#   Includes core pure and in-place quick sort with Lomuto and Hoare partition schemes,
#   median-of-three and randomized pivot selection, Dutch National Flag 3-way partitioning,
#   iterative stack-based quick sort with tail-call optimization, Hoare's Quickselect algorithm
#   for O(n) order statistics, step-by-step partition trace visualizer, instability verification,
#   performance analytics benchmarks, exhaustive unit test suite, and Java practice code.

import random
import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Core Quick Sort & Partition Schemes (Lomuto & Hoare) ─────────────────


def lomuto_partition(
    arr: List[Any],
    low: int,
    high: int,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Lomuto partition scheme:
    Uses the last element arr[high] as pivot and maintains a single scan pointer i.
    Elements <= pivot (or >= if reverse) are moved to the left by swapping.

    Args:
        arr: Mutable list.
        low: Start index of sub-array.
        high: End index of sub-array (contains pivot).
        reverse: If True, partitions for descending order.
        key: Optional comparison projection.

    Returns:
        Final index where the pivot is placed.
    """
    key_func = key if key is not None else (lambda x: x)
    pivot_val = key_func(arr[high])
    i = low - 1

    for j in range(low, high):
        val_j = key_func(arr[j])
        cond = (val_j >= pivot_val) if reverse else (val_j <= pivot_val)
        if cond:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def hoare_partition(
    arr: List[Any],
    low: int,
    high: int,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Hoare's original 1961 bidirectional partition scheme:
    Two pointers scan inward from low and high until elements that belong on opposite sides
    are found, then swaps them. Executes ~3x fewer swaps than Lomuto.

    Args:
        arr: Mutable list.
        low: Start index.
        high: End index.
        reverse: If True, partitions for descending order.
        key: Optional comparison projection.

    Returns:
        Split point index p such that arr[low..p] <= arr[p+1..high] (or >= if reverse).
    """
    key_func = key if key is not None else (lambda x: x)
    pivot_val = key_func(arr[low])
    i = low - 1
    j = high + 1

    while True:
        if not reverse:
            i += 1
            while key_func(arr[i]) < pivot_val:
                i += 1
            j -= 1
            while key_func(arr[j]) > pivot_val:
                j -= 1
        else:
            i += 1
            while key_func(arr[i]) > pivot_val:
                i += 1
            j -= 1
            while key_func(arr[j]) < pivot_val:
                j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]


def quick_sort(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
    scheme: str = "hoare",
) -> List[Any]:
    """
    Sorts a sequence using Quick Sort and returns a new sorted list (pure function).

    Average Time Complexity: O(n log n).
    Worst-case Time Complexity: O(n^2).
    Space Complexity: O(n) for copy, O(log n) auxiliary call stack.

    Args:
        arr: Input sequence (list or tuple).
        reverse: If True, sorts descending.
        key: Comparison key function.
        scheme: 'hoare' or 'lomuto'.

    Returns:
        New sorted list.

    Raises:
        TypeError: If arr is not list or tuple.
        ValueError: If scheme is unknown.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    quick_sort_inplace(copied, reverse=reverse, key=key, scheme=scheme)
    return copied


def quick_sort_inplace(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
    scheme: str = "hoare",
) -> None:
    """
    Sorts a mutable list in-place using Quick Sort.

    Args:
        arr: Mutable list to sort in-place.
        reverse: If True, sorts descending.
        key: Key projection function.
        scheme: 'hoare' or 'lomuto'.

    Raises:
        TypeError: If arr is not a mutable list.
        ValueError: If scheme is unrecognized.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    scheme_lower = scheme.lower().strip()
    if scheme_lower not in ("hoare", "lomuto"):
        raise ValueError(f"Unknown partition scheme '{scheme}', expected 'hoare' or 'lomuto'")

    n = len(arr)
    if n <= 1:
        return

    def _quick_sort(low: int, high: int) -> None:
        if low < high:
            if scheme_lower == "lomuto":
                p = lomuto_partition(arr, low, high, reverse=reverse, key=key)
                _quick_sort(low, p - 1)
                _quick_sort(p + 1, high)
            else:  # hoare
                p = hoare_partition(arr, low, high, reverse=reverse, key=key)
                _quick_sort(low, p)
                _quick_sort(p + 1, high)

    _quick_sort(0, n - 1)


def quick_sort_metrics(
    arr: List[Any],
    reverse: bool = False,
    scheme: str = "hoare",
) -> Tuple[List[Any], Dict[str, Any]]:
    """
    Sorts a copy of arr while profiling comparisons, swaps, and maximum recursion depth.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        scheme: 'hoare' or 'lomuto'.

    Returns:
        Tuple of (sorted_list, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    comparisons = 0
    swaps = 0
    max_depth = 0

    if n <= 1:
        return (items, {"comparisons": 0, "swaps": 0, "max_depth": 0, "scheme": scheme})

    def _lomuto_profiled(low: int, high: int) -> int:
        nonlocal comparisons, swaps
        pivot_val = items[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            cond = (items[j] >= pivot_val) if reverse else (items[j] <= pivot_val)
            if cond:
                i += 1
                if i != j:
                    items[i], items[j] = items[j], items[i]
                    swaps += 1
        if i + 1 != high:
            items[i + 1], items[high] = items[high], items[i + 1]
            swaps += 1
        return i + 1

    def _hoare_profiled(low: int, high: int) -> int:
        nonlocal comparisons, swaps
        pivot_val = items[low]
        i = low - 1
        j = high + 1
        while True:
            if not reverse:
                i += 1
                while True:
                    comparisons += 1
                    if items[i] >= pivot_val:
                        break
                    i += 1
                j -= 1
                while True:
                    comparisons += 1
                    if items[j] <= pivot_val:
                        break
                    j -= 1
            else:
                i += 1
                while True:
                    comparisons += 1
                    if items[i] <= pivot_val:
                        break
                    i += 1
                j -= 1
                while True:
                    comparisons += 1
                    if items[j] >= pivot_val:
                        break
                    j -= 1

            if i >= j:
                return j
            items[i], items[j] = items[j], items[i]
            swaps += 1

    def _sort(low: int, high: int, depth: int) -> None:
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        if low < high:
            if scheme.lower() == "lomuto":
                p = _lomuto_profiled(low, high)
                _sort(low, p - 1, depth + 1)
                _sort(p + 1, high, depth + 1)
            else:
                p = _hoare_profiled(low, high)
                _sort(low, p, depth + 1)
                _sort(p + 1, high, depth + 1)

    _sort(0, n - 1, depth=1)
    metrics = {
        "comparisons": comparisons,
        "swaps": swaps,
        "max_depth": max_depth,
        "scheme": scheme,
        "length": n,
    }
    return (items, metrics)


# ─── 2. Randomized & Median-of-Three Pivot Selection Strategies ───────────────


def select_pivot_index(
    arr: List[Any],
    low: int,
    high: int,
    strategy: str = "median_of_three",
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Selects a pivot index based on strategy to prevent O(n^2) worst-case degradation.

    Strategies:
      - 'first': Returns low.
      - 'last': Returns high.
      - 'random': Returns uniform random index in [low, high].
      - 'median_of_three': Inspects arr[low], arr[mid], arr[high] and returns the index
                           of the median element. Standard in production sorts (qsort/Introsort).

    Args:
        arr: Sequence of elements.
        low: Sub-array lower bound.
        high: Sub-array upper bound.
        strategy: 'median_of_three', 'random', 'first', or 'last'.
        key: Key projection function.

    Returns:
        Index of the chosen pivot.

    Raises:
        ValueError: If strategy is unrecognized.
    """
    strat = strategy.lower().strip()
    if strat == "first":
        return low
    elif strat == "last":
        return high
    elif strat == "random":
        return random.randint(low, high)
    elif strat == "median_of_three":
        mid = low + (high - low) // 2
        key_func = key if key is not None else (lambda x: x)
        a = key_func(arr[low])
        b = key_func(arr[mid])
        c = key_func(arr[high])

        # Find median of {a, b, c}
        if (a <= b <= c) or (c <= b <= a):
            return mid
        elif (b <= a <= c) or (c <= a <= b):
            return low
        else:
            return high
    else:
        raise ValueError(f"Unknown pivot strategy: {strategy}")


def quick_sort_with_pivot(
    arr: List[Any],
    strategy: str = "median_of_three",
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Pure Quick Sort applying a specified pivot selection strategy.
    Prevents degenerate O(n^2) complexity on sorted or adversarial inputs.

    Args:
        arr: Input sequence.
        strategy: 'median_of_three', 'random', 'first', or 'last'.
        reverse: If True, sorts descending.
        key: Comparison key function.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    if n <= 1:
        return items

    def _quick_sort(low: int, high: int) -> None:
        if low < high:
            # Select pivot and swap with low to integrate with Hoare partition
            pivot_idx = select_pivot_index(items, low, high, strategy=strategy, key=key)
            items[low], items[pivot_idx] = items[pivot_idx], items[low]

            p = hoare_partition(items, low, high, reverse=reverse, key=key)
            _quick_sort(low, p)
            _quick_sort(p + 1, high)

    _quick_sort(0, n - 1)
    return items


# ─── 3. Dutch National Flag 3-Way Quick Sort (Dijkstra's Fat Partition) ────────


def dutch_flag_partition(
    arr: List[Any],
    low: int,
    high: int,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> Tuple[int, int]:
    """
    Dijkstra's 3-way Dutch National Flag partition.
    Partitions arr[low..high] into three contiguous sub-slices:
      - arr[low..lt-1]   : elements strictly less than pivot (or greater if reverse)
      - arr[lt..gt]       : elements strictly equal to pivot
      - arr[gt+1..high]  : elements strictly greater than pivot (or less if reverse)

    Args:
        arr: Mutable list.
        low: Start index.
        high: End index.
        reverse: If True, partitions for descending order.
        key: Key projection function.

    Returns:
        Tuple of (lt, gt) boundaries.
    """
    key_func = key if key is not None else (lambda x: x)
    pivot_val = key_func(arr[low])
    lt = low
    gt = high
    i = low + 1

    while i <= gt:
        val_i = key_func(arr[i])
        if not reverse:
            if val_i < pivot_val:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif val_i > pivot_val:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        else:
            if val_i > pivot_val:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif val_i < pivot_val:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1

    return (lt, gt)


def quick_sort_3way(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Sorts a sequence using 3-Way Quick Sort (pure function).
    Achieves O(n) linear performance on inputs with many duplicate keys,
    avoiding the O(n^2) degradation of standard 2-way quicksort.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        key: Comparison key function.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    quick_sort_3way_inplace(copied, reverse=reverse, key=key)
    return copied


def quick_sort_3way_inplace(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> None:
    """
    Sorts a mutable list in-place using 3-way Dutch National Flag Quick Sort.

    Args:
        arr: Mutable list.
        reverse: If True, sorts descending.
        key: Comparison key function.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    def _sort(low: int, high: int) -> None:
        if low < high:
            lt, gt = dutch_flag_partition(arr, low, high, reverse=reverse, key=key)
            _sort(low, lt - 1)
            _sort(gt + 1, high)

    _sort(0, n - 1)


# ─── 4. Iterative Quick Sort & Tail-Call Optimization ─────────────────────────


def iterative_quick_sort(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Non-recursive Quick Sort using an explicit stack of sub-array bounds.
    Guarantees O(log n) maximum stack space by always pushing the larger partition
    to the stack and evaluating the smaller partition first.
    Completely avoids Python's recursion limit.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        key: Comparison key function.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    if n <= 1:
        return items

    stack: List[Tuple[int, int]] = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        p = hoare_partition(items, low, high, reverse=reverse, key=key)

        left_len = p - low + 1
        right_len = high - (p + 1) + 1

        # Push larger partition first so smaller partition is processed immediately,
        # guaranteeing O(log n) maximum stack space
        if left_len > right_len:
            if low < p:
                stack.append((low, p))
            if p + 1 < high:
                stack.append((p + 1, high))
        else:
            if p + 1 < high:
                stack.append((p + 1, high))
            if low < p:
                stack.append((low, p))

    return items


def quick_sort_tail_optimized(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Tail-call optimized recursive Quick Sort.
    Recourses only on the smaller subproblem while iterating on the larger one,
    strictly bounding call-stack depth to O(log n).

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        key: Comparison key projection.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    if n <= 1:
        return items

    def _tail_sort(low: int, high: int) -> None:
        while low < high:
            p = hoare_partition(items, low, high, reverse=reverse, key=key)
            if (p - low) < (high - p):
                _tail_sort(low, p)
                low = p + 1  # Tail loop on larger right subproblem
            else:
                _tail_sort(p + 1, high)
                high = p     # Tail loop on larger left subproblem

    _tail_sort(0, n - 1)
    return items


# ─── 5. Quickselect (Hoare's Selection Algorithm for Order Statistics) ────────


def quickselect(
    arr: List[Any],
    k: int,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> Any:
    """
    Finds the k-th smallest (or largest if reverse=True) element in average O(n) time.
    Uses Lomuto partitioning to place the pivot at its exact sorted index,
    recursing only into the single partition containing index k - 1.

    Args:
        arr: Sequence of items.
        k: 1-indexed order statistic (1 <= k <= len(arr)).
        reverse: If True, finds k-th largest element.
        key: Optional comparison projection.

    Returns:
        The k-th element in sorted order.

    Raises:
        TypeError: If arr is not list or tuple.
        ValueError: If k is out of bounds [1, len(arr)].
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    n = len(arr)
    if k < 1 or k > n:
        raise ValueError(f"k must be in range [1, {n}], got {k}")

    items = list(arr)
    target_idx = k - 1
    low = 0
    high = n - 1

    while low <= high:
        if low == high:
            return items[low]

        # Use median-of-three for robust partitioning
        pivot_idx = select_pivot_index(items, low, high, strategy="median_of_three", key=key)
        items[pivot_idx], items[high] = items[high], items[pivot_idx]

        p = lomuto_partition(items, low, high, reverse=reverse, key=key)

        if p == target_idx:
            return items[p]
        elif p > target_idx:
            high = p - 1
        else:
            low = p + 1

    return items[target_idx]


def find_median_via_quickselect(
    arr: List[Any],
    key: Optional[Callable[[Any], Any]] = None,
) -> Any:
    """
    Finds the median element in O(n) average time using Quickselect.
    For even lengths, returns the lower median element (len(arr) // 2).

    Args:
        arr: Non-empty sequence of items.
        key: Comparison key function.

    Returns:
        The median item.

    Raises:
        ValueError: If arr is empty.
    """
    if not arr:
        raise ValueError("Cannot find median of empty sequence")
    n = len(arr)
    mid_k = (n + 1) // 2
    return quickselect(arr, k=mid_k, reverse=False, key=key)




