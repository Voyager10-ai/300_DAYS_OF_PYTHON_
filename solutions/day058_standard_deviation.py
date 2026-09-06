# Day 58: Standard Deviation
#
# Problem:
#   Write a Python program / module to calculate standard deviation and variance for datasets.
#   Includes population and sample formulas, Welford's single-pass online algorithm,
#   grouped data frequency tables, Z-score normalization & outlier detection,
#   Standard Error of the Mean (SEM) & confidence intervals, axis-wise matrix operations,
#   synthetic dataset generation, unit tests, and Java practice.

import math
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Variance & Standard Deviation Functions ─────────────────────────


def calculate_mean(data: List[float]) -> float:
    """
    Calculates the arithmetic mean of a list of numbers.

    Args:
        data: List of numerical values.

    Returns:
        Arithmetic mean as a float.

    Raises:
        ValueError: If dataset is empty.
        TypeError: If dataset contains non-numeric elements.
    """
    if not data:
        raise ValueError("Cannot calculate mean of an empty dataset.")
    
    total = 0.0
    for val in data:
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError(f"Invalid element type {type(val).__name__} in dataset.")
        total += float(val)
    
    return total / len(data)


def calculate_variance(data: List[float], is_sample: bool = True) -> float:
    """
    Calculates the variance of a list of numbers.

    Args:
        data: List of numerical values.
        is_sample: If True, calculates sample variance (n - 1 degrees of freedom).
                   If False, calculates population variance (n degrees of freedom).

    Returns:
        Variance value as a float.

    Raises:
        ValueError: If data has fewer than 2 elements for sample, or is empty for population.
    """
    if not data:
        raise ValueError("Cannot calculate variance of an empty dataset.")
    
    n = len(data)
    if is_sample and n < 2:
        raise ValueError("Sample variance requires at least 2 data points.")

    mean = calculate_mean(data)
    sum_squared_diff = sum((x - mean) ** 2 for x in data)
    divisor = (n - 1) if is_sample else n
    
    return sum_squared_diff / divisor


def calculate_std_dev(data: List[float], is_sample: bool = True) -> float:
    """
    Calculates the standard deviation of a list of numbers.

    Args:
        data: List of numerical values.
        is_sample: If True, returns sample standard deviation (s).
                   If False, returns population standard deviation (sigma).

    Returns:
        Standard deviation value as a float.
    """
    var = calculate_variance(data, is_sample=is_sample)
    return math.sqrt(var)


# ─── 2. Welford's Single-Pass Online Accumulator ─────────────────────────────


class WelfordAccumulator:
    """
    Implements Welford's algorithm for computing streaming mean, variance, and
    standard deviation in a single numerical-stable pass without storing history.
    """

    def __init__(self) -> None:
        """Initializes an empty Welford accumulator."""
        self._count: int = 0
        self._mean: float = 0.0
        self._M2: float = 0.0  # Sum of squared differences from current mean

    def update(self, x: float) -> None:
        """
        Updates the accumulator with a new value x.

        Args:
            x: Numerical value to stream in.
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError(f"Expected numeric input, got {type(x).__name__}")

        self._count += 1
        delta = x - self._mean
        self._mean += delta / self._count
        delta2 = x - self._mean
        self._M2 += delta * delta2

    def update_batch(self, data: List[float]) -> None:
        """
        Updates the accumulator with a list of values.

        Args:
            data: List of numerical values.
        """
        for val in data:
            self.update(val)

    @property
    def count(self) -> int:
        """Returns the number of elements processed."""
        return self._count

    @property
    def mean(self) -> float:
        """Returns the current streaming mean."""
        if self._count == 0:
            raise ValueError("No data points accumulated yet.")
        return self._mean

    @property
    def variance_sample(self) -> float:
        """Returns the current sample variance (s^2)."""
        if self._count < 2:
            raise ValueError("Sample variance requires at least 2 data points.")
        return self._M2 / (self._count - 1)

    @property
    def variance_population(self) -> float:
        """Returns the current population variance (sigma^2)."""
        if self._count < 1:
            raise ValueError("Population variance requires at least 1 data point.")
        return self._M2 / self._count

    @property
    def std_dev_sample(self) -> float:
        """Returns the current sample standard deviation (s)."""
        return math.sqrt(self.variance_sample)

    @property
    def std_dev_population(self) -> float:
        """Returns the current population standard deviation (sigma)."""
        return math.sqrt(self.variance_population)

    def reset(self) -> None:
        """Resets the accumulator state."""
        self._count = 0
        self._mean = 0.0
        self._M2 = 0.0

