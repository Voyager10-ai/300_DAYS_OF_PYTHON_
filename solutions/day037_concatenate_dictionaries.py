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


# ─── Merge with Conflict Resolution ──────────────────────────────────────────


def concat_with_resolver(d1: dict, d2: dict, resolver: Callable[[Any, Any, Any], Any]) -> dict:
    """
    Merges two dictionaries with a custom conflict resolution function.

    Args:
        d1: First dictionary.
        d2: Second dictionary.
        resolver: Callable(key, val_from_d1, val_from_d2) -> resolved_value.

    Returns:
        Merged dictionary with conflicts resolved by the resolver function.

    Example:
        concat_with_resolver({"a": 1}, {"a": 5}, lambda k, v1, v2: v1 + v2)
        -> {"a": 6}
    """
    result = dict(d1)
    for key, val in d2.items():
        if key in result:
            result[key] = resolver(key, result[key], val)
        else:
            result[key] = val
    return result


def concat_keep_first(d1: dict, d2: dict) -> dict:
    """
    Merges two dictionaries, keeping d1's value on conflict (first-wins).

    Example:
        concat_keep_first({"a": 1}, {"a": 99, "b": 2}) -> {"a": 1, "b": 2}
    """
    result = dict(d2)
    result.update(d1)
    return result


def concat_collect_values(d1: dict, d2: dict) -> dict:
    """
    Merges dictionaries by collecting conflicting values into lists.

    Example:
        concat_collect_values({"a": 1, "b": 2}, {"a": 10, "c": 3})
        -> {"a": [1, 10], "b": [2], "c": [3]}
    """
    result: Dict[Any, list] = {}
    all_keys = set(d1.keys()) | set(d2.keys())

    for key in all_keys:
        values = []
        if key in d1:
            values.append(d1[key])
        if key in d2:
            values.append(d2[key])
        result[key] = values

    return result


# ─── Multi-Dictionary Merge ──────────────────────────────────────────────────


def concat_multiple(*dicts: dict) -> dict:
    """
    Merges an arbitrary number of dictionaries left-to-right using reduce.
    Later dictionaries overwrite earlier ones on key conflict.

    Args:
        *dicts: Variable number of dictionaries.

    Returns:
        Single merged dictionary.

    Example:
        concat_multiple({"a": 1}, {"b": 2}, {"c": 3, "a": 99})
        -> {"a": 99, "b": 2, "c": 3}
    """
    if not dicts:
        return {}
    return reduce(lambda acc, d: {**acc, **d}, dicts)


def concat_from_list(dict_list: List[dict]) -> dict:
    """
    Merges a list of dictionaries into one using dict comprehension.

    Args:
        dict_list: List of dictionaries.

    Returns:
        Single merged dictionary.
    """
    result = {}
    for d in dict_list:
        result.update(d)
    return result


def concat_with_counter(d1: dict, d2: dict) -> dict:
    """
    Merges two dictionaries by summing numeric values for shared keys.
    Non-numeric shared keys use d2's value.

    Example:
        concat_with_counter({"a": 5, "b": 10}, {"a": 3, "c": 7})
        -> {"a": 8, "b": 10, "c": 7}
    """
    result = dict(d1)
    for key, val in d2.items():
        if key in result and isinstance(result[key], (int, float)) and isinstance(val, (int, float)):
            result[key] = result[key] + val
        else:
            result[key] = val
    return result



