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


# ─── 2. Custom Step & Gap-Tolerant Summary Range Algorithms ──────────────────


def summary_ranges_with_step(nums: List[int], step: int = 1) -> List[str]:
    """
    Computes summary ranges where consecutive numbers increase by a fixed step.

    For example, with step=2 and nums=[1, 3, 5, 10, 12], yields ["1->5", "10->12"].

    Args:
        nums: Sorted list of unique integers.
        step: Expected difference between consecutive elements (must be positive).

    Returns:
        List of range strings formatted as "a->b" or "a".

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If step <= 0 or nums is unsorted/has duplicates.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")
    if not isinstance(step, int) or isinstance(step, bool):
        raise TypeError(f"Expected int for step, got {type(step).__name__}")
    if step <= 0:
        raise ValueError(f"Step must be a positive integer, got {step}")

    n = len(nums)
    if n == 0:
        return []

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        if i > 0 and x <= nums[i - 1]:
            raise ValueError(f"Elements must be strictly increasing: {nums[i-1]} >= {x}")

    result: List[str] = []
    start = nums[0]

    for i in range(1, n):
        if nums[i] != nums[i - 1] + step:
            end = nums[i - 1]
            if start == end:
                result.append(str(start))
            else:
                result.append(f"{start}->{end}")
            start = nums[i]

    end = nums[-1]
    if start == end:
        result.append(str(start))
    else:
        result.append(f"{start}->{end}")

    return result


def summary_ranges_with_max_gap(nums: List[int], max_gap: int = 1) -> List[Tuple[int, int]]:
    """
    Clusters numbers into ranges where any consecutive pair has a difference <= max_gap.

    Args:
        nums: Sorted list of integers.
        max_gap: Maximum allowed gap between consecutive numbers in the same cluster.

    Returns:
        List of (start, end) tuples covering the clusters.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If max_gap < 1 or array is unsorted.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")
    if not isinstance(max_gap, int) or isinstance(max_gap, bool):
        raise TypeError(f"Expected int for max_gap, got {type(max_gap).__name__}")
    if max_gap < 1:
        raise ValueError(f"max_gap must be >= 1, got {max_gap}")

    n = len(nums)
    if n == 0:
        return []

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        if i > 0 and x < nums[i - 1]:
            raise ValueError(f"Array must be sorted in non-decreasing order: {nums[i-1]} > {x}")

    intervals: List[Tuple[int, int]] = []
    start = nums[0]

    for i in range(1, n):
        if nums[i] - nums[i - 1] > max_gap:
            intervals.append((start, nums[i - 1]))
            start = nums[i]

    intervals.append((start, nums[-1]))
    return intervals


# ─── 3. Range Parser & Reverse Array Reconstruction Helpers ──────────────────


def parse_range_string(range_str: str) -> Tuple[int, int]:
    """
    Parses a range string ("a->b" or "a") into an integer tuple (start, end).

    Args:
        range_str: Range string formatted as "a->b" or "a".

    Returns:
        Tuple of (start, end) integers inclusive.

    Raises:
        TypeError: If range_str is not a string.
        ValueError: If range_str format is invalid or start > end.
    """
    if not isinstance(range_str, str):
        raise TypeError(f"Expected str for range_str, got {type(range_str).__name__}")

    s = range_str.strip()
    if not s:
        raise ValueError("Range string cannot be empty")

    if "->" in s:
        parts = s.split("->")
        if len(parts) != 2:
            raise ValueError(f"Malformed range string '{range_str}' (expected single '->')")
        try:
            start = int(parts[0].strip())
            end = int(parts[1].strip())
        except ValueError as err:
            raise ValueError(f"Invalid integer in range string '{range_str}': {err}") from err

        if start > end:
            raise ValueError(f"Invalid range in '{range_str}': start ({start}) > end ({end})")
        return (start, end)
    else:
        try:
            val = int(s)
            return (val, val)
        except ValueError as err:
            raise ValueError(f"Invalid integer in range string '{range_str}': {err}") from err


