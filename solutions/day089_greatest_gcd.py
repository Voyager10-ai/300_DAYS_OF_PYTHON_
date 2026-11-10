# Day 89: Greatest GCD (Greatest Common Divisor)
#
# Problem:
#   Implement algorithms and mathematical tools for calculating the Greatest Common
#   Divisor (GCD) / Highest Common Factor (HCF) and Least Common Multiple (LCM)
#   of integers.
#   Includes:
#     - Naive brute-force search O(min(a, b))
#     - Subtraction-based Euclidean algorithm (historical Greek method)
#     - Standard Division-based Euclidean algorithm (iterative & recursive) O(log(min(a, b)))
#     - Binary GCD (Stein's algorithm) using bitwise shifts and subtractions
#     - Extended Euclidean algorithm (Bézout's coefficients: ax + by = gcd(a, b))
#     - Modular multiplicative inverse and linear Diophantine equations
#     - Multi-number GCD and LCM for lists / tuples
#     - Array Greatest Pair GCD search
#     - Step-by-step Euclidean and Stein trace visualizers
#     - Algorithm performance benchmarking suite
#     - Comprehensive unit tests and Java practice code

import time
import math
import unittest
from typing import List, Dict, Tuple, Any, Optional, Union


# ─── 1. Core Euclidean and Subtraction GCD Implementations ────────────────────


def gcd_naive(a: int, b: int) -> int:
    """
    Computes GCD(a, b) by brute-force testing all integers from min(|a|, |b|) down to 1.

    Time Complexity: O(min(|a|, |b|)).
    Space Complexity: O(1).

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Greatest common divisor as a non-negative integer.

    Raises:
        TypeError: If a or b is not an integer.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    a, b = abs(a), abs(b)
    if a == 0:
        return b
    if b == 0:
        return a

    for candidate in range(min(a, b), 0, -1):
        if a % candidate == 0 and b % candidate == 0:
            return candidate

    return 1


def gcd_subtraction(a: int, b: int) -> int:
    """
    Computes GCD(a, b) using repeated subtraction (Euclid's original geometric method).

    Time Complexity: O(max(a, b)) in worst case (e.g., gcd(1, 10^9)).
    Space Complexity: O(1).

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Non-negative GCD integer.

    Raises:
        TypeError: If a or b is not an integer.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    a, b = abs(a), abs(b)
    if a == 0:
        return b
    if b == 0:
        return a

    while a != b:
        if a > b:
            a -= b
        else:
            b -= a

    return a


def gcd_euclidean_iterative(a: int, b: int) -> int:
    """
    Computes GCD(a, b) using the standard iterative division-based Euclidean algorithm.

    Based on the theorem: gcd(a, b) = gcd(b, a % b).
    By Lamé's Theorem, the number of division steps is at most 5 * (number of digits in min(a, b)).

    Time Complexity: O(log(min(|a|, |b|))) divisions.
    Space Complexity: O(1) auxiliary space.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Non-negative GCD integer.

    Raises:
        TypeError: If a or b is not an integer.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def gcd_euclidean_recursive(a: int, b: int) -> int:
    """
    Computes GCD(a, b) using recursive Euclidean formulation.

    Time Complexity: O(log(min(|a|, |b|))).
    Space Complexity: O(log(min(|a|, |b|))) call stack.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Non-negative GCD integer.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    a, b = abs(a), abs(b)
    if b == 0:
        return a
    return gcd_euclidean_recursive(b, a % b)


def gcd_with_metrics(a: int, b: int) -> Tuple[int, Dict[str, Any]]:
    """
    Calculates GCD(a, b) while tracking division steps, quotients, and execution duration.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple of (gcd_result, metrics_dict).
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    t0 = time.perf_counter()
    orig_a, orig_b = a, b
    curr_a, curr_b = abs(a), abs(b)
    steps = 0
    history: List[Tuple[int, int, int, int]] = []

    while curr_b != 0:
        quotient = curr_a // curr_b
        remainder = curr_a % curr_b
        history.append((curr_a, curr_b, quotient, remainder))
        curr_a, curr_b = curr_b, remainder
        steps += 1

    elapsed = time.perf_counter() - t0
    metrics = {
        "a": orig_a,
        "b": orig_b,
        "gcd": curr_a,
        "division_steps": steps,
        "step_history": history,
        "time_seconds": elapsed,
        "algorithm": "Iterative Euclidean Division O(log(min(a, b)))",
    }
    return (curr_a, metrics)
