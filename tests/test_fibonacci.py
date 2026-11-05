import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day087_fibonacci import (
    fibonacci_recursive,
    fibonacci_iterative,
    fibonacci_memoized,
    fibonacci_lru_cached,
    fibonacci_fast_doubling,
    fibonacci_fast_doubling_iterative,
    fibonacci_matrix,
    fibonacci_binet,
    fibonacci_binet_decimal,
    fibonacci_generator,
    fibonacci_sequence_list,
    is_fibonacci_number,
    nearest_fibonacci,
    fibonacci_search,
)


class TestDay087Fibonacci(unittest.TestCase):
    """Unit tests for Day 87 Fibonacci Suite."""

    def setUp(self):
        self.known_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

    def test_algorithms_consistency(self):
        for n, expected in enumerate(self.known_sequence):
            self.assertEqual(fibonacci_recursive(n), expected)
            self.assertEqual(fibonacci_iterative(n), expected)
            self.assertEqual(fibonacci_memoized(n), expected)
            self.assertEqual(fibonacci_lru_cached(n), expected)
            self.assertEqual(fibonacci_fast_doubling(n), expected)
            self.assertEqual(fibonacci_fast_doubling_iterative(n), expected)
            self.assertEqual(fibonacci_matrix(n), expected)
            self.assertEqual(fibonacci_binet(n), expected)
            self.assertEqual(fibonacci_binet_decimal(n), expected)

    def test_large_values(self):
        n = 100
        val_iter = fibonacci_iterative(n)
        self.assertEqual(fibonacci_fast_doubling_iterative(n), val_iter)
        self.assertEqual(fibonacci_matrix(n), val_iter)
        self.assertEqual(fibonacci_binet_decimal(n), val_iter)

    def test_fibonacci_search(self):
        arr = [1, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        for idx, val in enumerate(arr):
            self.assertEqual(fibonacci_search(arr, val), idx)
        self.assertEqual(fibonacci_search(arr, 999), -1)

    def test_is_fibonacci(self):
        self.assertTrue(is_fibonacci_number(89))
        self.assertFalse(is_fibonacci_number(90))


if __name__ == "__main__":
    unittest.main()
