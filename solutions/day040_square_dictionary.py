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


# ─── 3. Conditional & Filtered Square Dictionaries ──────────────────────────


def filter_even_square_dict(n: int) -> Dict[int, int]:
    """
    Generates a square dictionary containing only even numbers from 1 to n.

    Args:
        n: Upper limit integer (inclusive).

    Returns:
        Dictionary mapping even numbers to their squares.

    Example:
        filter_even_square_dict(6) -> {2: 4, 4: 16, 6: 36}
    """
    return {i: i * i for i in range(1, n + 1) if i % 2 == 0}


def filter_odd_square_dict(n: int) -> Dict[int, int]:
    """
    Generates a square dictionary containing only odd numbers from 1 to n.

    Args:
        n: Upper limit integer (inclusive).

    Returns:
        Dictionary mapping odd numbers to their squares.

    Example:
        filter_odd_square_dict(5) -> {1: 1, 3: 9, 5: 25}
    """
    return {i: i * i for i in range(1, n + 1) if i % 2 != 0}


def generate_conditional_square_dict(
    n: int, predicate: Callable[[int], bool]
) -> Dict[int, int]:
    """
    Generates a square dictionary filtering keys using an arbitrary predicate callable.

    Args:
        n: Upper limit integer (inclusive).
        predicate: A function returning True if key should be included.

    Returns:
        Filtered square dictionary.

    Example:
        generate_conditional_square_dict(10, lambda x: x % 3 == 0)
        -> {3: 9, 6: 36, 9: 81}
    """
    return {i: i * i for i in range(1, n + 1) if predicate(i)}


def filter_squares_by_value(
    d: Dict[Any, Union[int, float]],
    min_val: Optional[Union[int, float]] = None,
    max_val: Optional[Union[int, float]] = None,
) -> Dict[Any, Union[int, float]]:
    """
    Filters an existing square dictionary keeping only pairs whose values fall in [min_val, max_val].

    Args:
        d: Input square dictionary.
        min_val: Minimum acceptable value threshold (inclusive).
        max_val: Maximum acceptable value threshold (inclusive).

    Returns:
        Filtered dictionary.

    Example:
        d = {1: 1, 2: 4, 3: 9, 4: 16}
        filter_squares_by_value(d, min_val=4, max_val=10) -> {2: 4, 3: 9}
    """
    result = {}
    for k, v in d.items():
        if min_val is not None and v < min_val:
            continue
        if max_val is not None and v > max_val:
            continue
        result[k] = v
    return result


# ─── 4. Nested & Multi-Dimensional Square Dictionaries ────────────────────────


def generate_nested_square_dict(rows: int, cols: int) -> Dict[int, Dict[int, int]]:
    """
    Generates a 2D nested dictionary where nested values are i * j or (i**2 + j**2).

    Args:
        rows: Number of row keys (1..rows).
        cols: Number of column keys (1..cols).

    Returns:
        Nested dictionary {i: {j: i**2 + j**2}}.

    Example:
        generate_nested_square_dict(2, 2) -> {1: {1: 2, 2: 5}, 2: {1: 5, 2: 8}}
    """
    return {
        i: {j: i ** 2 + j ** 2 for j in range(1, cols + 1)}
        for i in range(1, rows + 1)
    }


def generate_coordinate_square_dict(n: int) -> Dict[Tuple[int, int], int]:
    """
    Generates a dictionary with 2D coordinate tuple keys mapped to Euclidean square distance (x^2 + y^2).

    Args:
        n: Dimension bounds (1..n for x and y).

    Returns:
        Dictionary mapping (x, y) -> x**2 + y**2.

    Example:
        generate_coordinate_square_dict(2) -> {(1, 1): 2, (1, 2): 5, (2, 1): 5, (2, 2): 8}
    """
    return {
        (x, y): x ** 2 + y ** 2
        for x in range(1, n + 1)
        for y in range(1, n + 1)
    }


def flatten_nested_square_dict(nested_d: Dict[int, Dict[int, int]]) -> Dict[Tuple[int, int], int]:
    """
    Flattens a 2D nested dictionary into a single dictionary with (row, col) tuple keys.

    Args:
        nested_d: Nested dictionary structure {r: {c: val}}.

    Returns:
        Flattened dictionary with tuple keys.

    Example:
        flatten_nested_square_dict({1: {2: 5}}) -> {(1, 2): 5}
    """
    return {
        (r, c): val
        for r, row_dict in nested_d.items()
        for c, val in row_dict.items()
    }


# ─── 5. Inplace Modification & Dictionary Updates ─────────────────────────────


def square_dict_values_inplace(d: Dict[Any, Union[int, float]]) -> Dict[Any, Union[int, float]]:
    """
    Modifies an existing dictionary in-place by squaring all numeric values.

    Args:
        d: Input dictionary whose values are numeric.

    Returns:
        The mutated dictionary `d`.

    Example:
        d = {"a": 2, "b": 3}
        square_dict_values_inplace(d) -> {"a": 4, "b": 9}
    """
    for k in d:
        if isinstance(d[k], (int, float)):
            d[k] = d[k] ** 2
    return d


def update_dict_with_squares(
    d: Dict[int, int], keys: List[int]
) -> Dict[int, int]:
    """
    Updates or inserts keys in dictionary `d` with their squared values.

    Args:
        d: Target dictionary.
        keys: List of keys to update/add with key^2.

    Returns:
        Updated target dictionary.

    Example:
        d = {1: 1}
        update_dict_with_squares(d, [2, 3]) -> {1: 1, 2: 4, 3: 9}
    """
    d.update({k: k * k for k in keys})
    return d


def merge_with_square_dict(
    d: Dict[int, int], n: int, resolve_strategy: str = "sum"
) -> Dict[int, int]:
    """
    Merges an existing dictionary `d` with a generated square dictionary from 1..n.

    Args:
        d: Input dictionary.
        n: Upper limit for generated square dictionary.
        resolve_strategy: Strategy for overlapping keys: 'sum', 'keep_existing', or 'overwrite'.

    Returns:
        Merged dictionary.

    Example:
        merge_with_square_dict({2: 10}, 3, "sum") -> {1: 1, 2: 14, 3: 9}
    """
    sq_dict = generate_square_dict(n)
    result = dict(d)
    for k, v in sq_dict.items():
        if k in result:
            if resolve_strategy == "sum":
                result[k] += v
            elif resolve_strategy == "overwrite":
                result[k] = v
            # 'keep_existing' does nothing
        else:
            result[k] = v
    return result




