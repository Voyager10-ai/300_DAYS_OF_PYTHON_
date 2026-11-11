import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day092_print_words_vertically import (
    Solution,
    print_vertically_scan,
    print_vertically_zip,
    print_vertically_generator,
    reconstruct_sentence_from_vertical,
)


class TestDay092PrintWordsVertically(unittest.TestCase):
    """Unit tests for Day 92 Print Words Vertically."""

    def test_standard_cases(self):
        sol = Solution()
        self.assertEqual(sol.printVertically("HOW ARE YOU"), ["HAY", "ORO", "WEU"])
        self.assertEqual(print_vertically_scan("TO BE OR NOT TO BE"), ["TBONTB", "OEROOE", "   T"])
        self.assertEqual(
            list(print_vertically_generator("CONTEST IS COMING")),
            ["CIC", "OSO", "N M", "T I", "E N", "S G", "T"],
        )

    def test_round_trip(self):
        s = "CONTEST IS COMING"
        self.assertEqual(reconstruct_sentence_from_vertical(print_vertically_zip(s)), s)


if __name__ == "__main__":
    unittest.main()