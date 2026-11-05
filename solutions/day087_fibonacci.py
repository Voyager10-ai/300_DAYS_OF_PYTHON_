# Day 87: Fibonacci
#
# Problem:
#   Implement multiple algorithms to compute the n-th Fibonacci number F(n).
#   F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n >= 2.
#   Includes naive recursion, iterative bottom-up, memoised top-down,
#   closed-form Binet's formula, matrix exponentiation O(log n),
#   space-optimised generator, Fibonacci search, step-by-step visualiser,
#   performance benchmark, comprehensive unit tests, and Java practice code.

import time
import math
import unittest
from typing import List, Dict, Tuple, Any, Optional, Generator
from functools import lru_cache


# ─── 1. Core Iterative & Recursive Fibonacci ──────────────────────────────────


def fibonacci_recursive(n: int) -> int:
    """
    Computes the n-th Fibonacci number using naive tree recursion.

    Time Complexity: O(2^n) — exponential due to overlapping subproblems.
    Space Complexity: O(n) call stack depth.

    Args:
        n: Non-negative integer Fibonacci index.

    Returns:
        F(n) integer value.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """
    Computes F(n) using bottom-up iterative dynamic programming.

    Time Complexity: O(n) single linear pass.
    Space Complexity: O(1) — only two rolling variables.

    Args:
        n: Non-negative integer Fibonacci index.

    Returns:
        F(n) integer value.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_iterative_with_metrics(n: int) -> Tuple[int, Dict[str, Any]]:
    """
    Computes F(n) iteratively while tracking additions performed and elapsed time.

    Args:
        n: Non-negative integer Fibonacci index.

    Returns:
        Tuple of (result, metrics_dict).
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    t0 = time.perf_counter()
    additions = 0

    if n <= 1:
        result = n
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
            additions += 1
        result = b

    elapsed = time.perf_counter() - t0
    metrics = {
        "n": n,
        "result": result,
        "additions": additions,
        "time_seconds": elapsed,
        "algorithm": "Iterative Bottom-Up O(n)",
    }
    return (result, metrics)



# ─── 2. Top-Down Memoized Fibonacci (Dynamic Programming) ─────────────────────


def fibonacci_memoized(
    n: int,
    memo: Optional[Dict[int, int]] = None,
) -> int:
    """
    Computes F(n) using top-down recursion with explicit dictionary memoization.

    Eliminates redundant subproblem computations by caching intermediate results.

    Time Complexity: O(n) unique subproblems computed once.
    Space Complexity: O(n) call stack depth + memo dictionary table.

    Args:
        n: Non-negative integer Fibonacci index.
        memo: Optional dictionary storing previously computed Fibonacci values.

    Returns:
        F(n) integer value.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if memo is None:
        memo = {0: 0, 1: 1}

    if n in memo:
        return memo[n]

    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fibonacci_lru_cached(n: int) -> int:
    """
    Computes F(n) using recursion wrapped with functools.lru_cache.

    Time Complexity: O(n) memoized lookup.
    Space Complexity: O(n) call stack and cache entries.

    Args:
        n: Non-negative integer index.

    Returns:
        F(n) integer value.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n <= 1:
        return n
    return fibonacci_lru_cached(n - 1) + fibonacci_lru_cached(n - 2)


def fibonacci_memoized_with_metrics(
    n: int,
) -> Tuple[int, Dict[str, Any]]:
    """
    Computes F(n) with memoization while capturing cache hit/miss statistics.

    Args:
        n: Non-negative integer Fibonacci index.

    Returns:
        Tuple of (result, metrics_dict).
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    t0 = time.perf_counter()
    memo: Dict[int, int] = {0: 0, 1: 1}
    hits = 0
    misses = 0

    def _helper(k: int) -> int:
        nonlocal hits, misses
        if k in memo:
            hits += 1
            return memo[k]
        misses += 1
        memo[k] = _helper(k - 1) + _helper(k - 2)
        return memo[k]

    result = _helper(n)
    elapsed = time.perf_counter() - t0

    metrics = {
        "n": n,
        "result": result,
        "cache_hits": hits,
        "cache_misses": misses,
        "memo_size": len(memo),
        "time_seconds": elapsed,
        "algorithm": "Top-Down Memoized DP O(n)",
    }
    return (result, metrics)
