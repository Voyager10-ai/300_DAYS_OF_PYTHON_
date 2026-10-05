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


# ─── 3. Interval Intersection & Gap Utilities ───────────────────────────────


def interval_intersection(
    intervals1: List[Union[List[int], Tuple[int, int]]], intervals2: List[Union[List[int], Tuple[int, int]]]
) -> List[List[int]]:
    """
    Finds the intersection of two lists of sorted non-overlapping intervals.

    Args:
        intervals1: First list of non-overlapping intervals.
        intervals2: Second list of non-overlapping intervals.

    Returns:
        List of intersected intervals [start, end].

    Raises:
        TypeError: If inputs are invalid.
    """
    m1 = merge_intervals(intervals1, merge_adjacent=False)
    m2 = merge_intervals(intervals2, merge_adjacent=False)

    i, j = 0, 0
    intersections: List[List[int]] = []

    while i < len(m1) and j < len(m2):
        s1, e1 = m1[i][0], m1[i][1]
        s2, e2 = m2[j][0], m2[j][1]

        start_max = max(s1, s2)
        end_min = min(e1, e2)

        if start_max <= end_min:
            intersections.append([start_max, end_min])

        if e1 < e2:
            i += 1
        else:
            j += 1

    return intersections


def find_interval_gaps(
    intervals: List[Union[List[int], Tuple[int, int]]], bounds: Optional[Tuple[int, int]] = None
) -> List[List[int]]:
    """
    Finds uncovered gap intervals between merged intervals within optional bounds [min_b, max_b].

    Args:
        intervals: List of intervals.
        bounds: Optional tuple (start_bound, end_bound) specifying outer search range.

    Returns:
        List of gap intervals [gap_start, gap_end].

    Raises:
        TypeError: If bounds is provided but invalid.
        ValueError: If bounds start > end.
    """
    merged = merge_intervals(intervals, merge_adjacent=True)
    if not merged:
        if bounds is not None:
            if bounds[0] > bounds[1]:
                raise ValueError(f"Invalid bounds: {bounds}")
            return [[bounds[0], bounds[1]]]
        return []

    gaps: List[List[int]] = []

    # Check gap before first interval if bounds provided
    curr_min = merged[0][0]
    curr_max = merged[-1][1]

    if bounds is not None:
        if not (isinstance(bounds, (list, tuple)) and len(bounds) == 2):
            raise TypeError("bounds must be a 2-element sequence (min_b, max_b).")
        b_start, b_end = bounds[0], bounds[1]
        if b_start > b_end:
            raise ValueError(f"Invalid bounds: {b_start} > {b_end}")

        if b_start < curr_min:
            gaps.append([b_start, min(b_end, curr_min)])

    # Gaps between adjacent merged intervals
    for idx in range(len(merged) - 1):
        gap_start = merged[idx][1]
        gap_end = merged[idx + 1][0]
        if gap_start < gap_end:
            if bounds is not None:
                g_s = max(bounds[0], gap_start)
                g_e = min(bounds[1], gap_end)
                if g_s < g_e:
                    gaps.append([g_s, g_e])
            else:
                gaps.append([gap_start, gap_end])

    # Check gap after last interval if bounds provided
    if bounds is not None:
        b_start, b_end = bounds[0], bounds[1]
        if b_end > curr_max:
            gaps.append([max(b_start, curr_max), b_end])

    return gaps


# ─── 4. Interval Metrics & Coverage Analysis Engine ─────────────────────────


def analyze_interval_set(intervals: List[Union[List[int], Tuple[int, int]]]) -> Dict[str, Any]:
    """
    Analyzes coverage, total length, merge reduction ratio, and gap metrics for an interval set.

    Args:
        intervals: List of intervals.

    Returns:
        Dictionary of coverage metrics and statistics.

    Raises:
        TypeError: If intervals is not list/tuple.
    """
    if not isinstance(intervals, (list, tuple)):
        raise TypeError(f"Expected list or tuple of intervals, got {type(intervals).__name__}")

    total_input = len(intervals)
    if total_input == 0:
        return {
            "total_input_intervals": 0,
            "merged_interval_count": 0,
            "reduction_percentage": 0.0,
            "total_coverage_length": 0,
            "overall_span_length": 0,
            "total_gap_length": 0,
            "coverage_ratio": 0.0,
            "merged_intervals": [],
        }

    merged = merge_intervals(intervals, merge_adjacent=True)
    merged_count = len(merged)

    reduction_pct = round(((total_input - merged_count) / total_input) * 100, 2)
    total_coverage = sum(end - start for start, end in merged)

    overall_span = merged[-1][1] - merged[0][0]
    total_gap = max(0, overall_span - total_coverage)
    coverage_ratio = round((total_coverage / overall_span) * 100, 2) if overall_span > 0 else 100.0

    return {
        "total_input_intervals": total_input,
        "merged_interval_count": merged_count,
        "reduction_percentage": reduction_pct,
        "total_coverage_length": total_coverage,
        "overall_span_length": overall_span,
        "total_gap_length": total_gap,
        "coverage_ratio": coverage_ratio,
        "merged_intervals": merged,
    }


