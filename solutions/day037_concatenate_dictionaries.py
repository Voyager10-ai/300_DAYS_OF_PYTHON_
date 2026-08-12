# Day 37: Concatenate Dictionaries
#
# Problem:
#   Write a Python program to concatenate (merge) two or more dictionaries
#   using multiple approaches — update(), unpacking, ChainMap, loops, and more.

import sys
import re
import copy
import unittest
from collections import ChainMap
from functools import reduce
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Iterable


# ─── Core Concatenation Methods ───────────────────────────────────────────────


def concat_update(d1: dict, d2: dict) -> dict:
    """
    Concatenates two dictionaries using dict.update().
    Keys from d2 overwrite matching keys in d1.

    Args:
        d1: First dictionary (base).
        d2: Second dictionary (overwrites).

    Returns:
        New merged dictionary.

    Example:
        concat_update({"a": 1}, {"b": 2}) -> {"a": 1, "b": 2}
        concat_update({"a": 1}, {"a": 99}) -> {"a": 99}
    """
    result = dict(d1)
    result.update(d2)
    return result


def concat_unpack(d1: dict, d2: dict) -> dict:
    """
    Concatenates two dictionaries using ** unpacking (Python 3.5+).
    Keys from d2 overwrite matching keys in d1.

    Args:
        d1: First dictionary.
        d2: Second dictionary.

    Returns:
        New merged dictionary.

    Example:
        concat_unpack({"x": 10}, {"y": 20}) -> {"x": 10, "y": 20}
    """
    return {**d1, **d2}


def concat_union(d1: dict, d2: dict) -> dict:
    """
    Concatenates two dictionaries using the | merge operator (Python 3.9+).
    Keys from d2 overwrite matching keys in d1.

    Args:
        d1: First dictionary.
        d2: Second dictionary.

    Returns:
        New merged dictionary.
    """
    return d1 | d2


def concat_chainmap(d1: dict, d2: dict) -> dict:
    """
    Concatenates two dictionaries using collections.ChainMap.
    First dictionary takes priority for duplicate keys.

    Args:
        d1: First dictionary (higher priority).
        d2: Second dictionary (lower priority).

    Returns:
        New flattened merged dictionary.

    Note:
        ChainMap gives priority to the FIRST dict, unlike update/unpack.
    """
    return dict(ChainMap(d1, d2))


# ─── Deep Merge for Nested Dictionaries ──────────────────────────────────────


def deep_merge(d1: dict, d2: dict) -> dict:
    """
    Recursively merges two nested dictionaries. When both values for a key
    are dicts, they are merged recursively. Otherwise d2's value wins.

    Args:
        d1: Base dictionary.
        d2: Dictionary to merge in.

    Returns:
        New deeply merged dictionary.

    Example:
        deep_merge(
            {"a": 1, "cfg": {"x": 10, "y": 20}},
            {"b": 2, "cfg": {"y": 99, "z": 30}}
        ) -> {"a": 1, "b": 2, "cfg": {"x": 10, "y": 99, "z": 30}}
    """
    result = copy.deepcopy(d1)

    for key, val in d2.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = copy.deepcopy(val)

    return result


def deep_merge_many(*dicts: dict) -> dict:
    """
    Deep-merges an arbitrary number of nested dictionaries left-to-right.

    Args:
        *dicts: Variable number of dictionaries.

    Returns:
        Single deeply merged dictionary.

    Example:
        deep_merge_many({"a": 1}, {"b": 2}, {"a": 99, "c": 3})
        -> {"a": 99, "b": 2, "c": 3}
    """
    if not dicts:
        return {}
    return reduce(deep_merge, dicts)

