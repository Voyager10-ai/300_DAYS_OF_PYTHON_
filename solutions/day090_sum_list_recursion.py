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
