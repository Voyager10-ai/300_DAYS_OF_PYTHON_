import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day090_sum_list_recursion import (
    sum_list_recursive_slice,
    sum_list_recursive_index,
    sum_list_tail_recursive,
    sum_list_divide_and_conquer,
    sum_list_pairwise,
    sum_nested_list,
    sum_nested_list_weighted,
    sum_nested_list_inverse_weighted,
)


class TestDay090SumListRecursion(unittest.TestCase):
    """Unit tests for Day 90 Sum of List Recursion."""

    def test_basic_summation(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(sum_list_recursive_index(arr), 15)
        self.assertEqual(sum_list_divide_and_conquer(arr), 15)
        self.assertEqual(sum_list_tail_recursive(arr), 15)

    def test_nested_list(self):
        nested = [1, [2, [3, 4], 5], [[6]], 7]
        self.assertEqual(sum_nested_list(nested), 28)

    def test_weighted_nested(self):
        nested = [[1, 1], 2, [1, 1]]
        self.assertEqual(sum_nested_list_weighted(nested), 10)
        self.assertEqual(sum_nested_list_inverse_weighted(nested), 8)


if __name__ == "__main__":
    unittest.main()
