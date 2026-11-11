# Day 91: 3Sum (LeetCode 15 & Extensions)
#
# Problem:
#   Given an integer array nums, return all unique triplets [nums[i], nums[j], nums[k]]
#   such that i != j, i != k, j != k, and nums[i] + nums[j] + nums[k] == 0.
#   Notice that the solution set must not contain duplicate triplets.
#   Includes:
#     - Naive Brute Force O(n^3) with set deduplication
#     - Hash-Set 2Sum reduction O(n^2) time, O(n) auxiliary space
#     - Optimal Sorted Two-Pointer O(n^2) time, O(1) extra space + pruning
#     - LeetCode 15 Solution class
#     - Extensions: 3Sum Closest (LC 16), 3Sum Smaller (LC 259), and generalized kSum
#     - Step-by-step Two-Pointer trace visualizer
#     - Performance benchmark comparing all algorithms
#     - Comprehensive unit tests and Java practice code

import time
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional


# ─── 1. Naive Brute Force & Hash-Set 3Sum Implementations ─────────────────────


def three_sum_brute_force(nums: List[int], target: int = 0) -> List[List[int]]:
    """
    Finds all unique triplets summing to target using exhaustive O(n^3) triple loops.

    Time Complexity: O(n^3).
    Space Complexity: O(k) where k is the number of unique valid triplets stored in a set.

    Args:
        nums: Input list of integers.
        target: Target triplet sum (defaults to 0).

    Returns:
        Sorted list of unique sorted triplets.

    Raises:
        TypeError: If nums is not a list or contains non-integers.
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")
    for idx, val in enumerate(nums):
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(f"Element at index {idx} must be an integer, got {type(val).__name__}")
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError(f"target must be an integer, got {type(target).__name__}")

    n = len(nums)
    if n < 3:
        return []

    seen: Set[Tuple[int, int, int]] = set()
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == target:
                    triplet = tuple(sorted((nums[i], nums[j], nums[k])))
                    seen.add(triplet)  # type: ignore

    return [list(t) for t in sorted(seen)]


def three_sum_hashset(nums: List[int], target: int = 0) -> List[List[int]]:
    """
    Finds all unique triplets summing to target by reducing 3Sum to 2Sum via a hash set.

    Time Complexity: O(n^2) average.
    Space Complexity: O(n) for the inner lookup hash set and deduplication set.

    Args:
        nums: Input list of integers.
        target: Target triplet sum (defaults to 0).

    Returns:
        Sorted list of unique sorted triplets.
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")
    if len(nums) < 3:
        return []

    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    res: Set[Tuple[int, int, int]] = set()

    for i in range(n - 2):
        # Skip duplicate anchors
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue
        seen: Set[int] = set()
        for j in range(i + 1, n):
            complement = target - sorted_nums[i] - sorted_nums[j]
            if complement in seen:
                res.add((sorted_nums[i], complement, sorted_nums[j]))
            seen.add(sorted_nums[j])

    return [list(t) for t in sorted(res)]


