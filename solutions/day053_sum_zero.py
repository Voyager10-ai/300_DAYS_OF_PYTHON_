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


# ─── 4. 3Sum Closest to Target Solver ──────────────────────────────────────────


def three_sum_closest(nums: List[int], target: int = 0) -> int:
    """
    Finds three integers in nums such that the sum is closest to target.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        The sum of the three integers closest to target.

    Raises:
        ValueError: If len(nums) < 3.
    """
    if not isinstance(nums, list):
        raise TypeError(f"Expected list input, got {type(nums).__name__}")
    if len(nums) < 3:
        raise ValueError(f"List must contain at least 3 integers, got {len(nums)}")

    sorted_nums = sorted(nums)
    closest_sum = sorted_nums[0] + sorted_nums[1] + sorted_nums[2]
    n = len(sorted_nums)

    for i in range(n - 2):
        left = i + 1
        right = n - 1
        while left < right:
            current_sum = sorted_nums[i] + sorted_nums[left] + sorted_nums[right]

            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum

            if current_sum == target:
                return current_sum
            elif current_sum < target:
                left += 1
            else:
                right -= 1

    return closest_sum


# ─── 5. Subset Sum Zero Powerset Generator ─────────────────────────────────────


def subset_sum_zero(nums: List[int], max_length: Optional[int] = None) -> List[Tuple[int, ...]]:
    """
    Finds all non-empty unique subsets (combinations) of nums that sum to zero.

    Args:
        nums: List of integers.
        max_length: Maximum subset size limit (optional).

    Returns:
        Sorted list of unique tuples summing to 0.
    """
    if not isinstance(nums, list):
        raise TypeError(f"Expected list input, got {type(nums).__name__}")

    results: Set[Tuple[int, ...]] = set()
    n = len(nums)
    limit = max_length if max_length is not None else n

    def backtrack(index: int, current_subset: List[int], current_sum: int):
        if current_subset and current_sum == 0:
            results.add(tuple(sorted(current_subset)))

        if index >= n or len(current_subset) >= limit:
            return

        for i in range(index, n):
            backtrack(i + 1, current_subset + [nums[i]], current_sum + nums[i])

    backtrack(0, [], 0)
    return sorted(list(results), key=lambda t: (len(t), t))


# ─── 6. Matrix Balance & Zero-Sum Analyzer ─────────────────────────────────────


class ZeroSumMatrixAnalyzer:
    """
    Analyzes 2D integer matrices for zero-sum rows, columns, and overall balance.
    """

    def __init__(self, matrix: List[List[int]]):
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")

        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0

    def zero_sum_rows(self) -> List[int]:
        """Returns row indices whose elements sum to zero."""
        return [r for r, row in enumerate(self.matrix) if sum(row) == 0]

    def zero_sum_cols(self) -> List[int]:
        """Returns column indices whose elements sum to zero."""
        results = []
        for c in range(self.cols):
            col_sum = sum(self.matrix[r][c] for r in range(self.rows))
            if col_sum == 0:
                results.append(c)
        return results

    def is_perfect_zero_sum_matrix(self) -> bool:
        """True if all rows and all columns independently sum to zero."""
        return (
            len(self.zero_sum_rows()) == self.rows
            and len(self.zero_sum_cols()) == self.cols
        )


# ─── 7. Solution Validator & Dataset Generator ─────────────────────────────────


def validate_zero_sum_triplets(triplets: List[Tuple[int, int, int]]) -> bool:
    """
    Validates that every triplet in the list sums to 0 and all triplets are unique.

    Args:
        triplets: List of 3-element tuples.

    Returns:
        True if all triplets are valid and unique.
    """
    seen: Set[Tuple[int, int, int]] = set()
    for t in triplets:
        if len(t) != 3 or sum(t) != 0:
            return False
        if t in seen:
            return False
        seen.add(t)
    return True


