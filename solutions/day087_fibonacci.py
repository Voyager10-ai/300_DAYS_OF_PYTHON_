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



# ─── 4. Fast Doubling Fibonacci Algorithm O(log n) ────────────────────────────


def fibonacci_fast_doubling_pair(n: int) -> Tuple[int, int]:
    """
    Computes (F(n), F(n+1)) using the Fast Doubling identities recursively.

    Identities:
        F(2k)   = F(k) * (2*F(k+1) - F(k))
        F(2k+1) = F(k+1)^2 + F(k)^2

    Time Complexity: O(log n) multiplication steps.
    Space Complexity: O(log n) call stack frames.

    Args:
        n: Non-negative integer index.

    Returns:
        Tuple (F(n), F(n+1)).

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n == 0:
        return (0, 1)

    a, b = fibonacci_fast_doubling_pair(n >> 1)
    c = a * ((b << 1) - a)        # F(2k) = F(k) * (2*F(k+1) - F(k))
    d = a * a + b * b             # F(2k+1) = F(k)^2 + F(k+1)^2

    if n & 1:
        return (d, c + d)         # If odd: F(2k+1), F(2k+2) = F(2k+1) + F(2k)
    return (c, d)                 # If even: F(2k), F(2k+1)


def fibonacci_fast_doubling(n: int) -> int:
    """
    Computes F(n) in O(log n) time using fast doubling recursion.

    Args:
        n: Non-negative integer Fibonacci index.

    Returns:
        F(n) integer value.
    """
    return fibonacci_fast_doubling_pair(n)[0]


def fibonacci_fast_doubling_iterative(n: int) -> int:
    """
    Computes F(n) using iterative fast doubling with bitwise traversal.

    Traverses the binary representation of n from MSB to LSB.
    Achieves logarithmic execution with O(1) auxiliary memory.

    Time Complexity: O(log n) arithmetic operations.
    Space Complexity: O(1) auxiliary space.

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

    if n == 0:
        return 0

    a, b = 0, 1
    # Iterate through bits from highest non-zero bit down to bit 0
    bit_length = n.bit_length()
    for i in range(bit_length - 1, -1, -1):
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if (n >> i) & 1:
            a, b = d, c + d
        else:
            a, b = c, d

    return a


def fibonacci_fast_doubling_with_metrics(
    n: int,
) -> Tuple[int, Dict[str, Any]]:
    """
    Computes F(n) using fast doubling while measuring bit operations and time.

    Args:
        n: Non-negative integer index.

    Returns:
        Tuple of (result, metrics_dict).
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    t0 = time.perf_counter()
    res = fibonacci_fast_doubling_iterative(n)
    elapsed = time.perf_counter() - t0

    metrics = {
        "n": n,
        "result": res,
        "bit_length": n.bit_length() if n > 0 else 1,
        "doubling_steps": n.bit_length() if n > 0 else 0,
        "time_seconds": elapsed,
        "algorithm": "Iterative Fast Doubling O(log n)",
    }
    return (res, metrics)



# ─── 5. 2x2 Matrix Binary Exponentiation O(log n) ─────────────────────────────

Matrix2x2 = Tuple[Tuple[int, int], Tuple[int, int]]


def _matrix_multiply_2x2(
    A: Matrix2x2,
    B: Matrix2x2,
    mod: Optional[int] = None,
) -> Matrix2x2:
    """Multiplies two 2x2 integer matrices with optional modular reduction."""
    if mod is not None:
        return (
            (
                (A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod,
                (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod,
            ),
            (
                (A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod,
                (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod,
            ),
        )
    return (
        (
            A[0][0] * B[0][0] + A[0][1] * B[1][0],
            A[0][0] * B[0][1] + A[0][1] * B[1][1],
        ),
        (
            A[1][0] * B[0][0] + A[1][1] * B[1][0],
            A[1][0] * B[0][1] + A[1][1] * B[1][1],
        ),
    )


def _matrix_power_2x2(
    M: Matrix2x2,
    p: int,
    mod: Optional[int] = None,
) -> Matrix2x2:
    """Raises a 2x2 matrix to the p-th power in O(log p) matrix multiplications."""
    result: Matrix2x2 = ((1, 0), (0, 1))  # Identity matrix
    base = M

    while p > 0:
        if p & 1:
            result = _matrix_multiply_2x2(result, base, mod)
        base = _matrix_multiply_2x2(base, base, mod)
        p >>= 1

    return result


def fibonacci_matrix(n: int, mod: Optional[int] = None) -> int:
    """
    Computes F(n) [optionally modulo mod] using 2x2 matrix binary exponentiation.

    Based on the linear recurrence transformation:
        [[F(n+1), F(n)], [F(n), F(n-1)]] = [[1, 1], [1, 0]]^n

    Time Complexity: O(log n) matrix multiplications.
    Space Complexity: O(1) auxiliary space.

    Args:
        n: Non-negative integer Fibonacci index.
        mod: Optional positive integer modulus for modular arithmetic.

    Returns:
        F(n) [mod mod] integer value.

    Raises:
        TypeError: If n or mod is not an integer.
        ValueError: If n is negative or mod <= 0.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if mod is not None:
        if not isinstance(mod, int) or isinstance(mod, bool):
            raise TypeError(f"mod must be an integer, got {type(mod).__name__}")
        if mod <= 0:
            raise ValueError(f"mod must be positive, got {mod}")

    if n == 0:
        return 0

    trans: Matrix2x2 = ((1, 1), (1, 0))
    powered = _matrix_power_2x2(trans, n - 1, mod)
    result = powered[0][0]
    return (result % mod) if mod is not None else result


