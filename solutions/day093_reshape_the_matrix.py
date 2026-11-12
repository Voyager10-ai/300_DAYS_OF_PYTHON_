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



# ─── 2. Column-Major Reshape, Streaming Generator & 2D Transformations ─────────


def matrix_reshape_column_major(
    mat: List[List[int]],
    r: int,
    c: int,
) -> List[List[int]]:
    """
    Reshapes mat using Fortran/MATLAB-style column-major traversal order.

    Reads elements top-to-bottom column-by-column and populates the target r x c
    matrix column-by-column.

    Args:
        mat: Original m x n integer matrix.
        r: Target row count.
        c: Target column count.

    Returns:
        Column-major reshaped matrix, or copy of mat if m * n != r * c.
    """
    m, n = _validate_matrix(mat, r, c)
    if m * n != r * c:
        return [row[:] for row in mat]

    reshaped: List[List[int]] = [[0] * c for _ in range(r)]
    total = m * n

    for k in range(total):
        # Column-major coordinate mapping
        src_c, src_r = divmod(k, m)
        dst_c, dst_r = divmod(k, r)
        reshaped[dst_r][dst_c] = mat[src_r][src_c]

    return reshaped


def matrix_reshape_generator(
    mat: List[List[int]],
    r: int,
    c: int,
) -> Generator[List[int], None, None]:
    """
    Lazily yields reshaped matrix rows one at a time without materializing the full grid.

    Space Complexity: O(c) buffer per yielded row.

    Args:
        mat: Original m x n matrix.
        r: Target rows.
        c: Target columns.

    Yields:
        Rows of length c (or original rows if incompatible).
    """
    m, n = _validate_matrix(mat, r, c)
    if m * n != r * c:
        for row in mat:
            yield row[:]
        return

    row_buf: List[int] = []
    for row in mat:
        for val in row:
            row_buf.append(val)
            if len(row_buf) == c:
                yield row_buf
                row_buf = []


def matrix_transpose(mat: List[List[int]]) -> List[List[int]]:
    """Returns the matrix transpose (m x n -> n x m)."""
    if not mat or not mat[0]:
        return []
    return [list(col) for col in zip(*mat)]


def matrix_rotate_90_cw(mat: List[List[int]]) -> List[List[int]]:
    """Rotates an m x n matrix 90 degrees clockwise."""
    if not mat or not mat[0]:
        return []
    return [list(row) for row in zip(*mat[::-1])]


def matrix_spiral_flatten(mat: List[List[int]]) -> List[int]:
    """Traverses and flattens a 2D matrix in clockwise spiral order."""
    if not mat or not mat[0]:
        return []

    top, bottom = 0, len(mat) - 1
    left, right = 0, len(mat[0]) - 1
    result: List[int] = []

    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            result.append(mat[top][c])
        top += 1

        for r in range(top, bottom + 1):
            result.append(mat[r][right])
        right -= 1

        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(mat[bottom][c])
            bottom -= 1

        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(mat[r][left])
            left += 1

    return result



# ─── 3. ASCII Matrix Visualizer & Performance Benchmarking ────────────────────


def _render_ascii_matrix(mat: List[List[int]], title: str) -> List[str]:
    """Helper rendering a clean boxed ASCII grid for a 2D integer matrix."""
    width = max(len(str(val)) for row in mat for val in row) + 1
    out: List[str] = [title]
    border = "+" + "-" * (len(mat[0]) * (width + 1) + 1) + "+"
    out.append(border)
    for row in mat:
        cells = " ".join(f"{val:>{width}}" for val in row)
        out.append(f"| {cells} |")
    out.append(border)
    return out


def visualize_matrix_reshape(
    mat: List[List[int]],
    r: int,
    c: int,
) -> str:
    """
    Renders an ASCII diagram illustrating original matrix, flat traversal, and target shape.

    Args:
        mat: Original m x n integer matrix.
        r: Target row count.
        c: Target column count.

    Returns:
        Formatted ASCII string diagram.
    """
    m, n = _validate_matrix(mat, r, c)
    lines: List[str] = []
    lines.append(f"Matrix Reshape Visualization: ({m}x{n}) -> ({r}x{c})")
    lines.append("=" * 68)
    lines.extend(_render_ascii_matrix(mat, f"Original Matrix ({m}x{n}):"))

    if m * n != r * c:
        lines.append(f"\n[!] Incompatible dimensions: {m}*{n} ({m*n}) != {r}*{c} ({r*c})")
        lines.append("    Returning copy of original matrix unchanged.")
    else:
        flat = [val for row in mat for val in row]
        lines.append(f"\nLinear Row-Major Stream: {flat}")
        reshaped = matrix_reshape_divmod(mat, r, c)
        lines.append("")
        lines.extend(_render_ascii_matrix(reshaped, f"Reshaped Matrix ({r}x{c}):"))

    lines.append("=" * 68)
    return "\n".join(lines)


def benchmark_reshape_algorithms(
    shapes: Optional[List[Tuple[int, int, int, int]]] = None,
    iterations: int = 10,
) -> Dict[str, Any]:
    """
    Benchmarks matrix reshape strategies across varying matrix dimensions.

    Args:
        shapes: List of (m, n, r, c) tuples. Defaults to common scaling shapes.
        iterations: Runs per test point.

    Returns:
        Structured benchmark metrics dictionary.
    """
    if shapes is None:
        shapes = [
            (10, 10, 5, 20),
            (50, 50, 25, 100),
            (200, 200, 100, 400),
            (400, 400, 800, 200),
        ]

    records: List[Dict[str, Any]] = []

    for m, n, r, c in shapes:
        mat = [[(i * n + j) for j in range(n)] for i in range(m)]
        row: Dict[str, Any] = {"shape_str": f"{m}x{n}->{r}x{c}", "elements": m * n}

        # 1. Flatten Buffer
        times: List[float] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            matrix_reshape_flatten(mat, r, c)
            times.append(time.perf_counter() - t0)
        row["flatten"] = min(times)

        # 2. Divmod Single-Pass
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            matrix_reshape_divmod(mat, r, c)
            times.append(time.perf_counter() - t0)
        row["divmod"] = min(times)

        # 3. Column-Major
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            matrix_reshape_column_major(mat, r, c)
            times.append(time.perf_counter() - t0)
        row["col_major"] = min(times)

        # 4. Lazy Generator
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            list(matrix_reshape_generator(mat, r, c))
            times.append(time.perf_counter() - t0)
        row["generator"] = min(times)

        records.append(row)

    return {"records": records, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """Formats the reshape benchmark dictionary into an ASCII table."""
    lines: List[str] = []
    lines.append("Matrix Reshape Algorithms Performance Benchmark")
    lines.append("=" * 84)
    header = (
        f"{'Transform':>16} | {'Cells':>8} | {'Flatten Buffer':>15} | "
        f"{'Divmod Map':>12} | {'Col-Major':>11} | {'Generator':>11}"
    )
    lines.append(header)
    lines.append("-" * 84)

    def _fmt(val: float) -> str:
        us = val * 1_000_000.0
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['shape_str']:>16} | {r['elements']:>8} | "
            f"{_fmt(r['flatten']):>15} | "
            f"{_fmt(r['divmod']):>12} | "
            f"{_fmt(r['col_major']):>11} | "
            f"{_fmt(r['generator']):>11}"
        )
        lines.append(line)

    lines.append("=" * 84)
    return "\n".join(lines)
