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


# ─── 3. Iterative Bitwise Fast Exponentiation & LeetCode 50 Solution ──────────


def power_binary_iterative(
    a: Union[int, float],
    b: int,
) -> Union[int, float]:
    """
    Computes a^b using iterative bitwise binary exponentiation.

    Inspects each bit of b from least significant to most significant:
      - If bit is 1 (exp & 1): multiply accumulator by current base.
      - Square base for next bit position: base *= base.
      - Shift exponent right: exp >>= 1.

    Time Complexity: O(log |b|) multiplications.
    Space Complexity: O(1) auxiliary space (no recursion stack).

    Args:
        a: Base number (int or float).
        b: Exponent integer.

    Returns:
        Result of a^b.

    Raises:
        TypeError: If invalid types provided.
        ZeroDivisionError: If a == 0 and b < 0.
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

    if b == 0:
        return 1

    exp = abs(b)
    curr_base = a
    result = 1

    while exp > 0:
        if exp & 1:
            result *= curr_base
        curr_base *= curr_base
        exp >>= 1

    return (1.0 / result) if b < 0 else result


def power_binary_iterative_with_metrics(
    a: Union[int, float],
    b: int,
) -> Tuple[Union[int, float], Dict[str, Any]]:
    """
    Computes a^b via bitwise iterative exponentiation while tracking operations.

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

    t0 = time.perf_counter()
    multiplications = 0
    bit_shifts = 0

    if a == 0:
        ans = 1 if b == 0 else 0
    elif b == 0:
        ans = 1
    else:
        exp = abs(b)
        curr_base = a
        result = 1

        while exp > 0:
            if exp & 1:
                result *= curr_base
                multiplications += 1
            if exp > 1:
                curr_base *= curr_base
                multiplications += 1
            exp >>= 1
            bit_shifts += 1

        ans = (1.0 / result) if b < 0 else result

    elapsed = time.perf_counter() - t0
    metrics = {
        "base": a,
        "exponent": b,
        "result": ans,
        "multiplications": multiplications,
        "bit_shifts": bit_shifts,
        "time_seconds": elapsed,
        "algorithm": "Iterative Bitwise Binary Exponentiation (O(log |b|))",
    }
    return (ans, metrics)


class Solution:
    """
    LeetCode 50: Pow(x, n) solution class wrapper.
    https://leetcode.com/problems/powx-n/
    """

    def myPow(self, x: float, n: int) -> float:
        """
        Calculates x raised to the power n (x^n).

        Args:
            x: Base float.
            n: Exponent integer.

        Returns:
            Computed float value of x^n.
        """
        return float(power_binary_iterative(x, n))