def fibonacci_matrix_with_metrics(
    n: int,
    mod: Optional[int] = None,
) -> Tuple[int, Dict[str, Any]]:
    """
    Computes F(n) via matrix exponentiation while measuring execution metrics.

    Args:
        n: Non-negative integer Fibonacci index.
        mod: Optional modulus.

    Returns:
        Tuple of (result, metrics_dict).
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    t0 = time.perf_counter()
    res = fibonacci_matrix(n, mod)
    elapsed = time.perf_counter() - t0

    metrics = {
        "n": n,
        "result": res,
        "mod": mod,
        "matrix_multiplications": (n - 1).bit_length() if n > 1 else 0,
        "time_seconds": elapsed,
        "algorithm": "2x2 Matrix Binary Exponentiation O(log n)",
    }
    return (res, metrics)



# ─── 6. Fibonacci Generator, Streamer & Identification ────────────────────────


def _is_perfect_square(x: int) -> bool:
    """Returns True if integer x is a non-negative perfect square."""
    if x < 0:
        return False
    s = math.isqrt(x)
    return s * s == x


def is_fibonacci_number(x: int) -> bool:
    """
    Determines if a number x is a valid Fibonacci number in O(1) time.

    By Gessel's theorem, an integer x is a Fibonacci number if and only if
    5*x^2 + 4 or 5*x^2 - 4 is a perfect square.

    Args:
        x: Non-negative integer to test.

    Returns:
        True if x is in the Fibonacci sequence, False otherwise.

    Raises:
        TypeError: If x is not an integer.
        ValueError: If x is negative.
    """
    if not isinstance(x, int) or isinstance(x, bool):
        raise TypeError(f"x must be an integer, got {type(x).__name__}")
    if x < 0:
        raise ValueError(f"x must be non-negative, got {x}")

    return _is_perfect_square(5 * x * x + 4) or _is_perfect_square(5 * x * x - 4)


def fibonacci_generator(
    limit: Optional[int] = None,
) -> Generator[int, None, None]:
    """
    Generates Fibonacci numbers lazily in O(1) memory space.

    Args:
        limit: Optional maximum number of Fibonacci terms to yield.
               If None, yields indefinitely.

    Yields:
        Consecutive Fibonacci numbers: F(0), F(1), F(2), ...

    Raises:
        TypeError: If limit is not an int or None.
        ValueError: If limit < 0.
    """
    if limit is not None:
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise TypeError(f"limit must be an integer or None, got {type(limit).__name__}")
        if limit < 0:
            raise ValueError(f"limit must be non-negative, got {limit}")

    a, b = 0, 1
    yielded = 0

    while limit is None or yielded < limit:
        yield a
        a, b = b, a + b
        yielded += 1


def fibonacci_sequence_list(count: int) -> List[int]:
    """
    Generates a list containing the first count Fibonacci numbers.

    Args:
        count: Number of elements to generate.

    Returns:
        List of first count Fibonacci numbers.
    """
    return list(fibonacci_generator(limit=count))


def nearest_fibonacci(x: int) -> Tuple[int, int]:
    """
    Finds the Fibonacci number closest to x, and returns (nearest_fib, distance).

    Args:
        x: Non-negative integer.

    Returns:
        Tuple of (closest_fibonacci_number, abs_difference).

    Raises:
        TypeError: If x is not an integer.
        ValueError: If x is negative.
    """
    if not isinstance(x, int) or isinstance(x, bool):
        raise TypeError(f"x must be an integer, got {type(x).__name__}")
    if x < 0:
        raise ValueError(f"x must be non-negative, got {x}")

    if x == 0:
        return (0, 0)

    a, b = 0, 1
    while b < x:
        a, b = b, a + b

    # Closest is either a or b
    if abs(x - a) <= abs(b - x):
        return (a, abs(x - a))
    return (b, abs(b - x))



# ─── 7. Fibonacci Search Algorithm for Sorted Arrays ──────────────────────────


def fibonacci_search(arr: List[Any], target: Any) -> int:
    """
    Searches for target in a sorted list using the Fibonacci Search algorithm.

    Fibonacci search divides the search space according to Fibonacci numbers.
    Unlike Binary Search, it requires only addition and subtraction rather than
    division or bit shifts, offering advantages on constrained arithmetic hardware.

    Time Complexity: O(log n) comparisons.
    Space Complexity: O(1) auxiliary space.

    Args:
        arr: Sorted list of comparable elements in ascending order.
        target: Element to find.

    Returns:
        Index of target if found; -1 otherwise.

    Raises:
        TypeError: If arr is not a list.
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")

    n = len(arr)
    if n == 0:
        return -1

    # Initialize Fibonacci numbers:
    # fib_m2 is (m-2)'th Fibonacci number
    # fib_m1 is (m-1)'th Fibonacci number
    # fib_m is m'th Fibonacci number (smallest >= n)
    fib_m2 = 0
    fib_m1 = 1
    fib_m = fib_m2 + fib_m1

    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m = fib_m2 + fib_m1

    # Marks eliminated range from front
    offset = -1

    while fib_m > 1:
        # Check valid index
        i = min(offset + fib_m2, n - 1)

        if arr[i] < target:
            # Move Fibonacci numbers 1 down, reset offset
            fib_m = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i
        elif arr[i] > target:
            # Move Fibonacci numbers 2 down
            fib_m = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1
        else:
            return i

    # Comparing the last candidate element
    if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
        return offset + 1

    return -1


