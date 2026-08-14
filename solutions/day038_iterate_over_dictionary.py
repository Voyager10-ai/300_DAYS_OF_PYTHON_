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


# ─── Filtered & Conditional Iteration ─────────────────────────────────────────


def iterate_filtered_by_key(d: dict, predicate: Callable[[Any], bool]) -> List[Tuple[Any, Any]]:
    """
    Iterates over dictionary items where the key satisfies a predicate function.

    Args:
        d: Input dictionary.
        predicate: Function taking key and returning True/False.

    Returns:
        List of (key, value) tuples matching the predicate.

    Example:
        iterate_filtered_by_key({"apple": 1, "banana": 2, "avocado": 3}, lambda k: k.startswith("a"))
        -> [("apple", 1), ("avocado", 3)]
    """
    return [(k, v) for k, v in d.items() if predicate(k)]


def iterate_filtered_by_value(d: dict, predicate: Callable[[Any], bool]) -> List[Tuple[Any, Any]]:
    """
    Iterates over dictionary items where the value satisfies a predicate function.

    Args:
        d: Input dictionary.
        predicate: Function taking value and returning True/False.

    Returns:
        List of (key, value) tuples matching the predicate.

    Example:
        iterate_filtered_by_value({"a": 10, "b": 25, "c": 5}, lambda v: v > 9)
        -> [("a", 10), ("b", 25)]
    """
    return [(k, v) for k, v in d.items() if predicate(v)]


def iterate_with_min_max_threshold(
    d: dict,
    min_val: Optional[Any] = None,
    max_val: Optional[Any] = None
) -> List[Tuple[Any, Any]]:
    """
    Iterates over items whose numeric or comparable values fall within [min_val, max_val].

    Args:
        d: Input dictionary.
        min_val: Minimum threshold inclusive (or None for no lower bound).
        max_val: Maximum threshold inclusive (or None for no upper bound).

    Returns:
        List of (key, value) tuples within specified bounds.
    """
    result = []
    for k, v in d.items():
        if min_val is not None and v < min_val:
            continue
        if max_val is not None and v > max_val:
            continue
        result.append((k, v))
    return result


# ─── Nested & Recursive Iteration ──────────────────────────────────────────────


def iterate_nested_dict(
    d: dict,
    parent_path: Tuple[str, ...] = ()
) -> Generator[Tuple[Tuple[str, ...], Any], None, None]:
    """
    Recursively iterates over a nested dictionary yielding key paths and leaf values.

    Args:
        d: Input dictionary (may contain nested dicts).
        parent_path: Tuple tracking parent key hierarchy (used internally).

    Yields:
        Tuples of (key_path_tuple, leaf_value).

    Example:
        d = {"a": {"b": 1, "c": 2}, "d": 3}
        list(iterate_nested_dict(d)) -> [(("a", "b"), 1), (("a", "c"), 2), (("d",), 3)]
    """
    for k, v in d.items():
        current_path = parent_path + (str(k),)
        if isinstance(v, dict):
            yield from iterate_nested_dict(v, current_path)
        else:
            yield current_path, v


def flatten_dict(d: dict, sep: str = ".") -> Dict[str, Any]:
    """
    Flattens a nested dictionary into a single-level dictionary with delimited keys.

    Args:
        d: Input nested dictionary.
        sep: Separator for joining key paths (default: ".").

    Returns:
        Flattened dictionary mapping key path strings to leaf values.

    Example:
        flatten_dict({"user": {"name": "Alice", "meta": {"age": 30}}})
        -> {"user.name": "Alice", "user.meta.age": 30}
    """
    return {sep.join(path): val for path, val in iterate_nested_dict(d)}


# ─── Index-based & Enumerated Iteration ───────────────────────────────────────


def iterate_with_index(d: dict, start: int = 0) -> List[Tuple[int, Any, Any]]:
    """
    Iterates over dictionary items yielding 0-based or start-based index alongside key and value.

    Args:
        d: Input dictionary.
        start: Starting index number (default: 0).

    Returns:
        List of (index, key, value) tuples.

    Example:
        iterate_with_index({"a": 10, "b": 20}, start=1) -> [(1, "a", 10), (2, "b", 20)]
    """
    return [(idx, k, v) for idx, (k, v) in enumerate(d.items(), start=start)]


