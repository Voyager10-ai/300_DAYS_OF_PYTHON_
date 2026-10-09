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


# ─── 2. Two Sum II - Sorted Array Solvers (LeetCode 167) ─────────────────────


def two_sum_two_pointers(
    nums: List[int], target: int, one_indexed: bool = False
) -> Optional[Tuple[int, int]]:
    """
    Finds two indices in a sorted array that sum to target using the two-pointer technique.
    Achieves O(n) time and O(1) auxiliary space (LeetCode 167).

    Args:
        nums: Sorted list of integers in non-decreasing order.
        target: Target sum.
        one_indexed: If True, returns 1-based indices (as required by LeetCode 167).

    Returns:
        Tuple of (index1, index2) or None if no pair exists.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If nums is not sorted.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    n = len(nums)
    if n < 2:
        return None

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        if i > 0 and x < nums[i - 1]:
            raise ValueError(f"Array must be sorted in non-decreasing order: {nums[i-1]} > {x}")

    left, right = 0, n - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            offset = 1 if one_indexed else 0
            return (left + offset, right + offset)
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return None


def two_sum_binary_search(
    nums: List[int], target: int, one_indexed: bool = False
) -> Optional[Tuple[int, int]]:
    """
    Finds two indices in a sorted array using binary search for each complement.
    Runs in O(n log n) time and O(1) auxiliary space.

    Args:
        nums: Sorted list of integers.
        target: Target sum.
        one_indexed: If True, returns 1-based indices.

    Returns:
        Tuple of (index1, index2) or None.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If nums is not sorted.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    n = len(nums)
    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        if i > 0 and x < nums[i - 1]:
            raise ValueError(f"nums must be sorted: {nums[i-1]} > {x}")

    offset = 1 if one_indexed else 0

    for i in range(n - 1):
        complement = target - nums[i]
        # Binary search for complement in nums[i + 1:]
        low = i + 1
        high = n - 1
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == complement:
                return (i + offset, mid + offset)
            elif nums[mid] < complement:
                low = mid + 1
            else:
                high = mid - 1

    return None


# ─── 3. Two Sum Closest & Inequality Variants ────────────────────────────────


def two_sum_closest(nums: List[int], target: int) -> Tuple[int, int, int]:
    """
    Finds two elements whose sum is closest to the given target.

    Args:
        nums: List of integers (length >= 2).
        target: Target integer.

    Returns:
        Tuple of (val1, val2, closest_sum) where val1 <= val2.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If nums has fewer than 2 elements.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")
    if len(nums) < 2:
        raise ValueError("nums must have at least 2 elements")

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")

    sorted_nums = sorted(nums)
    left, right = 0, len(sorted_nums) - 1
    best_pair = (sorted_nums[left], sorted_nums[right])
    best_diff = abs(sorted_nums[left] + sorted_nums[right] - target)

    while left < right:
        curr_sum = sorted_nums[left] + sorted_nums[right]
        diff = abs(curr_sum - target)

        if diff < best_diff:
            best_diff = diff
            best_pair = (sorted_nums[left], sorted_nums[right])

        if curr_sum == target:
            return (sorted_nums[left], sorted_nums[right], target)
        elif curr_sum < target:
            left += 1
        else:
            right -= 1

    return (best_pair[0], best_pair[1], best_pair[0] + best_pair[1])


def two_sum_less_than_k(nums: List[int], k: int) -> Optional[Tuple[int, int, int]]:
    """
    Finds two elements whose sum is strictly less than k, but as close to k as possible (LeetCode 1099).

    Args:
        nums: List of integers.
        k: Upper limit bound (sum < k).

    Returns:
        Tuple of (val1, val2, max_sum) with val1 <= val2, or None if no pair sums to < k.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")

    if len(nums) < 2:
        return None

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")

    sorted_nums = sorted(nums)
    left, right = 0, len(sorted_nums) - 1
    best_sum: Optional[int] = None
    best_pair: Optional[Tuple[int, int]] = None

    while left < right:
        curr_sum = sorted_nums[left] + sorted_nums[right]
        if curr_sum < k:
            if best_sum is None or curr_sum > best_sum:
                best_sum = curr_sum
                best_pair = (sorted_nums[left], sorted_nums[right])
            left += 1
        else:
            right -= 1

    if best_pair is not None and best_sum is not None:
        return (best_pair[0], best_pair[1], best_sum)
    return None


