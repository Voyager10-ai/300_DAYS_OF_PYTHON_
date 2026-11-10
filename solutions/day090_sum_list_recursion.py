# Day 90: Sum of List (Recursion)
#
# Problem:
#   Implement recursive algorithms to calculate the sum of numbers in a list,
#   as well as arbitrarily nested multi-dimensional lists.
#   Includes:
#     - Head-tail recursive slicing O(n^2 time, O(n) space due to list copying)
#     - Index pointer recursion O(n time, O(n) stack space without slicing)
#     - Tail-recursive accumulator pattern O(n)
#     - Divide-and-conquer binary split recursion O(n time, O(log n) stack depth)
#     - High-precision pairwise summation for minimizing floating-point roundoff
#     - Arbitrarily nested recursive list summation (flat and deep)
#     - Depth-weighted nested list sums (LeetCode 339 & 364)
#     - Recursion step tree visualizer
#     - Algorithm performance benchmarking suite
#     - Comprehensive unit test suite and Java practice code

import time
import math
import unittest
from typing import List, Dict, Tuple, Any, Optional, Union


# ─── 1. Core Recursive Summation & Tail Recursion ──────────────────────────────


def sum_list_recursive_slice(arr: List[Union[int, float]]) -> Union[int, float]:
    """
    Computes list sum using naive head-and-tail recursion via list slicing.

    Time Complexity: O(n^2) because each slice arr[1:] creates an O(n) copy.
    Space Complexity: O(n^2) auxiliary memory due to accumulated slice objects.

    Args:
        arr: List of integer or float numbers.

    Returns:
        Sum of elements in arr (0 if empty).

    Raises:
        TypeError: If arr is not a list or elements are not numeric.
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")

    if not arr:
        return 0

    first = arr[0]
    if not isinstance(first, (int, float)) or isinstance(first, bool):
        raise TypeError(f"List elements must be int or float, got {type(first).__name__}")

    return first + sum_list_recursive_slice(arr[1:])


def sum_list_recursive_index(
    arr: List[Union[int, float]],
    index: int = 0,
) -> Union[int, float]:
    """
    Computes list sum recursively using an index pointer without slicing.

    Eliminates O(n) list slicing overhead, reducing time complexity to O(n).

    Time Complexity: O(n) additions.
    Space Complexity: O(n) call stack depth.

    Args:
        arr: List of numbers.
        index: Starting element index (defaults to 0).

    Returns:
        Sum of elements from index to len(arr) - 1.

    Raises:
        TypeError: If arr is not a list or elements are not numeric.
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("index must be an integer")

    if index >= len(arr):
        return 0

    val = arr[index]
    if not isinstance(val, (int, float)) or isinstance(val, bool):
        raise TypeError(f"List element at index {index} must be numeric, got {type(val).__name__}")

    return val + sum_list_recursive_index(arr, index + 1)


def sum_list_tail_recursive(
    arr: List[Union[int, float]],
    index: int = 0,
    accumulator: Union[int, float] = 0,
) -> Union[int, float]:
    """
    Computes list sum using tail recursion with an accumulator parameter.

    Args:
        arr: List of numbers.
        index: Current scanning index.
        accumulator: Running total.

    Returns:
        Sum of all elements.
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("index must be an integer")

    if index >= len(arr):
        return accumulator

    val = arr[index]
    if not isinstance(val, (int, float)) or isinstance(val, bool):
        raise TypeError(f"List element at index {index} must be numeric, got {type(val).__name__}")

    return sum_list_tail_recursive(arr, index + 1, accumulator + val)


def sum_list_with_metrics(
    arr: List[Union[int, float]],
) -> Tuple[Union[int, float], Dict[str, Any]]:
    """
    Computes list sum recursively while tracking execution statistics.

    Args:
        arr: List of numeric values.

    Returns:
        Tuple of (total_sum, metrics_dict).
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")

    t0 = time.perf_counter()
    additions = 0

    def _helper(idx: int) -> Union[int, float]:
        nonlocal additions
        if idx >= len(arr):
            return 0
        val = arr[idx]
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError(f"Element must be numeric, got {type(val).__name__}")
        additions += 1
        return val + _helper(idx + 1)

    total = _helper(0)
    elapsed = time.perf_counter() - t0

    metrics = {
        "length": len(arr),
        "sum": total,
        "additions": additions,
        "time_seconds": elapsed,
        "algorithm": "Index-based Linear Recursion O(n)",
    }
    return (total, metrics)



