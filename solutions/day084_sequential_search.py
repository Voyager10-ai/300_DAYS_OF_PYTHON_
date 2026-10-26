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


# ─── 4. Ordered Sequential Search (Sorted Early-Exit Optimization) ───────────


def ordered_sequential_search(
    arr: List[Any],
    target: Any,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> int:
    """
    Performs Sequential Search on a pre-sorted sequence with early-exit termination.
    Terminates immediately when an element surpasses target, cutting unsuccessful search
    comparisons from n down to an average of n / 2 without needing random access indexing.

    Args:
        arr: Pre-sorted list or tuple.
        target: Target item to search for.
        reverse: If True, assumes arr is sorted descending.
        key: Optional comparison projection.

    Returns:
        Index of target, or -1 if missing.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    for idx, item in enumerate(arr):
        k_item = key_func(item)
        if k_item == target_key:
            return idx

        # Early exit check on ordered elements
        early_exit = (k_item < target_key) if reverse else (k_item > target_key)
        if early_exit:
            break

    return -1


def ordered_sequential_search_metrics(
    arr: List[Any],
    target: Any,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluates Ordered Sequential Search while tracking early-exit savings.

    Args:
        arr: Sorted sequence.
        target: Target item.
        reverse: If True, sorted descending.
        key: Key projection.

    Returns:
        Tuple of (found_index, metrics_dict).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    key_func = key if key is not None else (lambda x: x)
    target_key = key_func(target) if key is not None else target

    n = len(arr)
    comparisons = 0
    found_idx = -1
    early_exit_triggered = False

    for idx, item in enumerate(arr):
        comparisons += 1
        k_item = key_func(item)
        if k_item == target_key:
            found_idx = idx
            break

        early_exit = (k_item < target_key) if reverse else (k_item > target_key)
        if early_exit:
            early_exit_triggered = True
            break

    comparisons_saved = n - comparisons

    metrics = {
        "found": (found_idx != -1),
        "index": found_idx,
        "comparisons": comparisons,
        "total_elements": n,
        "early_exit_triggered": early_exit_triggered,
        "comparisons_saved": comparisons_saved,
        "savings_percentage": round((comparisons_saved / max(1, n)) * 100, 2),
    }
    return (found_idx, metrics)


# ─── 5. Predicate / Conditional Sequential Search ─────────────────────────────


def sequential_search_predicate(
    arr: List[Any],
    predicate: Callable[[Any], bool],
) -> Optional[Tuple[int, Any]]:
    """
    Finds the first element in arr that satisfies the predicate function.
    Equivalent to C++ std::find_if or Javascript Array.prototype.find.

    Args:
        arr: Sequence of items.
        predicate: Callable taking an element and returning True if matching.

    Returns:
        Tuple of (index, item) for first match, or None if no match found.

    Raises:
        TypeError: If arr is not list or tuple, or predicate is not callable.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if not callable(predicate):
        raise TypeError(f"Expected callable predicate, got {type(predicate).__name__}")

    for idx, item in enumerate(arr):
        if predicate(item):
            return (idx, item)

    return None


def sequential_search_predicate_last(
    arr: List[Any],
    predicate: Callable[[Any], bool],
) -> Optional[Tuple[int, Any]]:
    """
    Finds the last element in arr that satisfies the predicate (scans backward).

    Args:
        arr: Sequence of items.
        predicate: Predicate callable.

    Returns:
        Tuple of (index, item) for last match, or None if no match.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if not callable(predicate):
        raise TypeError(f"Expected callable predicate, got {type(predicate).__name__}")

    for idx in range(len(arr) - 1, -1, -1):
        item = arr[idx]
        if predicate(item):
            return (idx, item)

    return None


def sequential_search_predicate_all(
    arr: List[Any],
    predicate: Callable[[Any], bool],
) -> List[Tuple[int, Any]]:
    """
    Collects all elements and their indices that satisfy the predicate.

    Args:
        arr: Sequence of items.
        predicate: Predicate callable.

    Returns:
        List of (index, item) tuples matching the condition.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if not callable(predicate):
        raise TypeError(f"Expected callable predicate, got {type(predicate).__name__}")

    matches = []
    for idx, item in enumerate(arr):
        if predicate(item):
            matches.append((idx, item))

    return matches


# ─── 6. Step-by-Step Traversal Visualizer & ASCII Pointer Renderer ────────────


def trace_sequential_search(
    arr: List[Any],
    target: Any,
) -> List[Dict[str, Any]]:
    """
    Executes Sequential Search while recording every inspection step.

    Args:
        arr: Sequence of elements.
        target: Target item to locate.

    Returns:
        List of trace dictionaries describing each inspection step.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    steps = []
    for idx, item in enumerate(arr):
        is_match = (item == target)
        desc = (
            f"Step {idx + 1}: Inspecting index {idx} (value = {item}). "
            + (f"MATCH FOUND! Target {target} located." if is_match else f"No match; advancing pointer.")
        )
        steps.append({
            "step": idx + 1,
            "index": idx,
            "value": item,
            "target": target,
            "is_match": is_match,
            "description": desc,
        })
        if is_match:
            break

    return steps


def render_sequential_trace(
    arr: List[Any],
    trace: List[Dict[str, Any]],
    target: Any,
) -> str:
    """
    Formats the search trace into a graphical ASCII step-by-step diagram
    with moving pointers pointing to the active cell.

    Args:
        arr: Original sequence.
        trace: Events list from trace_sequential_search.
        target: Searched value.

    Returns:
        Multi-line formatted string.
    """
    if not arr:
        return "Array is empty; search terminates immediately with -1."

    lines = []
    lines.append("=" * 72)
    lines.append("           SEQUENTIAL SEARCH STEP-BY-STEP TRAVERSAL TRACE         ")
    lines.append("=" * 72)
    lines.append(f"Array  : {arr}")
    lines.append(f"Target : {target}")
    lines.append("-" * 72)

    for ev in trace:
        step = ev["step"]
        idx = ev["index"]
        val = ev["value"]
        is_match = ev["is_match"]
        tag = "[MATCH]" if is_match else "[SCAN ]"

        lines.append(f"{tag} Step {step:<2} | Index {idx:<2}: {val} == {target} -> {is_match}")

        # Build visual pointer over array cells
        cell_strs = [str(x) for x in arr]
        # Calculate visual offset of current cell
        prefix = "  Array: [ "
        cell_offsets = []
        curr_offset = len(prefix)
        for i, cs in enumerate(cell_strs):
            cell_offsets.append(curr_offset)
            curr_offset += len(cs) + 2  # plus ", "

        rendered_cells = prefix + ", ".join(cell_strs) + " ]"
        lines.append(rendered_cells)

        pointer_pad = " " * cell_offsets[idx]
        lines.append(f"{pointer_pad}^-- (Active cursor)")
        lines.append("-" * 72)

    found_step = next((e for e in trace if e["is_match"]), None)
    if found_step:
        lines.append(f"Search Result: SUCCESS! Target {target} found at index {found_step['index']}.")
    else:
        lines.append(f"Search Result: FAILED. Target {target} not present after {len(trace)} comparisons.")
    lines.append("=" * 72)
    return "\n".join(lines)


# ─── 7. Self-Organizing Search Benchmark & Complexity Analytics Engine ─────────


def benchmark_self_organizing_searches(
    n: int = 100,
    query_count: int = 1000,
    skew_ratio: float = 0.8,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Simulates non-uniform access patterns (80/20 Pareto distribution) across
    Standard Sequential Search vs. Move-To-Front (MTF) vs. Transpose
    vs. Frequency Count heuristics.

    Args:
        n: Number of unique items in list.
        query_count: Total queries to perform.
        skew_ratio: Fraction of queries targeted at the top 20% "hot" items.
        seed: Random seed for reproducibility.

    Returns:
        Dict with benchmark comparative statistics.
    """
    if n <= 0 or query_count <= 0:
        raise ValueError("n and query_count must be positive integers.")

    rng = random.Random(seed)
    base_items = list(range(n))

    # Partition into hot (20%) and cold (80%) keys
    hot_count = max(1, int(n * 0.2))
    hot_keys = base_items[:hot_count]
    cold_keys = base_items[hot_count:]

    # Generate synthetic queries following skewed Pareto distribution
    queries = []
    for _ in range(query_count):
        if rng.random() < skew_ratio and hot_keys:
            queries.append(rng.choice(hot_keys))
        else:
            queries.append(rng.choice(cold_keys) if cold_keys else rng.choice(hot_keys))

    # 1. Standard (Static) Search
    static_arr = list(base_items)
    static_comps = 0
    t0 = time.perf_counter()
    for q in queries:
        res = sequential_search(static_arr, q)
        static_comps += res.comparisons
    static_time = time.perf_counter() - t0

    # 2. Move-To-Front (MTF)
    mtf_arr = list(base_items)
    mtf_comps = 0
    t0 = time.perf_counter()
    for q in queries:
        res = sequential_search_mtf(mtf_arr, q)
        mtf_comps += res.comparisons
    mtf_time = time.perf_counter() - t0

    # 3. Transpose
    trans_arr = list(base_items)
    trans_comps = 0
    t0 = time.perf_counter()
    for q in queries:
        res = sequential_search_transpose(trans_arr, q)
        trans_comps += res.comparisons
    trans_time = time.perf_counter() - t0

    # 4. Frequency Count
    freq_organizer = FrequencyCountSearch(list(base_items))
    freq_comps = 0
    t0 = time.perf_counter()
    for q in queries:
        res = freq_organizer.search(q)
        freq_comps += res.comparisons
    freq_time = time.perf_counter() - t0

    return {
        "n_elements": n,
        "query_count": query_count,
        "skew_ratio": skew_ratio,
        "results": {
            "Standard (Static)": {
                "total_comparisons": static_comps,
                "avg_comparisons": static_comps / query_count,
                "time_sec": static_time,
                "efficiency_gain_pct": 0.0,
            },
            "Move-To-Front (MTF)": {
                "total_comparisons": mtf_comps,
                "avg_comparisons": mtf_comps / query_count,
                "time_sec": mtf_time,
                "efficiency_gain_pct": ((static_comps - mtf_comps) / static_comps) * 100.0,
            },
            "Transpose": {
                "total_comparisons": trans_comps,
                "avg_comparisons": trans_comps / query_count,
                "time_sec": trans_time,
                "efficiency_gain_pct": ((static_comps - trans_comps) / static_comps) * 100.0,
            },
            "Frequency Count": {
                "total_comparisons": freq_comps,
                "avg_comparisons": freq_comps / query_count,
                "time_sec": freq_time,
                "efficiency_gain_pct": ((static_comps - freq_comps) / static_comps) * 100.0,
            },
        },
    }


def analyze_linear_search_complexity(
    sizes: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Computes theoretical best, average (successful and unsuccessful), and worst case
    comparison numbers for standard unordered vs. ordered sequential search.

    Args:
        sizes: Sequence of array sizes N to evaluate.

    Returns:
        List of complexity records for each size.
    """
    if sizes is None:
        sizes = [10, 50, 100, 500, 1000, 5000, 10000]

    records = []
    for n in sizes:
        if n <= 0:
            continue
        records.append({
            "size": n,
            "best_case": 1,
            "avg_case_successful": (n + 1) / 2.0,
            "avg_case_unsuccessful_unordered": n,
            "avg_case_unsuccessful_ordered": (n + 1) / 2.0,
            "worst_case": n,
        })
    return records


def format_complexity_table(records: List[Dict[str, Any]]) -> str:
    """
    Renders complexity analysis records into a formatted Markdown/ASCII table.
    """
    header = (
        f"{'N Size':>8} | {'Best':>6} | {'Avg (Hit)':>10} | {'Avg Unordered Miss':>18} | "
        f"{'Avg Ordered Miss':>16} | {'Worst':>8}"
    )
    sep = "-" * len(header)
    rows = [header, sep]
    for r in records:
        row = (
            f"{r['size']:>8} | {r['best_case']:>6} | {r['avg_case_successful']:>10.1f} | "
            f"{r['avg_case_unsuccessful_unordered']:>18} | {r['avg_case_unsuccessful_ordered']:>16.1f} | "
            f"{r['worst_case']:>8}"
        )
        rows.append(row)
    return "\n".join(rows)