def fibonacci_search_with_metrics(
    arr: List[Any],
    target: Any,
) -> Tuple[int, Dict[str, Any]]:
    """
    Performs Fibonacci search on a sorted list while recording probe path and metrics.

    Args:
        arr: Sorted list of comparable elements.
        target: Element to locate.

    Returns:
        Tuple of (index_or_minus_1, metrics_dict).
    """
    if not isinstance(arr, list):
        raise TypeError(f"arr must be a list, got {type(arr).__name__}")

    t0 = time.perf_counter()
    n = len(arr)
    probes: List[int] = []
    comparisons = 0

    if n == 0:
        elapsed = time.perf_counter() - t0
        return (-1, {"index": -1, "comparisons": 0, "probes": [], "time_seconds": elapsed})

    fib_m2 = 0
    fib_m1 = 1
    fib_m = fib_m2 + fib_m1

    while fib_m < n:
        fib_m2 = fib_m1
        fib_m1 = fib_m
        fib_m = fib_m2 + fib_m1

    offset = -1
    result_idx = -1

    while fib_m > 1:
        i = min(offset + fib_m2, n - 1)
        probes.append(i)
        comparisons += 1

        if arr[i] < target:
            fib_m = fib_m1
            fib_m1 = fib_m2
            fib_m2 = fib_m - fib_m1
            offset = i
        elif arr[i] > target:
            fib_m = fib_m2
            fib_m1 = fib_m1 - fib_m2
            fib_m2 = fib_m - fib_m1
        else:
            result_idx = i
            break

    if result_idx == -1 and fib_m1 and offset + 1 < n:
        probes.append(offset + 1)
        comparisons += 1
        if arr[offset + 1] == target:
            result_idx = offset + 1

    elapsed = time.perf_counter() - t0
    metrics = {
        "index": result_idx,
        "found": result_idx != -1,
        "comparisons": comparisons,
        "probes": probes,
        "array_size": n,
        "time_seconds": elapsed,
        "algorithm": "Fibonacci Search O(log n)",
    }
    return (result_idx, metrics)
