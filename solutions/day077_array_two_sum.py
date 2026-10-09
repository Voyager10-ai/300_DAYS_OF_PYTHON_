# Day 77: Array Two Sum
#
# Problem:
#   Write a Python program / module implementing the Two Sum problem and its algorithmic variants.
#   Includes core hash map (O(n)) and brute force solvers, Two Sum II (sorted array two-pointer and binary search),
#   Two Sum Closest and Less Than K, dynamic TwoSum data structure design (LeetCode 170),
#   pair counting with multiplicity, 2D matrix Two Sum, algorithmic benchmarking and trace engine,
#   comprehensive unit test suite, and Java practice.

import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Two Sum Solvers (LeetCode 1) ─────────────────────────────────────


def two_sum_hash_map(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Finds two distinct indices (i, j) such that nums[i] + nums[j] == target using an O(n) hash map.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        Tuple of (i, j) with i < j, or None if no such pair exists.

    Raises:
        TypeError: If nums is not a list/tuple, contains non-integers, or target is not an int.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    seen: Dict[int, int] = {}
    for i, num in enumerate(nums):
        if not isinstance(num, int) or isinstance(num, bool):
            raise TypeError(f"Element at index {i} is not an integer: {num!r}")

        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i

    return None


def two_sum_brute_force(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Finds two indices such that nums[i] + nums[j] == target using an O(n^2) brute force search.
    Used for algorithmic comparison and baseline verification.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        Tuple of (i, j) with i < j, or None if no such pair exists.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    n = len(nums)
    for i in range(n):
        if not isinstance(nums[i], int) or isinstance(nums[i], bool):
            raise TypeError(f"Element at index {i} is not an integer: {nums[i]!r}")
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)

    return None


def two_sum_all_pairs(
    nums: List[int], target: int, unique_values_only: bool = False
) -> List[Tuple[int, int]]:
    """
    Finds all index pairs (i, j) with i < j where nums[i] + nums[j] == target.

    Args:
        nums: List of integers.
        target: Target sum.
        unique_values_only: If True, returns unique (val1, val2) pairs instead of index pairs.

    Returns:
        List of index pairs (i, j) or value pairs (val1, val2) sorted.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")

    index_pairs: List[Tuple[int, int]] = []
    val_map: Dict[int, List[int]] = {}

    for i, val in enumerate(nums):
        complement = target - val
        if complement in val_map:
            for prev_idx in val_map[complement]:
                index_pairs.append((prev_idx, i))
        if val not in val_map:
            val_map[val] = []
        val_map[val].append(i)

    if not unique_values_only:
        return index_pairs

    unique_vals: Set[Tuple[int, int]] = set()
    for i, j in index_pairs:
        v1, v2 = nums[i], nums[j]
        pair = (min(v1, v2), max(v1, v2))
        unique_vals.add(pair)

    return sorted(list(unique_vals))