# ─── 5. Batch Collection Processors & Threshold Filters ──────────────────────


def batch_merge_intervals(
    dataset: List[List[Union[List[int], Tuple[int, int]]]]
) -> List[List[List[int]]]:
    """
    Processes multiple sets of intervals and merges each.

    Args:
        dataset: List of interval sets.

    Returns:
        List of merged interval sets.

    Raises:
        TypeError: If dataset is not a list or tuple.
    """
    if not isinstance(dataset, (list, tuple)):
        raise TypeError(f"Expected list or tuple of interval sets, got {type(dataset).__name__}")

    return [merge_intervals(interval_set) for interval_set in dataset]


def filter_intervals_by_min_length(
    intervals: List[Union[List[int], Tuple[int, int]]], min_length: Union[int, float]
) -> List[List[int]]:
    """
    Filters intervals keeping only those with duration/length (end - start) >= min_length.

    Args:
        intervals: List of intervals.
        min_length: Minimum required interval length.

    Returns:
        Filtered list of intervals [start, end].

    Raises:
        TypeError: If min_length is not numeric or intervals is invalid.
        ValueError: If min_length < 0.
    """
    if not isinstance(min_length, (int, float)):
        raise TypeError(f"Expected int or float for min_length, got {type(min_length).__name__}")
    if min_length < 0:
        raise ValueError("min_length must be >= 0.")
    if not isinstance(intervals, (list, tuple)):
        raise TypeError(f"Expected list or tuple of intervals, got {type(intervals).__name__}")

    filtered: List[List[int]] = []
    for item in intervals:
        if not (isinstance(item, (list, tuple)) and len(item) == 2):
            raise TypeError(f"Each interval must be a 2-element sequence, got {item}")
        start, end = item[0], item[1]
        if (end - start) >= min_length:
            filtered.append([start, end])
    return filtered


# ─── 6. Interval Formatters & ASCII Visualizer ──────────────────────────────


