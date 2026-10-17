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


# ─── 6. Trace Visualizer & ASCII Step Renderer ────────────────────────────────


def trace_selection_sort(
    arr: List[Any], reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Executes Selection Sort and returns a complete, step-by-step diagnostic trace.
    Records array states, candidate comparisons, selected minimum/maximum, and swaps.

    Args:
        arr: Sequence of items.
        reverse: If True, sorts descending.

    Returns:
        List of dictionaries describing each iteration step.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    trace = []

    for i in range(n - 1):
        state_before = list(items)
        target_idx = i
        target_val = items[i]

        for j in range(i + 1, n):
            val_j = items[j]
            condition = (val_j > target_val) if reverse else (val_j < target_val)
            if condition:
                target_idx = j
                target_val = val_j

        swapped = (target_idx != i)
        if swapped:
            items[i], items[target_idx] = items[target_idx], items[i]

        extreme_name = "maximum" if reverse else "minimum"
        if swapped:
            desc = (
                f"Pass {i + 1}: Found {extreme_name} {target_val} at index {target_idx}. "
                f"Swapped arr[{i}] ({state_before[i]}) with arr[{target_idx}] ({target_val})."
            )
        else:
            desc = (
                f"Pass {i + 1}: arr[{i}] ({target_val}) is already the {extreme_name}. "
                f"No swap needed."
            )

        trace.append({
            "pass_index": i + 1,
            "boundary_index": i,
            "state_before": state_before,
            "target_idx": target_idx,
            "target_val": target_val,
            "swapped": swapped,
            "state_after": list(items),
            "description": desc,
        })

    return trace


def render_selection_trace(trace: List[Dict[str, Any]]) -> str:
    """
    Renders a trace generated by trace_selection_sort into a readable ASCII log.

    Args:
        trace: Step list from trace_selection_sort.

    Returns:
        Formatted ASCII multi-line representation.
    """
    if not trace:
        return "Array has <= 1 elements; no passes required."

    lines = []
    lines.append("=" * 68)
    lines.append("           SELECTION SORT STEP-BY-STEP EXECUTION TRACE           ")
    lines.append("=" * 68)

    initial = trace[0]["state_before"]
    lines.append(f"Initial State : {initial}")
    lines.append("-" * 68)

    for step in trace:
        p = step["pass_index"]
        b = step["boundary_index"]
        t = step["target_idx"]
        after = step["state_after"]
        swapped = step["swapped"]

        sorted_part = after[: b + 1]
        unsorted_part = after[b + 1 :]
        formatted_state = f"{sorted_part} | {unsorted_part}" if unsorted_part else f"{sorted_part}"

        status_marker = "SWAP" if swapped else "STAY"
        lines.append(f"[{status_marker}] {step['description']}")
        lines.append(f"       Current Array State: {formatted_state}")
        lines.append("-" * 68)

    final = trace[-1]["state_after"]
    lines.append(f"Final Sorted State: {final}")
    lines.append("=" * 68)
    return "\n".join(lines)


# ─── 7. Write-Minimization Analytics Engine & Batch Sorter ────────────────────


def analyze_selection_memory_writes(
    sizes: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Analyzes the write-minimization property of Selection Sort.
    Unlike Bubble Sort (up to n(n-1)/2 swaps) or Insertion Sort (up to n(n-1)/2 writes),
    Selection Sort guarantees at most n - 1 swaps (at most 2(n - 1) writes).
    This makes Selection Sort historically preferred for EEPROM/Flash memory architectures
    where write operations inflict physical cell wear or consume significant energy.

    Args:
        sizes: List of sample input sizes to evaluate. Defaults to [5, 10, 20, 50, 100].

    Returns:
        List of analytical reports for each input size across different permutations.
    """
    if sizes is None:
        sizes = [5, 10, 20, 50, 100]

    report = []
    for n in sizes:
        # Worst-case scenario for swaps in selection sort
        # A cycle permutation can require n - 1 swaps
        worst_case_arr = list(range(2, n + 1)) + [1]
        sorted_arr = list(range(1, n + 1))
        reversed_arr = list(range(n, 0, -1))

        _, worst_metrics = selection_sort_metrics(worst_case_arr)
        _, sorted_metrics = selection_sort_metrics(sorted_arr)
        _, rev_metrics = selection_sort_metrics(reversed_arr)

        theoretical_max_swaps = n - 1
        theoretical_comparisons = n * (n - 1) // 2

        report.append({
            "size": n,
            "theoretical_comparisons": theoretical_comparisons,
            "theoretical_max_swaps": theoretical_max_swaps,
            "sorted_input_swaps": sorted_metrics["swaps"],
            "reversed_input_swaps": rev_metrics["swaps"],
            "worst_case_swaps": worst_metrics["swaps"],
            "max_memory_write_operations": theoretical_max_swaps * 2,
            "bubble_sort_max_swaps": theoretical_comparisons,
            "write_reduction_factor": (
                round(theoretical_comparisons / theoretical_max_swaps, 2)
                if theoretical_max_swaps > 0
                else 1.0
            ),
        })

    return report


def batch_selection_sort(
    datasets: List[List[Any]],
    reverse: bool = False,
    key: Optional[Callable[[Any], Any]] = None,
) -> List[List[Any]]:
    """
    Sorts a collection of distinct datasets using Selection Sort.
    Ensures input immutability by producing fresh lists for each dataset.

    Args:
        datasets: List of lists/tuples to sort.
        reverse: If True, sorts each dataset descending.
        key: Key projection function.

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
        results.append(selection_sort(ds, reverse=reverse, key=key))

    return results


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestSelectionSort(unittest.TestCase):
    """Exhaustive unit test suite covering all Selection Sort variations and edge cases."""

    def setUp(self):
        self.sample = [64, 25, 12, 22, 11]
        self.expected = [11, 12, 22, 25, 64]
        self.duplicates = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        self.negatives = [-10, 5, -2, 0, 15, -7]

    # --- Core Selection Sort Tests ---
    def test_selection_sort_empty_and_single(self):
        self.assertEqual(selection_sort([]), [])
        self.assertEqual(selection_sort([42]), [42])

    def test_selection_sort_standard(self):
        self.assertEqual(selection_sort(self.sample), self.expected)
        self.assertEqual(selection_sort(self.duplicates), sorted(self.duplicates))
        self.assertEqual(selection_sort(self.negatives), sorted(self.negatives))

    def test_selection_sort_reverse(self):
        self.assertEqual(
            selection_sort(self.sample, reverse=True), sorted(self.sample, reverse=True)
        )
        self.assertEqual(
            selection_sort(self.duplicates, reverse=True),
            sorted(self.duplicates, reverse=True),
        )

    def test_selection_sort_key(self):
        words = ["banana", "pie", "apple", "fig"]
        self.assertEqual(
            selection_sort(words, key=len), sorted(words, key=len)
        )

    def test_selection_sort_inplace(self):
        arr = list(self.sample)
        selection_sort_inplace(arr)
        self.assertEqual(arr, self.expected)

    def test_selection_sort_type_error(self):
        with self.assertRaises(TypeError):
            selection_sort(12345)  # type: ignore
        with self.assertRaises(TypeError):
            selection_sort_inplace((1, 2, 3))  # type: ignore

    # --- Metrics Tests ---
    def test_selection_sort_metrics(self):
        arr = [5, 4, 3, 2, 1]
        sorted_arr, metrics = selection_sort_metrics(arr)
        self.assertEqual(sorted_arr, [1, 2, 3, 4, 5])
        n = len(arr)
        # Selection sort always executes strictly n(n-1)/2 comparisons
        self.assertEqual(metrics["comparisons"], n * (n - 1) // 2)
        self.assertLessEqual(metrics["swaps"], n - 1)
        self.assertEqual(metrics["passes_executed"], n - 1)

    # --- Double Selection Sort Tests ---
    def test_double_selection_sort_basics(self):
        self.assertEqual(double_selection_sort([]), [])
        self.assertEqual(double_selection_sort([99]), [99])
        self.assertEqual(double_selection_sort(self.sample), self.expected)
        self.assertEqual(
            double_selection_sort(self.sample, reverse=True),
            sorted(self.sample, reverse=True),
        )
        self.assertEqual(
            double_selection_sort(self.duplicates), sorted(self.duplicates)
        )

    def test_double_selection_sort_edge_cases(self):
        # Max at left boundary, min at right boundary
        inverted = [100, 50, 20, 10, 1]
        self.assertEqual(double_selection_sort(inverted), [1, 10, 20, 50, 100])
        self.assertEqual(
            double_selection_sort(inverted, reverse=True), [100, 50, 20, 10, 1]
        )
        # All identical elements
        identical = [7, 7, 7, 7]
        self.assertEqual(double_selection_sort(identical), [7, 7, 7, 7])

    # --- Stable Selection Sort Tests ---
    def test_stable_selection_sort_preserves_order(self):
        items = [(2, "first"), (1, "only"), (2, "second"), (2, "third")]
        result = stable_selection_sort(items, key=lambda x: x[0])
        expected_tuples = [(1, "only"), (2, "first"), (2, "second"), (2, "third")]
        self.assertEqual(result, expected_tuples)

    def test_verify_selection_sort_stability(self):
        res = verify_selection_sort_stability()
        self.assertTrue(res["all_cases_passed"])
        self.assertTrue(res["standard_sort_unstable_demonstrated"])

    # --- K-Pass Partial Sorter & Order Statistics Tests ---
    def test_selection_sort_k_passes(self):
        arr = [50, 20, 10, 40, 30]
        # After 2 passes, first 2 elements must be 10, 20
        res = selection_sort_k_passes(arr, k=2)
        self.assertEqual(res[:2], [10, 20])
        self.assertEqual(sorted(res), [10, 20, 30, 40, 50])

    def test_find_kth_order_statistics(self):
        arr = [7, 10, 4, 3, 20, 15]
        # Sorted: [3, 4, 7, 10, 15, 20]
        self.assertEqual(find_kth_smallest_via_selection(arr, 1), 3)
        self.assertEqual(find_kth_smallest_via_selection(arr, 3), 7)
        self.assertEqual(find_kth_smallest_via_selection(arr, 6), 20)

        self.assertEqual(find_kth_largest_via_selection(arr, 1), 20)
        self.assertEqual(find_kth_largest_via_selection(arr, 2), 15)
        self.assertEqual(find_kth_largest_via_selection(arr, 6), 3)

    def test_kth_statistics_invalid_k(self):
        with self.assertRaises(ValueError):
            find_kth_smallest_via_selection([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            find_kth_smallest_via_selection([1, 2, 3], 4)

    # --- Recursive Selection Sort Tests ---
    def test_selection_sort_recursive(self):
        self.assertEqual(selection_sort_recursive([]), [])
        self.assertEqual(selection_sort_recursive([5]), [5])
        self.assertEqual(selection_sort_recursive(self.sample), self.expected)
        self.assertEqual(
            selection_sort_recursive(self.sample, reverse=True),
            sorted(self.sample, reverse=True),
        )

    # --- Range Slice Selection Sort Tests ---
    def test_selection_sort_range(self):
        arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        # Sort only index 3 to 7: elements at indices 3,4,5,6 -> [7, 6, 5, 4] -> [4, 5, 6, 7]
        selection_sort_range(arr, start=3, end=7)
        self.assertEqual(arr[:3], [10, 9, 8])
        self.assertEqual(arr[3:7], [4, 5, 6, 7])
        self.assertEqual(arr[7:], [3, 2, 1])

    # --- Trace Visualizer & ASCII Tests ---
    def test_trace_and_render(self):
        arr = [5, 2, 4, 1]
        trace = trace_selection_sort(arr)
        self.assertEqual(len(trace), 3)
        output = render_selection_trace(trace)
        self.assertIn("SELECTION SORT STEP-BY-STEP EXECUTION TRACE", output)
        self.assertIn("Final Sorted State: [1, 2, 4, 5]", output)

    # --- Memory Analytics & Batch Tests ---
    def test_analyze_selection_memory_writes(self):
        report = analyze_selection_memory_writes([4, 8])
        self.assertEqual(len(report), 2)
        for row in report:
            self.assertIn("write_reduction_factor", row)
            self.assertLessEqual(row["worst_case_swaps"], row["size"] - 1)

    def test_batch_selection_sort(self):
        sets = [[3, 2, 1], [9, 5, 7], [1]]
        results = batch_selection_sort(sets)
        self.assertEqual(results, [[1, 2, 3], [5, 7, 9], [1]])







