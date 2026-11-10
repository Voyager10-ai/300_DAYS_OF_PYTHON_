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



# ─── 4. Step-by-Step Visualizer & Performance Benchmarking ────────────────────


def visualize_euclidean_steps(a: int, b: int) -> str:
    """
    Renders an ASCII step-by-step trace of Euclidean division steps for gcd(a, b).

    Displays dividend, divisor, quotient, remainder, and the exact invariant equation:
    dividend = divisor * quotient + remainder.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Formatted ASCII string diagram.
    """
    orig_a, orig_b = a, b
    curr_a, curr_b = abs(a), abs(b)

    lines: List[str] = []
    lines.append(f"Euclidean Algorithm Division Trace for GCD({orig_a}, {orig_b})")
    lines.append("=" * 76)
    header = f"{'Step':>4} | {'Dividend (a)':>14} | {'Divisor (b)':>14} | {'Quotient':>9} | {'Remainder':>10} | {'Equation':>12}"
    lines.append(header)
    lines.append("-" * 76)

    step = 1
    if curr_b == 0:
        lines.append(f"{step:>4} | {curr_a:>14} | {0:>14} | {'-':>9} | {0:>10} | gcd = {curr_a}")
        lines.append("=" * 76)
        return "\n".join(lines)

    while curr_b != 0:
        q = curr_a // curr_b
        r = curr_a % curr_b
        eq = f"{curr_a} = {curr_b}*{q} + {r}"
        lines.append(f"{step:>4} | {curr_a:>14} | {curr_b:>14} | {q:>9} | {r:>10} | {eq}")
        curr_a, curr_b = curr_b, r
        step += 1

    lines.append("=" * 76)
    lines.append(f"Final Result: GCD({orig_a}, {orig_b}) = {curr_a}")
    return "\n".join(lines)


