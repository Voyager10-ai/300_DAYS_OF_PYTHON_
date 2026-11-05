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
        memo = {}

    if 0 not in memo:
        memo[0] = 0
    if 1 not in memo:
        memo[1] = 1

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



# ─── 8. Step-by-Step Visualizer & Recursion Call Tree ─────────────────────────


def visualize_fibonacci_call_tree(n: int) -> str:
    """
    Renders an ASCII tree diagram representing the naive recursive execution call tree.

    Illustrates exponential branching and repeated subproblem calculations.

    Args:
        n: Non-negative integer index (recommended <= 6).

    Returns:
        Formatted ASCII string diagram.

    Raises:
        ValueError: If n > 7 (to avoid console buffer explosion).
    """
    if n > 7:
        raise ValueError("Call tree visualizer is limited to n <= 7 due to exponential size")
    if n < 0:
        raise ValueError("n must be non-negative")

    lines: List[str] = []
    lines.append(f"Naive Recursive Call Tree for F({n}) [Total calls: {2 * fibonacci_iterative(n + 1) - 1 if n > 0 else 1}]:")
    lines.append("=" * 60)

    def _build_tree(val: int, prefix: str = "", is_last: bool = True) -> None:
        branch = "└── " if is_last else "├── "
        lines.append(f"{prefix}{branch}F({val})")
        if val > 1:
            next_prefix = prefix + ("    " if is_last else "│   ")
            _build_tree(val - 1, next_prefix, False)
            _build_tree(val - 2, next_prefix, True)

    _build_tree(n, "", True)
    return "\n".join(lines)


