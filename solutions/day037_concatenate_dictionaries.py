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