# ─── 4. Modular Exponentiation (A^B mod M) & Modular Inverse ─────────────────


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Computes Extended Euclidean Algorithm.
    Returns tuple (gcd, x, y) such that a*x + b*y = gcd(a, b).
    """
    if b == 0:
        return (a, 1, 0)
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (gcd_val, x, y)


def modular_inverse(a: int, m: int) -> int:
    """
    Computes modular multiplicative inverse of a modulo m using extended GCD.
    Solves for x in: (a * x) % m == 1.

    Args:
        a: Integer.
        m: Modulus.

    Returns:
        Inverse x in range [0, m - 1].

    Raises:
        ValueError: If gcd(a, m) != 1 (inverse does not exist).
    """
    gcd_val, x, _ = extended_gcd(a % m, m)
    if gcd_val != 1:
        raise ValueError(f"Modular inverse does not exist: gcd({a}, {m}) = {gcd_val} != 1")
    return (x % m + m) % m


def modular_power(
    base: int,
    exp: int,
    mod: int,
) -> int:
    """
    Computes (base^exp) % mod using binary exponentiation with modulo reduction.

    Prevents numeric overflow by bounding all intermediate products to [0, mod - 1].
    Fundamental in modern cryptography (RSA public-key encryption, Diffie-Hellman key exchange).

    Time Complexity: O(log |exp|) multiplications modulo mod.
    Space Complexity: O(1) auxiliary space.

    Args:
        base: Base integer.
        exp: Exponent integer (can be negative if gcd(base, mod) == 1).
        mod: Modulus integer (must be >= 1).

    Returns:
        Integer result in range [0, mod - 1].

    Raises:
        ValueError: If mod <= 0.
        TypeError: If arguments are not integers.
    """
    if not isinstance(base, int) or isinstance(base, bool):
        raise TypeError(f"base must be an integer, got {type(base).__name__}")
    if not isinstance(exp, int) or isinstance(exp, bool):
        raise TypeError(f"exp must be an integer, got {type(exp).__name__}")
    if not isinstance(mod, int) or isinstance(mod, bool):
        raise TypeError(f"mod must be an integer, got {type(mod).__name__}")

    if mod <= 0:
        raise ValueError(f"Modulus must be a positive integer, got {mod}")

    if mod == 1:
        return 0

    # Handle negative exponent via modular inverse
    if exp < 0:
        base = modular_inverse(base, mod)
        exp = -exp

    result = 1
    curr_base = base % mod

    while exp > 0:
        if exp & 1:
            result = (result * curr_base) % mod
        curr_base = (curr_base * curr_base) % mod
        exp >>= 1

    return result


def modular_power_with_metrics(
    base: int,
    exp: int,
    mod: int,
) -> Tuple[int, Dict[str, Any]]:
    """
    Computes modular power while tracking modular multiplications and runtime.
    """
    t0 = time.perf_counter()
    ans = modular_power(base, exp, mod)
    elapsed = time.perf_counter() - t0

    metrics = {
        "base": base,
        "exponent": exp,
        "modulus": mod,
        "result": ans,
        "time_seconds": elapsed,
        "algorithm": "Modular Binary Exponentiation (O(log |exp|))",
    }
    return (ans, metrics)


# ─── 5. Fractional & Real Exponentiation Engine (a^b = exp(b * ln(a))) ────────


LN2: float = 0.693147180559945309417232121458


def natural_log(x: float, max_terms: int = 50) -> float:
    """
    Computes natural logarithm ln(x) using argument reduction and artanh series.

    Decomposes x = m * 2^k where m in [1, 2).
    Then ln(x) = ln(m) + k * ln(2).
    For m, uses:
      z = (m - 1) / (m + 1)
      ln(m) = 2 * sum_{i=0}^N (z^(2i + 1) / (2i + 1))

    Args:
        x: Real positive float.
        max_terms: Truncation threshold for series.

    Returns:
        Natural logarithm ln(x).

    Raises:
        ValueError: If x <= 0 (outside real logarithm domain).
    """
    if x <= 0.0:
        raise ValueError(f"Domain error: ln(x) is only defined for x > 0, got {x}")

    if x == 1.0:
        return 0.0

    # Range reduction: decompose x = m * 2^k with m in [1.0, 2.0)
    k = 0
    m = float(x)
    while m >= 2.0:
        m /= 2.0
        k += 1
    while m < 1.0:
        m *= 2.0
        k -= 1

    # Artanh series for m in [1, 2)
    z = (m - 1.0) / (m + 1.0)
    z_sq = z * z
    curr_pow = z
    total = 0.0

    for i in range(max_terms):
        term = curr_pow / (2 * i + 1)
        total += term
        if abs(term) < 1e-16:
            break
        curr_pow *= z_sq

    return 2.0 * total + (k * LN2)


def exponential_series(x: float, max_terms: int = 60) -> float:
    """
    Computes e^x using range reduction and Maclaurin Taylor expansion.

    Decomposes x = k * ln(2) + r where |r| <= ln(2) / 2.
    Then e^x = 2^k * e^r, with e^r = sum_{n=0}^inf (r^n / n!).

    Args:
        x: Real exponent.
        max_terms: Number of Taylor polynomial terms.

    Returns:
        e^x float approximation.
    """
    if x == 0.0:
        return 1.0

    # Range reduction: x = k * ln(2) + r
    k = round(x / LN2)
    r = x - (k * LN2)

    # Maclaurin series for e^r
    term = 1.0
    total = 1.0
    for n in range(1, max_terms):
        term *= r / n
        total += term
        if abs(term) < 1e-16:
            break

    # Scale by 2^k
    return total * (2.0 ** k)


def power_fractional(
    a: Union[int, float],
    b: Union[int, float],
) -> float:
    """
    Computes a^b for arbitrary real numbers a and b using analytical identity:
      a^b = exp(b * ln(a))

    Falls back to exact integer binary exponentiation when b is an integer.

    Args:
        a: Base (int or float).
        b: Exponent (int or float).

    Returns:
        Float value of a^b.

    Raises:
        ZeroDivisionError: If a == 0 and b < 0.
        ValueError: If a < 0 and b is non-integer (complex result).
    """
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        raise TypeError(f"Base a must be int or float, got {type(a).__name__}")
    if not isinstance(b, (int, float)) or isinstance(b, bool):
        raise TypeError(f"Exponent b must be int or float, got {type(b).__name__}")

    # Check for integer exponent shortcut for exact precision
    if isinstance(b, int) or (isinstance(b, float) and b.is_integer()):
        int_exp = int(b)
        return float(power_binary_iterative(a, int_exp))

    if a == 0.0:
        if b < 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        return 0.0

    if a < 0.0:
        raise ValueError(
            f"Negative base {a} raised to non-integer power {b} results in a complex number."
        )

    # a^b = exp(b * ln(a))
    ln_a = natural_log(float(a))
    return exponential_series(float(b) * ln_a)


# ─── 6. 2x2 Matrix Binary Exponentiation & O(log N) Fibonacci ─────────────────


Matrix2x2 = List[List[int]]


def matrix_2x2_mult(
    A: Matrix2x2,
    B: Matrix2x2,
    mod: Optional[int] = None,
) -> Matrix2x2:
    """
    Multiplies two 2x2 integer matrices with optional modulo arithmetic.
    """
    m00 = A[0][0] * B[0][0] + A[0][1] * B[1][0]
    m01 = A[0][0] * B[0][1] + A[0][1] * B[1][1]
    m10 = A[1][0] * B[0][0] + A[1][1] * B[1][0]
    m11 = A[1][0] * B[0][1] + A[1][1] * B[1][1]

    if mod is not None:
        return [
            [m00 % mod, m01 % mod],
            [m10 % mod, m11 % mod],
        ]
    return [
        [m00, m01],
        [m10, m11],
    ]


def matrix_2x2_power(
    M: Matrix2x2,
    n: int,
    mod: Optional[int] = None,
) -> Matrix2x2:
    """
    Computes M^n for a 2x2 matrix using binary exponentiation by squaring.

    Time Complexity: O(log n) matrix multiplications.
    Space Complexity: O(1) auxiliary space.

    Args:
        M: 2x2 matrix as list of two 2-element lists.
        n: Exponent non-negative integer.
        mod: Optional integer modulus.

    Returns:
        2x2 matrix result.

    Raises:
        ValueError: If n < 0.
    """
    if n < 0:
        raise ValueError("Matrix power currently only supports non-negative exponents")

    # 2x2 Identity matrix
    result: Matrix2x2 = [[1, 0], [0, 1]]
    curr: Matrix2x2 = [[M[0][0], M[0][1]], [M[1][0], M[1][1]]]

    if mod is not None:
        curr[0][0] %= mod
        curr[0][1] %= mod
        curr[1][0] %= mod
        curr[1][1] %= mod

    exp = n
    while exp > 0:
        if exp & 1:
            result = matrix_2x2_mult(result, curr, mod)
        curr = matrix_2x2_mult(curr, curr, mod)
        exp >>= 1

    return result


def fibonacci_matrix_power(
    n: int,
    mod: Optional[int] = None,
) -> int:
    """
    Computes the n-th Fibonacci number F(n) in O(log n) time using matrix binary exponentiation.
    F(0) = 0, F(1) = 1, F(2) = 1, F(3) = 2, F(4) = 3, F(5) = 5, ...

    Uses the matrix transformation:
      [[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]

    Args:
        n: 0-indexed Fibonacci index (n >= 0).
        mod: Optional modulus for large n.

    Returns:
        F(n) integer value.

    Raises:
        ValueError: If n < 0.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative")

    if n == 0:
        return 0
    if n == 1:
        return 1 if mod is None else (1 % mod)

    T: Matrix2x2 = [[1, 1], [1, 0]]
    powered = matrix_2x2_power(T, n - 1, mod)
    ans = powered[0][0]

    return ans if mod is None else (ans % mod)


# ─── 7. Step-by-Step Bitwise Exponentiation Trace Visualizer ──────────────────


def trace_binary_exponentiation(
    a: Union[int, float],
    b: int,
) -> List[Dict[str, Any]]:
    """
    Simulates bitwise binary exponentiation while recording state transitions at each bit.

    Args:
        a: Base.
        b: Exponent.

    Returns:
        List of trace dictionaries describing bit inspection, multiplication, and squaring.
    """
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"Exponent must be an int, got {type(b).__name__}")
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        raise TypeError(f"Base must be an int or float, got {type(a).__name__}")

    steps = []
    exp = abs(b)
    curr_base = a
    result = 1
    step_num = 1

    if exp == 0:
        steps.append({
            "step": 1,
            "exponent_remaining": 0,
            "binary_remaining": "0b0",
            "active_bit": 0,
            "current_base": curr_base,
            "action": "Exponent is 0 -> Result is 1 immediately",
            "accumulator": 1,
            "next_base": curr_base,
        })
        return steps

    while exp > 0:
        active_bit = exp & 1
        prev_result = result
        prev_base = curr_base

        if active_bit == 1:
            result *= curr_base
            action_desc = f"Bit is 1: acc = {prev_result} * {curr_base} = {result}"
        else:
            action_desc = f"Bit is 0: skip acc multiply (remains {result})"

        next_base = curr_base * curr_base
        steps.append({
            "step": step_num,
            "exponent_remaining": exp,
            "binary_remaining": bin(exp),
            "active_bit": active_bit,
            "current_base": prev_base,
            "action": action_desc,
            "accumulator": result,
            "next_base": next_base,
        })

        curr_base = next_base
        exp >>= 1
        step_num += 1

    return steps


