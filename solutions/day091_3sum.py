# Day 91: 3Sum (LeetCode 15 & Extensions)
#
# Problem:
#   Given an integer array nums, return all unique triplets [nums[i], nums[j], nums[k]]
#   such that i != j, i != k, j != k, and nums[i] + nums[j] + nums[k] == 0.
#   Notice that the solution set must not contain duplicate triplets.
#   Includes:
#     - Naive Brute Force O(n^3) with set deduplication
#     - Hash-Set 2Sum reduction O(n^2) time, O(n) auxiliary space
#     - Optimal Sorted Two-Pointer O(n^2) time, O(1) extra space + pruning
#     - LeetCode 15 Solution class
#     - Extensions: 3Sum Closest (LC 16), 3Sum Smaller (LC 259), and generalized kSum
#     - Step-by-step Two-Pointer trace visualizer
#     - Performance benchmark comparing all algorithms
#     - Comprehensive unit tests and Java practice code

import time
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional


# ─── 1. Naive Brute Force & Hash-Set 3Sum Implementations ─────────────────────


def three_sum_brute_force(nums: List[int], target: int = 0) -> List[List[int]]:
    """
    Finds all unique triplets summing to target using exhaustive O(n^3) triple loops.

    Time Complexity: O(n^3).
    Space Complexity: O(k) where k is the number of unique valid triplets stored in a set.

    Args:
        nums: Input list of integers.
        target: Target triplet sum (defaults to 0).

    Returns:
        Sorted list of unique sorted triplets.

    Raises:
        TypeError: If nums is not a list or contains non-integers.
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")
    for idx, val in enumerate(nums):
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(f"Element at index {idx} must be an integer, got {type(val).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"target must be an integer, got {type(target).__name__}")

    n = len(nums)
    if n < 3:
        return []

    seen: Set[Tuple[int, int, int]] = set()
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == target:
                    triplet = tuple(sorted((nums[i], nums[j], nums[k])))
                    seen.add(triplet)  # type: ignore

    return [list(t) for t in sorted(seen)]


def three_sum_hashset(nums: List[int], target: int = 0) -> List[List[int]]:
    """
    Finds all unique triplets summing to target by reducing 3Sum to 2Sum via a hash set.

    Time Complexity: O(n^2) average.
    Space Complexity: O(n) for the inner lookup hash set and deduplication set.

    Args:
        nums: Input list of integers.
        target: Target triplet sum (defaults to 0).

    Returns:
        Sorted list of unique sorted triplets.
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")
    if len(nums) < 3:
        return []

    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    res: Set[Tuple[int, int, int]] = set()

    for i in range(n - 2):
        # Skip duplicate anchors
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue
        seen: Set[int] = set()
        for j in range(i + 1, n):
            complement = target - sorted_nums[i] - sorted_nums[j]
            if complement in seen:
                res.add((sorted_nums[i], complement, sorted_nums[j]))
            seen.add(sorted_nums[j])

    return [list(t) for t in sorted(res)]


def three_sum_with_metrics(
    nums: List[int],
    target: int = 0,
) -> Tuple[List[List[int]], Dict[str, Any]]:
    """
    Solves 3Sum using the hash-set approach while recording operation statistics.

    Args:
        nums: Input list of integers.
        target: Target triplet sum.

    Returns:
        Tuple of (triplets, metrics_dict).
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")

    t0 = time.perf_counter()
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    res: Set[Tuple[int, int, int]] = set()
    hash_lookups = 0

    for i in range(n - 2):
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue
        seen: Set[int] = set()
        for j in range(i + 1, n):
            complement = target - sorted_nums[i] - sorted_nums[j]
            hash_lookups += 1
            if complement in seen:
                res.add((sorted_nums[i], complement, sorted_nums[j]))
            seen.add(sorted_nums[j])

    elapsed = time.perf_counter() - t0
    triplets = [list(t) for t in sorted(res)]
    metrics = {
        "input_length": n,
        "target": target,
        "triplets_found": len(triplets),
        "hash_lookups": hash_lookups,
        "time_seconds": elapsed,
        "algorithm": "Hash-Set 2Sum Reduction O(n^2)",
    }
    return (triplets, metrics)



# ─── 2. Optimal Sorted Two-Pointer 3Sum & LeetCode Solution ───────────────────


def three_sum_two_pointer(nums: List[int], target: int = 0) -> List[List[int]]:
    """
    Finds all unique triplets summing to target using sorted two-pointer technique.

    Uses early-exit pruning bounds:
      1. If nums[i] + nums[i+1] + nums[i+2] > target -> break (all remaining sums exceed target)
      2. If nums[i] + nums[-2] + nums[-1] < target -> continue (anchor too small)

    Time Complexity: O(n^2) after O(n log n) sort.
    Space Complexity: O(1) auxiliary space (excluding output list and sort buffer).

    Args:
        nums: Input list of integers.
        target: Target triplet sum (defaults to 0).

    Returns:
        List of unique sorted triplets summing to target.
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")
    for idx, val in enumerate(nums):
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(f"Element at index {idx} must be an integer, got {type(val).__name__}")

    n = len(nums)
    if n < 3:
        return []

    arr = sorted(nums)
    result: List[List[int]] = []

    for i in range(n - 2):
        # Skip duplicate anchor values
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        # Lower-bound pruning
        if arr[i] + arr[i + 1] + arr[i + 2] > target:
            break

        # Upper-bound pruning
        if arr[i] + arr[n - 2] + arr[n - 1] < target:
            continue

        left, right = i + 1, n - 1
        while left < right:
            curr_sum = arr[i] + arr[left] + arr[right]
            if curr_sum < target:
                left += 1
            elif curr_sum > target:
                right -= 1
            else:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicate left and right values
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1

    return result


class Solution:
    """LeetCode 15: 3Sum solution wrapper."""

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """Finds all unique triplets in nums which give the sum of zero."""
        return three_sum_two_pointer(nums, target=0)