def format_intervals_string(
    intervals: List[Union[List[int], Tuple[int, int]]], delimiter: str = ", "
) -> str:
    """
    Formats a list of intervals as a formatted string representation.

    Args:
        intervals: List of intervals.
        delimiter: Delimiter string between interval pairs.

    Returns:
        Formatted string representation e.g. "[1, 3], [2, 6], [8, 10]".

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(intervals, (list, tuple)):
        raise TypeError(f"Expected list or tuple of intervals, got {type(intervals).__name__}")
    if not isinstance(delimiter, str):
        raise TypeError(f"Expected str for delimiter, got {type(delimiter).__name__}")

    formatted_pairs = []
    for item in intervals:
        if not (isinstance(item, (list, tuple)) and len(item) == 2):
            raise TypeError(f"Each interval must be a 2-element sequence, got {item}")
        formatted_pairs.append(f"[{item[0]}, {item[1]}]")

    return delimiter.join(formatted_pairs)


def visualize_intervals_ascii(
    intervals: List[Union[List[int], Tuple[int, int]]], width: int = 40
) -> str:
    """
    Renders an ASCII timeline visualization of intervals across a fixed timeline width.

    Args:
        intervals: List of intervals.
        width: Character width for rendering.

    Returns:
        Multi-line string representation of the timeline.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If width < 10.
    """
    if not isinstance(width, int):
        raise TypeError(f"Expected int for width, got {type(width).__name__}")
    if width < 10:
        raise ValueError("width must be at least 10.")
    if not isinstance(intervals, (list, tuple)):
        raise TypeError(f"Expected list or tuple of intervals, got {type(intervals).__name__}")

    if not intervals:
        return "No intervals to visualize."

    merged = merge_intervals(intervals, merge_adjacent=True)
    min_val = min(item[0] for item in intervals)
    max_val = max(item[1] for item in intervals)

    span = max_val - min_val
    if span == 0:
        span = 1

    lines = []
    lines.append(f"Timeline Bounds: [{min_val} ... {max_val}]")
    lines.append("-" * (width + 12))

    for idx, (s, e) in enumerate(intervals):
        rel_s = int(round(((s - min_val) / span) * width))
        rel_e = int(round(((e - min_val) / span) * width))
        rel_e = max(rel_s + 1, rel_e)

        row = ["."] * (width + 1)
        for i in range(rel_s, min(rel_e + 1, width + 1)):
            row[i] = "="
        
        row_str = "".join(row)
        lines.append(f"Int #{idx+1:<2} [{s:>3}, {e:>3}] | {row_str}")

    return "\n".join(lines)


# ─── 7. Unit Test Suite ───────────────────────────────────────────────────────


class TestArrayMergeIntervals(unittest.TestCase):
    """Unit test suite for Array Merge Intervals utilities and algorithms."""

    def test_is_overlapping(self):
        self.assertTrue(is_overlapping([1, 4], [2, 6]))
        self.assertFalse(is_overlapping([1, 3], [5, 7]))
        self.assertTrue(is_overlapping([1, 3], [3, 5], allow_adjacent=True))
        self.assertFalse(is_overlapping([1, 3], [3, 5], allow_adjacent=False))

    def test_merge_intervals(self):
        intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
        self.assertEqual(merge_intervals(intervals), [[1, 6], [8, 10], [15, 18]])

        intervals_adjacent = [[1, 4], [4, 5]]
        self.assertEqual(merge_intervals(intervals_adjacent, merge_adjacent=True), [[1, 5]])
        self.assertEqual(merge_intervals(intervals_adjacent, merge_adjacent=False), [[1, 4], [4, 5]])

        self.assertEqual(merge_intervals([]), [])

    def test_insert_interval(self):
        intervals = [[1, 3], [6, 9]]
        new_int = [2, 5]
        self.assertEqual(insert_interval(intervals, new_int), [[1, 5], [6, 9]])

    def test_find_intervals_containing_point(self):
        intervals = [[1, 5], [3, 8], [10, 15]]
        self.assertEqual(find_intervals_containing_point(intervals, 4), [[1, 5], [3, 8]])
        self.assertEqual(find_intervals_containing_point(intervals, 20), [])

    def test_interval_intersection(self):
        i1 = [[0, 2], [5, 10], [13, 23], [24, 25]]
        i2 = [[1, 5], [8, 12], [15, 24], [25, 26]]
        expected = [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
        self.assertEqual(interval_intersection(i1, i2), expected)

    def test_find_interval_gaps(self):
        intervals = [[1, 3], [6, 9]]
        gaps = find_interval_gaps(intervals, bounds=(0, 10))
        self.assertEqual(gaps, [[0, 1], [3, 6], [9, 10]])

    def test_analyze_interval_set(self):
        intervals = [[1, 4], [2, 6], [8, 10]]
        stats = analyze_interval_set(intervals)
        self.assertEqual(stats["total_input_intervals"], 3)
        self.assertEqual(stats["merged_interval_count"], 2)
        self.assertEqual(stats["total_coverage_length"], 7)
        self.assertEqual(stats["overall_span_length"], 9)
        self.assertEqual(stats["total_gap_length"], 2)

    def test_batch_merge_intervals(self):
        dataset = [[[1, 3], [2, 4]], [[5, 7], [6, 8]]]
        results = batch_merge_intervals(dataset)
        self.assertEqual(results, [[[1, 4]], [[5, 8]]])

    def test_filter_intervals_by_min_length(self):
        intervals = [[1, 2], [3, 8], [10, 15]]
        filtered = filter_intervals_by_min_length(intervals, 4)
        self.assertEqual(filtered, [[3, 8], [10, 15]])

    def test_format_intervals_string(self):
        intervals = [[1, 3], [2, 6]]
        self.assertEqual(format_intervals_string(intervals), "[1, 3], [2, 6]")

    def test_visualize_intervals_ascii(self):
        intervals = [[1, 5], [6, 10]]
        output = visualize_intervals_ascii(intervals, width=20)
        self.assertIn("Timeline Bounds", output)
        self.assertIn("Int #1", output)

    def test_error_handling(self):
        with self.assertRaises(TypeError):
            merge_intervals("invalid")
        with self.assertRaises(ValueError):
            merge_intervals([[5, 2]])
        with self.assertRaises(ValueError):
            insert_interval([[1, 3]], [5, 2])


# ─── 8. Interactive CLI Demo Runner ──────────────────────────────────────────


def main():
    """Runs interactive demonstration and executes test suite."""
    print("=" * 65)
    print(" Day 73: Array Merge Intervals - Demonstration Engine")
    print("=" * 65)

    sample_intervals = [[1, 3], [2, 6], [8, 10], [15, 18], [17, 20]]
    print(f"Sample Input Intervals   : {sample_intervals}")
    merged = merge_intervals(sample_intervals)
    print(f"Merged Intervals         : {merged}")
    print(f"Formatted String         : '{format_intervals_string(merged)}'")

    inserted = insert_interval(merged, [7, 12])
    print(f"After Inserting [7, 12]  : {inserted}")

    print("\n--- Interval Set Coverage Metrics ---")
    stats = analyze_interval_set(sample_intervals)
    for k, v in stats.items():
        print(f"  {k:<24}: {v}")

    print("\n--- ASCII Timeline Visualization ---")
    print(visualize_intervals_ascii(sample_intervals, width=30))

    print("\n--- Running Unit Test Suite ---")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArrayMergeIntervals)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    main()







