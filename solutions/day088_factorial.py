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



# ─── 2. Divide-and-Conquer Binary Split & Memoized Factorial ──────────────────


def _binary_split_product(low: int, high: int) -> int:
    """
    Multiplies the range [low, high] inclusive using divide-and-conquer tree reduction.

    By balancing operand bit sizes during big-integer multiplication,
    reduces Karatsuba/FFT multiplication overhead compared to linear sequential accumulation.

    Time Complexity: O(M(n log n) log n) ~ O(n (log n)^2).
    Space Complexity: O(log n) call stack.
    """
    diff = high - low
    if diff < 0:
        return 1
    if diff == 0:
        return low
    if diff == 1:
        return low * high
    if diff == 2:
        return low * (low + 1) * high

    mid = (low + high) // 2
    return _binary_split_product(low, mid) * _binary_split_product(mid + 1, high)


def factorial_binary_split(n: int) -> int:
    """
    Computes n! using divide-and-conquer binary splitting.

    Significantly outperforms naive linear multiplication for large n (e.g., n >= 1000)
    due to balanced big-integer multiplication operands.

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
    return _binary_split_product(1, n)


def factorial_memoized(
    n: int,
    memo: Optional[Dict[int, int]] = None,
) -> int:
    """
    Computes n! using top-down recursion with explicit dictionary memoization.

    Args:
        n: Non-negative integer.
        memo: Optional dictionary storing precomputed factorials.

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

    if memo is None:
        memo = {}

    if 0 not in memo:
        memo[0] = 1
    if 1 not in memo:
        memo[1] = 1

    if n in memo:
        return memo[n]

    memo[n] = n * factorial_memoized(n - 1, memo)
    return memo[n]


class FactorialLookupTable:
    """
    Precomputed factorial table allowing O(1) query time for 0..max_n.
    Ideal for combinatorial applications (permutations, combinations).
    """

    def __init__(self, max_n: int = 1000) -> None:
        if not isinstance(max_n, int) or isinstance(max_n, bool):
            raise TypeError(f"max_n must be an integer, got {type(max_n).__name__}")
        if max_n < 0:
            raise ValueError(f"max_n must be non-negative, got {max_n}")

        self.max_n = max_n
        self._table: List[int] = [1] * (max_n + 1)
        for i in range(2, max_n + 1):
            self._table[i] = self._table[i - 1] * i

    def get(self, n: int) -> int:
        """Retrieves n! in O(1) time."""
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError(f"n must be an integer, got {type(n).__name__}")
        if not (0 <= n <= self.max_n):
            raise ValueError(f"n must be between 0 and {self.max_n}, got {n}")
        return self._table[n]

    def __getitem__(self, n: int) -> int:
        return self.get(n)

    def __len__(self) -> int:
        return len(self._table)



# ─── 3. Number Theory: Trailing Zeros, Stirling & Subfactorials ───────────────


def prime_factor_exponent_in_factorial(n: int, p: int) -> int:
    """
    Computes the highest exponent k such that p^k divides n!, using Legendre's Formula.

    Formula:
        E_p(n!) = floor(n / p) + floor(n / p^2) + floor(n / p^3) + ...

    Time Complexity: O(log_p n) divisions.
    Space Complexity: O(1) space.

    Args:
        n: Non-negative integer.
        p: Prime integer >= 2.

    Returns:
        Multiplicity of prime p in the prime factorization of n!.

    Raises:
        TypeError: If n or p is not an integer.
        ValueError: If n < 0 or p < 2.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if not isinstance(p, int) or isinstance(p, bool):
        raise TypeError(f"p must be an integer, got {type(p).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if p < 2:
        raise ValueError(f"p must be a prime integer >= 2, got {p}")

    count = 0
    power = p
    while power <= n:
        count += n // power
        power *= p
    return count


def count_trailing_zeros(n: int) -> int:
    """
    Counts the number of trailing zeros in the decimal representation of n!.

    Trailing zeros are formed by factors of 10 = 2 * 5. Since factors of 2 are always
    more abundant than factors of 5 in n!, the trailing zero count equals E_5(n!).

    LeetCode Reference: Problem 172: Factorial Trailing Zeroes.

    Time Complexity: O(log_5 n).
    Space Complexity: O(1).

    Args:
        n: Non-negative integer.

    Returns:
        Number of trailing zeros in n!.
    """
    return prime_factor_exponent_in_factorial(n, 5)


def count_digits_in_factorial(n: int) -> int:
    """
    Computes the number of decimal digits in n! without evaluating the full factorial.

    Uses sum of base-10 logarithms:
        digits(n!) = 1 if n <= 1 else floor(sum_{i=1..n} log10(i)) + 1
    For large n (n > 50000), Kamenetsky's formula provides O(1) approximation.

    Args:
        n: Non-negative integer.

    Returns:
        Number of digits in base-10 representation of n!.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n <= 1:
        return 1

    # Kamenetsky's formula for large n:
    # digits = floor(log10(2 * pi * n) / 2 + n * (log10(n / e))) + 1
    if n > 50000:
        val = (math.log10(2 * math.pi * n) / 2.0) + (n * (math.log10(n / math.e)))
        return math.floor(val) + 1

    # Exact logarithmic summation for exact precision
    log_sum = 0.0
    for i in range(2, n + 1):
        log_sum += math.log10(i)
    return math.floor(log_sum) + 1


def stirling_approximation(n: int) -> float:
    """
    Approximates n! using Stirling's asymptotic formula:
        n! ~ sqrt(2 * pi * n) * (n / e)^n

    Accurate for moderate to large n where exact factorial exceeds float bounds.

    Args:
        n: Positive integer.

    Returns:
        Approximate float value of n!.

    Raises:
        ValueError: If n <= 0 or n > 170 (float overflow).
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n <= 0:
        raise ValueError("Stirling approximation is defined for positive integers")
    if n > 170:
        raise OverflowError("n > 170 exceeds standard IEEE 754 float capacity")

    return math.sqrt(2.0 * math.pi * n) * ((n / math.e) ** n)


def subfactorial(n: int) -> int:
    """
    Computes the subfactorial !n (number of derangements of n elements).

    A derangement is a permutation where no element appears in its original position.
    Recurrence:
        !0 = 1, !1 = 0
        !n = (n - 1) * (!(n - 1) + !(n - 2)) for n >= 2.

    Time Complexity: O(n).
    Space Complexity: O(1) iterative space.

    Args:
        n: Non-negative integer.

    Returns:
        !n integer count of derangements.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n == 0:
        return 1
    if n == 1:
        return 0

    d0, d1 = 1, 0
    for i in range(2, n + 1):
        d0, d1 = d1, (i - 1) * (d1 + d0)

    return d1
