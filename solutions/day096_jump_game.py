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
