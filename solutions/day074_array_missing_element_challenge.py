# Day 74: Array Missing Element Challenge
#
# Problem:
#   Write a Python program / module to solve missing element challenges in arrays.
#   Includes core single missing element solvers (Sum & XOR methods), multiple missing elements finder,
#   shuffled array comparison, duplicate & missing finder, first missing positive integer solver,
#   completeness metrics engine, batch dataset processors, array reconstruction helpers, unit test suite, and Java practice code.

import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Single Missing Element Solvers (Sum & XOR Methods) ──────────────


def find_missing_element_sum(arr: List[int], n: Optional[int] = None) -> int:
    """
    Finds a single missing number in an array containing numbers from 1 to N using the Gauss sum formula.

    Args:
        arr: List of integers from 1 to N with exactly one element missing.
        n: Expected upper limit N. If None, inferred as len(arr) + 1.

    Returns:
        The missing integer.

    Raises:
        TypeError: If arr is not a list or elements are not ints.
        ValueError: If array contains invalid range elements or more/fewer missing items.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    
    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    if n is None:
        n = len(arr) + 1

    if n <= 0:
        raise ValueError("Range limit N must be greater than 0.")

    expected_sum = (n * (n + 1)) // 2
    actual_sum = sum(arr)
    missing = expected_sum - actual_sum

    if missing <= 0 or missing > n:
        raise ValueError(f"Calculated missing element {missing} is out of expected range [1, {n}]. Check input array.")

    return missing


def find_missing_element_xor(arr: List[int], n: Optional[int] = None) -> int:
    """
    Finds a single missing number in an array containing numbers from 1 to N using bitwise XOR.

    Args:
        arr: List of integers from 1 to N with exactly one element missing.
        n: Expected upper limit N. If None, inferred as len(arr) + 1.

    Returns:
        The missing integer.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If n <= 0.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    if n is None:
        n = len(arr) + 1

    if n <= 0:
        raise ValueError("Range limit N must be greater than 0.")

    xor_all = 0
    for i in range(1, n + 1):
        xor_all ^= i

    xor_arr = 0
    for x in arr:
        xor_arr ^= x

    return xor_all ^ xor_arr


# ─── 2. Multiple Missing Elements & Shuffled Array Comparison ────────────────


def find_all_missing_elements(arr: List[int], start: int = 1, end: Optional[int] = None) -> List[int]:
    """
    Finds all missing numbers in an array within a given inclusive range [start, end].

    Args:
        arr: List of integers.
        start: Start of inclusive target range (default 1).
        end: End of inclusive target range. If None, defaults to max(arr) or start.

    Returns:
        Sorted list of all missing integers in the range.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If start > end.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    if not isinstance(start, int):
        raise TypeError(f"Expected int for start, got {type(start).__name__}")

    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    if end is None:
        end = max(arr) if arr else start

    if not isinstance(end, int):
        raise TypeError(f"Expected int for end, got {type(end).__name__}")
    if start > end:
        raise ValueError(f"Invalid range: start {start} > end {end}")

    present_set = set(arr)
    missing_list = [num for num in range(start, end + 1) if num not in present_set]
    return missing_list


def find_missing_element_shuffled(arr1: List[Any], arr2: List[Any]) -> Any:
    """
    Finds the single element present in arr1 but missing in shuffled arr2 (handles duplicates).

    Args:
        arr1: Original list of elements.
        arr2: Shuffled list with one element missing.

    Returns:
        The missing element.

    Raises:
        TypeError: If inputs are not lists/tuples.
        ValueError: If len(arr1) != len(arr2) + 1 or no missing element found.
    """
    if not isinstance(arr1, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr1, got {type(arr1).__name__}")
    if not isinstance(arr2, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr2, got {type(arr2).__name__}")

    if len(arr1) != len(arr2) + 1:
        raise ValueError(f"arr1 length ({len(arr1)}) must be exactly 1 greater than arr2 length ({len(arr2)})")

    counts: Dict[Any, int] = {}
    for item in arr1:
        counts[item] = counts.get(item, 0) + 1

    for item in arr2:
        if item in counts:
            counts[item] -= 1
            if counts[item] == 0:
                del counts[item]
        else:
            raise ValueError(f"Element {item} in arr2 was not present in arr1.")

    if len(counts) == 1:
        return next(iter(counts.keys()))

    raise ValueError("Failed to find unique missing element between arrays.")


# ─── 3. Range Anomaly Detection & Special Solvers ───────────────────────────


def find_duplicate_and_missing(arr: List[int]) -> Tuple[int, int]:
    """
    Finds the duplicate and missing numbers in an array of size N containing values 1..N.

    Args:
        arr: List of N integers where one number is repeated and one is missing.

    Returns:
        Tuple of (duplicate_number, missing_number).

    Raises:
        TypeError: If input is not a list of ints.
        ValueError: If array format does not match duplicate/missing pattern.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")

    n = len(arr)
    if n < 2:
        raise ValueError("Array length must be at least 2.")

    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    seen = set()
    duplicate = -1
    for num in arr:
        if num in seen:
            duplicate = num
        seen.add(num)

    if duplicate == -1:
        raise ValueError("No duplicate element found in input array.")

    expected_sum = (n * (n + 1)) // 2
    actual_sum = sum(arr)
    missing = expected_sum - (actual_sum - duplicate)

    return (duplicate, missing)


