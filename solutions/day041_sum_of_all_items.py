# Day 41: Sum of All Items
#
# Problem:
#   Write a Python program to calculate the sum of all items (values/keys/containers)
#   in a dictionary, including basic numeric sum, safe type conversion, conditional filtering,
#   recursive nested dictionary summation, container list aggregation, weighted sums,
#   functional reductions, statistical summaries, and robust unit testing.

import sys
import unittest
import functools
import operator
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Union


# ─── 1. Core Dictionary Summation ─────────────────────────────────────────────


def sum_dict_values(d: Dict[Any, Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of all numeric values in a dictionary.

    Args:
        d: Input dictionary containing numeric values.

    Returns:
        Total sum of values (int or float).

    Example:
        sum_dict_values({"a": 100, "b": 200, "c": 300}) -> 600
    """
    if not d:
        return 0
    return sum(v for v in d.values() if isinstance(v, (int, float)) and not isinstance(v, bool))


def sum_dict_keys(d: Dict[Union[int, float], Any]) -> Union[int, float]:
    """
    Calculates the sum of all numeric keys in a dictionary.

    Args:
        d: Input dictionary with numeric keys.

    Returns:
        Total sum of keys (int or float).

    Example:
        sum_dict_keys({10: "apple", 20: "banana", 30: "cherry"}) -> 60
    """
    if not d:
        return 0
    return sum(k for k in d.keys() if isinstance(k, (int, float)) and not isinstance(k, bool))


def sum_dict_keys_and_values(d: Dict[Union[int, float], Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of all numeric keys and numeric values combined in a dictionary.

    Args:
        d: Input dictionary with numeric keys and values.

    Returns:
        Total sum of keys and values.

    Example:
        sum_dict_keys_and_values({1: 10, 2: 20, 3: 30}) -> 66
    """
    total = 0
    for k, v in d.items():
        if isinstance(k, (int, float)) and not isinstance(k, bool):
            total += k
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v
    return total


# ─── 2. Safe Type Conversion & Robust Summation ──────────────────────────────


def sum_dict_values_safe(d: Dict[Any, Any], default_val: float = 0.0) -> float:
    """
    Safely sums values in a dictionary by attempting to parse string representation
    of numbers into floats. Ignores invalid non-numeric entries gracefully.

    Args:
        d: Input dictionary with potentially mixed types (ints, floats, numeric strings).
        default_val: Default starting accumulator value.

    Returns:
        Total accumulated float sum.

    Example:
        sum_dict_values_safe({"a": 10, "b": "20.5", "c": "invalid", "d": 5}) -> 35.5
    """
    total = default_val
    for v in d.values():
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)):
            total += v
        elif isinstance(v, str):
            try:
                total += float(v)
            except ValueError:
                pass
    return total


def extract_numeric_values(d: Dict[Any, Any]) -> List[Union[int, float]]:
    """
    Extracts all valid numeric values from a dictionary into a list.

    Args:
        d: Input dictionary.

    Returns:
        List of numeric values.

    Example:
        extract_numeric_values({"a": 10, "b": "hello", "c": 3.14}) -> [10, 3.14]
    """
    nums = []
    for v in d.values():
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)):
            nums.append(v)
        elif isinstance(v, str):
            try:
                val = float(v)
                nums.append(int(val) if val.is_integer() else val)
            except ValueError:
                pass
    return nums


# ─── 3. Conditional & Filtered Summation ──────────────────────────────────────


def sum_dict_values_conditional(
    d: Dict[Any, Any], predicate: Callable[[Any, Any], bool]
) -> Union[int, float]:
    """
    Sums values in a dictionary that satisfy a predicate function `predicate(key, value)`.

    Args:
        d: Input dictionary.
        predicate: Callable taking (key, value) and returning bool.

    Returns:
        Sum of filtered numeric values.

    Example:
        sum_dict_values_conditional({"a": 10, "b": 25, "c": 30}, lambda k, v: v > 15) -> 55
    """
    total = 0
    for k, v in d.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if predicate(k, v):
                total += v
    return total


def sum_even_values(d: Dict[Any, int]) -> int:
    """
    Sums only even integer values in a dictionary.

    Args:
        d: Input dictionary with integer values.

    Returns:
        Sum of even values.

    Example:
        sum_even_values({"a": 1, "b": 2, "c": 3, "d": 4}) -> 6
    """
    return sum(v for v in d.values() if isinstance(v, int) and not isinstance(v, bool) and v % 2 == 0)


def sum_odd_values(d: Dict[Any, int]) -> int:
    """
    Sums only odd integer values in a dictionary.

    Args:
        d: Input dictionary with integer values.

    Returns:
        Sum of odd values.

    Example:
        sum_odd_values({"a": 1, "b": 2, "c": 3, "d": 4}) -> 4
    """
    return sum(v for v in d.values() if isinstance(v, int) and not isinstance(v, bool) and v % 2 != 0)


