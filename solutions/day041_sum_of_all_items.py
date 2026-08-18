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
