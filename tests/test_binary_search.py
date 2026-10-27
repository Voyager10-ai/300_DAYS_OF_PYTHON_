import unittest
from solutions.day085_binary_search_implement import Solution


class TestBinarySearch(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_target_found(self):
        self.assertEqual(
            self.solution.search([-1, 0, 3, 5, 9, 12], 9), 4
        )

    def test_target_not_found(self):
        self.assertEqual(
            self.solution.search([-1, 0, 3, 5, 9, 12], 2), -1
        )

    def test_empty_list(self):
        self.assertEqual(self.solution.search([], 5), -1)

    def test_single_element_found(self):
        self.assertEqual(self.solution.search([5], 5), 0)

    def test_single_element_not_found(self):
        self.assertEqual(self.solution.search([5], 2), -1)


if __name__ == "__main__":
    unittest.main()