def render_exponentiation_trace(
    trace: List[Dict[str, Any]],
    a: Union[int, float],
    b: int,
) -> str:
    """
    Renders the recorded exponentiation trace as a formatted ASCII diagram.

    Args:
        trace: List of trace steps from trace_binary_exponentiation.
        a: Initial base.
        b: Initial exponent.

    Returns:
        Multi-line formatted ASCII table.
    """
    lines = []
    lines.append("=" * 78)
    lines.append("         BINARY EXPONENTIATION (FAST POW) STEP-BY-STEP TRACE          ")
    lines.append("=" * 78)
    lines.append(f"Problem  : {a}^{b}")
    lines.append(f"Exponent : {b} (Binary: {bin(abs(b))}, Bits: {abs(b).bit_length()})")
    lines.append("-" * 78)
    header = f"{'Step':<5} | {'Bit':<4} | {'Exp (bin)':<10} | {'Base Value':<12} | {'Accumulator':<14} | {'Action'}"
    lines.append(header)
    lines.append("-" * 78)

    for step in trace:
        step_str = f"{step['step']:<5} | {step['active_bit']:<4} | {step['binary_remaining']:<10} | "
        base_val = f"{step['current_base']:.4g}" if isinstance(step['current_base'], float) else str(step['current_base'])
        acc_val = f"{step['accumulator']:.4g}" if isinstance(step['accumulator'], float) else str(step['accumulator'])
        step_str += f"{base_val:<12} | {acc_val:<14} | {step['action']}"
        lines.append(step_str)

    lines.append("-" * 78)
    final_res = trace[-1]["accumulator"] if trace else 1
    if b < 0:
        final_res = 1.0 / final_res
        lines.append(f"Negative Exponent Inversion: 1.0 / {trace[-1]['accumulator']} = {final_res}")

    mult_done = sum(1 for s in trace if s["active_bit"] == 1) + (len(trace) - 1)
    naive_mult = abs(b)
    saved = max(0, naive_mult - mult_done)
    lines.append(f"Final Answer : {final_res}")
    lines.append(f"Multiplications : {mult_done} vs Naive {naive_mult} (Saved: {saved} ops, ~{round(saved/max(1, naive_mult)*100, 1)}% reduction)")
    lines.append("=" * 78)
    return "\n".join(lines)