def sum_values_above_threshold(d: Dict[Any, Union[int, float]], threshold: Union[int, float]) -> Union[int, float]:
    """
    Sums values strictly greater than a threshold value.

    Args:
        d: Input dictionary.
        threshold: Numeric threshold cut-off.

    Returns:
        Sum of values > threshold.

    Example:
        sum_values_above_threshold({"a": 5, "b": 15, "c": 25}, 10) -> 40
    """
    return sum(v for v in d.values() if isinstance(v, (int, float)) and not isinstance(v, bool) and v > threshold)


# ─── 4. Recursive Nested Dictionary Summation ─────────────────────────────────


def sum_nested_dict_values(d: Dict[Any, Any]) -> Union[int, float]:
    """
    Recursively sums all numeric values in an arbitrarily nested dictionary structure.

    Args:
        d: Input nested dictionary.

    Returns:
        Total sum of all nested numeric values.

    Example:
        nested = {"a": 10, "b": {"c": 20, "d": {"e": 30}}}
        sum_nested_dict_values(nested) -> 60
    """
    total = 0
    for v in d.values():
        if isinstance(v, dict):
            total += sum_nested_dict_values(v)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v
    return total


def sum_nested_dict_by_key(d: Dict[Any, Any], target_key: Any) -> Union[int, float]:
    """
    Recursively sums values associated with a specific `target_key` across a nested dictionary.

    Args:
        d: Input nested dictionary.
        target_key: Key name to search and sum values for.

    Returns:
        Sum of values corresponding to target_key.

    Example:
        d = {"a": {"price": 10}, "b": {"price": 20, "tax": 5}}
        sum_nested_dict_by_key(d, "price") -> 30
    """
    total = 0
    for k, v in d.items():
        if k == target_key and isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v
        if isinstance(v, dict):
            total += sum_nested_dict_by_key(v, target_key)
    return total


def sum_nested_dict_depth_weighted(d: Dict[Any, Any], current_depth: int = 1) -> float:
    """
    Sums values in a nested dictionary where values are multiplied by their nesting depth level.

    Args:
        d: Input nested dictionary.
        current_depth: Current nesting depth level (starts at 1).

    Returns:
        Depth-weighted total sum.

    Example:
        d = {"a": 10, "b": {"c": 20}}  # 10*1 + 20*2 = 50
        sum_nested_dict_depth_weighted(d) -> 50
    """
    total = 0.0
    for v in d.values():
        if isinstance(v, dict):
            total += sum_nested_dict_depth_weighted(v, current_depth + 1)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            total += v * current_depth
    return total


# ─── 5. Container & Collection Value Summation ────────────────────────────────


def sum_dict_list_values(d: Dict[Any, Union[List[Union[int, float]], Tuple[Union[int, float], ...]]]) -> Union[int, float]:
    """
    Sums all elements across dictionary values that are lists or tuples of numbers.

    Args:
        d: Input dictionary with list/tuple values.

    Returns:
        Total sum of all elements in all container values.

    Example:
        sum_dict_list_values({"a": [1, 2, 3], "b": [4, 5]}) -> 15
    """
    total = 0
    for container in d.values():
        if isinstance(container, (list, tuple, set)):
            for elem in container:
                if isinstance(elem, (int, float)) and not isinstance(elem, bool):
                    total += elem
    return total


def flatten_and_sum_all_containers(d: Dict[Any, Any]) -> Union[int, float]:
    """
    Recursively flattens mixed scalars, lists, tuples, sets, and nested dicts into a single total sum.

    Args:
        d: Input dictionary with arbitrary mixed structure.

    Returns:
        Total sum of all numeric values anywhere in the structure.

    Example:
        d = {"a": 10, "b": [1, 2, {"c": 3}], "d": (4, 5)} -> 25
    """
    total = 0

    def _traverse(val: Any):
        nonlocal total
        if isinstance(val, bool):
            return
        if isinstance(val, (int, float)):
            total += val
        elif isinstance(val, dict):
            for item in val.values():
                _traverse(item)
        elif isinstance(val, (list, tuple, set)):
            for item in val:
                _traverse(item)

    _traverse(d)
    return total


# ─── 6. Weighted Sum, Average, & Statistical Aggregations ────────────────────


def weighted_sum_dict(
    d: Dict[Any, Union[int, float]], weights: Dict[Any, Union[int, float]]
) -> float:
    """
    Computes a weighted sum of dictionary values based on a corresponding weights dictionary.

    Args:
        d: Input dictionary with values to weight.
        weights: Dictionary mapping keys to numeric weight multipliers.

    Returns:
        Weighted total sum sum(d[k] * weights[k]).

    Example:
        weighted_sum_dict({"exam1": 80, "exam2": 90}, {"exam1": 0.4, "exam2": 0.6}) -> 86.0
    """
    total = 0.0
    for k, v in d.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool) and k in weights:
            w = weights[k]
            if isinstance(w, (int, float)) and not isinstance(w, bool):
                total += v * w
    return total