def generate_zero_sum_dataset(size: int = 20, seed: Optional[int] = None) -> List[int]:
    """
    Generates a synthetic list of integers containing guaranteed zero-sum pairs and triplets.

    Args:
        size: Target list size.
        seed: Random seed.

    Returns:
        List of positive and negative integers.
    """
    if seed is not None:
        random.seed(seed)

    data: List[int] = []
    half = size // 2
    for _ in range(half):
        val = random.randint(1, 50)
        data.extend([val, -val])

    while len(data) < size:
        data.append(random.randint(-20, 20))

    random.shuffle(data)
    return data


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestSumZeroOperations(unittest.TestCase):
    def test_two_sum_zero(self):
        nums = [-3, -1, 0, 1, 3, 5]
        pairs = two_sum_zero(nums)
        self.assertEqual(pairs, [(-3, 3), (-1, 1)])

    def test_three_sum_standard(self):
        nums = [-1, 0, 1, 2, -1, -4]
        triplets = three_sum(nums)
        expected = [(-1, -1, 2), (-1, 0, 1)]
        self.assertEqual(triplets, expected)
        self.assertTrue(validate_zero_sum_triplets(triplets))

    def test_three_sum_edge_cases(self):
        self.assertEqual(three_sum([0, 0, 0, 0]), [(0, 0, 0)])
        self.assertEqual(three_sum([1, 2, 3]), [])
        self.assertEqual(three_sum([1]), [])

    def test_k_sum_and_four_sum(self):
        nums = [1, 0, -1, 0, -2, 2]
        quads = four_sum_zero(nums)
        expected = [(-2, -1, 1, 2), (-2, 0, 0, 2), (-1, 0, 0, 1)]
        self.assertEqual(quads, expected)

    def test_subarray_sum_zero(self):
        nums = [4, 2, -3, 1, 6]
        self.assertTrue(has_zero_sum_subarray(nums))
        ranges = subarray_sum_zero(nums)
        self.assertIn((1, 3), ranges)  # 2 + (-3) + 1 = 0

    def test_three_sum_closest(self):
        nums = [-1, 2, 1, -4]
        self.assertEqual(three_sum_closest(nums, target=1), 2)

    def test_subset_sum_zero(self):
        nums = [-2, 1, 1]
        subsets = subset_sum_zero(nums)
        self.assertIn((-2, 1, 1), subsets)

    def test_matrix_analyzer_and_validator(self):
        matrix = [
            [1, -1],
            [-1, 1],
        ]
        analyzer = ZeroSumMatrixAnalyzer(matrix)
        self.assertEqual(analyzer.zero_sum_rows(), [0, 1])
        self.assertTrue(analyzer.is_perfect_zero_sum_matrix())


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" 🔢 Day 53: Sum Zero (3Sum / K-Sum) - Interactive Demo")
    print("=" * 60)

    sample_nums = [-1, 0, 1, 2, -1, -4, 3, -2]
    print(f"\n1. Input Array:\n   {sample_nums}")

    # 2. 2Sum and 3Sum Zero Solutions
    print("\n2. Unique Pairs Summing to 0 (2Sum):")
    print(f"   {two_sum_zero(sample_nums)}")

    print("\n3. Unique Triplets Summing to 0 (3Sum):")
    triplets = three_sum(sample_nums)
    for trip in triplets:
        print(f"   {trip} -> sum = {sum(trip)}")

    # 4. 4Sum Zero Solutions
    print("\n4. Unique Quadruplets Summing to 0 (4Sum):")
    quads = four_sum_zero(sample_nums)
    for q in quads:
        print(f"   {q} -> sum = {sum(q)}")

    # 5. Continuous Subarray Zero Sum
    print("\n5. Contiguous Subarrays Summing to 0:")
    sub_ranges = subarray_sum_zero(sample_nums)
    for start, end in sub_ranges:
        sub_arr = sample_nums[start : end + 1]
        print(f"   Indices [{start}:{end}] -> {sub_arr} (sum = {sum(sub_arr)})")

    # 6. Unit Test Suite Execution
    print("\n6. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSumZeroOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








