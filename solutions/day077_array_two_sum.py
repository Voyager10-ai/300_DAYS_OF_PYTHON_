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


# ─── 4. Dynamic TwoSum Data Structure (LeetCode 170) ─────────────────────────


class TwoSum:
    """
    Data structure supporting dynamic number additions and O(n) two-sum lookups (LeetCode 170).

    Uses a frequency counter hash map to handle duplicates and duplicate complements.
    """

    def __init__(self) -> None:
        """Initializes an empty TwoSum container."""
        self._counts: Dict[int, int] = {}

    def add(self, number: int) -> None:
        """
        Adds a number to the internal data structure.

        Args:
            number: Integer to store.

        Raises:
            TypeError: If number is not an integer.
        """
        if not isinstance(number, int) or isinstance(number, bool):
            raise TypeError(f"Expected int for number, got {type(number).__name__}")
        self._counts[number] = self._counts.get(number, 0) + 1

    def find(self, value: int) -> bool:
        """
        Finds if there exists any pair of numbers whose sum equals the value.

        Args:
            value: Target sum to search for.

        Returns:
            True if a valid pair exists, False otherwise.

        Raises:
            TypeError: If value is not an integer.
        """
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"Expected int for value, got {type(value).__name__}")

        for num, count in self._counts.items():
            complement = value - num
            if complement == num:
                if count >= 2:
                    return True
            else:
                if complement in self._counts:
                    return True
        return False

    def remove(self, number: int) -> bool:
        """
        Removes one occurrence of number from the structure if present.

        Args:
            number: Integer to decrement/remove.

        Returns:
            True if removed, False if number was not present.
        """
        if not isinstance(number, int) or isinstance(number, bool):
            raise TypeError(f"Expected int for number, got {type(number).__name__}")

        if number not in self._counts:
            return False

        self._counts[number] -= 1
        if self._counts[number] == 0:
            del self._counts[number]
        return True

    def get_count(self, number: int) -> int:
        """Returns the occurrence frequency of the given number."""
        return self._counts.get(number, 0)

    def get_all_elements(self) -> List[int]:
        """Returns all elements stored in the structure in ascending order."""
        res: List[int] = []
        for num in sorted(self._counts.keys()):
            res.extend([num] * self._counts[num])
        return res

    def clear(self) -> None:
        """Resets the data structure to empty."""
        self._counts.clear()

    def __len__(self) -> int:
        """Returns total count of stored numbers including duplicates."""
        return sum(self._counts.values())


# ─── 5. Two Sum Multiplicity & Unique Pair Solvers ───────────────────────────


def two_sum_count_pairs(nums: List[int], target: int) -> int:
    """
    Counts the total number of index pairs (i < j) such that nums[i] + nums[j] == target.
    Runs in optimal O(n) time using frequency counts.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        Integer count of matching index pairs.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple for nums, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    counts: Dict[int, int] = {}
    pair_count = 0

    for i, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {i} is not an integer: {x!r}")
        complement = target - x
        if complement in counts:
            pair_count += counts[complement]
        counts[x] = counts.get(x, 0) + 1

    return pair_count


def two_sum_unique_value_pairs(nums: List[int], target: int) -> List[Tuple[int, int]]:
    """
    Finds all unique (value1, value2) pairs (val1 <= val2) such that val1 + val2 == target.
    Prevents duplicate reporting when duplicate numbers exist in the array.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        Sorted list of unique (val1, val2) pairs.

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

    seen: Set[int] = set()
    unique_pairs: Set[Tuple[int, int]] = set()

    for x in nums:
        complement = target - x
        if complement in seen:
            pair = (min(x, complement), max(x, complement))
            unique_pairs.add(pair)
        seen.add(x)

    return sorted(list(unique_pairs))


# ─── 6. Batch Two Sum & 2D Matrix Sum Coordinators ───────────────────────────


def batch_two_sum(queries: List[Tuple[List[int], int]]) -> List[Optional[Tuple[int, int]]]:
    """
    Executes Two Sum queries in batch.

    Args:
        queries: List of (nums, target) tuples.

    Returns:
        List of results corresponding to each query.

    Raises:
        TypeError: If queries format is invalid.
    """
    if not isinstance(queries, (list, tuple)):
        raise TypeError(f"Expected list or tuple of queries, got {type(queries).__name__}")

    results: List[Optional[Tuple[int, int]]] = []
    for idx, item in enumerate(queries):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise TypeError(f"Query at index {idx} must be a 2-tuple (nums, target), got {item!r}")
        nums, target = item
        results.append(two_sum_hash_map(nums, target))

    return results


