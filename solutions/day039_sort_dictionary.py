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


# ─── 4. Custom Key Transformations & Frequency Sorting ───────────────────────


def sort_by_custom_key(
    d: dict, key_func: Callable[[Any, Any], Any], reverse: bool = False
) -> dict:
    """
    Sorts a dictionary using a custom function `key_func(key, value)`.

    Args:
        d: Input dictionary.
        key_func: Function accepting (key, value) and returning a sortable value.
        reverse: If True, sort in descending order.

    Returns:
        Sorted dictionary.

    Example:
        sort_by_custom_key({"a": 5, "b": 10}, key_func=lambda k, v: v % 3)
    """
    return dict(sorted(d.items(), key=lambda item: key_func(item[0], item[1]), reverse=reverse))


def sort_by_frequency_or_count(d: dict, reverse: bool = True) -> dict:
    """
    Sorts a frequency dictionary (element -> count) by count descending, then element ascending.

    Args:
        d: Input dictionary where values are integers (frequencies).
        reverse: If True, higher frequencies come first.

    Returns:
        Sorted frequency dictionary.

    Example:
        sort_by_frequency_or_count({"apple": 3, "banana": 5, "cherry": 3})
        -> {"banana": 5, "apple": 3, "cherry": 3}
    """
    items = sorted(d.items(), key=lambda x: x[0])  # Alphabetical tie-breaker
    items = sorted(items, key=lambda x: x[1], reverse=reverse)
    return dict(items)


# ─── 5. Recursive Nested Dictionary Sorting ──────────────────────────────────


def sort_nested_dictionary(d: dict, by: str = "key", reverse: bool = False) -> dict:
    """
    Recursively sorts nested dictionaries at all levels by key or by value.

    Args:
        d: Input dictionary (can be nested).
        by: 'key' or 'value'.
        reverse: If True, sort in descending order.

    Returns:
        Recursively sorted dictionary.

    Example:
        d = {"z": 1, "a": {"c": 3, "b": 2}}
        sort_nested_dictionary(d, by="key") -> {"a": {"b": 2, "c": 3}, "z": 1}
    """
    if not isinstance(d, dict):
        return d

    # First recursively process nested dictionary values
    processed = {}
    for k, v in d.items():
        if isinstance(v, dict):
            processed[k] = sort_nested_dictionary(v, by=by, reverse=reverse)
        elif isinstance(v, list):
            processed[k] = [
                sort_nested_dictionary(elem, by=by, reverse=reverse)
                if isinstance(elem, dict) else elem
                for elem in v
            ]
        else:
            processed[k] = v

    # Now sort current level
    if by == "key":
        return dict(sorted(processed.items(), key=lambda x: x[0], reverse=reverse))
    elif by == "value":
        # String representation of values to allow comparing dicts/lists safely
        return dict(
            sorted(
                processed.items(),
                key=lambda x: (isinstance(x[1], (dict, list)), str(x[1])),
                reverse=reverse,
            )
        )
    else:
        raise ValueError(f"Invalid sorting criterion: {by}. Choose 'key' or 'value'.")


# ─── 6. Top-K, Bottom-K & Chunked Sorting ─────────────────────────────────────


def get_top_k_by_value(d: dict, k: int, reverse: bool = True) -> dict:
    """
    Extracts top K items from dictionary sorted by value.

    Args:
        d: Input dictionary.
        k: Number of elements to retrieve.
        reverse: If True, highest values first.

    Returns:
        Dictionary containing top K items.

    Example:
        get_top_k_by_value({"a": 10, "b": 50, "c": 30}, k=2) -> {"b": 50, "c": 30}
    """
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=reverse)
    return dict(sorted_items[:k])


def get_bottom_k_by_value(d: dict, k: int) -> dict:
    """
    Extracts bottom K items (lowest values) from dictionary.

    Args:
        d: Input dictionary.
        k: Number of elements to retrieve.

    Returns:
        Dictionary containing bottom K items in ascending value order.

    Example:
        get_bottom_k_by_value({"a": 10, "b": 50, "c": 30}, k=2) -> {"a": 10, "c": 30}
    """
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=False)
    return dict(sorted_items[:k])


def sort_dictionary_in_chunks(
    d: dict, chunk_size: int, by: str = "key", reverse: bool = False
) -> List[dict]:
    """
    Sorts a dictionary and splits it into chunks of fixed size.

    Args:
        d: Input dictionary.
        chunk_size: Max elements per dictionary chunk.
        by: 'key' or 'value'.
        reverse: Sort order.

    Returns:
        List of sorted dictionary chunks.

    Example:
        sort_dictionary_in_chunks({"c": 3, "a": 1, "b": 2}, chunk_size=2, by="key")
        -> [{"a": 1, "b": 2}, {"c": 3}]
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    key_func = (lambda x: x[0]) if by == "key" else (lambda x: x[1])
    sorted_items = sorted(d.items(), key=key_func, reverse=reverse)

    chunks = []
    for i in range(0, len(sorted_items), chunk_size):
        chunks.append(dict(sorted_items[i : i + chunk_size]))
    return chunks


# ─── 7. OrderedDict & Order Verification ─────────────────────────────────────


def sort_to_ordered_dict(
    d: dict, by: str = "key", reverse: bool = False
) -> OrderedDict:
    """
    Sorts a dictionary and returns an explicit collections.OrderedDict instance.

    Args:
        d: Input dictionary.
        by: 'key' or 'value'.
        reverse: Sort order.

    Returns:
        OrderedDict instance maintaining sorted order.

    Example:
        sort_to_ordered_dict({"b": 2, "a": 1}, by="key") -> OrderedDict([('a', 1), ('b', 2)])
    """
    key_func = (lambda x: x[0]) if by == "key" else (lambda x: x[1])
    return OrderedDict(sorted(d.items(), key=key_func, reverse=reverse))


def is_dictionary_sorted(d: dict, by: str = "key", reverse: bool = False) -> bool:
    """
    Verifies if keys or values of a dictionary are strictly in sorted order.

    Args:
        d: Input dictionary.
        by: 'key' or 'value'.
        reverse: Sort order to check against.

    Returns:
        True if the dictionary is sorted according to criteria, False otherwise.

    Example:
        is_dictionary_sorted({"a": 1, "b": 2}, by="key") -> True
        is_dictionary_sorted({"b": 2, "a": 1}, by="key") -> False
    """
    if len(d) <= 1:
        return True

    elements = list(d.keys()) if by == "key" else list(d.values())
    
    for i in range(len(elements) - 1):
        if reverse:
            if elements[i] < elements[i + 1]:
                return False
        else:
            if elements[i] > elements[i + 1]:
                return False
    return True






