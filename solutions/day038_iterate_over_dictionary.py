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