def two_sum_matrix(
    matrix: List[List[int]], target: int
) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Finds two distinct cell coordinates in a 2D matrix whose values sum to target.

    Args:
        matrix: 2D list of integers.
        target: Target sum.

    Returns:
        Tuple of ((r1, c1), (r2, c2)) or None.

    Raises:
        TypeError: If matrix format is invalid or contains non-integers.
    """
    if not isinstance(matrix, (list, tuple)):
        raise TypeError(f"Expected 2D list or tuple for matrix, got {type(matrix).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    seen: Dict[int, Tuple[int, int]] = {}
    for r, row in enumerate(matrix):
        if not isinstance(row, (list, tuple)):
            raise TypeError(f"Row {r} must be a list or tuple, got {type(row).__name__}")
        for c, val in enumerate(row):
            if not isinstance(val, int) or isinstance(val, bool):
                raise TypeError(f"Matrix element at ({r}, {c}) is not an int: {val!r}")
            complement = target - val
            if complement in seen:
                return (seen[complement], (r, c))
            seen[val] = (r, c)

    return None


# ─── 7. Step-by-Step Trace & Algorithm Benchmark Engine ──────────────────────


def explain_two_sum_step_by_step(nums: List[int], target: int) -> List[Dict[str, Any]]:
    """
    Produces a pedagogical trace of the hash map Two Sum algorithm.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        List of trace step dictionaries containing step details.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"Expected list or tuple, got {type(nums).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"Expected int for target, got {type(target).__name__}")

    steps: List[Dict[str, Any]] = []
    seen: Dict[int, int] = {}

    for i, num in enumerate(nums):
        if not isinstance(num, int) or isinstance(num, bool):
            raise TypeError(f"Element at index {i} is not an integer: {num!r}")

        complement = target - num
        match_found = complement in seen
        step_info = {
            "step": i + 1,
            "current_index": i,
            "current_value": num,
            "complement_needed": complement,
            "hash_map_state": dict(seen),
            "match_found": match_found,
            "solution": (seen[complement], i) if match_found else None,
        }
        steps.append(step_info)

        if match_found:
            break
        seen[num] = i

    return steps


def benchmark_two_sum_algorithms(nums: List[int], target: int) -> Dict[str, Any]:
    """
    Compares runtime performance between hash map, brute force, and two-pointer approaches.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        Dictionary mapping algorithm names to their execution metrics.
    """
    results: Dict[str, Any] = {}

    # 1. Hash Map
    t0 = time.perf_counter()
    res_hm = two_sum_hash_map(nums, target)
    t_hm = (time.perf_counter() - t0) * 1000.0
    results["hash_map"] = {"result": res_hm, "time_ms": round(t_hm, 4), "complexity": "O(n)"}

    # 2. Brute Force
    t0 = time.perf_counter()
    res_bf = two_sum_brute_force(nums, target)
    t_bf = (time.perf_counter() - t0) * 1000.0
    results["brute_force"] = {"result": res_bf, "time_ms": round(t_bf, 4), "complexity": "O(n^2)"}

    # 3. Two Pointers (includes sorting overhead)
    t0 = time.perf_counter()
    indexed = sorted([(val, idx) for idx, val in enumerate(nums)], key=lambda x: x[0])
    l, r = 0, len(indexed) - 1
    res_tp = None
    while l < r:
        s = indexed[l][0] + indexed[r][0]
        if s == target:
            res_tp = (min(indexed[l][1], indexed[r][1]), max(indexed[l][1], indexed[r][1]))
            break
        elif s < target:
            l += 1
        else:
            r -= 1
    t_tp = (time.perf_counter() - t0) * 1000.0
    results["two_pointers_sorted"] = {"result": res_tp, "time_ms": round(t_tp, 4), "complexity": "O(n log n)"}

    return results


# ─── 8. Comprehensive Unit Test Suite ────────────────────────────────────────


