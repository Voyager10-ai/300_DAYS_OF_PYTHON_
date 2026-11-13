# Day 96: Jump Game (LeetCode 55 & 45)
#
# Problem:
#   You are given an integer array nums. You are initially positioned at the array's
#   first index, and each element in the array represents your maximum jump length
#   at that position.
#   Return true if you can reach the last index, or false otherwise.
#   Includes:
#     - Greedy forward maximum reach scan O(n) time, O(1) space
#     - Greedy backward destination shift O(n) time, O(1) space
#     - Dynamic Programming memoization approach O(n^2) worst case
#     - LeetCode 55 Solution wrapper
#     - Jump Game II: Minimum jumps to reach end (LeetCode 45) O(n)
#     - Complete jump path trajectory reconstructor
#     - Jump Game III: Bidirectional zero reachability (LeetCode 1306)
#     - ASCII jump arc & reach envelope visualizer
#     - Multi-algorithm performance benchmark
#     - Comprehensive unit tests and Java practice code

import time
import unittest
from collections import deque
from typing import List, Dict, Tuple, Set, Any, Optional


# ─── 1. Core Jump Game Solvers (LeetCode 55) ───────────────────────────────────


def _validate_nums(nums: List[int]) -> int:
    """Validates that nums is a non-empty list of non-negative integers."""
    if not isinstance(nums, list):
        raise TypeError(f"nums must be a list, got {type(nums).__name__}")
    if not nums:
        raise ValueError("nums must not be empty")
    for idx, x in enumerate(nums):
        if not isinstance(x, int) or isinstance(x, bool):
            raise TypeError(f"Element at index {idx} must be an integer, got {type(x).__name__}")
        if x < 0:
            raise ValueError(f"Jump lengths must be non-negative, got {x} at index {idx}")
    return len(nums)


def can_jump_greedy(nums: List[int]) -> bool:
    """
    Determines if the last index is reachable using forward greedy maximum reach.

    At each index i:
      1. If i > max_reach, we are stranded and cannot proceed -> return False.
      2. Update max_reach = max(max_reach, i + nums[i]).
      3. If max_reach >= len(nums) - 1, destination is reachable -> return True.

    Time Complexity: O(n) single pass with early termination.
    Space Complexity: O(1) auxiliary space.

    Args:
        nums: List of non-negative integers.

    Returns:
        True if the last index can be reached, False otherwise.
    """
    n = _validate_nums(nums)
    max_reach = 0

    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        if i + jump > max_reach:
            max_reach = i + jump
        if max_reach >= n - 1:
            return True

    return max_reach >= n - 1


def can_jump_backward(nums: List[int]) -> bool:
    """
    Determines reachability by shifting the target destination backwards from n - 1 to 0.

    If an earlier index i can reach the current target (i + nums[i] >= target),
    we greedily update target = i. The array is traversable iff target reaches 0.

    Time Complexity: O(n) backward scan.
    Space Complexity: O(1) auxiliary space.

    Args:
        nums: List of non-negative integers.

    Returns:
        True if index 0 can reach index n - 1.
    """
    n = _validate_nums(nums)
    target = n - 1

    for i in range(n - 2, -1, -1):
        if i + nums[i] >= target:
            target = i

    return target == 0


def can_jump_dp(nums: List[int]) -> bool:
    """
    Determines reachability using bottom-up dynamic programming.

    dp[i] is True if index i can reach the last index.

    Time Complexity: O(n^2) worst case.
    Space Complexity: O(n) for the dp boolean table.

    Args:
        nums: List of non-negative integers.

    Returns:
        True if dp[0] is True, False otherwise.
    """
    n = _validate_nums(nums)
    dp = [False] * n
    dp[-1] = True

    for i in range(n - 2, -1, -1):
        max_jump = min(i + nums[i], n - 1)
        for j in range(i + 1, max_jump + 1):
            if dp[j]:
                dp[i] = True
                break

    return dp[0]


