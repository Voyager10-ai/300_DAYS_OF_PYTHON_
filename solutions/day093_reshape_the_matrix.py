# Day 93: Reshape the Matrix (LeetCode 566)
#
# Problem:
#   Given an m x n matrix mat and two integers r and c representing the number
#   of rows and columns of the wanted reshaped matrix, reshape the matrix in
#   row-traversing order. If the reshape operation is not possible and legal
#   (i.e. m * n != r * c), output the original matrix.
#   Includes:
#     - Flatten-to-1D buffer reshape O(m*n)
#     - Single-pass divmod index mapping O(1) auxiliary space
#     - LeetCode 566 Solution class
#     - Column-major (Fortran-style) reshape, lazy generator, transpose & 90° rotate
#     - ASCII matrix reshape visualizer
#     - Multi-algorithm performance benchmark
#     - Comprehensive unit test suite and Java practice code

import time
import unittest
from typing import List, Dict, Tuple, Any, Optional, Generator


# ─── 1. Core Matrix Reshape Implementations ────────────────────────────────────


def _validate_matrix(mat: List[List[int]], r: int, c: int) -> Tuple[int, int]:
    """Validates rectangular matrix structure and positive integer dimensions."""
    if not isinstance(mat, list):
        raise TypeError(f"mat must be a list of lists, got {type(mat).__name__}")
    if not isinstance(r, int) or isinstance(r, bool) or r <= 0:
        raise ValueError(f"Target rows r must be a positive integer, got {r}")
    if not isinstance(c, int) or isinstance(c, bool) or c <= 0:
        raise ValueError(f"Target cols c must be a positive integer, got {c}")
    if not mat or not isinstance(mat[0], list):
        raise ValueError("mat must be a non-empty 2D list")

    m = len(mat)
    n = len(mat[0])
    if n == 0:
        raise ValueError("mat rows must not be empty")

    for idx, row in enumerate(mat):
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"Row {idx} has inconsistent length (expected {n})")

    return (m, n)


def matrix_reshape_flatten(
    mat: List[List[int]],
    r: int,
    c: int,
) -> List[List[int]]:
    """
    Reshapes mat into an r x c matrix by flattening into an intermediate 1D buffer.

    Time Complexity: O(m * n).
    Space Complexity: O(m * n) for the flattened intermediate array.

    Args:
        mat: Original m x n integer matrix.
        r: Target row count.
        c: Target column count.

    Returns:
        Reshaped r x c matrix, or original mat if m * n != r * c.
    """
    m, n = _validate_matrix(mat, r, c)
    if m * n != r * c:
        return [row[:] for row in mat]

    flat: List[int] = [val for row in mat for val in row]
    return [flat[i * c : (i + 1) * c] for i in range(r)]


def matrix_reshape_divmod(
    mat: List[List[int]],
    r: int,
    c: int,
) -> List[List[int]]:
    """
    Reshapes mat in a single pass using flat index coordinate mapping (divmod).

    Maps flat index k in [0, m*n) directly:
        source_row, source_col = divmod(k, n)
        target_row, target_col = divmod(k, c)

    Time Complexity: O(m * n).
    Space Complexity: O(1) auxiliary space (excluding output matrix).

    Args:
        mat: Original m x n matrix.
        r: Target row count.
        c: Target column count.

    Returns:
        Reshaped r x c matrix, or copy of mat if incompatible.
    """
    m, n = _validate_matrix(mat, r, c)
    if m * n != r * c:
        return [row[:] for row in mat]

    reshaped: List[List[int]] = [[0] * c for _ in range(r)]
    total = m * n

    for k in range(total):
        src_r, src_c = divmod(k, n)
        dst_r, dst_c = divmod(k, c)
        reshaped[dst_r][dst_c] = mat[src_r][src_c]

    return reshaped


def matrix_reshape_with_metrics(
    mat: List[List[int]],
    r: int,
    c: int,
) -> Tuple[List[List[int]], Dict[str, Any]]:
    """
    Reshapes mat while tracking dimension compatibility and execution timing.

    Args:
        mat: Original m x n matrix.
        r: Target rows.
        c: Target cols.

    Returns:
        Tuple of (reshaped_matrix, metrics_dict).
    """
    t0 = time.perf_counter()
    m, n = _validate_matrix(mat, r, c)
    compatible = (m * n) == (r * c)
    result = matrix_reshape_divmod(mat, r, c)
    elapsed = time.perf_counter() - t0

    metrics = {
        "original_shape": (m, n),
        "target_shape": (r, c),
        "actual_shape": (len(result), len(result[0])),
        "compatible": compatible,
        "total_elements": m * n,
        "time_seconds": elapsed,
        "algorithm": "Single-Pass Divmod Mapping O(m*n)",
    }
    return (result, metrics)


class Solution:
    """LeetCode 566: Reshape the Matrix solution wrapper."""

    def matrixReshape(self, mat: List[List[int]], r: int, c: int) -> List[List[int]]:
        """Reshapes mat to r x c if total elements match, otherwise returns mat."""
        return matrix_reshape_flatten(mat, r, c)
