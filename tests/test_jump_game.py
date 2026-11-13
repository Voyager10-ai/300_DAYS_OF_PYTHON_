import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day096_jump_game import (
    Solution,
    can_jump_greedy,
    can_jump_backward,
    can_jump_dp,
    jump_game_ii_min_jumps,
    reconstruct_jump_path,
    jump_game_iii_reach_zero,
)


class TestDay096JumpGame(unittest.TestCase):
    """Unit tests for Day 96 Jump Game."""

    def test_standard_cases(self):
        sol = Solution()
        self.assertTrue(sol.canJump([2, 3, 1, 1, 4]))
        self.assertFalse(sol.canJump([3, 2, 1, 0, 4]))
        self.assertTrue(can_jump_greedy([2, 3, 1, 1, 4]))
        self.assertTrue(can_jump_backward([2, 3, 1, 1, 4]))
        self.assertTrue(can_jump_dp([2, 3, 1, 1, 4]))

    def test_jump_game_ii_and_path(self):
        self.assertEqual(jump_game_ii_min_jumps([2, 3, 1, 1, 4]), 2)
        path = reconstruct_jump_path([2, 3, 1, 1, 4])
        self.assertEqual(path, [0, 1, 4])

    def test_jump_game_iii(self):
        self.assertTrue(jump_game_iii_reach_zero([4, 2, 3, 0, 3, 1, 2], 5))
        self.assertFalse(jump_game_iii_reach_zero([3, 0, 2, 1, 2], 2))


if __name__ == "__main__":
    unittest.main()
