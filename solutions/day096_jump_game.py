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
