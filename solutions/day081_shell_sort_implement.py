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


# ─── 3. Gap Comparative Benchmark & Scalability Analytics ─────────────────────


def compare_gap_sequences(
    arr: List[Any], strategies: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Evaluates and compares different gap sequence strategies on the exact same dataset.

    Args:
        arr: Input sequence to sort.
        strategies: List of strategy names. Defaults to ['ciura', 'knuth', 'sedgewick', 'hibbard', 'shell'].

    Returns:
        Mapping of strategy name to performance metrics (comparisons, shifts, time_us, etc.).
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    if strategies is None:
        strategies = ["ciura", "knuth", "sedgewick", "hibbard", "shell"]

    expected = sorted(arr)
    results = {}

    for strat in strategies:
        data_copy = list(arr)
        t0 = time.perf_counter()
        sorted_res, metrics = shell_sort_metrics(data_copy, gap_sequence=strat)
        t1 = time.perf_counter()

        elapsed_us = round((t1 - t0) * 1_000_000, 2)
        is_correct = (sorted_res == expected)

        results[strat] = {
            "is_correct": is_correct,
            "comparisons": metrics["comparisons"],
            "shifts": metrics["shifts"],
            "gaps": metrics["gaps_applied"],
            "gap_count": metrics["gap_count"],
            "elapsed_us": elapsed_us,
        }

    return results


def analyze_shell_sort_scalability(
    sizes: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Analyzes algorithmic scalability across input sizes and permutation topologies:
    random, sorted, reversed, and duplicate-dense.

    Args:
        sizes: Sample input sizes. Defaults to [10, 30, 60, 120].

    Returns:
        List of analytical reports for each input size.
    """
    if sizes is None:
        sizes = [10, 30, 60, 120]

    report = []
    for n in sizes:
        # 1. Sorted array
        sorted_arr = list(range(n))
        _, sorted_m = shell_sort_metrics(sorted_arr, gap_sequence="ciura")

        # 2. Reverse sorted array
        rev_arr = list(range(n, 0, -1))
        _, rev_m = shell_sort_metrics(rev_arr, gap_sequence="ciura")

        # 3. Deterministic pseudo-random / alternating array
        pseudo_random = [(i * 37 + 13) % (n * 3) for i in range(n)]
        _, rand_m = shell_sort_metrics(pseudo_random, gap_sequence="ciura")

        # 4. Duplicate heavy
        dup_arr = [i % 5 for i in range(n)]
        _, dup_m = shell_sort_metrics(dup_arr, gap_sequence="ciura")

        report.append({
            "size": n,
            "sorted_comparisons": sorted_m["comparisons"],
            "sorted_shifts": sorted_m["shifts"],
            "reversed_comparisons": rev_m["comparisons"],
            "reversed_shifts": rev_m["shifts"],
            "random_comparisons": rand_m["comparisons"],
            "random_shifts": rand_m["shifts"],
            "duplicates_comparisons": dup_m["comparisons"],
            "duplicates_shifts": dup_m["shifts"],
            "insertion_sort_worst_case_shifts": n * (n - 1) // 2,
            "shell_vs_insertion_speedup_ratio": (
                round((n * (n - 1) / 2) / max(1, rev_m["shifts"]), 2)
            ),
        })

    return report


# ─── 4. Range-Bounded Slice Sorter & Chunk Sorter ─────────────────────────────


def shell_sort_range(
    arr: List[Any],
    start: int = 0,
    end: Optional[int] = None,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
    gap_sequence: Optional[Union[str, List[int]]] = None,
) -> List[Any]:
    """
    Sorts an in-place bounded range arr[start:end] using Shell Sort.
    Leaves all elements before start and after end unmodified.

    Args:
        arr: Mutable list to sort in-place.
        start: Start index (inclusive). Supports negative indices.
        end: End index (exclusive). Supports negative indices. Defaults to len(arr).
        reverse: If True, sorts descending.
        key: Optional comparison key function.
        gap_sequence: Strategy or custom gaps.

    Returns:
        The mutated array arr.

    Raises:
        TypeError: If arr is not a mutable list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return arr

    norm_start = start if start >= 0 else max(0, n + start)
    norm_end = n if end is None else (end if end >= 0 else max(0, n + end))

    norm_start = max(0, min(n, norm_start))
    norm_end = max(0, min(n, norm_end))

    sub_len = norm_end - norm_start
    if sub_len <= 1:
        return arr

    gaps = get_gap_sequence(gap_sequence if gap_sequence is not None else "ciura", sub_len)
    key_func = key if key is not None else (lambda x: x)

    for gap in gaps:
        for i in range(norm_start + gap, norm_end):
            temp_item = arr[i]
            temp_key = key_func(temp_item)
            j = i

            while j >= norm_start + gap:
                prev_key = key_func(arr[j - gap])
                condition = (prev_key < temp_key) if reverse else (prev_key > temp_key)
                if condition:
                    arr[j] = arr[j - gap]
                    j -= gap
                else:
                    break

            arr[j] = temp_item

    return arr


def shell_sort_chunks(
    arr: List[Any],
    chunk_size: int,
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[Any]:
    """
    Partitions the input into consecutive chunks of chunk_size and sorts each chunk
    independently using Shell Sort (pure function).

    Args:
        arr: Input sequence.
        chunk_size: Size of each chunk to sort independently.
        reverse: If True, sorts each chunk descending.
        key: Key projection function.

    Returns:
        New list with individually sorted chunks.

    Raises:
        ValueError: If chunk_size <= 0.
        TypeError: If arr is not list or tuple.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")

    result = list(arr)
    n = len(result)

    for start in range(0, n, chunk_size):
        end = min(n, start + chunk_size)
        shell_sort_range(result, start=start, end=end, reverse=reverse, key=key)

    return result


# ─── 5. Step-by-Step Gap Phase Trace & ASCII Visualizer ───────────────────────


def trace_shell_sort(
    arr: List[Any],
    reverse: bool = False,
    gap_sequence: Optional[Union[str, List[int]]] = None,
) -> List[Dict[str, Any]]:
    """
    Executes Shell Sort while collecting snapshots after each diminishing gap phase.
    Each phase renders the array h-sorted for the current gap h.

    Args:
        arr: Sequence of items.
        reverse: If True, sorts descending.
        gap_sequence: Gap sequence strategy or custom gaps.

    Returns:
        List of phase dictionaries with detailed metrics and states.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    if n <= 1:
        return []

    gaps = get_gap_sequence(gap_sequence if gap_sequence is not None else "ciura", n)
    trace = []

    for phase_idx, gap in enumerate(gaps, 1):
        state_before = list(items)
        comparisons = 0
        shifts = 0

        for i in range(gap, n):
            temp_item = items[i]
            j = i

            while j >= gap:
                comparisons += 1
                condition = (items[j - gap] < temp_item) if reverse else (items[j - gap] > temp_item)
                if condition:
                    items[j] = items[j - gap]
                    shifts += 1
                    j -= gap
                else:
                    break

            items[j] = temp_item

        desc = (
            f"Phase {phase_idx} (Gap = {gap}): Processed {gap} interleaved sub-array(s). "
            f"Array is now {gap}-sorted with {comparisons} comps and {shifts} shifts."
        )

        trace.append({
            "phase_index": phase_idx,
            "gap": gap,
            "state_before": state_before,
            "state_after": list(items),
            "comparisons": comparisons,
            "shifts": shifts,
            "description": desc,
        })

    return trace


def render_shell_trace(trace: List[Dict[str, Any]]) -> str:
    """
    Formats a list of phase traces into an ASCII execution diagram.

    Args:
        trace: Result from trace_shell_sort.

    Returns:
        Multi-line formatted ASCII string.
    """
    if not trace:
        return "Array has <= 1 element; already in trivial 1-sorted state."

    lines = []
    lines.append("=" * 72)
    lines.append("           SHELL SORT DIMINISHING GAP TRACE & VISUALIZER         ")
    lines.append("=" * 72)

    initial = trace[0]["state_before"]
    lines.append(f"Initial State : {initial}")
    lines.append("-" * 72)

    total_comps = 0
    total_shifts = 0

    for step in trace:
        p = step["phase_index"]
        gap = step["gap"]
        comps = step["comparisons"]
        shifts = step["shifts"]
        after = step["state_after"]

        total_comps += comps
        total_shifts += shifts

        lines.append(f"[Phase {p} | Gap h = {gap:<3}] Comps: {comps:<4} | Shifts: {shifts:<4}")
        lines.append(f"  Description : {step['description']}")
        lines.append(f"  h-Sorted Array: {after}")
        lines.append("-" * 72)

    final = trace[-1]["state_after"]
    lines.append(f"Final 1-Sorted Output : {final}")
    lines.append(f"Cumulative Totals     : Comparisons = {total_comps}, Shifts = {total_shifts}")
    lines.append("=" * 72)
    return "\n".join(lines)


# ─── 6. Batch Processor & Multi-Attribute Record Shell Sorter ─────────────────


def batch_shell_sort(
    datasets: List[List[Any]],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
    gap_sequence: Optional[Union[str, List[int]]] = None,
) -> List[List[Any]]:
    """
    Sorts a collection of distinct datasets using Shell Sort.
    Ensures input immutability by returning newly allocated sorted lists.

    Args:
        datasets: List of lists/tuples to sort.
        reverse: If True, sorts each dataset descending.
        key: Key projection function.
        gap_sequence: Gap sequence strategy or custom list.

    Returns:
        List of newly sorted lists.

    Raises:
        TypeError: If datasets is not a list or contains non-sequence elements.
    """
    if not isinstance(datasets, list):
        raise TypeError(f"Expected list of datasets, got {type(datasets).__name__}")

    results = []
    for idx, ds in enumerate(datasets):
        if not isinstance(ds, (list, tuple)):
            raise TypeError(f"Dataset at index {idx} must be a list or tuple")
        results.append(shell_sort(ds, reverse=reverse, key=key, gap_sequence=gap_sequence))

    return results


def shell_sort_records(
    records: List[Dict[str, Any]],
    sort_keys: List[Tuple[str, bool]],
) -> List[Dict[str, Any]]:
    """
    Sorts an array of dictionaries by multiple attributes with individual asc/desc directions.
    Since Shell Sort is unstable, multi-column sorting requires building a single composite comparison key.

    For string fields, reverse sorting is handled by custom invertible key wrappers.
    For numeric fields, reverse sorting negates the value.

    Args:
        records: List of dictionary records.
        sort_keys: List of (field_name, is_descending) tuples in order of sorting priority.

    Returns:
        New list of sorted dictionary records.

    Raises:
        TypeError: If records is not a list or sort_keys is not a list.
        KeyError: If a field in sort_keys is missing from any record.
    """
    if not isinstance(records, list):
        raise TypeError(f"Expected list of records, got {type(records).__name__}")
    if not isinstance(sort_keys, list):
        raise TypeError(f"Expected list of sort keys, got {type(sort_keys).__name__}")

    class InvertedKey:
        def __init__(self, val: Any):
            self.val = val

        def __lt__(self, other: "InvertedKey") -> bool:
            return self.val > other.val

        def __gt__(self, other: "InvertedKey") -> bool:
            return self.val < other.val

        def __eq__(self, other: Any) -> bool:
            return isinstance(other, InvertedKey) and self.val == other.val

    def record_key(item: Dict[str, Any]) -> Tuple[Any, ...]:
        key_parts = []
        for field, is_desc in sort_keys:
            if field not in item:
                raise KeyError(f"Field '{field}' missing from record {item}")
            val = item[field]
            if is_desc:
                key_parts.append(InvertedKey(val))
            else:
                key_parts.append(val)
        return tuple(key_parts)

    return shell_sort(records, reverse=False, key=record_key)





