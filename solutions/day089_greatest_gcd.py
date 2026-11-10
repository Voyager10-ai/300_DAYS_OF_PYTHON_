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



# ─── 2. Stein's Binary GCD, Extended Euclidean & Modular Inverse ──────────────


def gcd_binary_stein(a: int, b: int) -> int:
    """
    Computes GCD(a, b) using Stein's Binary GCD algorithm.

    Replaces division/modulo with bitwise right shifts and subtractions.
    Particularly fast for hardware without hardware division or in BigInt systems.

    Rules:
      1. gcd(0, b) = b, gcd(a, 0) = a
      2. If both a, b even: gcd(a, b) = 2 * gcd(a/2, b/2)
      3. If a even, b odd:  gcd(a, b) = gcd(a/2, b)
      4. If both odd:       gcd(a, b) = gcd(|a - b| / 2, min(a, b))

    Time Complexity: O((log(a) + log(b))^2) bit operations, O(log(max(a, b))) shifts.
    Space Complexity: O(1) auxiliary space.

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
    if a == 0:
        return b
    if b == 0:
        return a

    # Find common power of 2 factor
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1

    # Remove remaining factors of 2 from a
    while (a & 1) == 0:
        a >>= 1

    # From here on, a is always odd
    while b != 0:
        # Remove factors of 2 from b
        while (b & 1) == 0:
            b >>= 1

        # Now both a and b are odd. Ensure a <= b then subtract
        if a > b:
            a, b = b, a
        b -= a

    return a << shift


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Computes the GCD of a and b along with Bézout coefficients (x, y) such that:
        a * x + b * y = gcd(a, b)

    Time Complexity: O(log(min(|a|, |b|))).
    Space Complexity: O(1) iterative space.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple of (g, x, y) where g = gcd(a, b), and a*x + b*y = g.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    x0, x1 = 1, 0
    y0, y1 = 0, 1
    orig_a, orig_b = a, b

    sign_a = -1 if a < 0 else 1
    sign_b = -1 if b < 0 else 1
    a, b = abs(a), abs(b)

    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return (a, x0 * sign_a, y0 * sign_b)


def modular_inverse(a: int, m: int) -> int:
    """
    Calculates the modular multiplicative inverse of a modulo m:
        (a * x) % m == 1

    The inverse exists if and only if gcd(a, m) == 1 (a and m are coprime).

    Args:
        a: Integer base.
        m: Modulus (m >= 2).

    Returns:
        Modular inverse x in the range [0, m - 1].

    Raises:
        ValueError: If gcd(a, m) != 1 or m < 2.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(m, int) or isinstance(m, bool):
        raise TypeError(f"m must be an integer, got {type(m).__name__}")
    if m < 2:
        raise ValueError(f"Modulus m must be >= 2, got {m}")

    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist: gcd({a}, {m}) = {g} != 1")

    return (x % m + m) % m


def solve_linear_diophantine(
    a: int,
    b: int,
    c: int,
) -> Optional[Tuple[int, int]]:
    """
    Finds a particular integer solution (x, y) to the linear Diophantine equation:
        a * x + b * y = c

    A solution exists if and only if gcd(a, b) divides c.

    Args:
        a: Coefficient of x.
        b: Coefficient of y.
        c: Target constant.

    Returns:
        Tuple (x0, y0) if integer solution exists; None otherwise.
    """
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int):
        raise TypeError("a, b, and c must be integers")

    if a == 0 and b == 0:
        return (0, 0) if c == 0 else None

    g, x0, y0 = extended_gcd(a, b)
    if c % g != 0:
        return None

    factor = c // g
    return (x0 * factor, y0 * factor)



# ─── 3. Multi-Number GCD, LCM & Array Greatest GCD Pair ───────────────────────