def benchmark_gcd_algorithms(
    test_pairs: Optional[List[Tuple[int, int]]] = None,
    iterations: int = 1000,
) -> Dict[str, Any]:
    """
    Benchmarks and compares GCD algorithms across different number magnitudes and patterns.

    Algorithms:
      - Naive Brute Force (tested only on small inputs <= 20000)
      - Subtraction Euclidean (tested on small inputs)
      - Iterative Division Euclidean
      - Binary Stein's Algorithm
      - Builtin math.gcd (C implementation baseline)

    Args:
        test_pairs: List of (a, b) tuples to benchmark.
        iterations: Number of runs per algorithm per pair.

    Returns:
        Dictionary of benchmark records.
    """
    if test_pairs is None:
        test_pairs = [
            (48, 18),               # Small inputs
            (123456, 7890),         # Medium composite
            (4181, 2584),           # Worst case: consecutive Fibonacci (F_19, F_18)
            (75025, 46368),         # Consecutive Fibonacci (F_25, F_24)
            (1_000_000_007, 1_000_000_009),  # Large twin primes
        ]

    records: List[Dict[str, Any]] = []

    for a, b in test_pairs:
        row: Dict[str, Any] = {"a": a, "b": b, "label": f"({a}, {b})"}

        # 1. Naive Brute Force (only if min(a, b) <= 20,000)
        if min(abs(a), abs(b)) <= 20_000:
            times: List[float] = []
            for _ in range(min(iterations, 50)):
                t0 = time.perf_counter()
                gcd_naive(a, b)
                times.append(time.perf_counter() - t0)
            row["naive"] = min(times)
        else:
            row["naive"] = None

        # 2. Subtraction Euclidean (only if max(a, b) <= 100,000 to avoid hangs)
        if max(abs(a), abs(b)) <= 100_000 and abs(a - b) <= 50_000:
            times = []
            for _ in range(min(iterations, 100)):
                t0 = time.perf_counter()
                gcd_subtraction(a, b)
                times.append(time.perf_counter() - t0)
            row["subtraction"] = min(times)
        else:
            row["subtraction"] = None

        # 3. Iterative Division Euclidean
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            gcd_euclidean_iterative(a, b)
            times.append(time.perf_counter() - t0)
        row["euclidean"] = min(times)

        # 4. Binary Stein
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            gcd_binary_stein(a, b)
            times.append(time.perf_counter() - t0)
        row["stein"] = min(times)

        # 5. math.gcd builtin
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            math.gcd(a, b)
            times.append(time.perf_counter() - t0)
        row["math_gcd"] = min(times)

        records.append(row)

    return {"records": records, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """
    Formats the benchmark dictionary into an ASCII comparison table.

    Args:
        benchmark_data: Output from benchmark_gcd_algorithms.

    Returns:
        Formatted ASCII table string.
    """
    lines: List[str] = []
    lines.append("GCD Algorithms Performance Benchmark (Time per Operation)")
    lines.append("=" * 88)
    header = (
        f"{'Pair (a, b)':>26} | {'Naive':>10} | {'Subtraction':>12} | "
        f"{'Euclidean':>11} | {'Stein Binary':>13} | {'math.gcd':>10}"
    )
    lines.append(header)
    lines.append("-" * 88)

    def _fmt(val: Optional[float]) -> str:
        if val is None:
            return "N/A"
        ns = val * 1_000_000_000.0
        if ns < 1000.0:
            return f"{ns:.1f} ns"
        us = ns / 1000.0
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        pair_str = f"({r['a']}, {r['b']})"
        if len(pair_str) > 26:
            pair_str = pair_str[:23] + "..."
        line = (
            f"{pair_str:>26} | "
            f"{_fmt(r['naive']):>10} | "
            f"{_fmt(r['subtraction']):>12} | "
            f"{_fmt(r['euclidean']):>11} | "
            f"{_fmt(r['stein']):>13} | "
            f"{_fmt(r['math_gcd']):>10}"
        )
        lines.append(line)

    lines.append("=" * 88)
    return "\n".join(lines)



# ─── 5. Comprehensive Unit Test Suite ────────────────────────────────────────


class TestGreatestGCDImplementations(unittest.TestCase):
    """Exhaustive unit test suite verifying correctness, edge cases and properties."""

    def test_basic_gcd_consistency(self) -> None:
        """Verifies all GCD algorithms compute identical results on standard inputs."""
        test_pairs = [
            (48, 18, 6),
            (54, 24, 6),
            (101, 103, 1),
            (14, 28, 14),
            (252, 105, 21),
            (1071, 462, 21),
        ]
        for a, b, expected in test_pairs:
            self.assertEqual(gcd_naive(a, b), expected)
            self.assertEqual(gcd_subtraction(a, b), expected)
            self.assertEqual(gcd_euclidean_iterative(a, b), expected)
            self.assertEqual(gcd_euclidean_recursive(a, b), expected)
            self.assertEqual(gcd_binary_stein(a, b), expected)
            self.assertEqual(math.gcd(a, b), expected)

    def test_edge_cases_zeros_and_negatives(self) -> None:
        """Tests gcd with zero and negative numbers."""
        self.assertEqual(gcd_euclidean_iterative(0, 5), 5)
        self.assertEqual(gcd_euclidean_iterative(5, 0), 5)
        self.assertEqual(gcd_euclidean_iterative(0, 0), 0)
        self.assertEqual(gcd_binary_stein(0, 7), 7)
        self.assertEqual(gcd_binary_stein(7, 0), 7)
        self.assertEqual(gcd_binary_stein(0, 0), 0)
        self.assertEqual(gcd_euclidean_iterative(-12, 18), 6)
        self.assertEqual(gcd_euclidean_iterative(-12, -18), 6)
        self.assertEqual(gcd_binary_stein(-12, 18), 6)

    def test_extended_gcd_and_bezout(self) -> None:
        """Verifies Bézout identity a*x + b*y = gcd(a, b)."""
        pairs = [(35, 15), (120, 23), (12345, 678), (99, 78)]
        for a, b in pairs:
            g, x, y = extended_gcd(a, b)
            self.assertEqual(a * x + b * y, g)
            self.assertEqual(g, math.gcd(a, b))

    def test_modular_inverse(self) -> None:
        """Tests modular inverse calculation."""
        self.assertEqual(modular_inverse(3, 11), 4)     # (3 * 4) % 11 = 12 % 11 = 1
        self.assertEqual(modular_inverse(10, 17), 12)   # (10 * 12) % 17 = 120 % 17 = 1
        with self.assertRaises(ValueError):
            modular_inverse(6, 9)  # gcd(6, 9) = 3 != 1

    def test_diophantine_solver(self) -> None:
        """Tests linear Diophantine equation solver ax + by = c."""
        sol = solve_linear_diophantine(3, 5, 11)
        self.assertIsNotNone(sol)
        if sol is not None:
            x, y = sol
            self.assertEqual(3 * x + 5 * y, 11)

        no_sol = solve_linear_diophantine(4, 6, 9)  # gcd(4, 6) = 2 does not divide 9
        self.assertIsNone(no_sol)

    def test_multi_number_gcd_and_lcm(self) -> None:
        """Tests multi-number list GCD and LCM."""
        self.assertEqual(gcd_list([24, 36, 60]), 12)
        self.assertEqual(gcd_list([100, 25, 75]), 25)
        self.assertEqual(lcm(12, 18), 36)
        self.assertEqual(lcm_list([2, 3, 4, 5, 6]), 60)
        self.assertTrue(are_coprime(14, 15))
        self.assertFalse(are_coprime(14, 21))

    def test_array_greatest_gcd(self) -> None:
        """Tests LeetCode 1979 and array greatest pair GCD."""
        self.assertEqual(gcd_smallest_and_largest([2, 5, 6, 9, 10]), 2)
        max_g, a, b = find_greatest_gcd_pair([10, 15, 20, 25, 30])
        self.assertEqual(max_g, 15)

    def test_invalid_types_raise_type_error(self) -> None:
        """Ensures type errors are raised for invalid inputs."""
        for invalid in ["5", 3.14, None, [2], True]:
            with self.assertRaises(TypeError):
                gcd_euclidean_iterative(invalid, 10)  # type: ignore
            with self.assertRaises(TypeError):
                gcd_binary_stein(10, invalid)  # type: ignore


# ─── 6. Interactive CLI Demonstration ────────────────────────────────────────


def main() -> None:
    """Demonstrates GCD implementations, visualizer, and benchmarks."""
    print("=" * 80)
    print("              DAY 89: GREATEST GCD (ALGORITHMS & NUMBER THEORY)         ")
    print("=" * 80)

    # 1. Compare GCD algorithms
    a, b = 252, 105
    print(f"\n[1] Basic GCD Comparison for ({a}, {b}):")
    print(f"    - Naive Brute Force : {gcd_naive(a, b)}")
    print(f"    - Subtraction Euclid: {gcd_subtraction(a, b)}")
    print(f"    - Iterative Division: {gcd_euclidean_iterative(a, b)}")
    print(f"    - Recursive Division: {gcd_euclidean_recursive(a, b)}")
    print(f"    - Stein's Binary GCD: {gcd_binary_stein(a, b)}")
    print(f"    - Builtin math.gcd  : {math.gcd(a, b)}")

    # 2. Extended Euclidean and Bézout
    g, x, y = extended_gcd(a, b)
    print(f"\n[2] Extended Euclidean Algorithm (Bézout's Identity):")
    print(f"    {a} * ({x}) + {b} * ({y}) = {g}")

    # 3. Modular inverse and Diophantine
    base, mod = 3, 11
    inv = modular_inverse(base, mod)
    print(f"\n[3] Modular Multiplicative Inverse:")
    print(f"    ({base} * {inv}) mod {mod} = {(base * inv) % mod}")

    # 4. Multi-Number and LCM
    lst = [24, 36, 60]
    print(f"\n[4] Multi-Number GCD & LCM:")
    print(f"    gcd_list({lst}) = {gcd_list(lst)}")
    print(f"    lcm_list([2, 3, 4, 5, 6]) = {lcm_list([2, 3, 4, 5, 6])}")

    # 5. Array Greatest GCD Pair
    arr = [10, 15, 20, 25, 30]
    best_g, p1, p2 = find_greatest_gcd_pair(arr)
    print(f"\n[5] Array Greatest GCD Pair in {arr}:")
    print(f"    Max GCD = {best_g} between elements ({p1}, {p2})")

    # 6. Step-by-Step Visualizer
    print("\n[6] Euclidean Step-by-Step Division Trace:")
    print(visualize_euclidean_steps(252, 105))

    # 7. Benchmark
    print("\n[7] Multi-Algorithm Benchmark Comparison:")
    bench = benchmark_gcd_algorithms([(48, 18), (123456, 7890), (4181, 2584)], iterations=100)
    print(format_benchmark_table(bench))

    print("\n" + "=" * 80)
    print("                      DEMONSTRATION COMPLETE                                   ")
    print("=" * 80)


if __name__ == "__main__":
    main()
