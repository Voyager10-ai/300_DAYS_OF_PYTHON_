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


# ─── 6. Partition Step-by-Step Trace Visualizer ───────────────────────────────


def trace_quick_sort(
    arr: List[Any],
    reverse: bool = False,
    scheme: str = "lomuto",
) -> List[Dict[str, Any]]:
    """
    Executes Quick Sort while recording step-by-step diagnostic partition events.

    Args:
        arr: Sequence of items.
        reverse: If True, sorts descending.
        scheme: 'lomuto' or 'hoare'.

    Returns:
        List of chronological partition trace events.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    events = []
    step_num = 0

    def _trace(low: int, high: int, depth: int) -> None:
        nonlocal step_num
        if low < high:
            step_num += 1
            before = list(items)

            if scheme.lower() == "lomuto":
                p = lomuto_partition(items, low, high, reverse=reverse)
                pivot_val = items[p]
                desc = (
                    f"Depth {depth}: Lomuto partitioned items[{low}..{high}] around pivot {pivot_val} "
                    f"at index {p}."
                )
                events.append({
                    "step": step_num,
                    "depth": depth,
                    "low": low,
                    "high": high,
                    "pivot_index": p,
                    "pivot_value": pivot_val,
                    "state_before": before,
                    "state_after": list(items),
                    "description": desc,
                })
                _trace(low, p - 1, depth + 1)
                _trace(p + 1, high, depth + 1)
            else:
                p = hoare_partition(items, low, high, reverse=reverse)
                desc = (
                    f"Depth {depth}: Hoare split items[{low}..{high}] at boundary index {p}."
                )
                events.append({
                    "step": step_num,
                    "depth": depth,
                    "low": low,
                    "high": high,
                    "pivot_index": p,
                    "pivot_value": items[p],
                    "state_before": before,
                    "state_after": list(items),
                    "description": desc,
                })
                _trace(low, p, depth + 1)
                _trace(p + 1, high, depth + 1)

    _trace(0, n - 1, depth=1)
    return events


def render_quick_trace(trace: List[Dict[str, Any]]) -> str:
    """
    Renders trace events into an indented ASCII partitioning execution log.

    Args:
        trace: Events list from trace_quick_sort.

    Returns:
        Multi-line formatted string.
    """
    if not trace:
        return "Array has <= 1 elements; no partition steps required."

    lines = []
    lines.append("=" * 74)
    lines.append("            QUICK SORT DIVIDE-AND-CONQUER PARTITION TRACE        ")
    lines.append("=" * 74)

    initial = trace[0]["state_before"]
    lines.append(f"Initial State : {initial}")
    lines.append("-" * 74)

    for ev in trace:
        step = ev["step"]
        depth = ev["depth"]
        desc = ev["description"]
        after = ev["state_after"]

        indent = "  " * (depth - 1)
        lines.append(f"{indent}[Step {step:<2}] {desc}")
        lines.append(f"{indent}         Array state: {after}")

    final = trace[-1]["state_after"]
    lines.append("-" * 74)
    lines.append(f"Final Sorted State: {final}")
    lines.append("=" * 74)
    return "\n".join(lines)


# ─── 7. Instability Verification & Performance Analytics Benchmark ───────────


def verify_quick_sort_instability() -> Dict[str, Any]:
    """
    Demonstrates that standard Quick Sort is inherently unstable.
    Long-distance swaps over the pivot can jump an element over an identical element,
    inverting their relative order.

    Returns:
        Dictionary report proving instability with counterexamples.
    """
    counterexamples = [
        [(3, "alpha"), (3, "beta"), (2, "gamma"), (1, "delta"), (3, "epsilon")],
        [(2, "first"), (2, "second"), (1, "third"), (2, "fourth")],
    ]

    case_reports = []
    for case in counterexamples:
        lomuto_sorted = quick_sort(case, key=lambda x: x[0], scheme="lomuto")
        hoare_sorted = quick_sort(case, key=lambda x: x[0], scheme="hoare")
        stable_expected = sorted(case, key=lambda x: x[0])

        def is_unstable(orig, sorted_res):
            unique_keys = set(x[0] for x in orig)
            for k in unique_keys:
                if [x for x in orig if x[0] == k] != [x for x in sorted_res if x[0] == k]:
                    return True
            return False

        case_reports.append({
            "input": case,
            "lomuto_unstable": is_unstable(case, lomuto_sorted),
            "hoare_unstable": is_unstable(case, hoare_sorted),
            "lomuto_output": lomuto_sorted,
            "hoare_output": hoare_sorted,
            "stable_expected": stable_expected,
        })

    return {
        "algorithm": "Quick Sort",
        "is_stable": False,
        "instability_demonstrated": any(
            c["lomuto_unstable"] or c["hoare_unstable"] for c in case_reports
        ),
        "cases": case_reports,
    }


def analyze_quick_sort_benchmarks(
    sizes: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Benchmarks Hoare partition vs Lomuto partition and 3-way partition
    across random, sorted, and duplicate-dense topologies.

    Args:
        sizes: Array lengths. Defaults to [20, 50, 100, 200].

    Returns:
        List of analytical performance records.
    """
    if sizes is None:
        sizes = [20, 50, 100, 200]

    report = []
    for n in sizes:
        random_arr = [(i * 37 + 13) % (n * 3) for i in range(n)]
        duplicates_arr = [i % 4 for i in range(n)]

        _, hoare_m = quick_sort_metrics(random_arr, scheme="hoare")
        _, lomuto_m = quick_sort_metrics(random_arr, scheme="lomuto")

        # Benchmark timings
        t0 = time.perf_counter()
        _ = quick_sort(random_arr, scheme="hoare")
        t_hoare = round((time.perf_counter() - t0) * 1_000_000, 2)

        t0 = time.perf_counter()
        _ = quick_sort(random_arr, scheme="lomuto")
        t_lomuto = round((time.perf_counter() - t0) * 1_000_000, 2)

        t0 = time.perf_counter()
        _ = quick_sort_3way(duplicates_arr)
        t_3way_dups = round((time.perf_counter() - t0) * 1_000_000, 2)

        report.append({
            "size": n,
            "hoare_comparisons": hoare_m["comparisons"],
            "lomuto_comparisons": lomuto_m["comparisons"],
            "hoare_swaps": hoare_m["swaps"],
            "lomuto_swaps": lomuto_m["swaps"],
            "hoare_time_us": t_hoare,
            "lomuto_time_us": t_lomuto,
            "three_way_duplicates_us": t_3way_dups,
            "hoare_swap_reduction_ratio": round(
                lomuto_m["swaps"] / max(1, hoare_m["swaps"]), 2
            ),
        })

    return report


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestQuickSort(unittest.TestCase):
    """Exhaustive unit test suite covering Quick Sort algorithms and edge cases."""

    def setUp(self):
        self.sample = [38, 27, 43, 3, 9, 82, 10]
        self.expected = sorted(self.sample)
        self.duplicates = [5, 2, 8, 2, 5, 1, 9, 1, 8]
        self.all_same = [7, 7, 7, 7, 7, 7]
        self.negatives = [-15, 30, -2, 0, 18, -45, 9]
        self.floats = [3.14, 1.41, 2.71, 0.58, 1.73]

    # --- Core Tests ---
    def test_quick_sort_empty_and_single(self):
        self.assertEqual(quick_sort([]), [])
        self.assertEqual(quick_sort([42]), [42])

    def test_quick_sort_standard(self):
        self.assertEqual(quick_sort(self.sample), self.expected)
        self.assertEqual(quick_sort(self.duplicates), sorted(self.duplicates))
        self.assertEqual(quick_sort(self.all_same), self.all_same)
        self.assertEqual(quick_sort(self.negatives), sorted(self.negatives))
        self.assertEqual(quick_sort(self.floats), sorted(self.floats))

    def test_quick_sort_reverse(self):
        self.assertEqual(
            quick_sort(self.sample, reverse=True), sorted(self.sample, reverse=True)
        )
        self.assertEqual(
            quick_sort(self.duplicates, reverse=True),
            sorted(self.duplicates, reverse=True),
        )

    def test_quick_sort_key(self):
        words = ["apple", "fig", "banana", "watermelon", "kiwi"]
        self.assertEqual(quick_sort(words, key=len), sorted(words, key=len))

    def test_quick_sort_inplace(self):
        arr = list(self.sample)
        quick_sort_inplace(arr)
        self.assertEqual(arr, self.expected)

    def test_quick_sort_schemes(self):
        for scheme in ["hoare", "lomuto"]:
            self.assertEqual(quick_sort(self.sample, scheme=scheme), self.expected)

    def test_quick_sort_invalid_inputs(self):
        with self.assertRaises(TypeError):
            quick_sort(12345)  # type: ignore
        with self.assertRaises(TypeError):
            quick_sort_inplace((1, 2, 3))  # type: ignore
        with self.assertRaises(ValueError):
            quick_sort(self.sample, scheme="invalid_scheme")

    # --- Metrics Tests ---
    def test_quick_sort_metrics(self):
        sorted_arr, metrics = quick_sort_metrics(self.sample, scheme="hoare")
        self.assertEqual(sorted_arr, self.expected)
        self.assertGreater(metrics["comparisons"], 0)
        self.assertGreater(metrics["max_depth"], 0)

    # --- Pivot Strategy Tests ---
    def test_select_pivot_index(self):
        arr = [10, 50, 30]
        self.assertEqual(select_pivot_index(arr, 0, 2, strategy="first"), 0)
        self.assertEqual(select_pivot_index(arr, 0, 2, strategy="last"), 2)
        # Median of 10, 50, 30 is 30 at index 2
        self.assertEqual(select_pivot_index(arr, 0, 2, strategy="median_of_three"), 2)
        rand_idx = select_pivot_index(arr, 0, 2, strategy="random")
        self.assertTrue(0 <= rand_idx <= 2)

    def test_quick_sort_with_pivot(self):
        for strat in ["median_of_three", "random", "first", "last"]:
            self.assertEqual(
                quick_sort_with_pivot(self.sample, strategy=strat), self.expected
            )

    # --- Dutch Flag 3-Way Tests ---
    def test_quick_sort_3way(self):
        self.assertEqual(quick_sort_3way(self.all_same), self.all_same)
        self.assertEqual(quick_sort_3way(self.duplicates), sorted(self.duplicates))
        self.assertEqual(
            quick_sort_3way(self.duplicates, reverse=True),
            sorted(self.duplicates, reverse=True),
        )

    # --- Iterative & Tail-Call Tests ---
    def test_iterative_quick_sort(self):
        self.assertEqual(iterative_quick_sort([]), [])
        self.assertEqual(iterative_quick_sort(self.sample), self.expected)
        self.assertEqual(
            iterative_quick_sort(self.sample, reverse=True),
            sorted(self.sample, reverse=True),
        )

    def test_quick_sort_tail_optimized(self):
        self.assertEqual(quick_sort_tail_optimized(self.sample), self.expected)

    # --- Quickselect Tests ---
    def test_quickselect(self):
        arr = [7, 10, 4, 3, 20, 15]
        # Sorted: [3, 4, 7, 10, 15, 20]
        self.assertEqual(quickselect(arr, 1), 3)
        self.assertEqual(quickselect(arr, 3), 7)
        self.assertEqual(quickselect(arr, 6), 20)
        # Reverse (k-th largest)
        self.assertEqual(quickselect(arr, 1, reverse=True), 20)
        self.assertEqual(quickselect(arr, 2, reverse=True), 15)

    def test_find_median_via_quickselect(self):
        odd_arr = [7, 10, 4, 3, 20]  # Sorted: [3, 4, 7, 10, 20] -> median 7
        self.assertEqual(find_median_via_quickselect(odd_arr), 7)
        even_arr = [1, 2, 3, 4]       # Lower median: 2
        self.assertEqual(find_median_via_quickselect(even_arr), 2)

    def test_quickselect_invalid_k(self):
        with self.assertRaises(ValueError):
            quickselect([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            quickselect([1, 2, 3], 4)
        with self.assertRaises(ValueError):
            find_median_via_quickselect([])

    # --- Trace Visualizer Tests ---
    def test_trace_and_render_quick(self):
        trace = trace_quick_sort([29, 10, 14, 37])
        self.assertGreater(len(trace), 0)
        rendered = render_quick_trace(trace)
        self.assertIn("QUICK SORT DIVIDE-AND-CONQUER PARTITION TRACE", rendered)
        self.assertIn("Final Sorted State: [10, 14, 29, 37]", rendered)

    # --- Stability & Benchmark Tests ---
    def test_verify_quick_sort_instability(self):
        report = verify_quick_sort_instability()
        self.assertFalse(report["is_stable"])
        self.assertTrue(report["instability_demonstrated"])

    def test_analyze_quick_sort_benchmarks(self):
        report = analyze_quick_sort_benchmarks([10, 20])
        self.assertEqual(len(report), 2)
        for r in report:
            self.assertIn("hoare_swap_reduction_ratio", r)


# ─── 9. Interactive CLI Demonstration ─────────────────────────────────────────


def main() -> None:
    """Runs an interactive demonstration of Quick Sort and its advanced algorithmic variations."""
    print("=" * 74)
    print("  DAY 83: QUICK SORT (PARTITIONING & ORDER STATISTICS) IMPLEMENTATION")
    print("=" * 74)

    sample = [38, 27, 43, 3, 9, 82, 10, 19, 50, 1]

    # 1. Core Quick Sort & Schemes
    print("\n[1] Core Quick Sort Execution (Hoare vs Lomuto):")
    sorted_hoare, h_metrics = quick_sort_metrics(sample, scheme="hoare")
    sorted_lomuto, l_metrics = quick_sort_metrics(sample, scheme="lomuto")
    print(f"  Input Sequence   : {sample}")
    print(f"  Hoare Sorted     : {sorted_hoare}")
    print(f"  Hoare Metrics    : Comparisons = {h_metrics['comparisons']}, Swaps = {h_metrics['swaps']}, Max Depth = {h_metrics['max_depth']}")
    print(f"  Lomuto Metrics   : Comparisons = {l_metrics['comparisons']}, Swaps = {l_metrics['swaps']}, Max Depth = {l_metrics['max_depth']}")
    print(f"  Hoare Swap Ratio : Lomuto performed {l_metrics['swaps'] / max(1, h_metrics['swaps']):.2f}x as many swaps as Hoare!")

    # 2. Pivot Selection Strategies
    print("\n[2] Robust Pivot Selection (Median-of-Three):")
    sorted_piv = quick_sort_with_pivot(sample, strategy="median_of_three")
    print(f"  Median-of-Three  : {sorted_piv}")

    # 3. 3-Way Quick Sort on Duplicates
    print("\n[3] Dutch National Flag 3-Way Quick Sort on Duplicates:")
    dup_sample = [4, 2, 4, 1, 4, 3, 4, 2, 4]
    sorted_3way = quick_sort_3way(dup_sample)
    print(f"  Input with Dups  : {dup_sample}")
    print(f"  3-Way Sorted     : {sorted_3way}")

    # 4. Quickselect Order Statistics
    print("\n[4] Quickselect O(n) Order Statistics:")
    dataset = [7, 10, 4, 3, 20, 15]
    print(f"  Dataset          : {dataset}")
    print(f"  1st Smallest     : {quickselect(dataset, 1)}")
    print(f"  3rd Smallest     : {quickselect(dataset, 3)}")
    print(f"  1st Largest      : {quickselect(dataset, 1, reverse=True)}")
    print(f"  Median Element   : {find_median_via_quickselect(dataset)}")

    # 5. Iterative Quick Sort
    print("\n[5] Iterative Quick Sort (Explicit Stack with O(log n) Space Bound):")
    iter_sorted = iterative_quick_sort(sample)
    print(f"  Iterative Sorted : {iter_sorted}")

    # 6. Step-by-Step Visual Trace
    print("\n[6] Partitioning Step-by-Step Visual Trace:")
    trace = trace_quick_sort([29, 10, 14, 37, 13], scheme="lomuto")
    print(render_quick_trace(trace))

    # 7. Instability Proof
    print("\n[7] Quick Sort Instability Proof:")
    instab = verify_quick_sort_instability()
    print(f"  Is Quick Sort stable? {instab['is_stable']}")
    for idx, c in enumerate(instab["cases"], 1):
        print(f"  Case {idx}: Input={c['input']}")
        print(f"          Lomuto Result={c['lomuto_output']}")
        print(f"          Unstable detected? {c['lomuto_unstable']}")

    # 8. Performance Benchmark
    print("\n[8] Performance Benchmark & Swap Optimization Analytics:")
    benchmarks = analyze_quick_sort_benchmarks([20, 50, 100, 200])
    print(f"  {'Size n':<8} | {'Hoare Comps':<12} | {'Lomuto Comps':<13} | {'Hoare Swaps':<12} | {'Lomuto Swaps':<13} | {'Swap Ratio':<10}")
    print("  " + "-" * 78)
    for b in benchmarks:
        print(
            f"  {b['size']:<8} | {b['hoare_comparisons']:<12} | {b['lomuto_comparisons']:<13} | "
            f"{b['hoare_swaps']:<12} | {b['lomuto_swaps']:<13} | "
            f"{b['hoare_swap_reduction_ratio']}x"
        )
    print("\nDemonstration complete.")


if __name__ == "__main__":
    main()








