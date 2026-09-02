# Day 56: Random Number
#
# Problem:
#   Write a Python program / module to generate random numbers.
#   Includes custom LCG engine, uniform integer/float generators, list & 2D matrix sampling,
#   Gaussian/Normal (Box-Muller) & Exponential probability distributions, statistical analysis & Chi-Square test,
#   Fisher-Yates shuffle & sampling, cryptographically secure generation, unit tests, and Java practice.

import math
import random
import secrets
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union, TypeVar

T = TypeVar("T")


# ─── 1. Custom Linear Congruential Generator (LCG) Engine ───────────────────────


class CustomLCG:
    """
    Implements a Linear Congruential Generator (LCG) pseudorandom number generator:
    X_{n+1} = (a * X_n + c) mod m

    Uses standard Numerical Recipes parameters:
    m = 2^32, a = 1664525, c = 1013904223
    """

    def __init__(self, seed: int = 123456789, m: int = 2**32, a: int = 1664525, c: int = 1013904223):
        if m <= 0:
            raise ValueError(f"Modulus m must be > 0, got {m}")
        self.m = m
        self.a = a
        self.c = c
        self.state = seed % m

    def next_int(self, min_val: int = 0, max_val: int = 100) -> int:
        """Generates a random integer in range [min_val, max_val]."""
        if min_val > max_val:
            raise ValueError(f"min_val ({min_val}) cannot be > max_val ({max_val})")
        self.state = (self.a * self.state + self.c) % self.m
        span = max_val - min_val + 1
        return min_val + (self.state % span)

    def next_float(self) -> float:
        """Generates a random float in range [0.0, 1.0)."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m


# ─── 2. Uniform Random Integer & Float Generators ─────────────────────────────


def generate_random_int(min_val: int, max_val: int, seed: Optional[int] = None) -> int:
    """
    Generates a uniform random integer in inclusive range [min_val, max_val].

    Args:
        min_val: Lower bound.
        max_val: Upper bound.
        seed: Optional random seed.

    Returns:
        Random integer.

    Raises:
        ValueError: If min_val > max_val.
    """
    if not isinstance(min_val, int) or not isinstance(max_val, int):
        raise TypeError("min_val and max_val must be integers")
    if min_val > max_val:
        raise ValueError(f"min_val ({min_val}) cannot be greater than max_val ({max_val})")

    if seed is not None:
        random.seed(seed)

    return random.randint(min_val, max_val)


def generate_random_float(
    min_val: float = 0.0,
    max_val: float = 1.0,
    precision: Optional[int] = 4,
    seed: Optional[int] = None,
) -> float:
    """
    Generates a uniform random float in range [min_val, max_val] with specified precision.

    Args:
        min_val: Lower bound.
        max_val: Upper bound.
        precision: Rounding decimal places (optional).
        seed: Optional random seed.

    Returns:
        Random float.
    """
    if min_val > max_val:
        raise ValueError(f"min_val ({min_val}) cannot be greater than max_val ({max_val})")

    if seed is not None:
        random.seed(seed)

    val = min_val + (random.random() * (max_val - min_val))
    if precision is not None:
        return round(val, precision)
    return val


# ─── 3. Random Sequence & Matrix Sampler ───────────────────────────────────────


def generate_random_list(
    count: int,
    min_val: int,
    max_val: int,
    unique: bool = False,
    seed: Optional[int] = None,
) -> List[int]:
    """
    Generates a list of random integers.

    Args:
        count: Number of integers to generate.
        min_val: Minimum value.
        max_val: Maximum value.
        unique: If True, all elements must be unique.
        seed: Optional random seed.

    Returns:
        List of random integers.

    Raises:
        ValueError: If unique=True and count exceeds range size (max_val - min_val + 1).
    """
    if count < 0:
        raise ValueError(f"Count must be >= 0, got {count}")
    if min_val > max_val:
        raise ValueError(f"min_val ({min_val}) cannot be > max_val ({max_val})")

    if seed is not None:
        random.seed(seed)

    if unique:
        range_size = max_val - min_val + 1
        if count > range_size:
            raise ValueError(f"Cannot generate {count} unique numbers in range size {range_size}")
        return random.sample(range(min_val, max_val + 1), count)

    return [random.randint(min_val, max_val) for _ in range(count)]


def generate_random_matrix(
    rows: int,
    cols: int,
    min_val: int,
    max_val: int,
    seed: Optional[int] = None,
) -> List[List[int]]:
    """
    Generates a 2D matrix (list of lists) filled with random integers.

    Args:
        rows: Number of rows (rows >= 1).
        cols: Number of columns (cols >= 1).
        min_val: Minimum integer value.
        max_val: Maximum integer value.
        seed: Optional random seed.

    Returns:
        2D matrix of shape (rows, cols).
    """
    if rows < 1 or cols < 1:
        raise ValueError(f"Rows and cols must be >= 1, got rows={rows}, cols={cols}")

    if seed is not None:
        random.seed(seed)

    return [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]


# ─── 4. Non-Uniform Probability Distribution Generators ────────────────────────


def generate_normal_random(
    mean: float = 0.0,
    std_dev: float = 1.0,
    seed: Optional[int] = None,
) -> float:
    """
    Generates a Gaussian/Normal random variate N(mean, std_dev^2) using Box-Muller transform:
    Z0 = sqrt(-2 * ln(U1)) * cos(2 * pi * U2)

    Args:
        mean: Distribution mean (mu).
        std_dev: Standard deviation (sigma > 0).
        seed: Optional random seed.

    Returns:
        Gaussian random float value.

    Raises:
        ValueError: If std_dev <= 0.
    """
    if std_dev <= 0:
        raise ValueError(f"Standard deviation must be > 0, got {std_dev}")

    if seed is not None:
        random.seed(seed)

    u1 = random.random()
    u2 = random.random()

    # Prevent log(0)
    while u1 == 0.0:
        u1 = random.random()

    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return mean + (z0 * std_dev)


def generate_exponential_random(
    scale: float = 1.0,
    seed: Optional[int] = None,
) -> float:
    """
    Generates an Exponential random variate Exp(1/scale) using Inverse Transform Sampling:
    X = -scale * ln(1 - U)

    Args:
        scale: Scale parameter (beta = 1/lambda > 0).
        seed: Optional random seed.

    Returns:
        Exponential random float value.
    """
    if scale <= 0:
        raise ValueError(f"Scale parameter must be > 0, got {scale}")

    if seed is not None:
        random.seed(seed)

    u = random.random()
    while u >= 1.0 or u == 0.0:
        u = random.random()

    return -scale * math.log(1.0 - u)