def can_jump_with_metrics(
    nums: List[int],
) -> Tuple[bool, Dict[str, Any]]:
    """
    Evaluates reachability while collecting jump exploration metrics.

    Args:
        nums: List of non-negative integers.

    Returns:
        Tuple of (is_reachable, metrics_dict).
    """
    t0 = time.perf_counter()
    n = _validate_nums(nums)
    max_reach = 0
    zero_traps = 0
    steps_evaluated = 0

    reachable = True
    for i, jump in enumerate(nums):
        steps_evaluated += 1
        if i > max_reach:
            reachable = False
            break
        if jump == 0 and i < n - 1:
            zero_traps += 1
        max_reach = max(max_reach, i + jump)
        if max_reach >= n - 1:
            reachable = True
            break

    elapsed = time.perf_counter() - t0
    metrics = {
        "length": n,
        "reachable": reachable,
        "max_reach_attained": max_reach,
        "steps_evaluated": steps_evaluated,
        "zero_traps_encountered": zero_traps,
        "time_seconds": elapsed,
        "algorithm": "Forward Greedy Reach O(n)",
    }
    return (reachable, metrics)


class Solution:
    """LeetCode 55: Jump Game solution wrapper."""

    def canJump(self, nums: List[int]) -> bool:
        """Returns True if you can reach the last index from index 0."""
        return can_jump_greedy(nums)



# ─── 2. Jump Game II (Min Jumps), Path Reconstruction & Jump Game III ─────────


def jump_game_ii_min_jumps(nums: List[int]) -> int:
    """
    LeetCode 45: Jump Game II.
    Computes the minimum number of jumps required to reach the last index.

    Greedy Range Extension (BFS in O(1) space):
      Maintains `cur_end` (end of current jump range) and `farthest` (farthest reach
      possible from any point inside current jump range). When index hits `cur_end`,
      we must make another jump and set `cur_end = farthest`.

    Time Complexity: O(n).
    Space Complexity: O(1).

    Args:
        nums: List of non-negative integers.

    Returns:
        Minimum jump count to reach len(nums) - 1, or -1 if unreachable.
    """
    n = _validate_nums(nums)
    if n <= 1:
        return 0

    jumps = 0
    cur_end = 0
    farthest = 0

    for i in range(n - 1):
        if i > farthest:
            return -1  # Unreachable

        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
            if cur_end >= n - 1:
                break

    return jumps if cur_end >= n - 1 else -1


def reconstruct_jump_path(nums: List[int]) -> Optional[List[int]]:
    """
    Finds and reconstructs a minimal-jump path from index 0 to len(nums) - 1.

    Args:
        nums: List of non-negative integers.

    Returns:
        List of 0-based indices representing the jump path (e.g. [0, 1, 4]),
        or None if destination is unreachable.
    """
    n = _validate_nums(nums)
    if n == 1:
        return [0]
    if nums[0] == 0:
        return None

    # BFS to track parent pointers for shortest path reconstruction
    queue: deque = deque([0])
    parent: Dict[int, int] = {0: -1}
    visited: Set[int] = {0}
    max_reached = 0

    while queue:
        curr = queue.popleft()
        reach = curr + nums[curr]

        if reach >= n - 1:
            # Reconstruct path backwards
            path = [n - 1]
            p = curr
            while p != -1:
                path.append(p)
                p = parent[p]
            return path[::-1]

        # Only queue newly reachable unexplored indices to retain O(n) runtime
        start_probe = max(curr + 1, max_reached + 1)
        end_probe = min(reach, n - 1)
        for nxt in range(start_probe, end_probe + 1):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = curr
                queue.append(nxt)

        max_reached = max(max_reached, reach)

    return None


def jump_game_iii_reach_zero(arr: List[int], start: int) -> bool:
    """
    LeetCode 1306: Jump Game III.
    Given an array of non-negative integers arr and a starting index, determine
    if you can reach any index with value 0.
    At index i, you can jump to i + arr[i] or i - arr[i] if valid.

    Time Complexity: O(n).
    Space Complexity: O(n) for BFS queue and visited set.

    Args:
        arr: List of non-negative integers.
        start: 0-based starting index.

    Returns:
        True if an index with value 0 is reachable, False otherwise.
    """
    if not isinstance(arr, list):
        raise TypeError("arr must be a list")
    if not (0 <= start < len(arr)):
        raise ValueError(f"start index {start} out of bounds for len {len(arr)}")

    queue: deque = deque([start])
    visited: Set[int] = {start}

    while queue:
        node = queue.popleft()
        if arr[node] == 0:
            return True

        for next_node in (node + arr[node], node - arr[node]):
            if 0 <= next_node < len(arr) and next_node not in visited:
                visited.add(next_node)
                queue.append(next_node)

    return False



