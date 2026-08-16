# Day 39: Sort Dictionary
#
# Problem:
#   Write a Python program to sort dictionaries by keys, values, multiple criteria,
#   custom key functions, nested structures, frequencies, top-K/bottom-K elements,
#   and OrderedDict order preservation.

import re
import sys
import copy
import unittest
from collections import OrderedDict
from typing import List, Dict, Tuple, Set, Any, Callable, Optional


# ─── 1. Core Key Sorting ──────────────────────────────────────────────────────


def sort_by_keys(d: dict, reverse: bool = False) -> dict:
    """
    Sorts a dictionary by its keys in ascending or descending order.

    Args:
        d: Input dictionary.
        reverse: If True, sort keys in descending order.

    Returns:
        A new dictionary sorted by keys.

    Example:
        sort_by_keys({"b": 2, "a": 1, "c": 3}) -> {"a": 1, "b": 2, "c": 3}
    """
    return {k: d[k] for k in sorted(d.keys(), reverse=reverse)}


def sort_by_keys_natural(d: dict) -> dict:
    """
    Sorts a dictionary by keys using natural alphanumeric sorting
    (e.g., 'item2' comes before 'item10').

    Args:
        d: Input dictionary with string keys.

    Returns:
        A new dictionary sorted naturally by keys.

    Example:
        sort_by_keys_natural({"item10": 1, "item2": 2}) -> {"item2": 2, "item10": 1}
    """
    def natural_key(key_str: str) -> List[Any]:
        return [
            int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', str(key_str))
        ]

    return {k: d[k] for k in sorted(d.keys(), key=natural_key)}


# ─── 2. Value & Attribute Sorting ──────────────────────────────────────────────


def sort_by_values(d: dict, reverse: bool = False) -> dict:
    """
    Sorts a dictionary by its values in ascending or descending order.

    Args:
        d: Input dictionary.
        reverse: If True, sort values in descending order.

    Returns:
        A new dictionary sorted by values.

    Example:
        sort_by_values({"a": 30, "b": 10, "c": 20}) -> {"b": 10, "c": 20, "a": 30}
    """
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))


def sort_by_value_attribute(d: dict, attr: str, reverse: bool = False) -> dict:
    """
    Sorts a dictionary where values are dictionaries or objects by a specific attribute/key.

    Args:
        d: Input dictionary whose values are dicts or objects with attribute `attr`.
        attr: Key or attribute name in the nested value.
        reverse: If True, sort in descending order.

    Returns:
        A new dictionary sorted by the nested attribute.

    Example:
        d = {"alice": {"age": 25}, "bob": {"age": 20}}
        sort_by_value_attribute(d, "age") -> {"bob": {"age": 20}, "alice": {"age": 25}}
    """
    def get_attr(val: Any) -> Any:
        if isinstance(val, dict):
            return val[attr]
        return getattr(val, attr)

    return dict(sorted(d.items(), key=lambda item: get_attr(item[1]), reverse=reverse))


# ─── 3. Multi-Criteria & Tie-Breaker Sorting ─────────────────────────────────


def sort_by_value_then_key(
    d: dict, reverse_value: bool = False, reverse_key: bool = False
) -> dict:
    """
    Sorts a dictionary primarily by value, using key as a tie-breaker.

    Args:
        d: Input dictionary.
        reverse_value: If True, sort values in descending order.
        reverse_key: If True, sort key tie-breakers in descending order.

    Returns:
        Sorted dictionary.

    Example:
        sort_by_value_then_key({"a": 10, "b": 5, "c": 10}) -> {"b": 5, "a": 10, "c": 10}
    """
    # For numeric values & string keys, we can build tuple sort keys
    items = list(d.items())

    # We sort twice or use custom comparison key for general types
    if not reverse_value and not reverse_key:
        return dict(sorted(items, key=lambda x: (x[1], x[0])))
    
    # Python's Timsort is stable: sort secondary key first, then primary key
    items = sorted(items, key=lambda x: x[0], reverse=reverse_key)
    items = sorted(items, key=lambda x: x[1], reverse=reverse_value)
    return dict(items)


def sort_by_key_length_then_alpha(d: dict, reverse_length: bool = False) -> dict:
    """
    Sorts a dictionary by key length first, breaking ties alphabetically.

    Args:
        d: Input dictionary with string keys.
        reverse_length: If True, sort longer keys first.

    Returns:
        Sorted dictionary.

    Example:
        sort_by_key_length_then_alpha({"banana": 1, "apple": 2, "fig": 3})
        -> {"fig": 3, "apple": 2, "banana": 1}
    """
    items = sorted(d.items(), key=lambda x: x[0])  # Alphabetical tie-breaker first
    items = sorted(items, key=lambda x: len(str(x[0])), reverse=reverse_length)
    return dict(items)


