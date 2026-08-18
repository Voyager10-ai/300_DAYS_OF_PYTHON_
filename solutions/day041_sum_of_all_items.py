# Day 41: Sum of All Items
#
# Problem:
#   Write a Python program to calculate the sum of all items (values/keys/containers)
#   in a dictionary, including basic numeric sum, safe type conversion, conditional filtering,
#   recursive nested dictionary summation, container list aggregation, weighted sums,
#   functional reductions, statistical summaries, and robust unit testing.

import sys
import unittest
import functools
import operator
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Union


# ─── 1. Core Dictionary Summation ─────────────────────────────────────────────


def sum_dict_values(d: Dict[Any, Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of all numeric values in a dictionary.

    Args:
        d: Input dictionary containing numeric values.

    Returns:
        Total sum of values (int or float).

    Example:
        sum_dict_values({"a": 100, "b": 200, "c": 300}) -> 600
    """
    if not d:
        return 0
    return sum(v for v in d.values() if isinstance(v, (int, float)) and not isinstance(v, bool))


def sum_dict_keys(d: Dict[Union[int, float], Any]) -> Union[int, float]:
    """
    Calculates the sum of all numeric keys in a dictionary.

    Args:
        d: Input dictionary with numeric keys.

    Returns:
        Total sum of keys (int or float).

    Example:
        sum_dict_keys({10: "apple", 20: "banana", 30: "cherry"}) -> 60
    """
    if not d:
        return 0
    return sum(k for k in d.keys() if isinstance(k, (int, float)) and not isinstance(k, bool))


def sum_dict_keys_and_values(d: Dict[Union[int, float], Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of all numeric keys and numeric values combined in a dictionary.

    Args:
        d: Input dictionary with numeric keys and values.

    Returns:
        Total sum of keys and values.

    Example:
        sum_dict_keys_and_values({1: 10, 2: 20, 3: 30}) -> 66
    """
    total = 0
    for k, v in d.items():
        if isinstance(k, (int, float)) and not isinstance(k, bool):
            total += k
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v
    return total


# ─── 2. Safe Type Conversion & Robust Summation ──────────────────────────────


def sum_dict_values_safe(d: Dict[Any, Any], default_val: float = 0.0) -> float:
    """
    Safely sums values in a dictionary by attempting to parse string representation
    of numbers into floats. Ignores invalid non-numeric entries gracefully.

    Args:
        d: Input dictionary with potentially mixed types (ints, floats, numeric strings).
        default_val: Default starting accumulator value.

    Returns:
        Total accumulated float sum.

    Example:
        sum_dict_values_safe({"a": 10, "b": "20.5", "c": "invalid", "d": 5}) -> 35.5
    """
    total = default_val
    for v in d.values():
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)):
            total += v
        elif isinstance(v, str):
            try:
                total += float(v)
            except ValueError:
                pass
    return total


def extract_numeric_values(d: Dict[Any, Any]) -> List[Union[int, float]]:
    """
    Extracts all valid numeric values from a dictionary into a list.

    Args:
        d: Input dictionary.

    Returns:
        List of numeric values.

    Example:
        extract_numeric_values({"a": 10, "b": "hello", "c": 3.14}) -> [10, 3.14]
    """
    nums = []
    for v in d.values():
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)):
            nums.append(v)
        elif isinstance(v, str):
            try:
                val = float(v)
                nums.append(int(val) if val.is_integer() else val)
            except ValueError:
                pass
    return nums


# ─── 3. Conditional & Filtered Summation ──────────────────────────────────────


def sum_dict_values_conditional(
    d: Dict[Any, Any], predicate: Callable[[Any, Any], bool]
) -> Union[int, float]:
    """
    Sums values in a dictionary that satisfy a predicate function `predicate(key, value)`.

    Args:
        d: Input dictionary.
        predicate: Callable taking (key, value) and returning bool.

    Returns:
        Sum of filtered numeric values.

    Example:
        sum_dict_values_conditional({"a": 10, "b": 25, "c": 30}, lambda k, v: v > 15) -> 55
    """
    total = 0
    for k, v in d.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if predicate(k, v):
                total += v
    return total


def sum_even_values(d: Dict[Any, int]) -> int:
    """
    Sums only even integer values in a dictionary.

    Args:
        d: Input dictionary with integer values.

    Returns:
        Sum of even values.

    Example:
        sum_even_values({"a": 1, "b": 2, "c": 3, "d": 4}) -> 6
    """
    return sum(v for v in d.values() if isinstance(v, int) and not isinstance(v, bool) and v % 2 == 0)


def sum_odd_values(d: Dict[Any, int]) -> int:
    """
    Sums only odd integer values in a dictionary.

    Args:
        d: Input dictionary with integer values.

    Returns:
        Sum of odd values.

    Example:
        sum_odd_values({"a": 1, "b": 2, "c": 3, "d": 4}) -> 4
    """
    return sum(v for v in d.values() if isinstance(v, int) and not isinstance(v, bool) and v % 2 != 0)


def sum_values_above_threshold(d: Dict[Any, Union[int, float]], threshold: Union[int, float]) -> Union[int, float]:
    """
    Sums values strictly greater than a threshold value.

    Args:
        d: Input dictionary.
        threshold: Numeric threshold cut-off.

    Returns:
        Sum of values > threshold.

    Example:
        sum_values_above_threshold({"a": 5, "b": 15, "c": 25}, 10) -> 40
    """
    return sum(v for v in d.values() if isinstance(v, (int, float)) and not isinstance(v, bool) and v > threshold)


# ─── 4. Recursive Nested Dictionary Summation ─────────────────────────────────


def sum_nested_dict_values(d: Dict[Any, Any]) -> Union[int, float]:
    """
    Recursively sums all numeric values in an arbitrarily nested dictionary structure.

    Args:
        d: Input nested dictionary.

    Returns:
        Total sum of all nested numeric values.

    Example:
        nested = {"a": 10, "b": {"c": 20, "d": {"e": 30}}}
        sum_nested_dict_values(nested) -> 60
    """
    total = 0
    for v in d.values():
        if isinstance(v, dict):
            total += sum_nested_dict_values(v)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v
    return total


def sum_nested_dict_by_key(d: Dict[Any, Any], target_key: Any) -> Union[int, float]:
    """
    Recursively sums values associated with a specific `target_key` across a nested dictionary.

    Args:
        d: Input nested dictionary.
        target_key: Key name to search and sum values for.

    Returns:
        Sum of values corresponding to target_key.

    Example:
        d = {"a": {"price": 10}, "b": {"price": 20, "tax": 5}}
        sum_nested_dict_by_key(d, "price") -> 30
    """
    total = 0
    for k, v in d.items():
        if k == target_key and isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v
        if isinstance(v, dict):
            total += sum_nested_dict_by_key(v, target_key)
    return total


def sum_nested_dict_depth_weighted(d: Dict[Any, Any], current_depth: int = 1) -> float:
    """
    Sums values in a nested dictionary where values are multiplied by their nesting depth level.

    Args:
        d: Input nested dictionary.
        current_depth: Current nesting depth level (starts at 1).

    Returns:
        Depth-weighted total sum.

    Example:
        d = {"a": 10, "b": {"c": 20}}  # 10*1 + 20*2 = 50
        sum_nested_dict_depth_weighted(d) -> 50
    """
    total = 0.0
    for v in d.values():
        if isinstance(v, dict):
            total += sum_nested_dict_depth_weighted(v, current_depth + 1)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v * current_depth
    return total



