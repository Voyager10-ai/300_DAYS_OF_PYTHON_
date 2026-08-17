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
