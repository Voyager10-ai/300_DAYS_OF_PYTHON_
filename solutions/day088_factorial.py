# Day 88: Factorial
#
# Problem:
#   Implement algorithms and mathematical tools for calculating the factorial of a
#   non-negative integer n! (n! = n * (n - 1) * ... * 1, with 0! = 1).
#   Includes:
#     - Iterative linear multiplication O(n)
#     - Naive recursive O(n) and tail-recursive O(n)
#     - Divide-and-conquer binary split tree multiplication O(n (log n)^2)
#     - Memoized factorial & precomputed table
#     - Legendre's formula for prime factor exponents & trailing zeros O(log_p n)
#     - Digit count estimation via Kamenetsky's and Stirling's approximation
#     - Subfactorial / derangements (!n)
#     - Visualizer table and recursion breakdown
#     - Multi-algorithm performance benchmark
#     - Comprehensive unit test suite and Java practice code

import time
import math
import unittest
from typing import List, Dict, Tuple, Any, Optional, Generator


# ─── 1. Core Iterative, Recursive & Tail-Recursive Factorial ──────────────────


def factorial_iterative(n: int) -> int:
    """
    Computes n! iteratively using a linear accumulator.

    Time Complexity: O(n) multiplications.
    Space Complexity: O(1) auxiliary space (excluding result size).

    Args:
        n: Non-negative integer.

    Returns:
        n! integer value.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    """
    Computes n! using standard recursion.

    Time Complexity: O(n) recursive calls and multiplications.
    Space Complexity: O(n) call stack depth.

    Args:
        n: Non-negative integer.

    Returns:
        n! integer value.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_tail_recursive(n: int, accumulator: int = 1) -> int:
    """
    Computes n! using tail-recursive accumulator pattern.

    Args:
        n: Non-negative integer.
        accumulator: Running product (defaults to 1).

    Returns:
        n! integer value.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n <= 1:
        return accumulator
    return factorial_tail_recursive(n - 1, accumulator * n)


def factorial_with_metrics(n: int) -> Tuple[int, Dict[str, Any]]:
    """
    Computes n! iteratively while collecting operational metrics.

    Args:
        n: Non-negative integer.

    Returns:
        Tuple of (result, metrics_dict).
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    t0 = time.perf_counter()
    multiplications = 0
    result = 1

    for i in range(2, n + 1):
        result *= i
        multiplications += 1

    elapsed = time.perf_counter() - t0
    metrics = {
        "n": n,
        "result": result,
        "multiplications": multiplications,
        "time_seconds": elapsed,
        "digit_count": len(str(result)),
        "algorithm": "Iterative Linear O(n)",
    }
    return (result, metrics)
