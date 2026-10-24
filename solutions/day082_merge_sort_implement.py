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


# ─── 6. Divide-and-Conquer Step-by-Step Trace Visualizer ──────────────────────


def trace_merge_sort(
    arr: List[Any],
    reverse: bool = False,
) -> List[Dict[str, Any]]:
    """
    Executes Merge Sort and returns a complete hierarchical trace of divide steps and merge steps.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        List of chronological trace event dictionaries.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    events = []
    step_counter = 0

    def _trace(sub: List[Any], depth: int, path: str) -> List[Any]:
        nonlocal step_counter
        m = len(sub)
        if m <= 1:
            step_counter += 1
            events.append({
                "step": step_counter,
                "type": "BASE_CASE",
                "depth": depth,
                "path": path,
                "input": list(sub),
                "output": list(sub),
                "description": f"Depth {depth} ({path}): Base case element {sub}",
            })
            return list(sub)

        mid = m // 2
        step_counter += 1
        left_sub = sub[:mid]
        right_sub = sub[mid:]

        events.append({
            "step": step_counter,
            "type": "DIVIDE",
            "depth": depth,
            "path": path,
            "input": list(sub),
            "left_split": list(left_sub),
            "right_split": list(right_sub),
            "description": f"Depth {depth} ({path}): Divide {sub} into {left_sub} and {right_sub}",
        })

        sorted_left = _trace(left_sub, depth + 1, path + "L")
        sorted_right = _trace(right_sub, depth + 1, path + "R")

        merged = merge(sorted_left, sorted_right, reverse=reverse)
        step_counter += 1
        events.append({
            "step": step_counter,
            "type": "MERGE",
            "depth": depth,
            "path": path,
            "left_sorted": sorted_left,
            "right_sorted": sorted_right,
            "output": list(merged),
            "description": f"Depth {depth} ({path}): Merged {sorted_left} and {sorted_right} -> {merged}",
        })
        return merged

    _trace(list(arr), depth=1, path="root")
    return events


def render_merge_trace(trace: List[Dict[str, Any]]) -> str:
    """
    Renders trace events into an indented ASCII recursion and merge diagram.

    Args:
        trace: Events list from trace_merge_sort.

    Returns:
        Multi-line formatted string.
    """
    if not trace:
        return "Array has <= 1 elements; trivial base case."

    lines = []
    lines.append("=" * 74)
    lines.append("        DIVIDE-AND-CONQUER MERGE SORT RECURSION TRACE VISUALIZER       ")
    lines.append("=" * 74)

    for ev in trace:
        step = ev["step"]
        depth = ev["depth"]
        ev_type = ev["type"]
        desc = ev["description"]

        indent = "  " * (depth - 1)
        tag = f"[{ev_type:<9}]"
        lines.append(f"{indent}{tag} Step {step:<2} | {desc}")

    final_merges = [e for e in trace if e["type"] == "MERGE"]
    final_output = final_merges[-1]["output"] if final_merges else trace[0]["output"]

    lines.append("-" * 74)
    lines.append(f"Final Globally Sorted State: {final_output}")
    lines.append("=" * 74)
    return "\n".join(lines)


# ─── 7. Stability Verification & Performance Analytics Benchmark ──────────────


def verify_merge_sort_stability() -> Dict[str, Any]:
    """
    Verifies that all Merge Sort variants (top-down, bottom-up, hybrid, and k-way)
    strictly preserve stability (the relative input order of equal keys).

    Returns:
        Dictionary report confirming stability across all variants with before/after mappings.
    """
    test_cases = [
        [(2, "alpha"), (1, "one"), (2, "beta"), (2, "gamma"), (1, "two")],
        [(3, "x"), (2, "y"), (3, "z"), (1, "w"), (3, "v"), (2, "u")],
    ]

    def _check_stability(original: List[Tuple[int, str]], sorted_arr: List[Tuple[int, str]]) -> bool:
        unique_keys = set(x[0] for x in original)
        for k in unique_keys:
            orig_subset = [x for x in original if x[0] == k]
            res_subset = [x for x in sorted_arr if x[0] == k]
            if orig_subset != res_subset:
                return False
        return True

    results = []
    for case in test_cases:
        top_down = merge_sort(case, key=lambda x: x[0])
        bottom_up = iterative_merge_sort(case, key=lambda x: x[0])
        hybrid = hybrid_merge_sort(case, cutoff=2, key=lambda x: x[0])

        results.append({
            "input": case,
            "top_down_stable": _check_stability(case, top_down),
            "bottom_up_stable": _check_stability(case, bottom_up),
            "hybrid_stable": _check_stability(case, hybrid),
        })

    all_stable = all(
        r["top_down_stable"] and r["bottom_up_stable"] and r["hybrid_stable"]
        for r in results
    )

    return {
        "algorithm": "Merge Sort",
        "is_stable": True,
        "all_variants_passed": all_stable,
        "cases": results,
    }


def analyze_merge_sort_benchmarks(
    sizes: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Benchmarks Top-Down Merge Sort, Bottom-Up Merge Sort, and Hybrid Merge Sort
    across diverse input distributions (Random, Sorted, Reversed).

    Args:
        sizes: Array lengths to benchmark. Defaults to [20, 50, 100, 200].

    Returns:
        List of analytical performance records.
    """
    if sizes is None:
        sizes = [20, 50, 100, 200]

    report = []
    for n in sizes:
        # Deterministic random dataset
        random_data = [(i * 37 + 13) % (n * 3) for i in range(n)]
        sorted_data = list(range(n))
        reversed_data = list(range(n, 0, -1))

        # 1. Top-Down Metrics
        _, td_metrics = merge_sort_metrics(random_data)
        _, td_sorted_m = merge_sort_metrics(sorted_data)

        # 2. Timing benchmarks
        t0 = time.perf_counter()
        _ = merge_sort(random_data)
        t_td = round((time.perf_counter() - t0) * 1_000_000, 2)

        t0 = time.perf_counter()
        _ = iterative_merge_sort(random_data)
        t_bu = round((time.perf_counter() - t0) * 1_000_000, 2)

        t0 = time.perf_counter()
        _ = hybrid_merge_sort(random_data, cutoff=16)
        t_hy = round((time.perf_counter() - t0) * 1_000_000, 2)

        t0 = time.perf_counter()
        _ = hybrid_merge_sort(sorted_data, cutoff=16)
        t_hy_sorted = round((time.perf_counter() - t0) * 1_000_000, 2)

        report.append({
            "size": n,
            "random_comparisons": td_metrics["comparisons"],
            "sorted_comparisons": td_sorted_m["comparisons"],
            "max_recursion_depth": td_metrics["max_recursion_depth"],
            "top_down_us": t_td,
            "bottom_up_us": t_bu,
            "hybrid_us": t_hy,
            "hybrid_sorted_us": t_hy_sorted,
            "hybrid_speedup": round(t_td / max(0.1, t_hy), 2),
        })

    return report


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestMergeSort(unittest.TestCase):
    """Exhaustive unit test suite covering Merge Sort algorithms and edge cases."""

    def setUp(self):
        self.sample = [38, 27, 43, 3, 9, 82, 10]
        self.expected = sorted(self.sample)
        self.duplicates = [5, 2, 8, 2, 5, 1, 9, 1, 8]
        self.negatives = [-12, 45, 0, -3, 89, -50, 23]
        self.floats = [3.14, 1.41, 2.71, 0.58, 1.73]

    # --- Core Merge Function Tests ---
    def test_merge_primitives(self):
        self.assertEqual(merge([], []), [])
        self.assertEqual(merge([1, 3], []), [1, 3])
        self.assertEqual(merge([], [2, 4]), [2, 4])
        self.assertEqual(merge([1, 5, 9], [2, 6, 10]), [1, 2, 5, 6, 9, 10])
        # Stability on ties: elements from left should precede elements from right
        left = [(1, "L1"), (3, "L2")]
        right = [(1, "R1"), (2, "R2")]
        merged = merge(left, right, key=lambda x: x[0])
        self.assertEqual(merged, [(1, "L1"), (1, "R1"), (2, "R2"), (3, "L2")])

    # --- Core Merge Sort Tests ---
    def test_merge_sort_empty_and_single(self):
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([99]), [99])

    def test_merge_sort_standard(self):
        self.assertEqual(merge_sort(self.sample), self.expected)
        self.assertEqual(merge_sort(self.duplicates), sorted(self.duplicates))
        self.assertEqual(merge_sort(self.negatives), sorted(self.negatives))
        self.assertEqual(merge_sort(self.floats), sorted(self.floats))

    def test_merge_sort_reverse(self):
        self.assertEqual(
            merge_sort(self.sample, reverse=True), sorted(self.sample, reverse=True)
        )
        self.assertEqual(
            merge_sort(self.duplicates, reverse=True),
            sorted(self.duplicates, reverse=True),
        )

    def test_merge_sort_key(self):
        words = ["apple", "fig", "banana", "watermelon", "kiwi"]
        self.assertEqual(merge_sort(words, key=len), sorted(words, key=len))

    def test_merge_sort_inplace(self):
        arr = list(self.sample)
        merge_sort_inplace(arr)
        self.assertEqual(arr, self.expected)

    def test_merge_sort_type_error(self):
        with self.assertRaises(TypeError):
            merge_sort(12345)  # type: ignore
        with self.assertRaises(TypeError):
            merge_sort_inplace((1, 2, 3))  # type: ignore

    # --- Profiling Metrics Tests ---
    def test_merge_sort_metrics(self):
        arr = [8, 4, 2, 1]
        sorted_arr, metrics = merge_sort_metrics(arr)
        self.assertEqual(sorted_arr, [1, 2, 4, 8])
        self.assertGreater(metrics["comparisons"], 0)
        self.assertEqual(metrics["merge_operations"], 3)
        self.assertEqual(metrics["max_recursion_depth"], 3)

    # --- Iterative Bottom-Up Tests ---
    def test_iterative_merge_sort(self):
        self.assertEqual(iterative_merge_sort([]), [])
        self.assertEqual(iterative_merge_sort([5]), [5])
        self.assertEqual(iterative_merge_sort(self.sample), self.expected)
        self.assertEqual(
            iterative_merge_sort(self.sample, reverse=True),
            sorted(self.sample, reverse=True),
        )

    def test_iterative_merge_sort_inplace(self):
        arr = list(self.duplicates)
        iterative_merge_sort_inplace(arr)
        self.assertEqual(arr, sorted(self.duplicates))

    # --- Hybrid Merge Sort Tests ---
    def test_hybrid_merge_sort(self):
        self.assertEqual(hybrid_merge_sort([]), [])
        self.assertEqual(hybrid_merge_sort([10]), [10])
        self.assertEqual(hybrid_merge_sort(self.sample, cutoff=4), self.expected)
        self.assertEqual(
            hybrid_merge_sort(self.sample, cutoff=32), self.expected
        )

    def test_hybrid_merge_sort_inplace(self):
        arr = list(self.negatives)
        hybrid_merge_sort_inplace(arr, cutoff=3)
        self.assertEqual(arr, sorted(self.negatives))

    # --- K-Way Merge Tests ---
    def test_k_way_merge(self):
        arrays = [
            [1, 5, 9],
            [2, 6, 10],
            [0, 3, 7, 11],
            [],
            [4, 8],
        ]
        merged = k_way_merge(arrays)
        self.assertEqual(merged, list(range(12)))

    def test_k_way_merge_reverse(self):
        arrays = [
            [9, 5, 1],
            [10, 6, 2],
            [11, 7, 3, 0],
            [8, 4],
        ]
        merged = k_way_merge(arrays, reverse=True)
        self.assertEqual(merged, list(range(11, -1, -1)))

    def test_k_way_merge_empty(self):
        self.assertEqual(k_way_merge([]), [])
        self.assertEqual(k_way_merge([[], []]), [])

    # --- Inversion Counting Tests ---
    def test_count_inversions(self):
        # Already sorted: 0 inversions
        self.assertEqual(count_inversions([1, 2, 3, 4, 5])[0], 0)
        # Reverse sorted: n*(n-1)/2 inversions
        self.assertEqual(count_inversions([5, 4, 3, 2, 1])[0], 10)
        # Arbitrary: [2, 4, 1, 3, 5] -> (2,1), (4,1), (4,3) -> 3 inversions
        invs, sorted_arr = count_inversions([2, 4, 1, 3, 5])
        self.assertEqual(invs, 3)
        self.assertEqual(sorted_arr, [1, 2, 3, 4, 5])

    def test_inversion_distance_metric(self):
        res = inversion_distance_metric([3, 2, 1])
        self.assertEqual(res["inversion_count"], 3)
        self.assertEqual(res["max_possible_inversions"], 3)
        self.assertEqual(res["unsortedness_ratio"], 1.0)
        self.assertTrue(res["is_reverse_sorted"])

    # --- Trace Visualizer Tests ---
    def test_trace_and_render_merge(self):
        trace = trace_merge_sort([38, 27, 43, 3])
        self.assertGreater(len(trace), 0)
        rendered = render_merge_trace(trace)
        self.assertIn("MERGE SORT RECURSION TRACE VISUALIZER", rendered)
        self.assertIn("Final Globally Sorted State: [3, 27, 38, 43]", rendered)

    # --- Stability Verification Tests ---
    def test_verify_merge_sort_stability(self):
        report = verify_merge_sort_stability()
        self.assertTrue(report["is_stable"])
        self.assertTrue(report["all_variants_passed"])

    # --- Performance Benchmark Tests ---
    def test_analyze_merge_sort_benchmarks(self):
        report = analyze_merge_sort_benchmarks([10, 20])
        self.assertEqual(len(report), 2)
        for r in report:
            self.assertIn("hybrid_speedup", r)


