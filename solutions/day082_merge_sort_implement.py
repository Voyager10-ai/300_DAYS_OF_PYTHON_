# Day 82: Merge Sort Implement
#
# Problem:
#   Write a Python program / module implementing Merge Sort (Divide and Conquer)
#   and its advanced algorithmic variations.
#   Includes core pure and in-place recursive merge sort, bottom-up iterative merge sort,
#   hybrid merge sort with insertion cutoff and skip-merge optimization, heap-based k-way merge,
#   O(n log n) inversion counting engine, step-by-step divide-and-conquer trace visualizer,
#   stability verification engine, performance analytics benchmark, exhaustive unit test suite,
#   and Java practice code.

import time
import heapq
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union, Iterator


# ─── 1. Core Top-Down Recursive Merge Sort ───────────────────────────────────


def merge(
    left: List[Any],
    right: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Merges two sorted lists into a single sorted list while maintaining stability.

    Uses '<=' (or '>=' if reverse) to preserve the relative order of equal keys,
    guaranteeing algorithmic stability.

    Args:
        left: First pre-sorted list.
        right: Second pre-sorted list.
        reverse: If True, merges in descending order.
        key: Optional projection function for comparisons.

    Returns:
        New merged sorted list of length len(left) + len(right).
    """
    key_func = key if key is not None else (lambda x: x)
    merged = []
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        k_left = key_func(left[i])
        k_right = key_func(right[j])

        # Using <= for ascending preserves left-before-right stability on ties
        condition = (k_left >= k_right) if reverse else (k_left <= k_right)
        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements
    if i < len_left:
        merged.extend(left[i:])
    if j < len_right:
        merged.extend(right[j:])

    return merged


def merge_sort(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Sorts a sequence using standard Top-Down Divide-and-Conquer Merge Sort (pure function).

    Guarantees O(n log n) comparisons in all cases (worst, average, and best).
    Space Complexity: O(n) auxiliary.

    Args:
        arr: Input sequence (list or tuple).
        reverse: If True, sorts descending.
        key: Optional comparison key projection.

    Returns:
        New sorted list.

    Raises:
        TypeError: If arr is not a list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return list(arr)

    mid = n // 2
    left_sorted = merge_sort(arr[:mid], reverse=reverse, key=key)
    right_sorted = merge_sort(arr[mid:], reverse=reverse, key=key)

    return merge(left_sorted, right_sorted, reverse=reverse, key=key)


def merge_sort_inplace(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> None:
    """
    Sorts a mutable list in-place using standard Merge Sort with an auxiliary buffer.

    Args:
        arr: Mutable list to sort in-place.
        reverse: If True, sorts descending.
        key: Key projection function.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return

    sorted_copy = merge_sort(arr, reverse=reverse, key=key)
    for idx, val in enumerate(sorted_copy):
        arr[idx] = val


def merge_sort_metrics(
    arr: List[Any],
    reverse: bool = False,
) -> Tuple[List[Any], Dict[str, Any]]:
    """
    Sorts a sequence using Merge Sort while tracking comparisons, merge operations,
    and maximum recursion depth.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        Tuple of (sorted_list, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    comparisons = 0
    merge_ops = 0
    max_depth = 0

    def _sort_with_profiling(sub: List[Any], depth: int) -> List[Any]:
        nonlocal comparisons, merge_ops, max_depth
        max_depth = max(max_depth, depth)

        m = len(sub)
        if m <= 1:
            return list(sub)

        mid = m // 2
        left = _sort_with_profiling(sub[:mid], depth + 1)
        right = _sort_with_profiling(sub[mid:], depth + 1)

        # Profiled merge
        merged = []
        i = 0
        j = 0
        len_l = len(left)
        len_r = len(right)
        merge_ops += 1

        while i < len_l and j < len_r:
            comparisons += 1
            cond = (left[i] >= right[j]) if reverse else (left[i] <= right[j])
            if cond:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        if i < len_l:
            merged.extend(left[i:])
        if j < len_r:
            merged.extend(right[j:])

        return merged

    sorted_result = _sort_with_profiling(list(arr), depth=1)
    metrics = {
        "comparisons": comparisons,
        "merge_operations": merge_ops,
        "max_recursion_depth": max_depth,
        "input_length": len(arr),
    }
    return (sorted_result, metrics)


# ─── 2. Bottom-Up Iterative Merge Sort ────────────────────────────────────────


def iterative_merge_sort(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Sorts a sequence using Bottom-Up (Iterative) Merge Sort (pure function).

    Instead of recursive splitting, starts with width = 1 and iteratively merges
    adjacent sub-lists of doubling sizes (1, 2, 4, 8, ...).
    Eliminates recursion stack frames, making it immune to recursion limit overflow.

    Time Complexity: O(n log n) comparisons.
    Space Complexity: O(n) auxiliary memory.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.
        key: Optional comparison key projection.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return list(arr)

    src = list(arr)
    dst = [None] * n
    key_func = key if key is not None else (lambda x: x)

    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)

            # Merge src[left:mid] and src[mid:right] into dst[left:right]
            l_idx = left
            r_idx = mid
            k = left

            while l_idx < mid and r_idx < right:
                k_l = key_func(src[l_idx])
                k_r = key_func(src[r_idx])
                cond = (k_l >= k_r) if reverse else (k_l <= k_r)
                if cond:
                    dst[k] = src[l_idx]
                    l_idx += 1
                else:
                    dst[k] = src[r_idx]
                    r_idx += 1
                k += 1

            while l_idx < mid:
                dst[k] = src[l_idx]
                l_idx += 1
                k += 1

            while r_idx < right:
                dst[k] = src[r_idx]
                r_idx += 1
                k += 1

        # Ping-pong buffer swap
        src, dst = dst, src
        width *= 2

    return src


def iterative_merge_sort_inplace(
    arr: List[Any],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> None:
    """
    In-place wrapper for iterative bottom-up merge sort.

    Args:
        arr: Mutable list to sort in-place.
        reverse: If True, sorts descending.
        key: Key projection function.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    res = iterative_merge_sort(arr, reverse=reverse, key=key)
    for idx, val in enumerate(res):
        arr[idx] = val


# ─── 3. Hybrid Merge Sort (Insertion Cutoff & Skip-Merge Optimization) ─────────


def _insertion_sort_slice(
    arr: List[Any],
    start: int,
    end: int,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> None:
    """Helper: In-place insertion sort on arr[start:end] slice."""
    key_func = key if key is not None else (lambda x: x)
    for i in range(start + 1, end):
        temp = arr[i]
        k_temp = key_func(temp)
        j = i - 1
        while j >= start:
            k_prev = key_func(arr[j])
            cond = (k_prev < k_temp) if reverse else (k_prev > k_temp)
            if cond:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = temp


def hybrid_merge_sort(
    arr: List[Any],
    cutoff: int = 16,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Sorts using Hybrid Merge Sort combining Merge Sort with Insertion Sort for small slices.
    Also incorporates the Skip-Merge optimization: if arr[mid] <= arr[mid+1],
    the two halves are already in relative order, avoiding the merge step entirely.

    Args:
        arr: Input sequence.
        cutoff: Sub-array size threshold to switch to Insertion Sort (default 16).
        reverse: If True, sorts descending.
        key: Comparison key projection.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if cutoff < 1:
        cutoff = 1

    items = list(arr)
    n = len(items)
    if n <= 1:
        return items

    key_func = key if key is not None else (lambda x: x)
    aux = [None] * n

    def _sort(low: int, high: int) -> None:
        if high - low <= cutoff:
            _insertion_sort_slice(items, low, high, reverse=reverse, key=key)
            return

        mid = low + (high - low) // 2
        _sort(low, mid)
        _sort(mid, high)

        # Skip-merge optimization: already ordered?
        k_mid = key_func(items[mid - 1])
        k_next = key_func(items[mid])
        already_sorted = (k_mid >= k_next) if reverse else (k_mid <= k_next)
        if already_sorted:
            return

        # Merge items[low:mid] and items[mid:high] using aux buffer
        for idx in range(low, high):
            aux[idx] = items[idx]

        i = low
        j = mid
        for k in range(low, high):
            if i >= mid:
                items[k] = aux[j]
                j += 1
            elif j >= high:
                items[k] = aux[i]
                i += 1
            else:
                k_i = key_func(aux[i])
                k_j = key_func(aux[j])
                cond = (k_i >= k_j) if reverse else (k_i <= k_j)
                if cond:
                    items[k] = aux[i]
                    i += 1
                else:
                    items[k] = aux[j]
                    j += 1

    _sort(0, n)
    return items


def hybrid_merge_sort_inplace(
    arr: List[Any],
    cutoff: int = 16,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> None:
    """
    In-place wrapper for hybrid merge sort.

    Args:
        arr: Mutable list.
        cutoff: Cutoff threshold for insertion sort.
        reverse: If True, sorts descending.
        key: Key projection function.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    sorted_res = hybrid_merge_sort(arr, cutoff=cutoff, reverse=reverse, key=key)
    for idx, val in enumerate(sorted_res):
        arr[idx] = val


# ─── 4. Heap-Based K-Way Merge for Multi-Stream Sorting ───────────────────────


def merge_sorted_streams(
    iterators: List[Iterator[Any]],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> Iterator[Any]:
    """
    Lazily merges k pre-sorted iterators into a single sorted generator in O(N log k) time.
    Maintains a min-heap (or max-heap if reverse) of size at most k.

    Args:
        iterators: List of iterators, each producing elements in sorted order.
        reverse: If True, input streams and output stream are descending.
        key: Projection function.

    Yields:
        Elements in globally sorted order.
    """
    key_func = key if key is not None else (lambda x: x)
    heap: List[Tuple[Any, int, Any, Iterator[Any]]] = []
    entry_counter = 0

    class InvertWrapper:
        """Helper to invert comparisons for reverse=True in Python's min-heap."""
        def __init__(self, val: Any):
            self.val = val

        def __lt__(self, other: "InvertWrapper") -> bool:
            return self.val > other.val

        def __gt__(self, other: "InvertWrapper") -> bool:
            return self.val < other.val

        def __eq__(self, other: Any) -> bool:
            return isinstance(other, InvertWrapper) and self.val == other.val

    # Initialize heap with the first item from each iterator
    for it in iterators:
        try:
            val = next(it)
            k_val = key_func(val)
            proj = InvertWrapper(k_val) if reverse else k_val
            heapq.heappush(heap, (proj, entry_counter, val, it))
            entry_counter += 1
        except StopIteration:
            continue

    # Pop minimum, push next from that iterator
    while heap:
        _, _, min_val, it = heapq.heappop(heap)
        yield min_val
        try:
            next_val = next(it)
            next_k = key_func(next_val)
            proj = InvertWrapper(next_k) if reverse else next_k
            heapq.heappush(heap, (proj, entry_counter, next_val, it))
            entry_counter += 1
        except StopIteration:
            pass


def k_way_merge(
    sorted_arrays: List[List[Any]],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Merges k sorted lists into a single consolidated sorted list.
    Standard building block for External Merge Sort.

    Time Complexity: O(N log k), where N is total items across all k lists.
    Space Complexity: O(N) for result list, O(k) auxiliary heap space.

    Args:
        sorted_arrays: List of k sorted sequences.
        reverse: If True, merges descending sorted lists.
        key: Key projection function.

    Returns:
        Consolidated sorted list.

    Raises:
        TypeError: If sorted_arrays is not a list.
    """
    if not isinstance(sorted_arrays, list):
        raise TypeError(f"Expected list of sorted arrays, got {type(sorted_arrays).__name__}")

    iterators = [iter(sub) for sub in sorted_arrays if len(sub) > 0]
    if not iterators:
        return []

    return list(merge_sorted_streams(iterators, reverse=reverse, key=key))


# ─── 5. Divide-and-Conquer Inversion Counting Engine ──────────────────────────


def count_inversions(arr: List[Any]) -> Tuple[int, List[Any]]:
    """
    Counts the number of inversions in a sequence in O(n log n) time using Divide and Conquer.
    An inversion is a pair of indices (i, j) such that i < j and arr[i] > arr[j].
    Also returns the sorted version of the array.

    Args:
        arr: Input sequence.

    Returns:
        Tuple of (inversion_count, sorted_list).

    Raises:
        TypeError: If arr is not list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return (0, list(arr))

    def _merge_and_count(items: List[Any]) -> Tuple[int, List[Any]]:
        m = len(items)
        if m <= 1:
            return (0, list(items))

        mid = m // 2
        inv_left, left = _merge_and_count(items[:mid])
        inv_right, right = _merge_and_count(items[mid:])

        merged = []
        i = 0
        j = 0
        split_invs = 0
        len_l = len(left)
        len_r = len(right)

        while i < len_l and j < len_r:
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                # All remaining elements in left[i:] are > right[j]
                split_invs += (len_l - i)
                j += 1

        if i < len_l:
            merged.extend(left[i:])
        if j < len_r:
            merged.extend(right[j:])

        total_invs = inv_left + inv_right + split_invs
        return (total_invs, merged)

    return _merge_and_count(list(arr))


def inversion_distance_metric(arr: List[Any]) -> Dict[str, Any]:
    """
    Computes inversion count and normalized unsortedness ratio (Kendall tau metric).

    Args:
        arr: Input sequence.

    Returns:
        Dictionary with inversion metrics, theoretical bounds, and normalized ratio [0.0, 1.0].
    """
    n = len(arr)
    if n <= 1:
        return {
            "inversion_count": 0,
            "max_possible_inversions": 0,
            "unsortedness_ratio": 0.0,
            "is_already_sorted": True,
        }

    max_invs = n * (n - 1) // 2
    inv_count, _ = count_inversions(arr)
    ratio = round(inv_count / max_invs, 4) if max_invs > 0 else 0.0

    return {
        "inversion_count": inv_count,
        "max_possible_inversions": max_invs,
        "unsortedness_ratio": ratio,
        "is_already_sorted": (inv_count == 0),
        "is_reverse_sorted": (inv_count == max_invs),
    }




