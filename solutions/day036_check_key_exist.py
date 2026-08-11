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