# ─── 2. Divide-and-Conquer Logarithmic & Pairwise Summation ───────────────────


def sum_list_divide_and_conquer(
    arr: List[Union[int, float]],
    low: int = 0,
    high: Optional[int] = None,
) -> Union[int, float]:
    """
    Computes list sum using divide-and-conquer binary splitting.

    Divides the array into two equal halves recursively:
        sum(arr[low..high]) = sum(arr[low..mid]) + sum(arr[mid+1..high])

    Reduces call stack depth from O(n) to O(log n), allowing summation of lists
    with hundreds of thousands of elements without triggering RecursionError.

    Time Complexity: O(n) additions.
    Space Complexity: O(log n) call stack frames.

    Args:
        arr: List of numbers.
        low: Starting index (inclusive).
        high: Ending index (inclusive). Defaults to len(arr) - 1.

    Returns:
        Sum of elements within [low, high].

    Raises:
        TypeError: If elements are non-numeric.
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")

    if not arr:
        return 0

    if high is None:
        high = len(arr) - 1

    if low > high:
        return 0
    if low == high:
        val = arr[low]
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError(f"Element at index {low} must be numeric, got {type(val).__name__}")
        return val

    mid = (low + high) // 2
    left_sum = sum_list_divide_and_conquer(arr, low, mid)
    right_sum = sum_list_divide_and_conquer(arr, mid + 1, high)
    return left_sum + right_sum


def sum_list_pairwise(
    arr: List[Union[int, float]],
    block_size: int = 16,
) -> Union[int, float]:
    """
    Computes list sum using high-precision pairwise summation.

    Pairwise summation is the algorithm adopted in high-performance computing
    (including NumPy and Julia) to significantly reduce floating-point roundoff errors.
    While naive accumulation accumulates error O(n * eps), pairwise summation
    bounds error to O(eps * log n).

    Args:
        arr: List of floating point or integer numbers.
        block_size: Base case threshold for iterative chunk summation (defaults to 16).

    Returns:
        High-precision accumulated sum.
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")

    n = len(arr)
    if n == 0:
        return 0

    def _pairwise_helper(start: int, length: int) -> Union[int, float]:
        if length <= block_size:
            # Base case: linear sum for small blocks
            total: Union[int, float] = 0
            for i in range(start, start + length):
                val = arr[i]
                if not isinstance(val, (int, float)) or isinstance(val, bool):
                    raise TypeError(f"Element at index {i} must be numeric, got {type(val).__name__}")
                total += val
            return total

        half = length // 2
        return _pairwise_helper(start, half) + _pairwise_helper(start + half, length - half)

    return _pairwise_helper(0, n)



# ─── 3. Deep Nested List Recursive Summation & Weighted Solvers ───────────────


def max_nesting_depth(nested: List[Any], current_depth: int = 1) -> int:
    """
    Computes the maximum depth of an arbitrarily nested list structure.

    Args:
        nested: List of elements and sublists.
        current_depth: Current recursion depth.

    Returns:
        Maximum integer depth (1 for a flat non-empty list, 0 for empty list).
    """
    if not isinstance(nested, list):
        return current_depth - 1
    if not nested:
        return current_depth if current_depth > 1 else 0

    max_d = current_depth
    for item in nested:
        if isinstance(item, list):
            sub_d = max_nesting_depth(item, current_depth + 1)
            if sub_d > max_d:
                max_d = sub_d
    return max_d


def sum_nested_list(nested: List[Any]) -> Union[int, float]:
    """
    Recursively sums all numeric values in an arbitrarily nested list of any depth.

    Example:
        sum_nested_list([1, [2, [3, 4], 5], [[6]], 7]) -> 28

    Time Complexity: O(N) where N is total number of nodes/elements.
    Space Complexity: O(D) where D is maximum nesting depth.

    Args:
        nested: List containing numbers and/or nested lists.

    Returns:
        Total accumulated numeric sum.

    Raises:
        TypeError: If non-list, non-numeric element encountered.
    """
    if not isinstance(nested, list):
        raise TypeError(f"Expected a list, got {type(nested).__name__}")

    total: Union[int, float] = 0
    for item in nested:
        if isinstance(item, list):
            total += sum_nested_list(item)
        elif isinstance(item, (int, float)) and not isinstance(item, bool):
            total += item
        else:
            raise TypeError(f"Invalid element type in nested list: {type(item).__name__}")

    return total


