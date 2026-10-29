# Day 86: A Power by B (pow(a, b) / Fast Exponentiation)
#
# Problem:
#   Implement algorithms to compute A raised to the power B (A^B).
#   Includes naive linear multiplication O(B), divide-and-conquer binary
#   exponentiation (recursive squaring) O(log B), bitwise iterative exponentiation
#   with O(1) auxiliary space, modular exponentiation (A^B mod M), fractional
#   and real exponentiation via Taylor/Newton series (A^B = exp(B * ln A)),
#   2x2 matrix binary exponentiation for O(log N) Fibonacci numbers, step-by-step
#   ASCII bit-traversal visualizer, performance benchmarking, exhaustive unit tests,
#   and Java practice code.
#
# LeetCode Reference:
#   Problem 50: Pow(x, n) [Medium]

import time
import math
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Callable, Union


# ─── 1. Naive Linear Power Implementations ────────────────────────────────────


def power_naive_iterative(
    a: Union[int, float],
    b: int,
) -> Union[int, float]:
    """
    Computes a^b using naive iterative multiplication.

    Time Complexity: O(|b|) multiplications.
    Space Complexity: O(1) auxiliary space.

    Args:
        a: Base number (integer or float).
        b: Exponent (integer).

    Returns:
        Result of a raised to the power b.

    Raises:
        TypeError: If b is not an integer or a is not a number.
        ZeroDivisionError: If a is 0 and b is negative.
    """
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"Exponent b must be an integer, got {type(b).__name__}")
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        raise TypeError(f"Base a must be an int or float, got {type(a).__name__}")

    # Edge case: 0 raised to negative power is division by zero
    if a == 0:
        if b < 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        if b == 0:
            return 1  # 0^0 is conventionally 1 in Python and IEEE standards
        return 0

    if b == 0:
        return 1

    exp = abs(b)
    result = 1
    for _ in range(exp):
        result *= a

    return (1.0 / result) if b < 0 else result


def power_naive_recursive(
    a: Union[int, float],
    b: int,
) -> Union[int, float]:
    """
    Computes a^b using naive linear recursion.

    Time Complexity: O(|b|) recursive calls and multiplications.
    Space Complexity: O(|b|) call stack depth.

    Args:
        a: Base number.
        b: Exponent integer.

    Returns:
        Result of a^b.

    Raises:
        TypeError: If invalid types are supplied.
        ZeroDivisionError: If 0 is raised to negative power.
    """
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"Exponent b must be an integer, got {type(b).__name__}")
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        raise TypeError(f"Base a must be an int or float, got {type(a).__name__}")

    if a == 0:
        if b < 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        if b == 0:
            return 1
        return 0

    if b < 0:
        return 1.0 / power_naive_recursive(a, -b)

    if b == 0:
        return 1

    return a * power_naive_recursive(a, b - 1)


def power_naive_with_metrics(
    a: Union[int, float],
    b: int,
) -> Tuple[Union[int, float], Dict[str, Any]]:
    """
    Computes a^b naively while tracking multiplications and execution elapsed time.

    Args:
        a: Base.
        b: Exponent.

    Returns:
        Tuple of (result, metrics_dict).
    """
    t0 = time.perf_counter()
    multiplications = 0

    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError("Exponent b must be an integer")

    if a == 0 and b < 0:
        raise ZeroDivisionError("0.0 cannot be raised to a negative power")

    if b == 0:
        ans = 1
    else:
        exp = abs(b)
        ans = 1
        for _ in range(exp):
            ans *= a
            multiplications += 1
        if b < 0:
            ans = 1.0 / ans

    elapsed = time.perf_counter() - t0
    metrics = {
        "base": a,
        "exponent": b,
        "result": ans,
        "multiplications": multiplications,
        "time_seconds": elapsed,
        "algorithm": "Naive Iterative (O(|b|))",
    }
    return (ans, metrics)


# ─── 2. Divide-and-Conquer Binary Exponentiation (Recursive Squaring) ─────────


def power_binary_recursive(
    a: Union[int, float],
    b: int,
) -> Union[int, float]:
    """
    Computes a^b using recursive binary exponentiation (exponentiation by squaring).

    Divides the exponent by 2 at each step:
      - If b == 0: return 1
      - If b is even: (a^(b // 2))^2
      - If b is odd:  a * (a^(b // 2))^2

    Time Complexity: O(log |b|) multiplications.
    Space Complexity: O(log |b|) recursion call stack.

    Args:
        a: Base number.
        b: Exponent integer.

    Returns:
        Value of a^b.

    Raises:
        TypeError: If b is not an integer.
        ZeroDivisionError: If 0 is raised to negative power.
    """
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"Exponent b must be an integer, got {type(b).__name__}")
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        raise TypeError(f"Base a must be an int or float, got {type(a).__name__}")

    if a == 0:
        if b < 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        if b == 0:
            return 1
        return 0

    if b < 0:
        return 1.0 / power_binary_recursive(a, -b)

    if b == 0:
        return 1

    half = power_binary_recursive(a, b // 2)
    squared = half * half

    return (a * squared) if (b % 2 == 1) else squared


def power_binary_recursive_with_metrics(
    a: Union[int, float],
    b: int,
) -> Tuple[Union[int, float], Dict[str, Any]]:
    """
    Computes a^b via recursive squaring while profiling exact operations.

    Args:
        a: Base.
        b: Exponent.

    Returns:
        Tuple of (result, metrics_dict).
    """
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError("Exponent b must be an integer")
    if a == 0 and b < 0:
        raise ZeroDivisionError("0.0 cannot be raised to a negative power")

    multiplications = 0
    max_depth = 0

    def _helper(base: Union[int, float], exp: int, depth: int) -> Union[int, float]:
        nonlocal multiplications, max_depth
        max_depth = max(max_depth, depth)

        if exp == 0:
            return 1

        half = _helper(base, exp // 2, depth + 1)
        res = half * half
        multiplications += 1

        if exp % 2 == 1:
            res *= base
            multiplications += 1

        return res

    t0 = time.perf_counter()
    if a == 0:
        ans = 1 if b == 0 else 0
    elif b == 0:
        ans = 1
    elif b < 0:
        raw = _helper(a, -b, 1)
        ans = 1.0 / raw
    else:
        ans = _helper(a, b, 1)

    elapsed = time.perf_counter() - t0

    metrics = {
        "base": a,
        "exponent": b,
        "result": ans,
        "multiplications": multiplications,
        "recursion_depth": max_depth,
        "time_seconds": elapsed,
        "algorithm": "Recursive Binary Exponentiation (O(log |b|))",
    }
    return (ans, metrics)

