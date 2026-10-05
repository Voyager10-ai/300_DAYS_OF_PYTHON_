# Day 73: Array Merge Intervals
#
# Problem:
#   Write a Python program / module to merge overlapping intervals in a collection of intervals.
#   Includes core interval merging/sorting, interval insertion into sorted lists, intersection/gap extractors,
#   interval metrics engine, batch processors, ASCII visualization formatters, unit test suite, and Java practice code.

import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Interval Merging & Sorting Algorithms ───────────────────────────


def is_overlapping(
    int1: Union[List[int], Tuple[int, int]], int2: Union[List[int], Tuple[int, int]], allow_adjacent: bool = False
) -> bool:
    """
    Checks whether two intervals overlap.

    Args:
        int1: First interval [start, end].
        int2: Second interval [start, end].
        allow_adjacent: If True, treats touching endpoints (e.g. [1, 3] and [3, 5]) as overlapping/mergeable.

    Returns:
        True if intervals overlap (or touch if allow_adjacent=True), False otherwise.

    Raises:
        TypeError: If inputs are not list or tuple of length 2.
        ValueError: If start > end for either interval.
    """
    if not (isinstance(int1, (list, tuple)) and len(int1) == 2):
        raise TypeError(f"Expected 2-element sequence for int1, got {type(int1).__name__}")
    if not (isinstance(int2, (list, tuple)) and len(int2) == 2):
        raise TypeError(f"Expected 2-element sequence for int2, got {type(int2).__name__}")

    s1, e1 = int1[0], int1[1]
    s2, e2 = int2[0], int2[1]

    if s1 > e1:
        raise ValueError(f"Invalid interval: start {s1} > end {e1}")
    if s2 > e2:
        raise ValueError(f"Invalid interval: start {s2} > end {e2}")

    if allow_adjacent:
        return max(s1, s2) <= min(e1, e2)
    return max(s1, s2) < min(e1, e2) or (s1 == s2 and e1 == e2)


def merge_intervals(
    intervals: List[Union[List[int], Tuple[int, int]]], merge_adjacent: bool = True
) -> List[List[int]]:
    """
    Sorts and merges all overlapping (and optionally adjacent) intervals.

    Args:
        intervals: List of interval pairs [start, end].
        merge_adjacent: If True, merges touching intervals like [1, 3] and [3, 5] into [1, 5].

    Returns:
        New list of merged interval pairs [start, end].

    Raises:
        TypeError: If intervals is not a list/tuple or elements are invalid.
        ValueError: If any interval has start > end.
    """
    if not isinstance(intervals, (list, tuple)):
        raise TypeError(f"Expected list or tuple of intervals, got {type(intervals).__name__}")
    if not intervals:
        return []

    # Validate and convert to list of [start, end]
    clean_intervals: List[List[int]] = []
    for item in intervals:
        if not (isinstance(item, (list, tuple)) and len(item) == 2):
            raise TypeError(f"Each interval must be a 2-element sequence, got {item}")
        s, e = item[0], item[1]
        if s > e:
            raise ValueError(f"Invalid interval: start {s} > end {e}")
        clean_intervals.append([s, e])

    # Sort intervals by start time
    sorted_intervals = sorted(clean_intervals, key=lambda x: x[0])
    merged: List[List[int]] = []

    for curr in sorted_intervals:
        if not merged:
            merged.append(curr)
        else:
            prev = merged[-1]
            # Check overlap or adjacency
            if merge_adjacent:
                should_merge = curr[0] <= prev[1]
            else:
                should_merge = curr[0] < prev[1]

            if should_merge:
                prev[1] = max(prev[1], curr[1])
            else:
                merged.append(curr)

    return merged


# ─── 2. Interval Insertion & Point Query Search ──────────────────────────────


def insert_interval(
    intervals: List[Union[List[int], Tuple[int, int]]], new_interval: Union[List[int], Tuple[int, int]]
) -> List[List[int]]:
    """
    Inserts a new interval into a list of sorted non-overlapping intervals and merges if necessary.

    Args:
        intervals: List of sorted, non-overlapping intervals.
        new_interval: New interval [start, end] to insert.

    Returns:
        Updated list of merged non-overlapping intervals.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If interval start > end.
    """
    if not (isinstance(new_interval, (list, tuple)) and len(new_interval) == 2):
        raise TypeError(f"Expected 2-element sequence for new_interval, got {type(new_interval).__name__}")

    s_new, e_new = new_interval[0], new_interval[1]
    if s_new > e_new:
        raise ValueError(f"Invalid new_interval: start {s_new} > end {e_new}")

    all_intervals = list(intervals) + [[s_new, e_new]]
    return merge_intervals(all_intervals, merge_adjacent=True)


def find_intervals_containing_point(
    intervals: List[Union[List[int], Tuple[int, int]]], point: Union[int, float]
) -> List[List[int]]:
    """
    Finds all intervals in a collection that contain a specific point (inclusive).

    Args:
        intervals: Collection of intervals.
        point: Numeric point value.

    Returns:
        List of matching intervals [start, end] containing point.

    Raises:
        TypeError: If point is not int or float, or intervals format is invalid.
    """
    if not isinstance(point, (int, float)):
        raise TypeError(f"Expected int or float for point, got {type(point).__name__}")
    if not isinstance(intervals, (list, tuple)):
        raise TypeError(f"Expected list or tuple of intervals, got {type(intervals).__name__}")

    result: List[List[int]] = []
    for item in intervals:
        if not (isinstance(item, (list, tuple)) and len(item) == 2):
            raise TypeError(f"Each interval must be a 2-element sequence, got {item}")
        start, end = item[0], item[1]
        if start <= point <= end:
            result.append([start, end])
    return result

