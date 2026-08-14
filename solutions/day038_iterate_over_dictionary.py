# Day 38: Iterate Over Dictionary
#
# Problem:
#   Write a Python program to iterate over dictionaries using multiple
#   approaches — keys, values, items, sorted, filtered, nested traversal,
#   indexed iteration, chunking, transformation, and safe mutations.

import sys
import copy
import unittest
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Generator, Iterable


# ─── Core Iteration Methods ───────────────────────────────────────────────────


def iterate_keys(d: dict) -> List[Any]:
    """
    Iterates over all keys of a dictionary.

    Args:
        d: Input dictionary.

    Returns:
        List of dictionary keys.

    Example:
        iterate_keys({"a": 1, "b": 2}) -> ["a", "b"]
    """
    return [key for key in d.keys()]


def iterate_values(d: dict) -> List[Any]:
    """
    Iterates over all values of a dictionary.

    Args:
        d: Input dictionary.

    Returns:
        List of dictionary values.

    Example:
        iterate_values({"a": 1, "b": 2}) -> [1, 2]
    """
    return [val for val in d.values()]


def iterate_items(d: dict) -> List[Tuple[Any, Any]]:
    """
    Iterates over key-value pairs (items) of a dictionary.

    Args:
        d: Input dictionary.

    Returns:
        List of (key, value) tuples.

    Example:
        iterate_items({"a": 1, "b": 2}) -> [("a", 1), ("b", 2)]
    """
    return [(k, v) for k, v in d.items()]


# ─── Sorted & Ordered Iteration ───────────────────────────────────────────────


def iterate_sorted_by_keys(d: dict, reverse: bool = False) -> List[Tuple[Any, Any]]:
    """
    Iterates over dictionary items sorted by key.

    Args:
        d: Input dictionary.
        reverse: If True, sort in descending order.

    Returns:
        List of (key, value) tuples sorted by key.

    Example:
        iterate_sorted_by_keys({"c": 3, "a": 1, "b": 2}) -> [("a", 1), ("b", 2), ("c", 3)]
    """
    return sorted(d.items(), key=lambda item: item[0], reverse=reverse)


def iterate_sorted_by_values(d: dict, reverse: bool = False) -> List[Tuple[Any, Any]]:
    """
    Iterates over dictionary items sorted by value.

    Args:
        d: Input dictionary.
        reverse: If True, sort in descending order.

    Returns:
        List of (key, value) tuples sorted by value.

    Example:
        iterate_sorted_by_values({"a": 10, "b": 5, "c": 20}) -> [("b", 5), ("a", 10), ("c", 20)]
    """
    return sorted(d.items(), key=lambda item: item[1], reverse=reverse)


def iterate_custom_order(d: dict, key_order: List[Any], include_missing: bool = False, default_val: Any = None) -> List[Tuple[Any, Any]]:
    """
    Iterates over dictionary items in a specified key sequence.

    Args:
        d: Input dictionary.
        key_order: List of keys in desired order.
        include_missing: If True, includes keys from key_order not present in d with default_val.
        default_val: Value to use when key is missing and include_missing is True.

    Returns:
        List of (key, value) tuples matching the custom key order.

    Example:
        iterate_custom_order({"a": 1, "b": 2, "c": 3}, ["c", "a"]) -> [("c", 3), ("a", 1)]
    """
    result = []
    for k in key_order:
        if k in d:
            result.append((k, d[k]))
        elif include_missing:
            result.append((k, default_val))
    return result

