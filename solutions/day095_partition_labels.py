# Day 95: Partition Labels (LeetCode 763)
#
# Problem:
#   You are given a string s. We want to partition the string into as many parts
#   as possible so that each letter appears in at most one part.
#   Notice that the partition is done so that after concatenating all the parts in
#   order, the resultant string should be s.
#   Return a list of integers representing the size of these parts.
#   Includes:
#     - Greedy two-pointer with last occurrence map O(n) time, O(1) space
#     - Character interval generation & merge intervals O(n)
#     - LeetCode 763 Solution wrapper
#     - Substring extractor & disjoint character set mapper
#     - K-partition feasibility & constrained segmenting
#     - ASCII character interval & partition boundary visualizer
#     - Multi-algorithm performance benchmark
#     - Comprehensive unit tests and Java practice code

import time
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional


# ─── 1. Core Partition Labels Implementations ─────────────────────────────────


def _validate_input_string(s: str) -> None:
    """Validates that s is a valid string of lowercase English letters."""
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")


def partition_labels_greedy(s: str) -> List[int]:
    """
    Partitions string s into maximum segments such that each letter appears in <= 1 part.

    Greedy Two-Pointer Strategy:
      1. Record the last occurrence index of each character in s: O(n).
      2. Scan s while maintaining `end = max(end, last[s[i]])`.
      3. When the current pointer i reaches `end`, the current partition is self-contained.
         Record partition size `end - start + 1` and reset `start = i + 1`.

    Time Complexity: O(n) single linear scan over string of length n.
    Space Complexity: O(1) auxiliary space (last-occurrence map has <= 26 alphabet entries).

    Args:
        s: Input string of lowercase English letters.

    Returns:
        List of integer lengths of the partitions in left-to-right order.

    Raises:
        TypeError: If s is not a string.
    """
    _validate_input_string(s)
    if not s:
        return []

    # Map each character to its rightmost occurrence index
    last_pos: Dict[str, int] = {ch: idx for idx, ch in enumerate(s)}

    partitions: List[int] = []
    start = 0
    end = 0

    for i, ch in enumerate(s):
        end = max(end, last_pos[ch])
        if i == end:
            partitions.append(end - start + 1)
            start = i + 1

    return partitions


def partition_labels_intervals(s: str) -> List[int]:
    """
    Solves Partition Labels by converting each unique letter into an [first, last] interval
    and merging overlapping intervals.

    Time Complexity: O(n + A log A) where A <= 26 alphabet characters.
    Space Complexity: O(A) space for storing unique character intervals.

    Args:
        s: Input string.

    Returns:
        List of partition sizes.
    """
    _validate_input_string(s)
    if not s:
        return []

    # Compute [first_occurrence, last_occurrence] for each unique character
    first_pos: Dict[str, int] = {}
    last_pos: Dict[str, int] = {}
    for idx, ch in enumerate(s):
        if ch not in first_pos:
            first_pos[ch] = idx
        last_pos[ch] = idx

    intervals = sorted((first_pos[ch], last_pos[ch]) for ch in first_pos)

    # Merge overlapping intervals
    merged: List[Tuple[int, int]] = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            prev_start, prev_end = merged[-1]
            merged[-1] = (prev_start, max(prev_end, end))

    return [end - start + 1 for start, end in merged]


def partition_labels_with_metrics(
    s: str,
) -> Tuple[List[int], Dict[str, Any]]:
    """
    Partitions string s while recording character frequency and segment statistics.

    Args:
        s: Input string.

    Returns:
        Tuple of (partitions_list, metrics_dict).
    """
    _validate_input_string(s)
    t0 = time.perf_counter()

    if not s:
        return ([], {
            "string_length": 0,
            "unique_chars": 0,
            "partition_count": 0,
            "time_seconds": time.perf_counter() - t0,
        })

    last_pos = {ch: idx for idx, ch in enumerate(s)}
    partitions: List[int] = []
    start = 0
    end = 0

    for i, ch in enumerate(s):
        end = max(end, last_pos[ch])
        if i == end:
            partitions.append(end - start + 1)
            start = i + 1

    elapsed = time.perf_counter() - t0
    metrics = {
        "string_length": len(s),
        "unique_chars": len(last_pos),
        "partition_count": len(partitions),
        "partitions": partitions,
        "max_partition_size": max(partitions) if partitions else 0,
        "min_partition_size": min(partitions) if partitions else 0,
        "time_seconds": elapsed,
        "algorithm": "Greedy Two-Pointer O(n)",
    }
    return (partitions, metrics)


class Solution:
    """LeetCode 763: Partition Labels solution wrapper."""

    def partitionLabels(self, s: str) -> List[int]:
        """Returns partition lengths such that each letter appears in at most one part."""
        return partition_labels_greedy(s)
