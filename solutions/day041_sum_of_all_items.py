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