def sum_nested_list_weighted(nested: List[Any], depth: int = 1) -> int:
    """
    LeetCode 339: Nested List Weight Sum.

    Given a nested list of integers, returns the sum of all integers in the list
    weighted by their depth. Each element at depth d is multiplied by d.

    Example:
        [[1, 1], 2, [1, 1]] -> 1*2 + 1*2 + 2*1 + 1*2 + 1*2 = 10
        [1, [4, [6]]] -> 1*1 + 4*2 + 6*3 = 27

    Args:
        nested: Arbitrarily nested list of integers.
        depth: Current depth level (starts at 1).

    Returns:
        Depth-weighted integer sum.
    """
    if not isinstance(nested, list):
        raise TypeError(f"Expected a list, got {type(nested).__name__}")

    total = 0
    for item in nested:
        if isinstance(item, list):
            total += sum_nested_list_weighted(item, depth + 1)
        elif isinstance(item, int) and not isinstance(item, bool):
            total += item * depth
        else:
            raise TypeError(f"Expected integer, got {type(item).__name__}")

    return total


def sum_nested_list_inverse_weighted(nested: List[Any]) -> int:
    """
    LeetCode 364: Nested List Weight Sum II.

    Returns the sum of all integers in the list weighted by their inverted depth:
    Weight of an integer = (max_depth - current_depth + 1).

    Example:
        [[1, 1], 2, [1, 1]] -> max_depth = 2
        Depth 1 weight: 2 - 1 + 1 = 2 -> 2 * 2 = 4
        Depth 2 weight: 2 - 2 + 1 = 1 -> 4 * 1 = 4
        Total = 4 + 4 = 8

    Args:
        nested: Arbitrarily nested list of integers.

    Returns:
        Inverted depth-weighted integer sum.
    """
    if not isinstance(nested, list):
        raise TypeError(f"Expected a list, got {type(nested).__name__}")
    if not nested:
        return 0

    max_d = max_nesting_depth(nested)

    def _inverse_helper(sublist: List[Any], depth: int) -> int:
        sub_total = 0
        for item in sublist:
            if isinstance(item, list):
                sub_total += _inverse_helper(item, depth + 1)
            elif isinstance(item, int) and not isinstance(item, bool):
                weight = max_d - depth + 1
                sub_total += item * weight
            else:
                raise TypeError(f"Expected integer, got {type(item).__name__}")
        return sub_total

    return _inverse_helper(nested, 1)


def count_nested_elements(nested: List[Any]) -> int:
    """Recursively counts total atomic (non-list) values inside nested list."""
    if not isinstance(nested, list):
        return 1
    count = 0
    for item in nested:
        if isinstance(item, list):
            count += count_nested_elements(item)
        else:
            count += 1
    return count



# ─── 4. Step-by-Step Recursion Visualizer & Benchmarking ──────────────────────


