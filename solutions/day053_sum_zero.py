# Day 53: Sum Zero
#
# Problem:
#   Write a Python program to find all unique triplets in an array that sum to zero (3Sum).
#   Includes 2Sum, generalized K-Sum, continuous subarray sum zero, 3Sum closest,
#   subset sum zero, matrix balance analyzer, unit tests, and Java practice.

import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union, Callable


# ─── 1. Core 3Sum & 2Sum Zero Algorithms ───────────────────────────────────────


def two_sum_zero(nums: List[int]) -> List[Tuple[int, int]]:
    """
    Finds all unique pairs (a, b) in the list such that a + b == 0.

    Args:
        nums: List of integers.

    Returns:
        Sorted list of unique integer pairs summing to 0.
    """
    if not isinstance(nums, list):
        raise TypeError(f"Expected list input, got {type(nums).__name__}")

    seen: Set[int] = set()
    pairs: Set[Tuple[int, int]] = set()

    for num in nums:
        target = -num
        if target in seen:
            pair = (min(num, target), max(num, target))
            pairs.add(pair)
        seen.add(num)

    return sorted(list(pairs))


def three_sum(nums: List[int]) -> List[Tuple[int, int, int]]:
    """
    Finds all unique triplets [a, b, c] in the list such that a + b + c == 0 using O(N^2) two-pointer technique.

    Args:
        nums: List of integers.

    Returns:
        Sorted list of unique 3-element tuples summing to 0.
    """
    if not isinstance(nums, list):
        raise TypeError(f"Expected list input, got {type(nums).__name__}")

    if len(nums) < 3:
        return []

    sorted_nums = sorted(nums)
    triplets: List[Tuple[int, int, int]] = []
    n = len(sorted_nums)

    for i in range(n - 2):
        # Skip duplicate first elements
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue

        # Pruning optimization
        if sorted_nums[i] + sorted_nums[i + 1] + sorted_nums[i + 2] > 0:
            break
        if sorted_nums[i] + sorted_nums[n - 2] + sorted_nums[n - 1] < 0:
            continue

        left = i + 1
        right = n - 1

        while left < right:
            current_sum = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]

            if current_sum == 0:
                triplets.append((sorted_nums[i], sorted_nums[left], sorted_nums[right]))

                # Skip duplicates for left and right
                while left < right and sorted_nums[left] == sorted_nums[left + 1]:
                    left += 1
                while left < right and sorted_nums[right] == sorted_nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1

    return triplets


# ─── 2. Generalized K-Sum & 4Sum Zero Solver ───────────────────────────────────


def k_sum_zero(nums: List[int], k: int = 4, target: int = 0) -> List[Tuple[int, ...]]:
    """
    Generalized K-Sum algorithm finding all unique K-tuples that sum to target.

    Args:
        nums: List of integers.
        k: Number of elements in tuple (k >= 2).
        target: Target sum (default 0).

    Returns:
        List of unique k-tuples summing to target.
    """
    if not isinstance(nums, list):
        raise TypeError(f"Expected list input, got {type(nums).__name__}")
    if k < 2:
        raise ValueError(f"k must be >= 2, got {k}")

    nums_sorted = sorted(nums)

    def helper(start: int, k_val: int, target_val: int) -> List[List[int]]:
        res: List[List[int]] = []
        n = len(nums_sorted)

        if start >= n:
            return res

        # Average value bounds check
        average_value = target_val // k_val
        if nums_sorted[start] > average_value or average_value > nums_sorted[-1]:
            return res

        if k_val == 2:
            left = start
            right = n - 1
            while left < right:
                s = nums_sorted[left] + nums_sorted[right]
                if s == target_val:
                    res.append([nums_sorted[left], nums_sorted[right]])
                    while left < right and nums_sorted[left] == nums_sorted[left + 1]:
                        left += 1
                    while left < right and nums_sorted[right] == nums_sorted[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target_val:
                    left += 1
                else:
                    right -= 1
            return res

        for i in range(start, n - k_val + 1):
            if i > start and nums_sorted[i] == nums_sorted[i - 1]:
                continue
            sub_results = helper(i + 1, k_val - 1, target_val - nums_sorted[i])
            for sub in sub_results:
                res.append([nums_sorted[i]] + sub)

        return res

    results = helper(0, k, target)
    return [tuple(r) for r in results]


def four_sum_zero(nums: List[int]) -> List[Tuple[int, int, int, int]]:
    """Convenience function for 4Sum Zero."""
    return [tuple(t) for t in k_sum_zero(nums, k=4, target=0)]  # type: ignore


# ─── 3. Continuous Subarray Sum Zero Finder ────────────────────────────────────


def subarray_sum_zero(nums: List[int]) -> List[Tuple[int, int]]:
    """
    Finds index ranges (start_idx, end_idx) of all contiguous subarrays that sum to zero.
    Uses O(N) prefix sum hash map index tracking.

    Args:
        nums: List of integers.

    Returns:
        List of (start_idx, end_idx) inclusive index ranges summing to 0.
    """
    if not isinstance(nums, list):
        raise TypeError(f"Expected list input, got {type(nums).__name__}")

    prefix_map: Dict[int, List[int]] = {0: [-1]}
    current_sum = 0
    results: List[Tuple[int, int]] = []

    for i, num in enumerate(nums):
        current_sum += num
        if current_sum in prefix_map:
            for prev_idx in prefix_map[current_sum]:
                results.append((prev_idx + 1, i))
            prefix_map[current_sum].append(i)
        else:
            prefix_map[current_sum] = [i]

    return results


def has_zero_sum_subarray(nums: List[int]) -> bool:
    """
    Checks if list contains at least one contiguous subarray with zero sum.

    Args:
        nums: List of integers.

    Returns:
        True if zero sum subarray exists, False otherwise.
    """
    if not isinstance(nums, list):
        raise TypeError(f"Expected list input, got {type(nums).__name__}")

    seen_sums: Set[int] = {0}
    current_sum = 0
    for num in nums:
        current_sum += num
        if current_sum in seen_sums:
            return True
        seen_sums.add(current_sum)
    return False