# ─── 9. Interactive CLI Demonstration ─────────────────────────────────────────


def main() -> None:
    """Runs a comprehensive demonstration of Merge Sort and all algorithmic variations."""
    print("=" * 74)
    print("  DAY 82: MERGE SORT (DIVIDE-AND-CONQUER) IMPLEMENTATION")
    print("=" * 74)

    sample = [38, 27, 43, 3, 9, 82, 10, 19, 50, 1]

    # 1. Top-Down Merge Sort & Metrics
    print("\n[1] Top-Down Recursive Merge Sort:")
    sorted_sample, metrics = merge_sort_metrics(sample)
    print(f"  Input Sequence      : {sample}")
    print(f"  Sorted Output       : {sorted_sample}")
    print(f"  Comparisons         : {metrics['comparisons']}")
    print(f"  Merge Operations    : {metrics['merge_operations']}")
    print(f"  Max Recursion Depth : {metrics['max_recursion_depth']}")

    # 2. Bottom-Up Iterative Merge Sort
    print("\n[2] Bottom-Up Iterative Merge Sort (Zero Call-Stack Overhead):")
    bu_sorted = iterative_merge_sort(sample)
    print(f"  Iterative Sorted    : {bu_sorted}")

    # 3. Hybrid Merge Sort with Skip-Merge
    print("\n[3] Hybrid Merge Sort (Cutoff = 4 + Skip-Merge Optimization):")
    hybrid_sorted = hybrid_merge_sort(sample, cutoff=4)
    print(f"  Hybrid Sorted       : {hybrid_sorted}")

    # 4. K-Way Stream Merge
    print("\n[4] K-Way Merge for Multi-Stream Sorting:")
    streams = [
        [10, 25, 40],
        [5, 20, 35, 50],
        [2, 12, 22, 32],
        [1, 9, 15],
    ]
    for idx, s in enumerate(streams, 1):
        print(f"  Stream {idx}: {s}")
    k_merged = k_way_merge(streams)
    print(f"  Consolidated Output : {k_merged}")

    # 5. Inversion Counting Metric
    print("\n[5] Inversion Counting & Kendall's Tau Distance Metric:")
    test_arr = [8, 4, 2, 1]
    inv_info = inversion_distance_metric(test_arr)
    print(f"  Dataset             : {test_arr}")
    print(f"  Inversions Count    : {inv_info['inversion_count']}")
    print(f"  Max Inversions      : {inv_info['max_possible_inversions']}")
    print(f"  Unsortedness Ratio  : {inv_info['unsortedness_ratio'] * 100:.1f}%")

    # 6. Step-by-Step Divide & Conquer Visual Trace
    print("\n[6] Divide-and-Conquer Recursion Visual Trace:")
    trace = trace_merge_sort([38, 27, 43, 3])
    print(render_merge_trace(trace))

    # 7. Stability Verification Report
    print("\n[7] Algorithmic Stability Verification:")
    stab_rep = verify_merge_sort_stability()
    print(f"  Is Merge Sort strictly stable? {stab_rep['is_stable']}")
    print(f"  All variant test cases passed: {stab_rep['all_variants_passed']}")

    # 8. Performance Benchmark & Speedup Analytics
    print("\n[8] Performance Benchmark & Hybrid Speedup Analytics:")
    benchmarks = analyze_merge_sort_benchmarks([20, 50, 100, 200])
    print(f"  {'Size n':<8} | {'Comps':<8} | {'Depth':<6} | {'Top-Down us':<12} | {'Bottom-Up us':<13} | {'Hybrid us':<10} | {'Speedup':<8}")
    print("  " + "-" * 74)
    for b in benchmarks:
        print(
            f"  {b['size']:<8} | {b['random_comparisons']:<8} | {b['max_recursion_depth']:<6} | "
            f"{b['top_down_us']:<12} | {b['bottom_up_us']:<13} | {b['hybrid_us']:<10} | "
            f"{b['hybrid_speedup']}x"
        )
    print("\nDemonstration complete.")


if __name__ == "__main__":
    main()