def gcd_list(numbers: List[int]) -> int:
    """
    Computes the GCD across an entire list or sequence of integers.

    Property: gcd(a, b, c) = gcd(gcd(a, b), c).

    Args:
        numbers: Non-empty list of integers.

    Returns:
        Greatest common divisor of all elements.

    Raises:
        ValueError: If numbers list is empty.
        TypeError: If elements are not integers.
    """
    if not isinstance(numbers, list):
        raise TypeError(f"numbers must be a list, got {type(numbers).__name__}")
    if not numbers:
        raise ValueError("Cannot compute GCD of an empty list")

    res = abs(numbers[0])
    for num in numbers[1:]:
        if not isinstance(num, int) or isinstance(num, bool):
            raise TypeError(f"List elements must be integers, got {type(num).__name__}")
        res = gcd_euclidean_iterative(res, num)
        if res == 1:
            break

    return res


def lcm(a: int, b: int) -> int:
    """
    Computes the Least Common Multiple (LCM) of two integers.

    Formula:
        lcm(a, b) = (|a * b|) // gcd(a, b)

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Non-negative LCM integer.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an integer, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an integer, got {type(b).__name__}")

    if a == 0 or b == 0:
        return 0

    g = gcd_euclidean_iterative(a, b)
    return abs(a * b) // g


def lcm_list(numbers: List[int]) -> int:
    """
    Computes the LCM of a list of integers.

    Args:
        numbers: Non-empty list of integers.

    Returns:
        Least common multiple integer.
    """
    if not isinstance(numbers, list):
        raise TypeError(f"numbers must be a list, got {type(numbers).__name__}")
    if not numbers:
        raise ValueError("Cannot compute LCM of an empty list")

    res = abs(numbers[0])
    for num in numbers[1:]:
        if not isinstance(num, int) or isinstance(num, bool):
            raise TypeError(f"List elements must be integers, got {type(num).__name__}")
        res = lcm(res, num)
    return res


def are_coprime(a: int, b: int) -> bool:
    """Returns True if a and b are mutually prime (gcd(a, b) == 1)."""
    return gcd_euclidean_iterative(a, b) == 1


def gcd_smallest_and_largest(arr: List[int]) -> int:
    """
    LeetCode 1979: Find Greatest Common Divisor of Array.
    Given an integer array nums, return the greatest common divisor of the smallest
    number and largest number in nums.

    Args:
        arr: Non-empty list of positive integers.

    Returns:
        GCD of min(arr) and max(arr).
    """
    if not arr:
        raise ValueError("arr must not be empty")
    return gcd_euclidean_iterative(min(arr), max(arr))


def find_greatest_gcd_pair(arr: List[int]) -> Tuple[int, int, int]:
    """
    Finds two distinct elements in arr that achieve the maximum GCD.

    For moderate array sizes, computes max GCD via frequency bucket sieve.
    For small arrays, evaluates pairwise GCDs.

    Args:
        arr: List of positive integers with length >= 2.

    Returns:
        Tuple of (max_gcd, elem1, elem2).

    Raises:
        ValueError: If len(arr) < 2.
    """
    if len(arr) < 2:
        raise ValueError("Array must contain at least two elements")

    # If maximum element is reasonably bounded, use divisor sieve O(max_val * log(max_val))
    max_val = max(arr)
    if max_val <= 100_000:
        freq = [0] * (max_val + 1)
        for x in arr:
            if x > 0:
                freq[x] += 1

        for g in range(max_val, 0, -1):
            count = 0
            matching: List[int] = []
            for multiple in range(g, max_val + 1, g):
                if freq[multiple] > 0:
                    count += freq[multiple]
                    matching.extend([multiple] * freq[multiple])
                if count >= 2:
                    return (g, matching[0], matching[1])

    # Fallback to all-pairs comparison
    best_gcd = 1
    best_pair = (arr[0], arr[1])
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            g = gcd_euclidean_iterative(arr[i], arr[j])
            if g > best_gcd:
                best_gcd = g
                best_pair = (arr[i], arr[j])

    return (best_gcd, best_pair[0], best_pair[1])