# ─── 3. ASCII Jump Trajectory Visualizer & Benchmarking ───────────────────────


def visualize_jump_trajectory(nums: List[int]) -> str:
    """
    Renders an ASCII diagram illustrating array jump reach and optimal path trajectory.

    Args:
        nums: Input list of integers (recommended length <= 15 for readable display).

    Returns:
        Formatted ASCII diagram string.
    """
    n = _validate_nums(nums)
    lines: List[str] = []
    lines.append(f"Jump Game Trajectory Visualization for nums = {nums}")
    lines.append("=" * 72)

    # 1. Index & Values Table
    header = f"{'Index':>7} | " + " | ".join(f"{i:>3}" for i in range(n))
    vals = f"{'Value':>7} | " + " | ".join(f"{nums[i]:>3}" for i in range(n))
    reach = f"{'Reach':>7} | " + " | ".join(f"{min(i + nums[i], n - 1):>3}" for i in range(n))

    lines.append(header)
    lines.append("-" * len(header))
    lines.append(vals)
    lines.append(reach)
    lines.append("=" * 72)

    # 2. Optimal Path & Reachability Analysis
    path = reconstruct_jump_path(nums)
    if path is not None:
        lines.append(f"Optimal Shortest Jump Path (Min Jumps = {len(path) - 1}):")
        path_str = " -> ".join(f"idx[{p}](val={nums[p]})" for p in path)
        lines.append(f"  {path_str} [TARGET REACHED!]")
    else:
        lines.append("[!] Target Unreachable: Zero-trap blocked all forward paths.")

    lines.append("=" * 72)
    return "\n".join(lines)


def benchmark_jump_algorithms(
    sizes: Optional[List[int]] = None,
    iterations: int = 15,
) -> Dict[str, Any]:
    """
    Benchmarks Jump Game algorithms across increasing array sizes.

    Algorithms:
      - Forward Greedy Max-Reach O(n)
      - Backward Greedy Target Shift O(n)
      - Jump Game II Min Jumps BFS O(n)
      - Dynamic Programming O(n^2) (tested on sizes <= 2000)

    Args:
        sizes: List of array sizes.
        iterations: Number of runs per benchmark point.

    Returns:
        Structured benchmark metrics dictionary.
    """
    if sizes is None:
        sizes = [100, 1000, 5000, 20000]

    import random
    rng = random.Random(42)
    records: List[Dict[str, Any]] = []

    for n in sizes:
        # Generate reachable array with occasional traps
        nums = [rng.randint(1, 4) for _ in range(n)]
        row: Dict[str, Any] = {"length": n}

        # 1. Forward Greedy
        times: List[float] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            can_jump_greedy(nums)
            times.append(time.perf_counter() - t0)
        row["forward"] = min(times)

        # 2. Backward Greedy
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            can_jump_backward(nums)
            times.append(time.perf_counter() - t0)
        row["backward"] = min(times)

        # 3. Min Jumps (Jump Game II)
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            jump_game_ii_min_jumps(nums)
            times.append(time.perf_counter() - t0)
        row["min_jumps"] = min(times)

        # 4. DP (n <= 2000)
        if n <= 2000:
            times = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                can_jump_dp(nums)
                times.append(time.perf_counter() - t0)
            row["dp"] = min(times)
        else:
            row["dp"] = None

        records.append(row)

    return {"records": records, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """Formats the Jump Game benchmark output into an ASCII table."""
    lines: List[str] = []
    lines.append("Jump Game Algorithms Performance Benchmark")
    lines.append("=" * 76)
    header = (
        f"{'Length':>8} | {'Forward Greedy':>16} | {'Backward Greedy':>17} | "
        f"{'Min Jumps O(n)':>16} | {'DP O(n^2)':>10}"
    )
    lines.append(header)
    lines.append("-" * 76)

    def _fmt(val: Optional[float]) -> str:
        if val is None:
            return "N/A (>O(n))"
        us = val * 1_000_000.0
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['length']:>8} | "
            f"{_fmt(r['forward']):>16} | "
            f"{_fmt(r['backward']):>17} | "
            f"{_fmt(r['min_jumps']):>16} | "
            f"{_fmt(r['dp']):>10}"
        )
        lines.append(line)

    lines.append("=" * 76)
    return "\n".join(lines)