def ranges_to_array(ranges: List[str]) -> List[int]:
    """
    Reconstructs the original sorted integer array from a list of summary range strings.

    For example, ["0->2", "4->5", "7"] -> [0, 1, 2, 4, 5, 7].

    Args:
        ranges: List of summary range strings.

    Returns:
        Reconstructed list of integers in increasing order.

    Raises:
        TypeError: If ranges is not a list/tuple of strings.
        ValueError: If ranges overlap or are not in strictly increasing order.
    """
    if not isinstance(ranges, (list, tuple)):
        raise TypeError(f"Expected list or tuple of strings, got {type(ranges).__name__}")

    result: List[int] = []
    prev_end: Optional[int] = None

    for i, r_str in enumerate(ranges):
        start, end = parse_range_string(r_str)
        if prev_end is not None and start <= prev_end:
            raise ValueError(
                f"Range at index {i} ('{r_str}') overlaps or is not strictly after previous range ending at {prev_end}"
            )
        result.extend(range(start, end + 1))
        prev_end = end

    return result


def intervals_to_array(intervals: List[Tuple[int, int]]) -> List[int]:
    """
    Reconstructs an integer array from a list of (start, end) intervals.

    Args:
        intervals: List of (start, end) inclusive tuples.

    Returns:
        Flattened list of integers covering all intervals.

    Raises:
        TypeError: If intervals is not a list of pairs.
        ValueError: If intervals overlap or are invalid.
    """
    if not isinstance(intervals, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(intervals).__name__}")

    result: List[int] = []
    prev_end: Optional[int] = None

    for i, item in enumerate(intervals):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise TypeError(f"Interval at index {i} must be a 2-tuple (start, end), got {item!r}")
        start, end = item
        if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool):
            raise TypeError(f"Interval bounds at index {i} must be integers: ({start!r}, {end!r})")
        if start > end:
            raise ValueError(f"Interval at index {i} has start ({start}) > end ({end})")
        if prev_end is not None and start <= prev_end:
            raise ValueError(f"Interval at index {i} overlaps or is not strictly after previous end {prev_end}")

        result.extend(range(start, end + 1))
        prev_end = end

    return result


# ─── 4. Missing Range Solver for Bounded Integer Arrays ──────────────────────


