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
import decimal
from decimal import Decimal, getcontext
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



# ─── 3. Closed-Form Binet's Formula & Precision-Safe Approximation ────────────


def fibonacci_binet(n: int) -> int:
    """
    Computes F(n) using Binet's closed-form formula using 64-bit floating point.

    Formula:
        phi = (1 + sqrt(5)) / 2  (the Golden Ratio ~ 1.6180339887)
        F(n) = round(phi^n / sqrt(5))

    Time Complexity: O(1) mathematical power operation.
    Space Complexity: O(1) auxiliary space.

    Note on Precision:
        Standard IEEE 754 64-bit double precision has 53 bits of mantissa,
        retaining accuracy strictly for n <= 70. For n >= 71, floating-point
        rounding errors corrupt the lowest significant digits. For larger n,
        use `fibonacci_binet_decimal` or exact integer algorithms.

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

    sqrt_5 = math.sqrt(5)
    phi = (1.0 + sqrt_5) / 2.0
    return round((phi ** n) / sqrt_5)


def fibonacci_binet_decimal(n: int, precision: Optional[int] = None) -> int:
    """
    Computes F(n) via Binet's formula using arbitrary-precision Decimals.

    Dynamically scales decimal context precision to avoid precision truncation,
    allowing exact results for n > 70.

    Time Complexity: O(M(d)) where d is precision digits and M is multiplication cost.
    Space Complexity: O(d) for Decimal storage.

    Args:
        n: Non-negative integer index.
        precision: Optional decimal precision. Defaults to max(100, int(n * 0.21) + 50).

    Returns:
        Exact F(n) integer value.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n <= 1:
        return n

    req_prec = max(100, int(n * 0.22) + 50) if precision is None else precision
    current_prec = decimal.getcontext().prec
    try:
        decimal.getcontext().prec = req_prec
        d5 = Decimal(5)
        sqrt_5 = d5.sqrt()
        phi = (Decimal(1) + sqrt_5) / Decimal(2)
        psi = (Decimal(1) - sqrt_5) / Decimal(2)
        # F(n) = (phi^n - psi^n) / sqrt(5)
        fn_dec = (phi ** n - psi ** n) / sqrt_5
        return int(fn_dec.to_integral_value(rounding=decimal.ROUND_HALF_UP))
    finally:
        decimal.getcontext().prec = current_prec


def fibonacci_binet_with_metrics(n: int) -> Tuple[int, Dict[str, Any]]:
    """
    Computes F(n) using Binet formula and returns metrics on accuracy and speed.

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
    if n <= 70:
        res = fibonacci_binet(n)
        method = "64-bit Float Binet"
    else:
        res = fibonacci_binet_decimal(n)
        method = "Arbitrary-Precision Decimal Binet"
    elapsed = time.perf_counter() - t0

    metrics = {
        "n": n,
        "result": res,
        "method": method,
        "exact_within_float_limits": n <= 70,
        "time_seconds": elapsed,
        "algorithm": "Closed-Form Binet O(1) / O(log n)",
    }
    return (res, metrics)
