import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day094_longest_common_prefix import (
    Solution,
    lcp_horizontal_scan,
    lcp_vertical_scan,
    lcp_divide_and_conquer,
    lcp_binary_search,
    lcp_sort_endpoints,
    lcp_trie,
    longest_common_suffix,
    longest_common_prefix_k_strings,
)


class TestDay094LongestCommonPrefix(unittest.TestCase):
    """Unit tests for Day 94 Longest Common Prefix."""

    def test_standard_cases(self):
        sol = Solution()
        words = ["flower", "flow", "flight"]
        for fn in [
            lcp_horizontal_scan,
            lcp_vertical_scan,
            lcp_divide_and_conquer,
            lcp_binary_search,
            lcp_sort_endpoints,
            lcp_trie,
            sol.longestCommonPrefix,
        ]:
            self.assertEqual(fn(words), "fl")
            self.assertEqual(fn(["dog", "racecar", "car"]), "")

    def test_extensions(self):
        self.assertEqual(longest_common_suffix(["running", "jogging", "walking"]), "ing")
        self.assertEqual(longest_common_prefix_k_strings(["apple", "app", "apricot", "banana"], 3), "ap")


if __name__ == "__main__":
    unittest.main()