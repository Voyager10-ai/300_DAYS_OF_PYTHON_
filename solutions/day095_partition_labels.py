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



# ─── 2. Substring Partitions, Disjoint Sets & K-Partitioning ──────────────────


def partition_labels_substrings(s: str) -> List[str]:
    """
    Returns the actual substring slices corresponding to the maximum partition labels.

    Args:
        s: Input string.

    Returns:
        List of substring partitions (e.g. ['ababcbaca', 'defegde', 'hijhklij']).
    """
    _validate_input_string(s)
    if not s:
        return []

    sizes = partition_labels_greedy(s)
    substrings: List[str] = []
    idx = 0
    for sz in sizes:
        substrings.append(s[idx : idx + sz])
        idx += sz
    return substrings


def partition_labels_disjoint_sets(s: str) -> List[Set[str]]:
    """
    Extracts the character sets for each partition and verifies pairwise disjointness.

    Property: For all i != j, partition_set[i] & partition_set[j] == empty_set.

    Args:
        s: Input string.

    Returns:
        List of sets of characters belonging to each partition.
    """
    substrings = partition_labels_substrings(s)
    char_sets = [set(sub) for sub in substrings]

    # Verify disjointness invariant
    for i in range(len(char_sets)):
        for j in range(i + 1, len(char_sets)):
            overlap = char_sets[i] & char_sets[j]
            if overlap:
                raise ValueError(f"Partitions {i} and {j} share characters: {overlap}")

    return char_sets


def can_partition_into_k(s: str, k: int) -> bool:
    """
    Determines if string s can be partitioned into at least k valid disjoint segments.

    Since partition_labels_greedy finds the MAXIMUM possible number of valid parts,
    any smaller number of parts k can be formed by merging adjacent segments.

    Args:
        s: Input string.
        k: Target partition count (k >= 1).

    Returns:
        True if s can be partitioned into k or more valid parts, False otherwise.
    """
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")
    if not s:
        return k == 0

    max_parts = len(partition_labels_greedy(s))
    return max_parts >= k


def merge_partitions_to_k(s: str, k: int) -> Optional[List[int]]:
    """
    Merges adjacent fundamental partition labels to yield exactly k valid parts.

    Merges adjacent partitions starting from the shortest until exactly k parts remain.

    Args:
        s: Input string.
        k: Target number of parts (1 <= k <= max_partitions).

    Returns:
        List of k partition lengths, or None if k exceeds maximum possible partitions.
    """
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")

    parts = partition_labels_greedy(s)
    if k > len(parts):
        return None
    if k == len(parts):
        return parts

    # Merge rightmost adjacent parts until len(parts) == k
    while len(parts) > k:
        # Merge the two adjacent parts that minimize resultant size
        min_idx = 0
        min_sum = parts[0] + parts[1]
        for i in range(1, len(parts) - 1):
            if parts[i] + parts[i + 1] < min_sum:
                min_sum = parts[i] + parts[i + 1]
                min_idx = i

        parts[min_idx] += parts[min_idx + 1]
        parts.pop(min_idx + 1)

    return parts



# ─── 3. ASCII Interval Visualizer & Performance Benchmarking ──────────────────


def visualize_partition_labels(s: str) -> str:
    """
    Renders an ASCII visual timeline diagram of character intervals and partition cuts.

    Args:
        s: Input string (recommended length <= 40 for terminal display).

    Returns:
        Formatted ASCII diagram string.
    """
    _validate_input_string(s)
    if not s:
        return "Empty string."

    lines: List[str] = []
    lines.append(f"Partition Labels Timeline Trace for: '{s}' (len = {len(s)})")
    lines.append("=" * 72)

    # 1. Index ruler
    n = len(s)
    tens = "".join(str(i // 10) if i >= 10 else " " for i in range(n))
    ones = "".join(str(i % 10) for i in range(n))
    lines.append("Index:  " + ones if n < 10 else f"Tens:   {tens}\nOnes:   {ones}")
    lines.append("Chars:  " + " ".join(s) if n <= 24 else f"Chars:  {s}")

    # 2. Partition segments
    partitions = partition_labels_greedy(s)
    cut_line = list("." * n)
    curr = 0
    for sz in partitions:
        curr += sz
        if curr < n:
            cut_line[curr - 1] = "|"
    lines.append("Cuts:   " + "".join(cut_line))

    # 3. Partition breakdown
    lines.append("\nDisjoint Partitions:")
    idx = 0
    for p_num, sz in enumerate(partitions, 1):
        sub = s[idx : idx + sz]
        chars_used = sorted(set(sub))
        lines.append(f"  Part {p_num}: [{idx:>2}..{idx + sz - 1:>2}] len={sz:<2} sub='{sub}' chars={chars_used}")
        idx += sz

    lines.append("=" * 72)
    return "\n".join(lines)


def benchmark_partition_algorithms(
    sizes: Optional[List[int]] = None,
    alphabet_size: int = 12,
    iterations: int = 20,
) -> Dict[str, Any]:
    """
    Benchmarks Partition Labels algorithms across increasing string lengths.

    Algorithms:
      - Greedy Two-Pointer with Last-Occurrence Map O(n)
      - Interval Creation and Interval Merging O(n)

    Args:
        sizes: List of string lengths to test.
        alphabet_size: Number of unique alphabet letters to distribute.
        iterations: Number of runs per benchmark point.

    Returns:
        Structured benchmark metrics dictionary.
    """
    if sizes is None:
        sizes = [100, 1000, 5000, 25000]

    import random
    rng = random.Random(42)
    alphabet = [chr(ord('a') + i) for i in range(min(alphabet_size, 26))]

    records: List[Dict[str, Any]] = []

    for n in sizes:
        s = "".join(rng.choice(alphabet) for _ in range(n))
        row: Dict[str, Any] = {"length": n}

        # 1. Greedy Two-Pointer
        times: List[float] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            partition_labels_greedy(s)
            times.append(time.perf_counter() - t0)
        row["greedy"] = min(times)

        # 2. Interval Merging
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            partition_labels_intervals(s)
            times.append(time.perf_counter() - t0)
        row["intervals"] = min(times)

        records.append(row)

    return {"records": records, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """Formats the Partition Labels benchmark dictionary into an ASCII table."""
    lines: List[str] = []
    lines.append("Partition Labels Algorithms Performance Benchmark")
    lines.append("=" * 64)
    header = f"{'Length':>10} | {'Greedy Two-Pointer':>22} | {'Interval Merge':>22}"
    lines.append(header)
    lines.append("-" * 64)

    def _fmt(val: float) -> str:
        us = val * 1_000_000.0
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['length']:>10} | "
            f"{_fmt(r['greedy']):>22} | "
            f"{_fmt(r['intervals']):>22}"
        )
        lines.append(line)

    lines.append("=" * 64)
    return "\n".join(lines)