# ─── 4. Comprehensive Unit Test Suite ────────────────────────────────────────


class TestJumpGame(unittest.TestCase):
    """Exhaustive unit test suite verifying Jump Game variants, traps, and paths."""

    def test_leetcode_55_reachability(self) -> None:
        """Tests standard reachability cases for LeetCode 55."""
        sol = Solution()

        # Reachable
        reachable = [2, 3, 1, 1, 4]
        self.assertTrue(can_jump_greedy(reachable))
        self.assertTrue(can_jump_backward(reachable))
        self.assertTrue(can_jump_dp(reachable))
        self.assertTrue(sol.canJump(reachable))

        # Unreachable trap
        trapped = [3, 2, 1, 0, 4]
        self.assertFalse(can_jump_greedy(trapped))
        self.assertFalse(can_jump_backward(trapped))
        self.assertFalse(can_jump_dp(trapped))
        self.assertFalse(sol.canJump(trapped))

    def test_single_element_and_zeros(self) -> None:
        """Tests boundary edge cases."""
        self.assertTrue(can_jump_greedy([0]))
        self.assertTrue(can_jump_backward([0]))
        self.assertTrue(can_jump_greedy([2, 0, 0]))
        self.assertFalse(can_jump_greedy([1, 0, 2]))
        self.assertTrue(can_jump_greedy([2, 5, 0, 0]))

    def test_jump_game_ii_min_jumps(self) -> None:
        """Tests minimum jumps calculation (LeetCode 45)."""
        self.assertEqual(jump_game_ii_min_jumps([2, 3, 1, 1, 4]), 2)
        self.assertEqual(jump_game_ii_min_jumps([2, 3, 0, 1, 4]), 2)
        self.assertEqual(jump_game_ii_min_jumps([0]), 0)
        self.assertEqual(jump_game_ii_min_jumps([1, 2, 3]), 2)
        self.assertEqual(jump_game_ii_min_jumps([3, 2, 1, 0, 4]), -1)

    def test_path_reconstruction(self) -> None:
        """Verifies reconstruct_jump_path yields valid continuous jumping sequence."""
        nums = [2, 3, 1, 1, 4]
        path = reconstruct_jump_path(nums)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 0)  # type: ignore
        self.assertEqual(path[-1], len(nums) - 1)  # type: ignore

        # Verify each jump in path was within bounds
        for i in range(len(path) - 1):  # type: ignore
            curr_idx = path[i]  # type: ignore
            next_idx = path[i + 1]  # type: ignore
            self.assertLessEqual(next_idx - curr_idx, nums[curr_idx])

        self.assertIsNone(reconstruct_jump_path([3, 2, 1, 0, 4]))

    def test_jump_game_iii_reach_zero(self) -> None:
        """Tests bidirectional jump reachability to zero (LeetCode 1306)."""
        self.assertTrue(jump_game_iii_reach_zero([4, 2, 3, 0, 3, 1, 2], 5))
        self.assertTrue(jump_game_iii_reach_zero([4, 2, 3, 0, 3, 1, 2], 0))
        self.assertFalse(jump_game_iii_reach_zero([3, 0, 2, 1, 2], 2))

    def test_metrics_structure(self) -> None:
        """Verifies metrics structure and collected parameters."""
        reach, m = can_jump_with_metrics([2, 3, 1, 1, 4])
        self.assertTrue(reach)
        self.assertEqual(m["length"], 5)
        self.assertGreaterEqual(m["max_reach_attained"], 4)

    def test_type_validation(self) -> None:
        """Ensures non-list or invalid entries raise TypeError/ValueError."""
        with self.assertRaises(TypeError):
            can_jump_greedy("not a list")  # type: ignore
        with self.assertRaises(ValueError):
            can_jump_greedy([])
        with self.assertRaises(ValueError):
            can_jump_greedy([1, -2, 3])