def find_missing_ranges(nums: List[int], lower: int, upper: int) -> List[str]:
    """
    Finds all missing ranges in a sorted array that fall within [lower, upper] (LeetCode 163).

    For example, nums=[0, 1, 3, 50, 75], lower=0, upper=99
    yields ["2", "4->49", "51->74", "76->99"].

    Args:
        nums: Sorted list of unique integers within or near [lower, upper].
        lower: Lower bound of the target range.
        upper: Upper bound of the target range.

    Returns:
        List of missing range strings formatted as "a->b" or "a".

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If lower > upper or nums is not sorted.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")
    if not isinstance(lower, int) or isinstance(lower, bool):
        raise TypeError(f"Expected int for lower, got {type(lower).__name__}")
    if not isinstance(upper, int) or isinstance(upper, bool):
        raise TypeError(f"Expected int for upper, got {type(upper).__name__}")
    if lower > upper:
        raise ValueError(f"lower ({lower}) cannot be greater than upper ({upper})")

    # Filter nums strictly inside [lower, upper] and ensure sorted
    curr = lower
    result: List[str] = []

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        if i > 0 and x < nums[i - 1]:
            raise ValueError(f"nums must be sorted: {nums[i-1]} > {x}")

        if x < curr:
            continue
        if x > upper:
            break

        if x > curr:
            if x - 1 == curr:
                result.append(str(curr))
            else:
                result.append(f"{curr}->{x - 1}")

        curr = x + 1

    if curr <= upper:
        if curr == upper:
            result.append(str(curr))
        else:
            result.append(f"{curr}->{upper}")

    return result


def find_missing_intervals(nums: List[int], lower: int, upper: int) -> List[Tuple[int, int]]:
    """
    Finds all missing intervals in [lower, upper] as (start, end) tuples.

    Args:
        nums: Sorted list of unique integers.
        lower: Lower bound.
        upper: Upper bound.

    Returns:
        List of (start, end) inclusive missing intervals.
    """
    missing_strs = find_missing_ranges(nums, lower, upper)
    return [parse_range_string(s) for s in missing_strs]


# ─── 5. Range Analytics & Coverage Metrics Engine ────────────────────────────


def analyze_range_density(nums: List[int]) -> Dict[str, Any]:
    """
    Computes structural density and compression statistics for an integer array.

    Args:
        nums: Sorted list of unique integers.

    Returns:
        Dictionary containing:
            - total_elements: Total count of integers.
            - total_ranges: Number of summarized ranges.
            - singleton_count: Number of 1-element ranges.
            - multi_count: Number of multi-element ranges.
            - longest_span: Length of the longest contiguous sequence.
            - total_span: (max_val - min_val + 1) if not empty.
            - compression_ratio: elements compressed per range (total_elements / total_ranges).
            - coverage_percentage: percentage of total span covered by nums.

    Raises:
        TypeError: If nums is invalid.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")

    n = len(nums)
    if n == 0:
        return {
            "total_elements": 0,
            "total_ranges": 0,
            "singleton_count": 0,
            "multi_count": 0,
            "longest_span": 0,
            "total_span": 0,
            "compression_ratio": 1.0,
            "coverage_percentage": 0.0,
        }

    intervals = summary_ranges_intervals(list(nums))
    singleton_count = sum(1 for s, e in intervals if s == e)
    multi_count = sum(1 for s, e in intervals if s != e)
    longest_span = max((e - s + 1) for s, e in intervals)
    total_span = nums[-1] - nums[0] + 1
    compression_ratio = round(n / len(intervals), 2)
    coverage_percentage = round((n / total_span) * 100.0, 2) if total_span > 0 else 100.0

    return {
        "total_elements": n,
        "total_ranges": len(intervals),
        "singleton_count": singleton_count,
        "multi_count": multi_count,
        "longest_span": longest_span,
        "total_span": total_span,
        "compression_ratio": compression_ratio,
        "coverage_percentage": coverage_percentage,
    }


def find_isolated_elements(nums: List[int]) -> List[int]:
    """
    Finds all elements that do not have immediate adjacent neighbors in the array.

    These are elements that form singletons (e.g. "x" rather than "a->b") in summary_ranges.

    Args:
        nums: Sorted list of unique integers.

    Returns:
        List of isolated integer elements.
    """
    intervals = summary_ranges_intervals(list(nums))
    return [s for s, e in intervals if s == e]


# ─── 6. Batch & Categorized Multi-Sequence Range Summarizers ─────────────────


def batch_summary_ranges(arrays: List[List[int]]) -> List[List[str]]:
    """
    Executes summary ranges across a batch of integer lists.

    Args:
        arrays: List of integer arrays.

    Returns:
        List of summary range string lists.

    Raises:
        TypeError: If arrays is not a list/tuple.
    """
    if not isinstance(arrays, (list, tuple)):
        raise TypeError(f"Expected list or tuple of arrays, got {type(arrays).__name__}")

    return [summary_ranges(arr) for arr in arrays]


def summary_ranges_by_category(data: Dict[str, List[int]]) -> Dict[str, List[str]]:
    """
    Computes summary ranges for multiple categorized series (e.g., timestamps, port lists).

    Args:
        data: Mapping from category name to integer array.

    Returns:
        Mapping from category name to summary range strings.

    Raises:
        TypeError: If data is not a dictionary.
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict for data, got {type(data).__name__}")

    result: Dict[str, List[str]] = {}
    for key, arr in data.items():
        if not isinstance(key, str):
            raise TypeError(f"Category keys must be strings, got {type(key).__name__}")
        result[key] = summary_ranges_unsorted(arr)

    return result





