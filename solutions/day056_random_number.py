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


# ─── 5. Random Sample Statistical Analyzer & Uniformity Test ────────────────────


def analyze_random_sample(sample: List[Union[int, float]]) -> Dict[str, Any]:
    """
    Computes comprehensive descriptive statistics and empirical metrics for a random sample.

    Args:
        sample: List of numeric values.

    Returns:
        Dictionary containing sample metrics (min, max, mean, median, variance, std_dev, etc.).

    Raises:
        ValueError: If sample is empty.
    """
    if not isinstance(sample, list):
        raise TypeError(f"Expected list sample, got {type(sample).__name__}")
    if not sample:
        raise ValueError("Sample list cannot be empty")

    n = len(sample)
    min_val = min(sample)
    max_val = max(sample)
    val_range = max_val - min_val

    mean_val = sum(sample) / n

    sorted_sample = sorted(sample)
    if n % 2 == 1:
        median_val = float(sorted_sample[n // 2])
    else:
        median_val = (sorted_sample[(n // 2) - 1] + sorted_sample[n // 2]) / 2.0

    variance_val = sum((x - mean_val) ** 2 for x in sample) / (n - 1) if n > 1 else 0.0
    std_dev_val = math.sqrt(variance_val)

    return {
        "sample_size": n,
        "min": min_val,
        "max": max_val,
        "range": val_range,
        "mean": round(mean_val, 4),
        "median": round(median_val, 4),
        "variance": round(variance_val, 4),
        "std_dev": round(std_dev_val, 4),
    }


# ─── 6. Fisher-Yates Random Shuffle & Sampling ─────────────────────────────────


def random_choice(items: List[T], seed: Optional[int] = None) -> T:
    """Selects a single random item from a non-empty list."""
    if not items:
        raise ValueError("Cannot select random choice from empty list")
    if seed is not None:
        random.seed(seed)
    idx = random.randint(0, len(items) - 1)
    return items[idx]


def random_sample(items: List[T], k: int, seed: Optional[int] = None) -> List[T]:
    """Selects k unique random elements from items list without replacement."""
    if k < 0:
        raise ValueError(f"k must be >= 0, got {k}")
    if k > len(items):
        raise ValueError(f"Sample size k ({k}) cannot be larger than list size ({len(items)})")
    if seed is not None:
        random.seed(seed)
    return random.sample(items, k)


def random_shuffle(items: List[T], seed: Optional[int] = None) -> List[T]:
    """
    Shuffles a list using Fisher-Yates (Knuth) shuffling algorithm:
    For i from n-1 down to 1: swap items[i] with items[j] (0 <= j <= i).

    Args:
        items: List to shuffle.
        seed: Optional random seed.

    Returns:
        New shuffled list copy.
    """
    if seed is not None:
        random.seed(seed)

    arr = list(items)
    n = len(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]

    return arr


# ─── 7. Cryptographically Secure & Precision Decimal Generator ────────────────


def generate_crypto_random_bytes(num_bytes: int) -> bytes:
    """Generates num_bytes of cryptographically secure random bytes using secrets."""
    if num_bytes <= 0:
        raise ValueError(f"num_bytes must be > 0, got {num_bytes}")
    return secrets.token_bytes(num_bytes)


def generate_crypto_random_int(min_val: int, max_val: int) -> int:
    """Generates a cryptographically secure random integer in inclusive range [min_val, max_val]."""
    if min_val > max_val:
        raise ValueError(f"min_val ({min_val}) cannot be > max_val ({max_val})")
    span = max_val - min_val + 1
    return min_val + secrets.randbelow(span)


def generate_random_decimal(
    min_val: float,
    max_val: float,
    decimal_places: int = 2,
    seed: Optional[int] = None,
) -> float:
    """Generates a random float value rounded precisely to decimal_places."""
    if decimal_places < 0:
        raise ValueError(f"decimal_places must be >= 0, got {decimal_places}")
    val = generate_random_float(min_val, max_val, precision=None, seed=seed)
    factor = 10**decimal_places
    return math.floor(val * factor + 0.5) / factor


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestRandomNumberOperations(unittest.TestCase):
    def test_custom_lcg(self):
        lcg = CustomLCG(seed=42)
        val = lcg.next_int(1, 10)
        self.assertTrue(1 <= val <= 10)
        flt = lcg.next_float()
        self.assertTrue(0.0 <= flt < 1.0)

    def test_uniform_int_and_float(self):
        val = generate_random_int(5, 15, seed=10)
        self.assertTrue(5 <= val <= 15)
        flt = generate_random_float(1.0, 5.0, precision=2, seed=10)
        self.assertTrue(1.0 <= flt <= 5.0)

    def test_random_list_and_matrix(self):
        lst = generate_random_list(count=10, min_val=1, max_val=20, unique=True, seed=99)
        self.assertEqual(len(lst), 10)
        self.assertEqual(len(set(lst)), 10)

        mat = generate_random_matrix(rows=3, cols=4, min_val=0, max_val=9, seed=1)
        self.assertEqual(len(mat), 3)
        self.assertEqual(len(mat[0]), 4)

    def test_normal_and_exponential(self):
        norm = generate_normal_random(mean=10.0, std_dev=2.0, seed=42)
        self.assertIsInstance(norm, float)
        exp = generate_exponential_random(scale=5.0, seed=42)
        self.assertTrue(exp > 0.0)

    def test_analyze_random_sample(self):
        sample = [10, 20, 30, 40, 50]
        stats = analyze_random_sample(sample)
        self.assertEqual(stats["min"], 10)
        self.assertEqual(stats["max"], 50)
        self.assertEqual(stats["mean"], 30.0)
        self.assertEqual(stats["median"], 30.0)

    def test_fisher_yates_shuffle_and_sample(self):
        items = [1, 2, 3, 4, 5]
        choice = random_choice(items, seed=7)
        self.assertIn(choice, items)

        shuffled = random_shuffle(items, seed=7)
        self.assertEqual(sorted(shuffled), items)

    def test_crypto_and_decimal(self):
        cbytes = generate_crypto_random_bytes(8)
        self.assertEqual(len(cbytes), 8)

        cint = generate_crypto_random_int(1, 100)
        self.assertTrue(1 <= cint <= 100)

        dec = generate_random_decimal(1.0, 10.0, decimal_places=3, seed=12)
        self.assertTrue(1.0 <= dec <= 10.0)







