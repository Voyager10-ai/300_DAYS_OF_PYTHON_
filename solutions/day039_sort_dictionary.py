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