def iterate_in_chunks(d: dict, chunk_size: int) -> Generator[Dict[Any, Any], None, None]:
    """
    Yields slices (chunks) of a dictionary as sub-dictionaries of fixed size.

    Args:
        d: Input dictionary.
        chunk_size: Maximum number of items per chunk.

    Yields:
        Sub-dictionaries of size <= chunk_size.

    Raises:
        ValueError: If chunk_size <= 0.

    Example:
        list(iterate_in_chunks({"a": 1, "b": 2, "c": 3, "d": 4}, 2))
        -> [{"a": 1, "b": 2}, {"c": 3, "d": 4}]
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    items = list(d.items())
    for i in range(0, len(items), chunk_size):
        yield dict(items[i : i + chunk_size])


# ─── Transformed Iteration & Dictionary Comprehensions ─────────────────────────


def transform_dict_values(d: dict, transform_fn: Callable[[Any], Any]) -> Dict[Any, Any]:
    """
    Iterates through dictionary and constructs a new dictionary with transformed values.

    Args:
        d: Input dictionary.
        transform_fn: Function to apply to each value.

    Returns:
        New dictionary with updated values.

    Example:
        transform_dict_values({"a": 1, "b": 2}, lambda v: v * 10) -> {"a": 10, "b": 20}
    """
    return {k: transform_fn(v) for k, v in d.items()}


def invert_dict_multi(d: dict) -> Dict[Any, List[Any]]:
    """
    Iterates through dictionary to invert keys and values, grouping duplicate values into lists.

    Args:
        d: Input dictionary.

    Returns:
        Inverted dictionary mapping each unique value to list of keys that had that value.

    Example:
        invert_dict_multi({"a": 1, "b": 2, "c": 1}) -> {1: ["a", "c"], 2: ["b"]}
    """
    inverted: Dict[Any, List[Any]] = {}
    for k, v in d.items():
        if v not in inverted:
            inverted[v] = []
        inverted[v].append(k)
    return inverted


# ─── Safe Mutation Iteration ──────────────────────────────────────────────────


def remove_matching_keys(d: dict, predicate: Callable[[Any, Any], bool]) -> dict:
    """
    Safely removes key-value pairs matching predicate during iteration without RuntimeError.

    Args:
        d: Dictionary to mutate.
        predicate: Function taking (key, value) returning True if item should be removed.

    Returns:
        Mutated dictionary d.

    Example:
        remove_matching_keys({"a": 1, "b": 2, "c": 3}, lambda k, v: v % 2 == 0) -> {"a": 1, "c": 3}
    """
    for k, v in list(d.items()):
        if predicate(k, v):
            del d[k]
    return d


def update_dict_in_place(d: dict, update_fn: Callable[[Any, Any], Any]) -> dict:
    """
    Modifies values in place by iterating over keys.

    Args:
        d: Dictionary to modify in place.
        update_fn: Function taking (key, value) returning new value.

    Returns:
        Mutated dictionary d.
    """
    for k in list(d.keys()):
        d[k] = update_fn(k, d[k])
    return d


# ─── Multi-Dictionary & Zip Iteration ─────────────────────────────────────────


def zip_iterate_dicts(
    d1: dict,
    d2: dict,
    combine_fn: Optional[Callable[[Any, Any], Any]] = None
) -> List[Tuple[Any, Any, Any]]:
    """
    Iterates over shared keys present in both dictionaries.

    Args:
        d1: First dictionary.
        d2: Second dictionary.
        combine_fn: Optional function to combine (val1, val2).

    Returns:
        List of (key, val1, val2) or (key, combined_val) tuples.

    Example:
        zip_iterate_dicts({"a": 1, "b": 2}, {"b": 20, "c": 30})
        -> [("b", 2, 20)]
    """
    shared_keys = [k for k in d1 if k in d2]
    result = []
    for k in shared_keys:
        v1, v2 = d1[k], d2[k]
        if combine_fn:
            result.append((k, combine_fn(v1, v2)))
        else:
            result.append((k, v1, v2))
    return result


def dict_difference_iterator(d1: dict, d2: dict) -> List[Tuple[str, Any, Any, Any]]:
    """
    Iterates over two dictionaries reporting structural and value differences.

    Args:
        d1: Original dictionary.
        d2: New dictionary.

    Returns:
        List of tuples: (change_type, key, val_in_d1, val_in_d2)
        where change_type is 'added', 'removed', 'modified', or 'unchanged'.
    """
    all_keys = sorted(set(d1.keys()) | set(d2.keys()), key=lambda x: str(x))
    diffs = []
    for k in all_keys:
        if k in d1 and k not in d2:
            diffs.append(("removed", k, d1[k], None))
        elif k not in d1 and k in d2:
            diffs.append(("added", k, None, d2[k]))
        elif d1[k] != d2[k]:
            diffs.append(("modified", k, d1[k], d2[k]))
        else:
            diffs.append(("unchanged", k, d1[k], d2[k]))
    return diffs






