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


# ─── 3. Stable Selection Sort & Stability Verification ────────────────────────


def stable_selection_sort(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> List[Any]:
    """
    Stable variation of Selection Sort.
    Standard selection sort is unstable because long-distance swaps can move an element
    past an identical element. Stable selection sort fixes this by shifting elements
    between index i and min_idx one position right instead of swapping.

    Time Complexity: O(n^2) comparisons, O(n^2) element shifts.
    Space Complexity: O(n) for pure list copy, O(1) auxiliary.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        key: Optional comparison key function.

    Returns:
        New sorted list preserving relative order of equal keys.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    if n <= 1:
        return items

    key_func = key if key is not None else (lambda x: x)

    for i in range(n - 1):
        target_idx = i
        target_val = key_func(items[i])

        for j in range(i + 1, n):
            val_j = key_func(items[j])
            condition = (val_j > target_val) if reverse else (val_j < target_val)
            if condition:
                target_idx = j
                target_val = val_j

        # Shift elements rightward instead of swapping to preserve stability
        if target_idx != i:
            selected_item = items[target_idx]
            for k in range(target_idx, i, -1):
                items[k] = items[k - 1]
            items[i] = selected_item

    return items


def verify_selection_sort_stability() -> Dict[str, Any]:
    """
    Verifies that standard selection sort is unstable on tied keys,
    whereas stable_selection_sort preserves relative input order.

    Returns:
        Dictionary with stability verification results and before/after pairs.
    """
    # Sample with tied primary keys and distinctive tag values
    test_cases = [
        [(4, "alpha"), (4, "beta"), (2, "gamma"), (4, "delta"), (1, "epsilon")],
        [(3, "first"), (2, "apple"), (3, "second"), (3, "third"), (1, "banana")],
    ]

    results = []
    for case in test_cases:
        # Sort using standard selection sort by key (first tuple item)
        std_sorted = selection_sort(case, key=lambda x: x[0])
        # Sort using stable selection sort by key
        stable_sorted = stable_selection_sort(case, key=lambda x: x[0])

        # Check relative order of equal keys
        def is_stable(original, sorted_arr):
            for i in range(len(sorted_arr) - 1):
                if sorted_arr[i][0] == sorted_arr[i + 1][0]:
                    orig_pos_i = original.index(sorted_arr[i])
                    orig_pos_next = original.index(sorted_arr[i + 1])
                    if orig_pos_i > orig_pos_next:
                        return False
            return True

        std_stable = is_stable(case, std_sorted)
        stb_stable = is_stable(case, stable_sorted)

        results.append({
            "original": case,
            "standard_sorted": std_sorted,
            "standard_stable": std_stable,
            "stable_sorted": stable_sorted,
            "stable_algorithm_stable": stb_stable,
        })

    return {
        "all_cases_passed": all(r["stable_algorithm_stable"] for r in results),
        "standard_sort_unstable_demonstrated": any(not r["standard_stable"] for r in results),
        "case_studies": results,
    }


# ─── 4. K-Pass Partial Sorter & Order Statistics ──────────────────────────────


def selection_sort_k_passes(
    arr: List[Any],
    k: int,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Executes exactly min(k, n - 1) passes of Selection Sort.
    Guarantees that the first k elements are the k extreme values in fully sorted order.
    Runs in O(k * n) time and O(n) space, highly efficient when k << n.

    Args:
        arr: Input sequence.
        k: Number of passes (0 <= k <= len(arr)).
        reverse: If True, finds k largest in descending order.
        key: Optional projection function.

    Returns:
        List where arr[:k] contains the first k sorted items.

    Raises:
        TypeError: If arr is invalid.
        ValueError: If k is negative.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if k < 0:
        raise ValueError(f"k must be non-negative, got {k}")

    items = list(arr)
    n = len(items)
    if n <= 1 or k == 0:
        return items

    key_func = key if key is not None else (lambda x: x)
    passes_to_run = min(k, n - 1)

    for i in range(passes_to_run):
        target_idx = i
        target_val = key_func(items[i])

        for j in range(i + 1, n):
            val_j = key_func(items[j])
            condition = (val_j > target_val) if reverse else (val_j < target_val)
            if condition:
                target_idx = j
                target_val = val_j

        if target_idx != i:
            items[i], items[target_idx] = items[target_idx], items[i]

    return items


def find_kth_smallest_via_selection(
    arr: List[Any], k: int, key: Optional[Callable[[Any], Any]] = None
) -> Any:
    """
    Finds the k-th smallest element (1-indexed) using k passes of Selection Sort in O(k * n) time.

    Args:
        arr: Sequence of elements.
        k: 1-indexed order statistic (1 <= k <= len(arr)).
        key: Optional comparison projection.

    Returns:
        The k-th smallest element.

    Raises:
        ValueError: If k is outside [1, len(arr)].
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    n = len(arr)
    if k < 1 or k > n:
        raise ValueError(f"k must be in range [1, {n}], got {k}")

    partially_sorted = selection_sort_k_passes(arr, k=k, reverse=False, key=key)
    return partially_sorted[k - 1]


def find_kth_largest_via_selection(
    arr: List[Any], k: int, key: Optional[Callable[[Any], Any]] = None
) -> Any:
    """
    Finds the k-th largest element (1-indexed) using k passes of Selection Sort in O(k * n) time.

    Args:
        arr: Sequence of elements.
        k: 1-indexed order statistic (1 <= k <= len(arr)).
        key: Optional comparison projection.

    Returns:
        The k-th largest element.

    Raises:
        ValueError: If k is outside [1, len(arr)].
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    n = len(arr)
    if k < 1 or k > n:
        raise ValueError(f"k must be in range [1, {n}], got {k}")

    partially_sorted = selection_sort_k_passes(arr, k=k, reverse=True, key=key)
    return partially_sorted[k - 1]


# ─── 5. Recursive Selection Sort & Range-Bounded Slice Sorting ────────────────


def selection_sort_recursive(
    arr: List[Any],
    start_idx: int = 0,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Pure recursive implementation of Selection Sort.
    At recursion level i, selects the minimum in arr[i:] and swaps with arr[i],
    then recursively sorts the remaining subproblem arr[i + 1:].

    Args:
        arr: Input sequence.
        start_idx: Current recursion frontier index (internal use).
        reverse: If True, sorts descending.
        key: Comparison key function.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    # Top-level entry: make copy to maintain purity
    items = list(arr)
    n = len(items)
    key_func = key if key is not None else (lambda x: x)

    def _recurse(idx: int) -> None:
        if idx >= n - 1:
            return

        target_idx = idx
        target_val = key_func(items[idx])

        for j in range(idx + 1, n):
            val_j = key_func(items[j])
            condition = (val_j > target_val) if reverse else (val_j < target_val)
            if condition:
                target_idx = j
                target_val = val_j

        if target_idx != idx:
            items[idx], items[target_idx] = items[target_idx], items[idx]

        _recurse(idx + 1)

    _recurse(start_idx)
    return items


def selection_sort_range(
    arr: List[Any],
    start: int = 0,
    end: Optional[int] = None,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Sorts an in-place bounded range arr[start:end] using Selection Sort,
    leaving elements before start and after end strictly untouched.

    Supports Python-style negative indices and boundary normalization.

    Args:
        arr: Mutable list.
        start: Starting index of slice to sort (inclusive).
        end: Ending index of slice to sort (exclusive). Defaults to len(arr).
        reverse: If True, sorts range descending.
        key: Optional comparison key projection.

    Returns:
        The mutated input list arr.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return arr

    # Normalize start and end
    norm_start = start if start >= 0 else max(0, n + start)
    norm_end = n if end is None else (end if end >= 0 else max(0, n + end))

    norm_start = max(0, min(n, norm_start))
    norm_end = max(0, min(n, norm_end))

    if norm_start >= norm_end - 1:
        return arr

    key_func = key if key is not None else (lambda x: x)

    for i in range(norm_start, norm_end - 1):
        target_idx = i
        target_val = key_func(arr[i])

        for j in range(i + 1, norm_end):
            val_j = key_func(arr[j])
            condition = (val_j > target_val) if reverse else (val_j < target_val)
            if condition:
                target_idx = j
                target_val = val_j

        if target_idx != i:
            arr[i], arr[target_idx] = arr[target_idx], arr[i]

    return arr