class TestArrayTwoSum(unittest.TestCase):
    """Test suite covering all Two Sum algorithms, variants, and data structures."""

    def test_two_sum_hash_map_standard(self):
        self.assertEqual(two_sum_hash_map([2, 7, 11, 15], 9), (0, 1))
        self.assertEqual(two_sum_hash_map([3, 2, 4], 6), (1, 2))
        self.assertEqual(two_sum_hash_map([3, 3], 6), (0, 1))
        self.assertIsNone(two_sum_hash_map([1, 2, 3], 10))

    def test_two_sum_hash_map_negatives_and_zeros(self):
        self.assertEqual(two_sum_hash_map([-1, -2, -3, -4, -5], -8), (2, 4))
        self.assertEqual(two_sum_hash_map([0, 4, 3, 0], 0), (0, 3))
        self.assertEqual(two_sum_hash_map([-5, 10, 2], 5), (0, 1))

    def test_two_sum_brute_force(self):
        nums = [2, 7, 11, 15]
        self.assertEqual(two_sum_brute_force(nums, 9), (0, 1))
        self.assertEqual(two_sum_brute_force([3, 2, 4], 6), (1, 2))
        self.assertIsNone(two_sum_brute_force([1, 2], 5))

    def test_two_sum_all_pairs(self):
        nums = [1, 2, 3, 2, 1]
        # target = 4: (1 at 0, 3 at 2), (2 at 1, 2 at 3), (3 at 2, 1 at 4)
        pairs = two_sum_all_pairs(nums, 4)
        self.assertEqual(len(pairs), 3)

        unique_vals = two_sum_all_pairs(nums, 4, unique_values_only=True)
        self.assertEqual(unique_vals, [(1, 3), (2, 2)])

    def test_two_sum_two_pointers(self):
        sorted_nums = [2, 7, 11, 15]
        self.assertEqual(two_sum_two_pointers(sorted_nums, 9), (0, 1))
        self.assertEqual(two_sum_two_pointers(sorted_nums, 9, one_indexed=True), (1, 2))
        self.assertEqual(two_sum_two_pointers([2, 3, 4], 6), (0, 2))
        self.assertIsNone(two_sum_two_pointers([1, 2, 3], 100))

    def test_two_sum_binary_search(self):
        sorted_nums = [1, 2, 3, 4, 4, 9, 56, 90]
        self.assertEqual(two_sum_binary_search(sorted_nums, 8), (3, 4))
        self.assertEqual(two_sum_binary_search(sorted_nums, 8, one_indexed=True), (4, 5))
        self.assertIsNone(two_sum_binary_search(sorted_nums, 1000))

    def test_two_sum_closest(self):
        self.assertEqual(two_sum_closest([10, 22, 28, 29, 30, 40], 54), (22, 30, 52))
        self.assertEqual(two_sum_closest([1, 2, 3, 4], 7), (3, 4, 7))
        self.assertEqual(two_sum_closest([-5, -2, 1, 9], 0), (-2, 1, -1))

    def test_two_sum_less_than_k(self):
        nums = [34, 23, 1, 24, 75, 33, 54, 8]
        self.assertEqual(two_sum_less_than_k(nums, 60), (24, 34, 58))
        self.assertIsNone(two_sum_less_than_k([10, 20, 30], 15))

    def test_two_sum_data_structure(self):
        ts = TwoSum()
        ts.add(1)
        ts.add(3)
        ts.add(5)
        self.assertTrue(ts.find(4))   # 1 + 3
        self.assertTrue(ts.find(6))   # 1 + 5
        self.assertFalse(ts.find(7))
        self.assertFalse(ts.find(2))  # only one 1

        ts.add(1)
        self.assertTrue(ts.find(2))   # two 1s
        self.assertEqual(ts.get_count(1), 2)
        self.assertEqual(len(ts), 4)

        self.assertTrue(ts.remove(1))
        self.assertEqual(ts.get_count(1), 1)
        self.assertFalse(ts.find(2))

        self.assertEqual(ts.get_all_elements(), [1, 3, 5])
        ts.clear()
        self.assertEqual(len(ts), 0)

    def test_two_sum_count_pairs(self):
        nums = [1, 1, 1, 1]
        self.assertEqual(two_sum_count_pairs(nums, 2), 6)  # 4C2 = 6
        self.assertEqual(two_sum_count_pairs([1, 2, 3, 4, 3], 6), 2)  # (2, 4) and (3, 3)

    def test_two_sum_unique_value_pairs(self):
        nums = [1, 1, 2, 4, 4, 5]
        self.assertEqual(two_sum_unique_value_pairs(nums, 6), [(1, 5), (2, 4)])

    def test_batch_and_matrix(self):
        queries = [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([1, 2], 10)]
        results = batch_two_sum(queries)
        self.assertEqual(results, [(0, 1), (1, 2), None])

        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(two_sum_matrix(matrix, 17), ((3 - 1, 3 - 2), (3 - 1, 3 - 1)))  # (2, 1)=8 and (2, 2)=9
        self.assertIsNone(two_sum_matrix(matrix, 100))

    def test_trace_and_benchmark(self):
        trace = explain_two_sum_step_by_step([2, 7, 11], 9)
        self.assertEqual(len(trace), 2)
        self.assertTrue(trace[1]["match_found"])
        self.assertEqual(trace[1]["solution"], (0, 1))

        bm = benchmark_two_sum_algorithms([1, 5, 3, 7, 9], 10)
        self.assertIn("hash_map", bm)
        self.assertIn("brute_force", bm)
        self.assertIn("two_pointers_sorted", bm)

    def test_error_handling(self):
        with self.assertRaises(TypeError):
            two_sum_hash_map(None, 5)
        with self.assertRaises(TypeError):
            two_sum_hash_map([1, "two"], 3)
        with self.assertRaises(TypeError):
            two_sum_hash_map([1, 2], "3")
        with self.assertRaises(ValueError):
            two_sum_two_pointers([3, 2, 1], 5)  # unsorted
        with self.assertRaises(ValueError):
            two_sum_closest([1], 5)  # len < 2







