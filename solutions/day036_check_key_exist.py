# Day 36: Check Key Exist
#
# Problem:
#   Write a Python program to check whether a given key exists in a dictionary using multiple approaches.
#   - Direct Membership Check: Fast O(1) membership test using `in` operator.
#   - Safe Value Retrieval: Using `.get()` with a unique sentinel object.
#   - View-Based Check: Using `.keys()` dictionary view object.

import sys
import re
import unittest
from typing import List, Set, Dict, Tuple, Optional, Iterable, Any, Union


_SENTINEL = object()


def check_key_in(d: dict, key: Any) -> bool:
    """
    Checks if a key exists in a dictionary using the `in` operator.

    Args:
        d: Input dictionary.
        key: Key to check for existence.

    Returns:
        True if key exists in d, False otherwise.

    Time Complexity: O(1) on average.
    Space Complexity: O(1).

    Example:
        check_key_in({"a": 1, "b": 2}, "a") -> True
        check_key_in({"a": 1, "b": 2}, "c") -> False
    """
    if not isinstance(d, dict):
        return False
    return key in d


def check_key_get(d: dict, key: Any) -> Tuple[bool, Any]:
    """
    Checks key existence and retrieves value safely using dict.get() with a sentinel object.

    Args:
        d: Input dictionary.
        key: Key to check.

    Returns:
        Tuple (exists: bool, value: Any). If key does not exist, value is None.

    Example:
        check_key_get({"a": None}, "a") -> (True, None)
        check_key_get({"a": None}, "b") -> (False, None)
    """
    if not isinstance(d, dict):
        return False, None
    val = d.get(key, _SENTINEL)
    if val is _SENTINEL:
        return False, None
    return True, val


def check_key_has_keys(d: dict, key: Any) -> bool:
    """
    Checks if key exists by inspecting the dict.keys() view.

    Args:
        d: Input dictionary.
        key: Key to look for.

    Returns:
        True if key is present in d.keys(), False otherwise.
    """
    if not isinstance(d, dict):
        return False
    return key in d.keys()


def check_nested_key(d: dict, key_path: List[Any]) -> Tuple[bool, Any]:
    """
    Traverses a sequence of keys through nested dictionaries to check for path existence.

    Args:
        d: Input dictionary.
        key_path: List of keys representing path (e.g., ['user', 'profile', 'id']).

    Returns:
        Tuple (exists: bool, value: Any).

    Example:
        check_nested_key({"a": {"b": {"c": 42}}}, ["a", "b", "c"]) -> (True, 42)
        check_nested_key({"a": {"b": 10}}, ["a", "b", "c"]) -> (False, None)
    """
    if not isinstance(d, dict) or not key_path:
        return False, None

    current = d
    for key in key_path:
        if not isinstance(current, dict) or key not in current:
            return False, None
        current = current[key]

    return True, current


def check_key_recursive(d: Any, target_key: Any) -> List[Any]:
    """
    Recursively searches for all occurrences of a target key in nested dicts/lists.

    Args:
        d: Input data structure (dict, list, or primitive).
        target_key: Key to find.

    Returns:
        List of values associated with target_key at any depth.

    Example:
        check_key_recursive({"a": 1, "sub": {"a": 2, "c": [{"a": 3}]}}, "a") -> [1, 2, 3]
    """
    results: List[Any] = []

    if isinstance(d, dict):
        for k, v in d.items():
            if k == target_key:
                results.append(v)
            results.extend(check_key_recursive(v, target_key))
    elif isinstance(d, list):
        for item in d:
            results.extend(check_key_recursive(item, target_key))

    return results


def check_all_keys_exist(d: dict, keys: Iterable[Any]) -> bool:
    """
    Checks whether ALL specified keys exist in the dictionary.

    Args:
        d: Input dictionary.
        keys: Iterable of keys to check.

    Returns:
        True if every key in keys exists in d, False otherwise.

    Example:
        check_all_keys_exist({"name": "Alice", "age": 30}, ["name", "age"]) -> True
        check_all_keys_exist({"name": "Alice"}, ["name", "age"]) -> False
    """
    if not isinstance(d, dict):
        return False
    return all(key in d for key in keys)


def check_any_key_exists(d: dict, keys: Iterable[Any]) -> bool:
    """
    Checks whether AT LEAST ONE of the specified keys exists in the dictionary.

    Args:
        d: Input dictionary.
        keys: Iterable of keys to check.

    Returns:
        True if at least one key exists in d, False otherwise.

    Example:
        check_any_key_exists({"name": "Alice"}, ["age", "name"]) -> True
        check_any_key_exists({"name": "Alice"}, ["age", "city"]) -> False
    """
    if not isinstance(d, dict):
        return False
    return any(key in d for key in keys)


def get_missing_keys(d: dict, required_keys: Iterable[Any]) -> Set[Any]:
    """
    Identifies which required keys are missing from the dictionary using set operations.

    Args:
        d: Input dictionary.
        required_keys: Iterable of expected keys.

    Returns:
        Set of keys present in required_keys but absent in d.

    Example:
        get_missing_keys({"a": 1}, ["a", "b", "c"]) -> {"b", "c"}
    """
    if not isinstance(d, dict):
        return set(required_keys)
    return set(required_keys) - set(d.keys())


