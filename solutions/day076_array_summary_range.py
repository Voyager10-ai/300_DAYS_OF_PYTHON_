# Day 76: Array Summary Range
#
# Problem:
#   Write a Python program / module to compute summary ranges for integer arrays (LeetCode 228 & extensions).
#   Includes core summary range solvers, interval generators, step & gap-tolerant algorithms,
#   reverse array reconstruction, missing range solvers (LeetCode 163), range analytics engine,
#   batch/categorized sequence processors, overlapping range mergers, unit test suite, and Java practice.

from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Summary Ranges Solvers & Interval Generators ────────────────────


def summary_ranges(nums: List[int]) -> List[str]:
    """
    Computes summary ranges for a sorted unique integer array (LeetCode 228).

    For consecutive numbers [a, a+1, ..., b], outputs "a->b" if a != b, or "a" if a == b.

    Args:
        nums: Sorted list of unique integers.

    Returns:
        List of range strings representing contiguous sequences.

    Raises:
        TypeError: If nums is not a list/tuple or contains non-integers.
        ValueError: If nums is not sorted or contains duplicates.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")

    n = len(nums)
    if n == 0:
        return []

    # Validate elements, sorting, and uniqueness
    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        if i > 0:
            if x < nums[i - 1]:
                raise ValueError(f"Array is not sorted in non-decreasing order: {nums[i-1]} > {x}")
            if x == nums[i - 1]:
                raise ValueError(f"Array contains duplicate element {x} at index {i}")

    result: List[str] = []
    start = nums[0]

    for i in range(1, n):
        if nums[i] != nums[i - 1] + 1:
            end = nums[i - 1]
            if start == end:
                result.append(str(start))
            else:
                result.append(f"{start}->{end}")
            start = nums[i]

    # Process final interval
    end = nums[-1]
    if start == end:
        result.append(str(start))
    else:
        result.append(f"{start}->{end}")

    return result


def summary_ranges_intervals(nums: List[int]) -> List[Tuple[int, int]]:
    """
    Computes summary ranges as integer interval tuples (start, end) inclusive.

    Args:
        nums: Sorted list of unique integers.

    Returns:
        List of (start, end) tuples representing contiguous ranges.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If nums is not sorted or has duplicates.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")

    n = len(nums)
    if n == 0:
        return []

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        if i > 0 and x <= nums[i - 1]:
            raise ValueError(f"Elements must be strictly increasing: {nums[i-1]} >= {x}")

    intervals: List[Tuple[int, int]] = []
    start = nums[0]

    for i in range(1, n):
        if nums[i] != nums[i - 1] + 1:
            intervals.append((start, nums[i - 1]))
            start = nums[i]

    intervals.append((start, nums[-1]))
    return intervals


def summary_ranges_unsorted(nums: List[int]) -> List[str]:
    """
    Computes summary ranges for an arbitrary list of integers by sorting
    and removing duplicates first.

    Args:
        nums: List of integers (can be unsorted and have duplicates).

    Returns:
        List of range strings.

    Raises:
        TypeError: If nums is not a list or contains non-integers.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")

    if not nums:
        return []

    unique_sorted = sorted(set(nums))
    return summary_ranges(unique_sorted)
