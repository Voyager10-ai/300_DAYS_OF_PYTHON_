import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day088_factorial import (
    factorial_iterative,
    factorial_recursive,
    factorial_tail_recursive,
    factorial_binary_split,
    factorial_memoized,
    count_trailing_zeros,
    count_digits_in_factorial,
    prime_factor_exponent_in_factorial,
    subfactorial,
)


class TestDay088Factorial(unittest.TestCase):
    """Unit tests for Day 88 Factorial Suite."""

    def test_known_values(self):
        expected = [1, 1, 2, 6, 24, 120, 720, 5040]
        for n, val in enumerate(expected):
            self.assertEqual(factorial_iterative(n), val)
            self.assertEqual(factorial_binary_split(n), val)

    def test_trailing_zeros(self):
        self.assertEqual(count_trailing_zeros(0), 0)
        self.assertEqual(count_trailing_zeros(25), 6)
        self.assertEqual(count_trailing_zeros(100), 24)

    def test_subfactorial(self):
        self.assertEqual(subfactorial(4), 9)
        self.assertEqual(subfactorial(5), 44)


if __name__ == "__main__":
    unittest.main()
