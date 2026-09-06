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