def average_dict_values(d: Dict[Any, Union[int, float]]) -> float:
    """
    Computes the arithmetic mean (average) of all numeric values in a dictionary.

    Args:
        d: Input dictionary.

    Returns:
        Mean average float, or 0.0 if empty/no valid numbers.

    Example:
        average_dict_values({"a": 10, "b": 20, "c": 30}) -> 20.0
    """
    nums = [v for v in d.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not nums:
        return 0.0
    return sum(nums) / len(nums)


def summary_statistics_dict(d: Dict[Any, Union[int, float]]) -> Dict[str, Union[int, float]]:
    """
    Returns summary statistics for numeric values in a dictionary.

    Args:
        d: Input dictionary.

    Returns:
        Dictionary with keys: 'sum', 'count', 'mean', 'min', 'max'.

    Example:
        summary_statistics_dict({"a": 10, "b": 20, "c": 30})
        -> {"sum": 60, "count": 3, "mean": 20.0, "min": 10, "max": 30}
    """
    nums = [v for v in d.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not nums:
        return {"sum": 0, "count": 0, "mean": 0.0, "min": 0, "max": 0}

    s = sum(nums)
    return {
        "sum": s,
        "count": len(nums),
        "mean": s / len(nums),
        "min": min(nums),
        "max": max(nums),
    }


# ─── 7. Functional Reduction & Cumulative Running Sums ───────────────────────


def sum_dict_functools_reduce(d: Dict[Any, Union[int, float]]) -> Union[int, float]:
    """
    Computes total sum of dictionary values using `functools.reduce` and `operator.add`.

    Args:
        d: Input dictionary with numeric values.

    Returns:
        Total sum.

    Example:
        sum_dict_functools_reduce({"a": 10, "b": 20, "c": 30}) -> 60
    """
    nums = [v for v in d.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not nums:
        return 0
    return functools.reduce(operator.add, nums, 0)


def running_sum_dict(d: Dict[Any, Union[int, float]]) -> Dict[Any, Union[int, float]]:
    """
    Computes a cumulative running sum dictionary where each key maps to the running total sum so far.

    Args:
        d: Input dictionary with numeric values.

    Returns:
        Dictionary mapping original keys to cumulative running sums.

    Example:
        running_sum_dict({"a": 10, "b": 20, "c": 30}) -> {"a": 10, "b": 30, "c": 60}
    """
    result = {}
    current_total = 0
    for k, v in d.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            current_total += v
            result[k] = current_total
        else:
            result[k] = current_total
    return result



# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestSumOfAllItems(unittest.TestCase):
    def test_core_summation(self):
        self.assertEqual(sum_dict_values({"a": 10, "b": 20, "c": 30}), 60)
        self.assertEqual(sum_dict_keys({10: "x", 20: "y"}), 30)
        self.assertEqual(sum_dict_keys_and_values({1: 10, 2: 20}), 33)
        self.assertEqual(sum_dict_values({}), 0)

    def test_safe_summation(self):
        d = {"a": 10, "b": "20.5", "c": "invalid", "d": True}
        self.assertEqual(sum_dict_values_safe(d), 30.5)
        self.assertEqual(extract_numeric_values(d), [10, 20.5])

    def test_conditional_summation(self):
        d = {"a": 5, "b": 15, "c": 20, "d": 3}
        self.assertEqual(sum_even_values(d), 20)
        self.assertEqual(sum_odd_values(d), 23)
        self.assertEqual(sum_values_above_threshold(d, 10), 35)
        self.assertEqual(sum_dict_values_conditional(d, lambda k, v: k in ("a", "c")), 25)


    def test_nested_summation(self):
        nested = {"a": 10, "b": {"c": 20, "d": {"e": 30, "price": 100}}}
        self.assertEqual(sum_nested_dict_values(nested), 160)
        self.assertEqual(sum_nested_dict_by_key(nested, "price"), 100)
        self.assertEqual(sum_nested_dict_depth_weighted({"a": 10, "b": {"c": 20}}), 50.0)

    def test_container_summation(self):
        d = {"a": [1, 2, 3], "b": (4, 5)}
        self.assertEqual(sum_dict_list_values(d), 15)

        mixed = {"a": 10, "b": [1, 2, {"c": 3}], "d": (4, 5)}
        self.assertEqual(flatten_and_sum_all_containers(mixed), 25)

    def test_weighted_and_stats(self):
        scores = {"exam1": 80, "exam2": 90}
        weights = {"exam1": 0.4, "exam2": 0.6}
        self.assertAlmostEqual(weighted_sum_dict(scores, weights), 86.0)
        self.assertEqual(average_dict_values({"a": 10, "b": 20, "c": 30}), 20.0)

        stats = summary_statistics_dict({"a": 10, "b": 20, "c": 30})
        self.assertEqual(stats["sum"], 60)
        self.assertEqual(stats["count"], 3)
        self.assertEqual(stats["min"], 10)
        self.assertEqual(stats["max"], 30)

    def test_reduce_and_running_sum(self):
        d = {"a": 10, "b": 20, "c": 30}
        self.assertEqual(sum_dict_functools_reduce(d), 60)
        self.assertEqual(running_sum_dict(d), {"a": 10, "b": 30, "c": 60})







