import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day095_partition_labels import (
    Solution,
    partition_labels_greedy,
    partition_labels_intervals,
    partition_labels_substrings,
    partition_labels_disjoint_sets,
    can_partition_into_k,
    merge_partitions_to_k,
)


class TestDay095PartitionLabels(unittest.TestCase):
    """Unit tests for Day 95 Partition Labels."""

    def test_standard_cases(self):
        sol = Solution()
        s = "ababcbacadefegdehijhklij"
        expected = [9, 7, 8]
        self.assertEqual(sol.partitionLabels(s), expected)
        self.assertEqual(partition_labels_greedy(s), expected)
        self.assertEqual(partition_labels_intervals(s), expected)
        self.assertEqual(partition_labels_substrings(s), ["ababcbaca", "defegde", "hijhklij"])

    def test_disjoint_sets(self):
        s = "ababcbacadefegdehijhklij"
        sets = partition_labels_disjoint_sets(s)
        self.assertEqual(len(sets), 3)

    def test_k_partitions(self):
        s = "ababcbacadefegdehijhklij"
        self.assertTrue(can_partition_into_k(s, 3))
        self.assertFalse(can_partition_into_k(s, 5))
        merged = merge_partitions_to_k(s, 2)
        self.assertEqual(len(merged), 2)


if __name__ == "__main__":
    unittest.main()