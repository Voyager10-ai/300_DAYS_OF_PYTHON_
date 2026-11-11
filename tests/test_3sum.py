import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day091_3sum import (
    Solution,
    three_sum_brute_force,
    three_sum_hashset,
    three_sum_two_pointer,
    three_sum_closest,
    three_sum_smaller,
    k_sum,
)


class TestDay091ThreeSum(unittest.TestCase):
    """Unit tests for Day 91 3Sum Suite."""

    def test_standard_3sum(self):
        sol = Solution()
        nums = [-1, 0, 1, 2, -1, -4]
        expected = [[-1, -1, 2], [-1, 0, 1]]
        self.assertEqual(sol.threeSum(nums), expected)
        self.assertEqual(three_sum_brute_force(nums), expected)
        self.assertEqual(three_sum_hashset(nums), expected)
        self.assertEqual(three_sum_two_pointer(nums), expected)

    def test_3sum_closest_and_smaller(self):
        self.assertEqual(three_sum_closest([-1, 2, 1, -4], 1), 2)
        self.assertEqual(three_sum_smaller([-2, 0, 1, 3], 2), 2)

    def test_ksum_4sum(self):
        self.assertEqual(
            k_sum([1, 0, -1, 0, -2, 2], 0, 4),
            [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]],
        )


if __name__ == "__main__":
    unittest.main()