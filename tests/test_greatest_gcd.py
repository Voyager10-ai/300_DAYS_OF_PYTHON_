import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day089_greatest_gcd import (
    gcd_naive,
    gcd_subtraction,
    gcd_euclidean_iterative,
    gcd_euclidean_recursive,
    gcd_binary_stein,
    extended_gcd,
    modular_inverse,
    solve_linear_diophantine,
    gcd_list,
    lcm,
    lcm_list,
    are_coprime,
    gcd_smallest_and_largest,
    find_greatest_gcd_pair,
)


class TestDay089GreatestGCD(unittest.TestCase):
    """Unit tests for Day 89 Greatest GCD Suite."""

    def test_basic_gcd(self):
        self.assertEqual(gcd_euclidean_iterative(48, 18), 6)
        self.assertEqual(gcd_binary_stein(48, 18), 6)
        self.assertEqual(gcd_euclidean_recursive(48, 18), 6)

    def test_extended_gcd(self):
        g, x, y = extended_gcd(252, 105)
        self.assertEqual(252 * x + 105 * y, g)
        self.assertEqual(g, 21)

    def test_modular_inverse(self):
        self.assertEqual(modular_inverse(3, 11), 4)

    def test_lcm(self):
        self.assertEqual(lcm(12, 18), 36)
        self.assertEqual(lcm_list([2, 3, 4, 5, 6]), 60)

    def test_array_greatest_gcd(self):
        self.assertEqual(gcd_smallest_and_largest([2, 5, 6, 9, 10]), 2)
        max_g, a, b = find_greatest_gcd_pair([10, 15, 20, 25, 30])
        self.assertEqual(max_g, 15)


if __name__ == "__main__":
    unittest.main()