def three_sum_with_metrics(
    nums: List[int],
    target: int = 0,
) -> Tuple[List[List[int]], Dict[str, Any]]:
    """
    Solves 3Sum using the hash-set approach while recording operation statistics.

    Args:
        nums: Input list of integers.
        target: Target triplet sum.

    Returns:
        Tuple of (triplets, metrics_dict).
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")

    t0 = time.perf_counter()
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    res: Set[Tuple[int, int, int]] = set()
    hash_lookups = 0

    for i in range(n - 2):
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue
        seen: Set[int] = set()
        for j in range(i + 1, n):
            complement = target - sorted_nums[i] - sorted_nums[j]
            hash_lookups += 1
            if complement in seen:
                res.add((sorted_nums[i], complement, sorted_nums[j]))
            seen.add(sorted_nums[j])

    elapsed = time.perf_counter() - t0
    triplets = [list(t) for t in sorted(res)]
    metrics = {
        "input_length": n,
        "target": target,
        "triplets_found": len(triplets),
        "hash_lookups": hash_lookups,
        "time_seconds": elapsed,
        "algorithm": "Hash-Set 2Sum Reduction O(n^2)",
    }
    return (triplets, metrics)



# ─── 2. Optimal Sorted Two-Pointer 3Sum & LeetCode Solution ───────────────────


def three_sum_two_pointer(nums: List[int], target: int = 0) -> List[List[int]]:
    """
    Finds all unique triplets summing to target using sorted two-pointer technique.

    Uses early-exit pruning bounds:
      1. If nums[i] + nums[i+1] + nums[i+2] > target -> break (all remaining sums exceed target)
      2. If nums[i] + nums[-2] + nums[-1] < target -> continue (anchor too small)

    Time Complexity: O(n^2) after O(n log n) sort.
    Space Complexity: O(1) auxiliary space (excluding output list and sort buffer).

    Args:
        nums: Input list of integers.
        target: Target triplet sum (defaults to 0).

    Returns:
        List of unique sorted triplets summing to target.
    """
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")
    for idx, val in enumerate(nums):
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(f"Element at index {idx} must be an integer, got {type(val).__name__}")

    n = len(nums)
    if n < 3:
        return []

    arr = sorted(nums)
    result: List[List[int]] = []

    for i in range(n - 2):
        # Skip duplicate anchor values
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        # Lower-bound pruning
        if arr[i] + arr[i + 1] + arr[i + 2] > target:
            break

        # Upper-bound pruning
        if arr[i] + arr[n - 2] + arr[n - 1] < target:
            continue

        left, right = i + 1, n - 1
        while left < right:
            curr_sum = arr[i] + arr[left] + arr[right]
            if curr_sum < target:
                left += 1
            elif curr_sum > target:
                right -= 1
            else:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicate left and right values
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1

    return result


class Solution:
    """LeetCode 15: 3Sum solution wrapper."""

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """Finds all unique triplets in nums which give the sum of zero."""
        return three_sum_two_pointer(nums, target=0)



# ─── 3. 3Sum Variants & Generalized kSum Solver ───────────────────────────────


def three_sum_closest(nums: List[int], target: int) -> int:
    """
    LeetCode 16: 3Sum Closest.
    Finds three integers in nums such that their sum is closest to target.

    Time Complexity: O(n^2).
    Space Complexity: O(1) auxiliary space (after sort).

    Args:
        nums: List of integers (length >= 3).
        target: Target integer.

    Returns:
        Sum of the three integers closest to target.

    Raises:
        ValueError: If len(nums) < 3.
    """
    if len(nums) < 3:
        raise ValueError("nums must contain at least 3 elements")

    arr = sorted(nums)
    n = len(arr)
    closest = arr[0] + arr[1] + arr[2]

    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        left, right = i + 1, n - 1
        while left < right:
            curr_sum = arr[i] + arr[left] + arr[right]
            if curr_sum == target:
                return target

            if abs(curr_sum - target) < abs(closest - target):
                closest = curr_sum

            if curr_sum < target:
                left += 1
            else:
                right -= 1

    return closest


def three_sum_smaller(nums: List[int], target: int) -> int:
    """
    LeetCode 259: 3Sum Smaller.
    Counts index triplets (i, j, k) with 0 <= i < j < k < n satisfying:
        nums[i] + nums[j] + nums[k] < target

    Time Complexity: O(n^2).
    Space Complexity: O(1) auxiliary space.

    Args:
        nums: List of integers.
        target: Exclusive upper bound integer.

    Returns:
        Count of valid index triplets.
    """
    if len(nums) < 3:
        return 0

    arr = sorted(nums)
    n = len(arr)
    count = 0

    for i in range(n - 2):
        left, right = i + 1, n - 1
        while left < right:
            if arr[i] + arr[left] + arr[right] < target:
                # Every element between left+1 and right also satisfies < target
                count += right - left
                left += 1
            else:
                right -= 1

    return count


def k_sum(nums: List[int], target: int, k: int) -> List[List[int]]:
    """
    Generalized k-Sum solver finding all unique k-tuples summing to target.

    Supports k >= 2 (2Sum, 3Sum, 4Sum, ...).
    Uses recursive dimensionality reduction down to O(n) two-pointer 2Sum.

    Time Complexity: O(n^(k-1)) for k >= 2.

    Args:
        nums: List of integers.
        target: Target tuple sum.
        k: Number of elements per tuple (k >= 2).

    Returns:
        List of unique sorted k-tuples summing to target.
    """
    if k < 2:
        raise ValueError(f"k must be >= 2, got {k}")
    if len(nums) < k:
        return []

    arr = sorted(nums)

    def _two_sum(start: int, tgt: int) -> List[List[int]]:
        res: List[List[int]] = []
        lo, hi = start, len(arr) - 1
        while lo < hi:
            curr = arr[lo] + arr[hi]
            if curr < tgt or (lo > start and arr[lo] == arr[lo - 1]):
                lo += 1
            elif curr > tgt or (hi < len(arr) - 1 and arr[hi] == arr[hi + 1]):
                hi -= 1
            else:
                res.append([arr[lo], arr[hi]])
                lo += 1
                hi -= 1
        return res

    def _ksum_helper(start: int, tgt: int, k_rem: int) -> List[List[int]]:
        res: List[List[int]] = []
        if start >= len(arr):
            return res

        # Early termination pruning using average bounds
        avg_val = tgt // k_rem
        if arr[start] > avg_val or arr[-1] < avg_val:
            return res

        if k_rem == 2:
            return _two_sum(start, tgt)

        for i in range(start, len(arr) - k_rem + 1):
            if i == start or arr[i] != arr[i - 1]:
                for subset in _ksum_helper(i + 1, tgt - arr[i], k_rem - 1):
                    res.append([arr[i]] + subset)

        return res

    return _ksum_helper(0, target, k)



# ─── 4. Two-Pointer Trace Visualizer & Performance Benchmarking ───────────────


def visualize_three_sum_trace(nums: List[int], target: int = 0) -> str:
    """
    Renders an ASCII trace table showing two-pointer convergence for 3Sum.

    Args:
        nums: Input list of integers.
        target: Target sum (defaults to 0).

    Returns:
        Formatted ASCII trace string.
    """
    if len(nums) < 3:
        return "Array too short (< 3 elements) for 3Sum trace."

    arr = sorted(nums)
    n = len(arr)
    lines: List[str] = []
    lines.append(f"3Sum Two-Pointer Convergence Trace (Sorted: {arr}, Target = {target})")
    lines.append("=" * 84)
    header = f"{'Anchor i':>10} | {'Left L':>10} | {'Right R':>10} | {'Triplet':>16} | {'Sum':>6} | {'Action':>18}"
    lines.append(header)
    lines.append("-" * 84)

    found: List[List[int]] = []

    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            lines.append(f"{f'{i}({arr[i]})':>10} | {'-':>10} | {'-':>10} | {'-':>16} | {'-':>6} | SKIP DUPLICATE i")
            continue

        left, right = i + 1, n - 1
        while left < right:
            s = arr[i] + arr[left] + arr[right]
            triplet_str = f"[{arr[i]}, {arr[left]}, {arr[right]}]"
            l_str = f"{left}({arr[left]})"
            r_str = f"{right}({arr[right]})"
            i_str = f"{i}({arr[i]})"

            if s < target:
                lines.append(f"{i_str:>10} | {l_str:>10} | {r_str:>10} | {triplet_str:>16} | {s:>6} | s < tgt -> L++")
                left += 1
            elif s > target:
                lines.append(f"{i_str:>10} | {l_str:>10} | {r_str:>10} | {triplet_str:>16} | {s:>6} | s > tgt -> R--")
                right -= 1
            else:
                lines.append(f"{i_str:>10} | {l_str:>10} | {r_str:>10} | {triplet_str:>16} | {s:>6} | MATCH FOUND!")
                found.append([arr[i], arr[left], arr[right]])
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1

    lines.append("=" * 84)
    lines.append(f"Total Unique Triplets Found: {found}")
    return "\n".join(lines)


def benchmark_three_sum_algorithms(
    sizes: Optional[List[int]] = None,
    iterations: int = 3,
) -> Dict[str, Any]:
    """
    Benchmarks 3Sum algorithms across increasing array sizes.

    Algorithms:
      - Naive Brute Force O(n^3) (tested up to n = 120)
      - Hash-Set 2Sum Reduction O(n^2)
      - Optimal Sorted Two-Pointer O(n^2)
      - Generalized kSum (k = 3)

    Args:
        sizes: List of input array lengths.
        iterations: Runs per benchmark point.

    Returns:
        Structured benchmark metrics dictionary.
    """
    if sizes is None:
        sizes = [20, 60, 120, 300, 600]

    rng = random.Random(42)
    records: List[Dict[str, Any]] = []

    for n in sizes:
        data = [rng.randint(-n // 2, n // 2) for _ in range(n)]
        row: Dict[str, Any] = {"n": n}

        # 1. Brute Force (n <= 120)
        if n <= 120:
            times: List[float] = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                three_sum_brute_force(data)
                times.append(time.perf_counter() - t0)
            row["brute_force"] = min(times)
        else:
            row["brute_force"] = None

        # 2. Hash-Set
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            three_sum_hashset(data)
            times.append(time.perf_counter() - t0)
        row["hashset"] = min(times)

        # 3. Sorted Two-Pointer
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            three_sum_two_pointer(data)
            times.append(time.perf_counter() - t0)
        row["two_pointer"] = min(times)

        # 4. Generalized kSum (k=3)
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            k_sum(data, 0, 3)
            times.append(time.perf_counter() - t0)
        row["ksum"] = min(times)

        records.append(row)

    return {"records": records, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """Formats the 3Sum benchmark output into an ASCII table."""
    lines: List[str] = []
    lines.append("3Sum Algorithms Performance Benchmark")
    lines.append("=" * 84)
    header = (
        f"{'n':>7} | {'Brute Force O(n^3)':>19} | {'Hash-Set O(n^2)':>17} | "
        f"{'Two-Pointer O(n^2)':>19} | {'kSum (k=3)':>13}"
    )
    lines.append(header)
    lines.append("-" * 84)

    def _fmt(val: Optional[float]) -> str:
        if val is None:
            return "N/A (>100ms)"
        ms = val * 1000.0
        if ms < 1.0:
            return f"{ms * 1000.0:.2f} µs"
        return f"{ms:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['n']:>7} | "
            f"{_fmt(r['brute_force']):>19} | "
            f"{_fmt(r['hashset']):>17} | "
            f"{_fmt(r['two_pointer']):>19} | "
            f"{_fmt(r['ksum']):>13}"
        )
        lines.append(line)

    lines.append("=" * 84)
    return "\n".join(lines)



# ─── 5. Comprehensive Unit Test Suite ────────────────────────────────────────


class TestThreeSumImplementations(unittest.TestCase):
    """Exhaustive unit test suite verifying 3Sum algorithms and variants."""

    def test_standard_cases(self) -> None:
        """Verifies all 3Sum engines agree on standard LeetCode inputs."""
        cases = [
            ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
            ([0, 1, 1], []),
            ([0, 0, 0], [[0, 0, 0]]),
            ([0, 0, 0, 0], [[0, 0, 0]]),
            ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),
            ([], []),
            ([1, -1], []),
        ]
        sol = Solution()
        for nums, expected in cases:
            self.assertEqual(three_sum_brute_force(nums), expected)
            self.assertEqual(three_sum_hashset(nums), expected)
            self.assertEqual(three_sum_two_pointer(nums), expected)
            self.assertEqual(sol.threeSum(nums), expected)
            self.assertEqual(k_sum(nums, 0, 3), expected)

    def test_custom_target_and_ksum(self) -> None:
        """Tests non-zero target and 4Sum via k_sum."""
        nums = [1, 0, -1, 0, -2, 2]
        expected_4sum = [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
        self.assertEqual(k_sum(nums, 0, 4), expected_4sum)
        self.assertEqual(three_sum_two_pointer([1, 2, 3, 4], target=7), [[1, 2, 4]])

    def test_three_sum_closest(self) -> None:
        """Tests LeetCode 16: 3Sum Closest."""
        self.assertEqual(three_sum_closest([-1, 2, 1, -4], 1), 2)
        self.assertEqual(three_sum_closest([0, 0, 0], 1), 0)
        with self.assertRaises(ValueError):
            three_sum_closest([1, 2], 0)

    def test_three_sum_smaller(self) -> None:
        """Tests LeetCode 259: 3Sum Smaller."""
        self.assertEqual(three_sum_smaller([-2, 0, 1, 3], 2), 2)
        self.assertEqual(three_sum_smaller([], 0), 0)
        self.assertEqual(three_sum_smaller([0], 0), 0)

    def test_type_validation(self) -> None:
        """Ensures invalid inputs raise TypeError."""
        with self.assertRaises(TypeError):
            three_sum_two_pointer("not a list")  # type: ignore
        with self.assertRaises(TypeError):
            three_sum_two_pointer([1, "a", 3])  # type: ignore


# ─── 6. Interactive CLI Demonstration ────────────────────────────────────────


def main() -> None:
    """Demonstrates 3Sum implementations, variants, trace, and benchmark."""
    print("=" * 80)
    print("                     DAY 91: 3SUM & K-SUM SUITE                         ")
    print("=" * 80)

    nums = [-1, 0, 1, 2, -1, -4]
    print(f"\n[1] Algorithm Consistency for nums = {nums}:")
    print(f"    - Brute Force O(n^3) : {three_sum_brute_force(nums)}")
    print(f"    - Hash-Set O(n^2)    : {three_sum_hashset(nums)}")
    print(f"    - Two-Pointer O(n^2) : {three_sum_two_pointer(nums)}")
    print(f"    - Generalized kSum   : {k_sum(nums, 0, 3)}")

    print("\n[2] 3Sum Variants & 4Sum:")
    print(f"    - 3Sum Closest([-1, 2, 1, -4], target=1) : {three_sum_closest([-1, 2, 1, -4], 1)}")
    print(f"    - 3Sum Smaller([-2, 0, 1, 3], target=2)  : {three_sum_smaller([-2, 0, 1, 3], 2)}")
    print(f"    - 4Sum([1, 0, -1, 0, -2, 2], target=0)   : {k_sum([1, 0, -1, 0, -2, 2], 0, 4)}")

    print("\n[3] Step-by-Step Two-Pointer Trace:")
    print(visualize_three_sum_trace(nums))

    print("\n[4] Multi-Algorithm Benchmark Comparison:")
    bench = benchmark_three_sum_algorithms([20, 60, 120, 300], iterations=2)
    print(format_benchmark_table(bench))

    print("\n" + "=" * 80)
    print("                      DEMONSTRATION COMPLETE                                   ")
    print("=" * 80)


if __name__ == "__main__":
    main()