def find_first_missing_positive(arr: List[int]) -> int:
    """
    Finds the smallest missing positive integer from an unsorted integer array.

    Example:
        [3, 4, -1, 1] -> 2
        [1, 2, 0]     -> 3

    Args:
        arr: Unsorted integer array.

    Returns:
        Smallest missing positive integer >= 1.

    Raises:
        TypeError: If arr is not a list or elements are not ints.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    nums = list(arr)
    n = len(nums)

    # Place each number in its right place: nums[i] should equal i + 1
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            target_idx = nums[i] - 1
            nums[i], nums[target_idx] = nums[target_idx], nums[i]

    for i in range(n):
        if nums[i] != i + 1:
            return i + 1

    return n + 1


# ─── 4. Array Completeness Metrics & Missingness Analysis Engine ───────────


def analyze_missing_element_array(
    arr: List[int], expected_range: Optional[Tuple[int, int]] = None
) -> Dict[str, Any]:
    """
    Analyzes completeness, missing elements, duplicates, and range statistics of an integer array.

    Args:
        arr: Target integer array.
        expected_range: Optional tuple (start, end) specifying overall expected bounds.

    Returns:
        Dictionary of missingness analysis metrics.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    if not arr:
        return {
            "array_length": 0,
            "min_val": 0,
            "max_val": 0,
            "expected_count": 0,
            "missing_count": 0,
            "completeness_ratio": 0.0,
            "missing_elements": [],
            "duplicate_elements": [],
            "first_missing_positive": 1,
        }

    if expected_range is not None:
        if not (isinstance(expected_range, (list, tuple)) and len(expected_range) == 2):
            raise TypeError("expected_range must be a 2-element sequence (start, end).")
        start, end = expected_range[0], expected_range[1]
    else:
        start = min(arr)
        end = max(arr)

    seen = set()
    duplicates = set()
    for x in arr:
        if x in seen:
            duplicates.add(x)
        seen.add(x)

    missing = [x for x in range(start, end + 1) if x not in seen]
    expected_count = (end - start + 1) if end >= start else 0
    unique_present_in_range = len([x for x in range(start, end + 1) if x in seen])
    completeness_ratio = (
        round((unique_present_in_range / expected_count) * 100, 2) if expected_count > 0 else 100.0
    )

    first_missing_pos = find_first_missing_positive(arr)

    return {
        "array_length": len(arr),
        "min_val": min(arr),
        "max_val": max(arr),
        "expected_count": expected_count,
        "missing_count": len(missing),
        "completeness_ratio": completeness_ratio,
        "missing_elements": missing,
        "duplicate_elements": sorted(list(duplicates)),
        "first_missing_positive": first_missing_pos,
    }


# ─── 5. Batch Dataset Solvers & Range Sanity Checkers ───────────────────────


def batch_find_missing(
    datasets: List[List[int]], start: int = 1
) -> List[Dict[str, Any]]:
    """
    Processes multiple array datasets and returns analysis metrics for each.

    Args:
        datasets: List of integer array datasets.
        start: Starting range bound for completeness calculation.

    Returns:
        List of missingness analysis dictionaries.

    Raises:
        TypeError: If datasets is not list or tuple.
    """
    if not isinstance(datasets, (list, tuple)):
        raise TypeError(f"Expected list or tuple of datasets, got {type(datasets).__name__}")

    results = []
    for arr in datasets:
        stats = analyze_missing_element_array(arr, expected_range=(start, max(arr) if arr else start))
        results.append(stats)
    return results


def filter_arrays_by_missing_count(
    datasets: List[List[int]], max_missing: int, start: int = 1
) -> List[List[int]]:
    """
    Filters datasets retaining only those with missing element count <= max_missing.

    Args:
        datasets: List of array datasets.
        max_missing: Maximum allowed missing count threshold.
        start: Starting range bound.

    Returns:
        Filtered list of array datasets.

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If max_missing < 0.
    """
    if not isinstance(datasets, (list, tuple)):
        raise TypeError(f"Expected list or tuple for datasets, got {type(datasets).__name__}")
    if not isinstance(max_missing, int):
        raise TypeError(f"Expected int for max_missing, got {type(max_missing).__name__}")
    if max_missing < 0:
        raise ValueError("max_missing must be >= 0.")

    qualifying: List[List[int]] = []
    for arr in datasets:
        if isinstance(arr, (list, tuple)):
            stats = analyze_missing_element_array(arr, expected_range=(start, max(arr) if arr else start))
            if stats["missing_count"] <= max_missing:
                qualifying.append(list(arr))
    return qualifying


# ─── 6. Array Reconstruction & Missing Element Patch Helpers ───────────────


def fill_missing_elements(
    arr: List[int], start: int = 1, end: Optional[int] = None
) -> List[int]:
    """
    Reconstructs the full sequence from start to end by filling in missing values.

    Args:
        arr: Target input array.
        start: Start bound (default 1).
        end: Optional end bound (defaults to max(arr) or start).

    Returns:
        Sorted list containing all numbers in range [start, end].

    Raises:
        TypeError: If input is invalid.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    if end is None:
        end = max(arr) if arr else start

    return list(range(start, end + 1))


def format_missing_summary_string(
    arr: List[int], expected_range: Optional[Tuple[int, int]] = None
) -> str:
    """
    Formats a concise human-readable summary of missing values in an array.

    Args:
        arr: Integer array.
        expected_range: Optional range bounds.

    Returns:
        Summary string e.g. "Array len=5 | Missing 2 element(s): [3, 7] | Complete: 71.43%".

    Raises:
        TypeError: If inputs are invalid.
    """
    stats = analyze_missing_element_array(arr, expected_range=expected_range)
    missing_str = ", ".join(map(str, stats["missing_elements"])) if stats["missing_elements"] else "None"
    return (
        f"Array len={stats['array_length']} | "
        f"Missing {stats['missing_count']} element(s): [{missing_str}] | "
        f"Completeness: {stats['completeness_ratio']}%"
    )