def visualize_fibonacci_steps(n: int) -> str:
    """
    Generates a step-by-step ASCII table tracing Fibonacci progression up to n.

    Displays index, subproblem terms, computed sum, and convergence to Golden Ratio.

    Args:
        n: Target Fibonacci index.

    Returns:
        Formatted table as a string.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    lines: List[str] = []
    lines.append(f"Fibonacci Sequence Derivation & Golden Ratio Convergence (0..{n})")
    lines.append("=" * 72)
    header = f"{'k':>4} | {'F(k-2)':>12} | {'F(k-1)':>12} | {'F(k)':>14} | {'Ratio F(k)/F(k-1)':>18}"
    lines.append(header)
    lines.append("-" * 72)

    if n == 0:
        lines.append(f"{0:>4} | {'-':>12} | {'-':>12} | {0:>14} | {'-':>18}")
        return "\n".join(lines)

    lines.append(f"{0:>4} | {'-':>12} | {'-':>12} | {0:>14} | {'-':>18}")
    lines.append(f"{1:>4} | {'-':>12} | {0:>12} | {1:>14} | {'-':>18}")

    a, b = 0, 1
    for k in range(2, n + 1):
        prev2, prev1 = a, b
        a, b = b, a + b
        ratio_str = f"{(b / prev1):.10f}" if prev1 > 0 else "-"
        lines.append(f"{k:>4} | {prev2:>12} | {prev1:>12} | {b:>14} | {ratio_str:>18}")

    lines.append("=" * 72)
    lines.append(f"Golden Ratio (phi) exact limit: {(1 + math.sqrt(5)) / 2:.10f}")
    return "\n".join(lines)



# ─── 9. Algorithm Performance Benchmarking Engine ─────────────────────────────


def benchmark_fibonacci_algorithms(
    test_values: Optional[List[int]] = None,
    iterations: int = 5,
) -> Dict[str, Any]:
    """
    Benchmarks and compares all Fibonacci calculation algorithms across scale orders.

    Measures average execution duration across multiple trials for:
      - Naive Recursive (n <= 30)
      - Top-Down Memoized DP
      - Iterative Bottom-Up
      - Closed-Form Binet Formula (n <= 70)
      - 2x2 Matrix Exponentiation
      - Fast Doubling Iterative

    Args:
        test_values: List of n values to benchmark. Defaults to [10, 25, 30, 100, 1000, 10000].
        iterations: Number of warmup/timed runs per algorithm per n.

    Returns:
        Structured dictionary containing benchmarking metrics.
    """
    if test_values is None:
        test_values = [10, 25, 30, 100, 1000, 10000]

    records: List[Dict[str, Any]] = []

    for n in test_values:
        row: Dict[str, Any] = {"n": n}

        # 1. Naive recursive (only up to 30 to prevent execution timeout)
        if n <= 30:
            times: List[float] = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                fibonacci_recursive(n)
                times.append(time.perf_counter() - t0)
            row["recursive"] = min(times)
        else:
            row["recursive"] = None

        # 2. Memoized DP (n <= 500 to avoid recursion stack overflow)
        if n <= 500:
            times = []
            try:
                for _ in range(iterations):
                    t0 = time.perf_counter()
                    fibonacci_memoized(n, {})
                    times.append(time.perf_counter() - t0)
                row["memoized"] = min(times)
            except RecursionError:
                row["memoized"] = None
        else:
            row["memoized"] = None

        # 3. Iterative bottom-up
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            fibonacci_iterative(n)
            times.append(time.perf_counter() - t0)
        row["iterative"] = min(times)

        # 4. Binet Formula
        if n <= 70:
            times = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                fibonacci_binet(n)
                times.append(time.perf_counter() - t0)
            row["binet"] = min(times)
        else:
            row["binet"] = None

        # 5. Matrix Exponentiation
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            fibonacci_matrix(n)
            times.append(time.perf_counter() - t0)
        row["matrix"] = min(times)

        # 6. Fast Doubling Iterative
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            fibonacci_fast_doubling_iterative(n)
            times.append(time.perf_counter() - t0)
        row["fast_doubling"] = min(times)

        records.append(row)

    return {"test_values": test_values, "records": records, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """
    Formats the benchmark dictionary into an ASCII comparison table.

    Args:
        benchmark_data: Output from benchmark_fibonacci_algorithms.

    Returns:
        Formatted ASCII table string.
    """
    lines: List[str] = []
    lines.append("Fibonacci Algorithms Performance Benchmark (Time in Microseconds µs)")
    lines.append("=" * 95)
    header = (
        f"{'n':>7} | {'Recursive':>13} | {'Memoized DP':>13} | {'Iterative':>13} | "
        f"{'Binet O(1)':>13} | {'Matrix O(log)':>14} | {'Fast Double':>14}"
    )
    lines.append(header)
    lines.append("-" * 95)

    def _fmt(val: Optional[float]) -> str:
        if val is None:
            return "N/A (OOM/Time)"
        us = val * 1_000_000.0
        if us < 0.001:
            return f"{us * 1000.0:.2f} ns"
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['n']:>7} | "
            f"{_fmt(r['recursive']):>13} | "
            f"{_fmt(r['memoized']):>13} | "
            f"{_fmt(r['iterative']):>13} | "
            f"{_fmt(r['binet']):>13} | "
            f"{_fmt(r['matrix']):>14} | "
            f"{_fmt(r['fast_doubling']):>14}"
        )
        lines.append(line)

    lines.append("=" * 95)
    return "\n".join(lines)



# ─── 10. Comprehensive Unit Test Suite ────────────────────────────────────────


class TestFibonacciImplementations(unittest.TestCase):
    """Exhaustive test suite verifying correctness, edge cases, and consistency."""

    def setUp(self) -> None:
        # Standard known sequence 0..15
        self.known_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

    def test_base_cases(self) -> None:
        """Tests F(0) and F(1) across all implementation engines."""
        engines = [
            fibonacci_recursive,
            fibonacci_iterative,
            fibonacci_memoized,
            fibonacci_lru_cached,
            fibonacci_fast_doubling,
            fibonacci_fast_doubling_iterative,
            fibonacci_matrix,
            fibonacci_binet,
            fibonacci_binet_decimal,
        ]
        for engine in engines:
            with self.subTest(engine=engine.__name__):
                self.assertEqual(engine(0), 0)
                self.assertEqual(engine(1), 1)

    def test_known_sequence_consistency(self) -> None:
        """Verifies that all algorithms compute identical values for n in 0..15."""
        for n, expected in enumerate(self.known_sequence):
            self.assertEqual(fibonacci_recursive(n), expected)
            self.assertEqual(fibonacci_iterative(n), expected)
            self.assertEqual(fibonacci_memoized(n), expected)
            self.assertEqual(fibonacci_lru_cached(n), expected)
            self.assertEqual(fibonacci_fast_doubling(n), expected)
            self.assertEqual(fibonacci_fast_doubling_iterative(n), expected)
            self.assertEqual(fibonacci_matrix(n), expected)
            self.assertEqual(fibonacci_binet(n), expected)
            self.assertEqual(fibonacci_binet_decimal(n), expected)

    def test_large_fibonacci_values(self) -> None:
        """Verifies large Fibonacci computations for fast doubling, matrix and decimal Binet."""
        test_n = [50, 100, 200, 500]
        for n in test_n:
            val_iter = fibonacci_iterative(n)
            val_fast = fibonacci_fast_doubling_iterative(n)
            val_matrix = fibonacci_matrix(n)
            val_binet_dec = fibonacci_binet_decimal(n)

            self.assertEqual(val_fast, val_iter)
            self.assertEqual(val_matrix, val_iter)
            self.assertEqual(val_binet_dec, val_iter)

    def test_modular_fibonacci(self) -> None:
        """Verifies modular arithmetic properties using matrix exponentiation."""
        mod = 1_000_000_007
        for n in [10, 50, 100, 250]:
            expected = fibonacci_iterative(n) % mod
            self.assertEqual(fibonacci_matrix(n, mod=mod), expected)

    def test_invalid_types_raise_type_error(self) -> None:
        """Ensures non-integer types raise TypeError."""
        invalid_inputs = ["10", 3.14, None, [5], (1, 2), True, False]
        for val in invalid_inputs:
            with self.assertRaises(TypeError):
                fibonacci_iterative(val)  # type: ignore
            with self.assertRaises(TypeError):
                fibonacci_fast_doubling_iterative(val)  # type: ignore
            with self.assertRaises(TypeError):
                fibonacci_matrix(val)  # type: ignore

    def test_negative_values_raise_value_error(self) -> None:
        """Ensures negative indices raise ValueError."""
        negatives = [-1, -5, -100]
        for val in negatives:
            with self.assertRaises(ValueError):
                fibonacci_iterative(val)
            with self.assertRaises(ValueError):
                fibonacci_fast_doubling_iterative(val)
            with self.assertRaises(ValueError):
                fibonacci_matrix(val)

    def test_generator_and_sequence(self) -> None:
        """Tests infinite generator and list slice helper."""
        gen = fibonacci_generator()
        first_10 = [next(gen) for _ in range(10)]
        self.assertEqual(first_10, self.known_sequence[:10])
        self.assertEqual(fibonacci_sequence_list(10), self.known_sequence[:10])

    def test_is_fibonacci_number(self) -> None:
        """Tests mathematical identification of Fibonacci numbers."""
        for num in self.known_sequence:
            self.assertTrue(is_fibonacci_number(num))
        non_fibs = [4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 20, 22, 100]
        for num in non_fibs:
            self.assertFalse(is_fibonacci_number(num))

    def test_nearest_fibonacci(self) -> None:
        """Tests closest Fibonacci calculation."""
        self.assertEqual(nearest_fibonacci(0), (0, 0))
        self.assertIn(nearest_fibonacci(4), [(3, 1), (5, 1)])
        self.assertEqual(nearest_fibonacci(10), (8, 2))
        self.assertEqual(nearest_fibonacci(13), (13, 0))

    def test_fibonacci_search(self) -> None:
        """Tests Fibonacci search on sorted lists."""
        arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        for idx, val in enumerate(arr):
            self.assertEqual(fibonacci_search(arr, val), idx)
        self.assertEqual(fibonacci_search(arr, 999), -1)
        self.assertEqual(fibonacci_search(arr, 1), -1)
        self.assertEqual(fibonacci_search([], 5), -1)
        self.assertEqual(fibonacci_search([42], 42), 0)
        self.assertEqual(fibonacci_search([42], 10), -1)

    def test_metrics_structures(self) -> None:
        """Tests structure and keys in metrics return dictionaries."""
        _, m_iter = fibonacci_iterative_with_metrics(10)
        self.assertIn("additions", m_iter)
        self.assertIn("time_seconds", m_iter)

        _, m_memo = fibonacci_memoized_with_metrics(10)
        self.assertIn("cache_hits", m_memo)
        self.assertIn("cache_misses", m_memo)

        _, m_fast = fibonacci_fast_doubling_with_metrics(10)
        self.assertIn("doubling_steps", m_fast)

        idx, m_search = fibonacci_search_with_metrics([1, 3, 5, 7, 9], 7)
        self.assertEqual(idx, 3)
        self.assertIn("probes", m_search)
        self.assertIn("comparisons", m_search)



# ─── 11. Interactive CLI Demonstration ────────────────────────────────────────


def main() -> None:
    """Demonstrates all Fibonacci implementations, search, visualizers, and benchmark."""
    print("=" * 80)
    print("                 DAY 87: FIBONACCI ALGORITHMS & SUITE                   ")
    print("=" * 80)

    # 1. Compare Core Algorithms for F(15)
    n = 15
    f_rec = fibonacci_recursive(n)
    f_iter = fibonacci_iterative(n)
    f_memo = fibonacci_memoized(n)
    f_fast = fibonacci_fast_doubling_iterative(n)
    f_mat = fibonacci_matrix(n)
    f_bin = fibonacci_binet(n)

    print(f"\n[1] Algorithm Output Consistency for F({n}):")
    print(f"    - Naive Recursive      : {f_rec}")
    print(f"    - Memoized Top-Down DP : {f_memo}")
    print(f"    - Iterative Bottom-Up  : {f_iter}")
    print(f"    - Fast Doubling O(log) : {f_fast}")
    print(f"    - 2x2 Matrix O(log)    : {f_mat}")
    print(f"    - Binet Closed-Form    : {f_bin}")

    # 2. Large Scale Computation (F(100) and F(300))
    big_n = 100
    big_fast = fibonacci_fast_doubling_iterative(big_n)
    big_mat = fibonacci_matrix(big_n)
    big_dec = fibonacci_binet_decimal(big_n)
    print(f"\n[2] High-Precision Evaluation for F({big_n}):")
    print(f"    - Fast Doubling : {big_fast}")
    print(f"    - 2x2 Matrix    : {big_mat}")
    print(f"    - Decimal Binet : {big_dec}")
    print(f"    - Digits count  : {len(str(big_fast))} digits")

    # 3. Fibonacci Streaming & Membership Detection
    print("\n[3] Generator Stream & Gessel Membership Test:")
    first_12 = fibonacci_sequence_list(12)
    print(f"    First 12 terms : {first_12}")
    test_vals = [55, 89, 90, 144, 200]
    for v in test_vals:
        print(f"    is_fibonacci_number({v:<3}) -> {is_fibonacci_number(v)}")

    # 4. Fibonacci Search on Sorted Array
    sample_arr = [10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100, 235]
    target = 85
    idx, m_search = fibonacci_search_with_metrics(sample_arr, target)
    print(f"\n[4] Fibonacci Search in Sorted List:")
    print(f"    Array       : {sample_arr}")
    print(f"    Target      : {target}")
    print(f"    Found Index : {idx} (Probes visited: {m_search['probes']}, Comparisons: {m_search['comparisons']})")

    # 5. Call Tree Visualization for F(4)
    print("\n[5] Naive Call Tree Visualizer:")
    print(visualize_fibonacci_call_tree(4))

    # 6. Step-by-Step Table and Golden Ratio Convergence
    print("\n[6] Step-by-Step Sequence Derivation (0..8):")
    print(visualize_fibonacci_steps(8))

    # 7. Benchmark Comparison
    print("\n[7] Multi-Algorithm Benchmark Comparison:")
    bench_data = benchmark_fibonacci_algorithms(test_values=[10, 25, 30, 100, 1000], iterations=3)
    print(format_benchmark_table(bench_data))

    print("\n" + "=" * 80)
    print("                      DEMONSTRATION COMPLETE                                   ")
    print("=" * 80)


if __name__ == "__main__":
    main()
