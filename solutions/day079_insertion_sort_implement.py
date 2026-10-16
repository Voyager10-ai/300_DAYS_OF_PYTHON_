# Day 79: Insertion Sort Implement
#
# Problem:
#   Write a Python program / module implementing Insertion Sort and its advanced algorithmic variations.
#   Includes core pure and in-place insertion sort, binary insertion sort, range-bounded slice sorting (Timsort building block),
#   recursive insertion sort, online streaming sorter, step-by-step trace visualizer, shift counter & efficiency analytics,
#   stability verification engine, comprehensive unit test suite, and Java practice.

import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Core Insertion Sort Implementations ───────────────────────────────────


def insertion_sort(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> List[Any]:
    """
    Sorts a sequence using Insertion Sort and returns a new sorted list (pure function).

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
    insertion_sort_inplace(copied, reverse=reverse, key=key)
    return copied


def insertion_sort_inplace(
    arr: List[Any], reverse: bool = False, key: Optional[Callable[[Any], Any]] = None
) -> None:
    """
    Sorts a list in-place using Insertion Sort (O(n^2) worst/average, O(n) best-case).
    Uses shifting rather than element swaps to minimize write overhead.

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

    for i in range(1, n):
        current_item = arr[i]
        current_key = key_func(current_item)
        j = i - 1

        # Shift elements of arr[0..i-1] that are greater (or smaller if reverse) than current_key
        if not reverse:
            while j >= 0 and key_func(arr[j]) > current_key:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= 0 and key_func(arr[j]) < current_key:
                arr[j + 1] = arr[j]
                j -= 1

        arr[j + 1] = current_item


def insertion_sort_metrics(
    arr: List[Any], reverse: bool = False
) -> Tuple[List[Any], Dict[str, int]]:
    """
    Executes Insertion Sort while recording exact comparisons, shifts, and insertions executed.

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
    shifts = 0
    passes = 0

    for i in range(1, n):
        passes += 1
        key = items[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            condition = (items[j] < key) if reverse else (items[j] > key)
            if condition:
                items[j + 1] = items[j]
                shifts += 1
                j -= 1
            else:
                break

        items[j + 1] = key

    metrics = {
        "comparisons": comparisons,
        "shifts": shifts,
        "passes_executed": passes,
        "total_elements": n,
    }
    return (items, metrics)


# ─── 2. Binary Insertion Sort (O(n log n) Comparisons) ───────────────────────


def binary_search_insert_pos(
    arr: List[Any], val: Any, low: int, high: int, reverse: bool = False
) -> int:
    """
    Finds the insertion index for `val` in sorted subsegment `arr[low..high]` using binary search.
    Preserves stability by inserting after equal elements.

    Args:
        arr: List containing sorted elements in arr[low..high].
        val: Target value to place.
        low: Start index.
        high: End index (inclusive).
        reverse: If True, indicates subsegment is descending.

    Returns:
        Insertion index.
    """
    while low <= high:
        mid = (low + high) // 2
        if not reverse:
            if arr[mid] <= val:
                low = mid + 1
            else:
                high = mid - 1
        else:
            if arr[mid] >= val:
                low = mid + 1
            else:
                high = mid - 1
    return low


def binary_insertion_sort(arr: List[Any], reverse: bool = False) -> List[Any]:
    """
    Sorts a sequence using Binary Insertion Sort.
    Reduces total comparisons from O(n^2) to O(n log n) using binary search for placement.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    binary_insertion_sort_inplace(copied, reverse=reverse)
    return copied


def binary_insertion_sort_inplace(arr: List[Any], reverse: bool = False) -> None:
    """
    In-place Binary Insertion Sort.

    Args:
        arr: Mutable list.
        reverse: If True, sorts descending.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")

    n = len(arr)
    for i in range(1, n):
        selected = arr[i]
        # Find position where selected should be inserted in arr[0..i-1]
        insert_idx = binary_search_insert_pos(arr, selected, 0, i - 1, reverse=reverse)

        # Shift elements from insert_idx to i - 1 one position right
        j = i - 1
        while j >= insert_idx:
            arr[j + 1] = arr[j]
            j -= 1

        arr[insert_idx] = selected


# ─── 3. Range-Bounded Slice Insertion Sort (Timsort Subroutine) ──────────────


def insertion_sort_range(
    arr: List[Any], left: int, right: int, reverse: bool = False
) -> None:
    """
    Sorts a designated subrange arr[left..right] in-place using Insertion Sort.
    This is the fundamental small-chunk optimization routine used in Timsort and Introsort.

    Args:
        arr: Mutable list.
        left: Left boundary index (inclusive).
        right: Right boundary index (inclusive).
        reverse: If True, sorts descending.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If indices are out of bounds or left > right.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected mutable list, got {type(arr).__name__}")
    if not isinstance(left, int) or isinstance(left, bool):
        raise TypeError(f"Expected int for left, got {type(left).__name__}")
    if not isinstance(right, int) or isinstance(right, bool):
        raise TypeError(f"Expected int for right, got {type(right).__name__}")

    n = len(arr)
    if left < 0 or right >= n or left > right:
        raise ValueError(f"Invalid range [{left}, {right}] for array of length {n}")

    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1

        if not reverse:
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= left and arr[j] < key:
                arr[j + 1] = arr[j]
                j -= 1

        arr[j + 1] = key


def insertion_sort_blocks(arr: List[Any], block_size: int = 16) -> List[Any]:
    """
    Partitions an array into blocks of size `block_size` and sorts each block in-place.
    Serves as the preliminary run-creation step in hybrid algorithms like Timsort.

    Args:
        arr: Input sequence.
        block_size: Size of individual chunks to sort (must be >= 1).

    Returns:
        New list with internally sorted blocks.

    Raises:
        ValueError: If block_size < 1.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")
    if block_size < 1:
        raise ValueError(f"block_size must be >= 1, got {block_size}")

    items = list(arr)
    n = len(items)
    for start in range(0, n, block_size):
        end = min(start + block_size - 1, n - 1)
        insertion_sort_range(items, start, end)

    return items


# ─── 4. Recursive Insertion Sort & Online Streaming Sorter ───────────────────


def insertion_sort_recursive(
    arr: List[Any], n: Optional[int] = None, reverse: bool = False
) -> List[Any]:
    """
    Sorts an array using recursive Insertion Sort.

    Base case: n <= 1 (already sorted).
    Recursive step: Recursively sort arr[0..n-2], then insert arr[n-1] into sorted prefix.

    Args:
        arr: Input sequence.
        n: Subarray size (defaults to len(arr)).
        reverse: If True, sorts descending.

    Returns:
        New sorted list.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    copied = list(arr)
    _insertion_sort_recursive_helper(copied, len(copied) if n is None else n, reverse=reverse)
    return copied


def _insertion_sort_recursive_helper(arr: List[Any], n: int, reverse: bool = False) -> None:
    """Helper mutating arr in-place recursively."""
    if n <= 1:
        return

    # Sort first n - 1 elements
    _insertion_sort_recursive_helper(arr, n - 1, reverse=reverse)

    # Insert last element at its correct position in sorted array
    last = arr[n - 1]
    j = n - 2

    if not reverse:
        while j >= 0 and arr[j] > last:
            arr[j + 1] = arr[j]
            j -= 1
    else:
        while j >= 0 and arr[j] < last:
            arr[j + 1] = arr[j]
            j -= 1

    arr[j + 1] = last


class OnlineInsertionSorter:
    """
    Online data stream sorter that maintains sorted order as new elements arrive dynamically.
    Demonstrates the premier practical strength of insertion sort: efficient online streaming insertion.
    """

    def __init__(self, reverse: bool = False) -> None:
        """Initializes empty online sorter."""
        self.reverse = reverse
        self._data: List[Any] = []

    def insert(self, item: Any) -> int:
        """
        Inserts a new item into the stream maintaining sorted invariant.

        Args:
            item: Comparable element.

        Returns:
            The insertion index where item was placed.
        """
        pos = binary_search_insert_pos(self._data, item, 0, len(self._data) - 1, reverse=self.reverse)
        self._data.insert(pos, item)
        return pos

    def get_sorted(self) -> List[Any]:
        """Returns a copy of the currently maintained sorted stream."""
        return list(self._data)

    def peek_median(self) -> float:
        """
        Returns the median of the current stream in O(1) time.

        Raises:
            ValueError: If stream is empty.
        """
        if not self._data:
            raise ValueError("Cannot calculate median of empty stream")

        n = len(self._data)
        mid = n // 2
        if n % 2 == 1:
            return float(self._data[mid])
        return (self._data[mid - 1] + self._data[mid]) / 2.0

    def clear(self) -> None:
        """Resets stream."""
        self._data.clear()

    def __len__(self) -> int:
        return len(self._data)


# ─── 5. Step-by-Step Pedagogical Trace & ASCII Visualizer ─────────────────────


def trace_insertion_sort(
    arr: List[Any], reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Generates a step-by-step trace of how Insertion Sort progressively builds the sorted prefix.

    Args:
        arr: Input sequence.
        reverse: If True, sorts descending.

    Returns:
        List of trace dictionaries for each pass.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    trace: List[Dict[str, Any]] = []

    # Initial state
    trace.append({
        "step": 0,
        "inserted_item": None,
        "from_index": None,
        "to_index": None,
        "shifts": 0,
        "sorted_prefix_len": 1 if n > 0 else 0,
        "snapshot": list(items),
    })

    for i in range(1, n):
        key = items[i]
        j = i - 1
        shifts = 0

        if not reverse:
            while j >= 0 and items[j] > key:
                items[j + 1] = items[j]
                shifts += 1
                j -= 1
        else:
            while j >= 0 and items[j] < key:
                items[j + 1] = items[j]
                shifts += 1
                j -= 1

        items[j + 1] = key
        trace.append({
            "step": i,
            "inserted_item": key,
            "from_index": i,
            "to_index": j + 1,
            "shifts": shifts,
            "sorted_prefix_len": i + 1,
            "snapshot": list(items),
        })

    return trace


def render_insertion_trace(trace: List[Dict[str, Any]], max_events: int = 10) -> str:
    """
    Formats the trace into an ASCII diagram illustrating the growing sorted prefix.

    Args:
        trace: List of trace event dicts.
        max_events: Maximum rows to display.

    Returns:
        Multi-line formatted string.
    """
    lines: List[str] = []
    lines.append(f"{'Pass':<5} | {'Item':<6} | {'From->To':<9} | {'Shifts':<6} | {'Array Snapshot'}")
    lines.append("-" * 65)

    displayed = trace[:max_events]
    for ev in displayed:
        if ev["step"] == 0:
            lines.append(f"{'Init':<5} | {'-':<6} | {'-':<9} | {0:<6} | {ev['snapshot']}")
        else:
            path = f"{ev['from_index']}->{ev['to_index']}"
            lines.append(
                f"{ev['step']:<5} | {str(ev['inserted_item']):<6} | {path:<9} | {ev['shifts']:<6} | {ev['snapshot']}"
            )

    if len(trace) > max_events:
        lines.append(f"... ({len(trace) - max_events} more insertion steps omitted) ...")

    return "\n".join(lines)


# ─── 6. Shift Counter & Efficiency Analytics Engine ──────────────────────────


def count_shifts_via_insertion(arr: List[Any]) -> int:
    """
    Counts the exact number of element shift operations performed during Insertion Sort.
    For standard unique arrays, this equals the number of inversions.

    Args:
        arr: Input sequence.

    Returns:
        Total count of shifts.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    items = list(arr)
    n = len(items)
    shifts = 0

    for i in range(1, n):
        key = items[i]
        j = i - 1
        while j >= 0 and items[j] > key:
            items[j + 1] = items[j]
            shifts += 1
            j -= 1
        items[j + 1] = key

    return shifts


def analyze_insertion_efficiency(arr: List[Any]) -> Dict[str, Any]:
    """
    Analyzes how efficiently Insertion Sort handles a given input sequence.
    Contrasts actual performance against best-case O(n) and worst-case O(n^2).

    Args:
        arr: Input sequence.

    Returns:
        Dictionary containing efficiency metrics.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(arr).__name__}")

    n = len(arr)
    if n <= 1:
        return {
            "total_elements": n,
            "actual_shifts": 0,
            "max_shifts": 0,
            "shift_ratio": 0.0,
            "is_already_sorted": True,
            "efficiency_rating": "Optimal (O(1))",
        }

    max_shifts = (n * (n - 1)) // 2
    actual_shifts = count_shifts_via_insertion(arr)
    shift_ratio = round(actual_shifts / max_shifts, 4) if max_shifts > 0 else 0.0

    if actual_shifts == 0:
        rating = "Best-Case (O(n) linear time)"
    elif shift_ratio < 0.25:
        rating = "Nearly Sorted (Near-linear time)"
    elif shift_ratio > 0.75:
        rating = "Heavily Inverted (Near worst-case O(n^2))"
    else:
        rating = "Average-Case (O(n^2))"

    return {
        "total_elements": n,
        "actual_shifts": actual_shifts,
        "max_shifts": max_shifts,
        "shift_ratio": shift_ratio,
        "is_already_sorted": actual_shifts == 0,
        "efficiency_rating": rating,
    }


# ─── 7. Batch Sorter & Stability Verification Engine ──────────────────────────


def batch_insertion_sort(
    arrays: List[List[Any]], reverse: bool = False
) -> List[List[Any]]:
    """
    Sorts a collection of sequences using Insertion Sort.

    Args:
        arrays: List of sequences to sort.
        reverse: If True, sorts descending.

    Returns:
        List of sorted lists.
    """
    if not isinstance(arrays, (list, tuple)):
        raise TypeError(f"Expected list or tuple of arrays, got {type(arrays).__name__}")

    return [insertion_sort(a, reverse=reverse) for a in arrays]


def verify_insertion_sort_stability() -> bool:
    """
    Verifies that Insertion Sort is intrinsically stable.
    Since elements are shifted strictly when they are greater (or smaller),
    elements with equal keys are never swapped past one another.

    Returns:
        True if stability is preserved, False otherwise.
    """
    records = [
        ("TaskA", 3),
        ("TaskB", 1),
        ("TaskC", 3),
        ("TaskD", 2),
        ("TaskE", 3),
        ("TaskF", 1),
    ]

    sorted_records = insertion_sort(records, key=lambda x: x[1])

    # Check priority 3 items preserved relative order: TaskA, TaskC, TaskE
    priority_3 = [name for name, p in sorted_records if p == 3]
    if priority_3 != ["TaskA", "TaskC", "TaskE"]:
        return False

    # Check priority 1 items preserved relative order: TaskB, TaskF
    priority_1 = [name for name, p in sorted_records if p == 1]
    if priority_1 != ["TaskB", "TaskF"]:
        return False

    return True






