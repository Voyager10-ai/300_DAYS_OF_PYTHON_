# Day 40: Square Dictionary
#
# Problem:
#   Write a Python program to generate, manipulate, and work with dictionaries
#   where keys are numbers (or elements) and values are their squares (x: x*x),
#   including range generators, custom power transformations, conditional filtering,
#   nested square matrices, in-place updates, functional stream generators,
#   inverse lookups, and mathematical verification.

import math
import sys
import unittest
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Union, Generator


# ─── 1. Core Square Dictionary Generation ──────────────────────────────────────


def generate_square_dict(n: int) -> Dict[int, int]:
    """
    Generates a dictionary where keys are numbers from 1 to n (inclusive)
    and values are the squares of the keys.

    Args:
        n: Upper limit integer (inclusive).

    Returns:
        A dictionary mapping integers 1..n to their squares.

    Example:
        generate_square_dict(5) -> {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
    """
    if n < 1:
        return {}
    return {i: i * i for i in range(1, n + 1)}


def generate_square_dict_range(start: int, stop: int, step: int = 1) -> Dict[int, int]:
    """
    Generates a square dictionary for numbers in a custom range [start, stop).

    Args:
        start: Starting integer (inclusive).
        stop: Ending integer (exclusive).
        step: Step size (default is 1).

    Returns:
        A dictionary mapping integers in the range to their squares.

    Example:
        generate_square_dict_range(2, 6) -> {2: 4, 3: 9, 4: 16, 5: 25}
    """
    return {i: i * i for i in range(start, stop, step)}


def generate_square_dict_from_list(numbers: List[Union[int, float]]) -> Dict[Union[int, float], Union[int, float]]:
    """
    Generates a square dictionary from an arbitrary list of numbers.

    Args:
        numbers: List of numbers (int or float).

    Returns:
        A dictionary mapping each number to its square.

    Example:
        generate_square_dict_from_list([3, 1.5, -4]) -> {3: 9, 1.5: 2.25, -4: 16}
    """
    return {num: num * num for num in numbers}


# ─── 2. Custom Power & Exponent Transformations ─────────────────────────────


def generate_power_dict(n: int, power: Union[int, float]) -> Dict[int, Union[int, float]]:
    """
    Generates a dictionary where keys are numbers from 1 to n
    and values are key elevated to the specified power (key ** power).

    Args:
        n: Upper limit integer (inclusive).
        power: Exponent power (e.g., 3 for cubes, 0.5 for square roots).

    Returns:
        A dictionary mapping 1..n to key ** power.

    Example:
        generate_power_dict(3, 3) -> {1: 1, 2: 8, 3: 27}
    """
    if n < 1:
        return {}
    return {i: round(i ** power, 4) if isinstance(power, float) else i ** power for i in range(1, n + 1)}


def generate_cube_dict(n: int) -> Dict[int, int]:
    """
    Convenience function to generate a dictionary of cubes from 1 to n.

    Args:
        n: Upper limit integer (inclusive).

    Returns:
        A dictionary mapping 1..n to key^3.

    Example:
        generate_cube_dict(4) -> {1: 1, 2: 8, 3: 27, 4: 64}
    """
    return generate_power_dict(n, 3)


def generate_custom_transform_dict(
    items: List[Any],
    key_func: Callable[[Any], Any] = lambda x: x,
    val_func: Callable[[Any], Any] = lambda x: x ** 2,
) -> Dict[Any, Any]:
    """
    Generates a dictionary with custom key and value transformation functions.

    Args:
        items: List of elements to process.
        key_func: Callable function to map item to key.
        val_func: Callable function to map item to value (default computes square).

    Returns:
        Transformed dictionary.

    Example:
        generate_custom_transform_dict([1, 2, 3], key_func=lambda x: f"num_{x}")
        -> {"num_1": 1, "num_2": 4, "num_3": 9}
    """
    return {key_func(x): val_func(x) for x in items}

