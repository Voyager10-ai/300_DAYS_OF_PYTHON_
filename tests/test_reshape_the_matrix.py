import unittest
import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solutions.day093_reshape_the_matrix import (
    Solution,
    matrix_reshape_flatten,
    matrix_reshape_divmod,
    matrix_reshape_column_major,
    matrix_reshape_generator,
    matrix_transpose,
    matrix_rotate_90_cw,
    matrix_spiral_flatten,
)


class TestDay093ReshapeTheMatrix(unittest.TestCase):
    """Unit tests for Day 93 Reshape the Matrix."""

    def test_reshape(self):
        sol = Solution()
        mat = [[1, 2], [3, 4]]
        self.assertEqual(sol.matrixReshape(mat, 1, 4), [[1, 2, 3, 4]])
        self.assertEqual(matrix_reshape_divmod(mat, 1, 4), [[1, 2, 3, 4]])
        self.assertEqual(matrix_reshape_flatten(mat, 2, 4), [[1, 2], [3, 4]])

    def test_column_major_and_generator(self):
        mat = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(matrix_reshape_column_major(mat, 3, 2), [[1, 5], [4, 3], [2, 6]])
        self.assertEqual(list(matrix_reshape_generator(mat, 3, 2)), [[1, 2], [3, 4], [5, 6]])

    def test_transforms(self):
        self.assertEqual(matrix_transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])
        self.assertEqual(matrix_rotate_90_cw([[1, 2], [3, 4]]), [[3, 1], [4, 2]])
        self.assertEqual(
            matrix_spiral_flatten([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            [1, 2, 3, 6, 9, 8, 7, 4, 5],
        )


if __name__ == "__main__":
    unittest.main()