def visualize_recursion_tree(
    arr: List[Union[int, float]],
    mode: str = "divide_and_conquer",
) -> str:
    """
    Renders an ASCII diagram tracing recursive execution call trees.

    Args:
        arr: Small list of numbers (recommended len <= 8).
        mode: Either "divide_and_conquer" (default) or "linear".

    Returns:
        Formatted ASCII string diagram.
    """
    if len(arr) > 16:
        raise ValueError("Visualizer is limited to list length <= 16 for readable output")

    lines: List[str] = []

    if mode == "divide_and_conquer":
        lines.append(f"Divide-and-Conquer Binary Split Sum Tree for {arr}:")
        lines.append("=" * 68)

        def _build_dnc(low: int, high: int, prefix: str = "", is_last: bool = True) -> Union[int, float]:
            branch = "└── " if is_last else "├── "
            if low == high:
                val = arr[low]
                lines.append(f"{prefix}{branch}arr[{low}] = {val}")
                return val
            mid = (low + high) // 2
            curr_str = f"sum(arr[{low}..{high}])"
            lines.append(f"{prefix}{branch}{curr_str}")

            next_prefix = prefix + ("    " if is_last else "│   ")
            l_val = _build_dnc(low, mid, next_prefix, False)
            r_val = _build_dnc(mid + 1, high, next_prefix, True)
            res = l_val + r_val
            return res

        total = _build_dnc(0, len(arr) - 1, "", True)
        lines.append("=" * 68)
        lines.append(f"Returned Combined Sum = {total}")

    else:
        lines.append(f"Linear Index-based Recursion Stack for {arr}:")
        lines.append("=" * 68)
        for i in range(len(arr)):
            indent = "  " * i
            lines.append(f"{indent}--> sum_list_index(arr, index={i}) [val = {arr[i]}]")
        indent = "  " * len(arr)
        lines.append(f"{indent}Base case hit: index={len(arr)} >= len -> return 0")
        for i in range(len(arr) - 1, -1, -1):
            indent = "  " * i
            lines.append(f"{indent}<-- return {arr[i]} + sub_sum")
        lines.append("=" * 68)

    return "\n".join(lines)


def benchmark_sum_algorithms(
    lengths: Optional[List[int]] = None,
    iterations: int = 20,
) -> Dict[str, Any]:
    """
    Benchmarks and compares recursive and iterative summation algorithms.

    Algorithms:
      - Recursive Slicing O(n^2) (tested for n <= 500)
      - Recursive Indexing O(n) (tested for n <= 500)
      - Divide-and-Conquer O(log n depth)
      - Pairwise Summation
      - Builtin Python sum() (C implementation baseline)

    Args:
        lengths: List of array sizes to test.
        iterations: Number of trials per test.

    Returns:
        Structured benchmark dictionary.
    """
    if lengths is None:
        lengths = [10, 50, 200, 1000, 5000, 20000]

    records: List[Dict[str, Any]] = []

    for n in lengths:
        data = list(range(1, n + 1))
        row: Dict[str, Any] = {"n": n}

        # 1. Recursive Slicing (only for n <= 500)
        if n <= 500:
            times: List[float] = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                sum_list_recursive_slice(data)
                times.append(time.perf_counter() - t0)
            row["slice"] = min(times)
        else:
            row["slice"] = None

        # 2. Recursive Indexing (n <= 500)
        if n <= 500:
            times = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                sum_list_recursive_index(data)
                times.append(time.perf_counter() - t0)
            row["index"] = min(times)
        else:
            row["index"] = None

        # 3. Divide-and-Conquer Binary Split
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            sum_list_divide_and_conquer(data)
            times.append(time.perf_counter() - t0)
        row["divide_conquer"] = min(times)

        # 4. Pairwise Summation
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            sum_list_pairwise(data)
            times.append(time.perf_counter() - t0)
        row["pairwise"] = min(times)

        # 5. Builtin sum()
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            sum(data)
            times.append(time.perf_counter() - t0)
        row["builtin_sum"] = min(times)

        records.append(row)

    return {"records": records, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """
    Formats the benchmark dictionary into an ASCII comparison table.

    Args:
        benchmark_data: Output from benchmark_sum_algorithms.

    Returns:
        Formatted ASCII table string.
    """
    lines: List[str] = []
    lines.append("List Summation Algorithms Performance Benchmark")
    lines.append("=" * 88)
    header = (
        f"{'n':>7} | {'Recursive Slice':>16} | {'Recursive Index':>16} | "
        f"{'Divide & Conquer':>17} | {'Pairwise':>11} | {'Builtin sum()':>14}"
    )
    lines.append(header)
    lines.append("-" * 88)

    def _fmt(val: Optional[float]) -> str:
        if val is None:
            return "N/A (Stack)"
        us = val * 1_000_000.0
        if us < 1.0:
            return f"{us * 1000.0:.1f} ns"
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['n']:>7} | "
            f"{_fmt(r['slice']):>16} | "
            f"{_fmt(r['index']):>16} | "
            f"{_fmt(r['divide_conquer']):>17} | "
            f"{_fmt(r['pairwise']):>11} | "
            f"{_fmt(r['builtin_sum']):>14}"
        )
        lines.append(line)

    lines.append("=" * 88)
    return "\n".join(lines)
