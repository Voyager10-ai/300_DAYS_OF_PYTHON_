# Day 92: Print Words Vertically (LeetCode 1324)
#
# Problem:
#   Given a string s of space-separated words, return all the words vertically
#   in the same order in which they appear in s.
#   Words are returned as a list of strings, padded with leading/internal spaces
#   where shorter words end early, with NO trailing spaces allowed.
#   Includes:
#     - Column-by-column index scan with right-stripping
#     - Pythonic itertools.zip_longest transposition
#     - LeetCode 1324 Solution wrapper
#     - O(1) memory lazy streaming column generator
#     - Bottom-up vertical column inversion & diagonal matrix traversal
#     - Round-trip reconstruction from vertical columns back to sentence
#     - ASCII grid visualizer showing character alignment & stripped whitespace
#     - Multi-algorithm performance benchmark
#     - Comprehensive unit tests and Java practice code

import time
import unittest
from itertools import zip_longest
from typing import List, Dict, Tuple, Any, Optional, Generator


# ─── 1. Core Print Words Vertically Implementations ───────────────────────────


def print_vertically_scan(s: str) -> List[str]:
    """
    Prints words vertically using explicit column-by-column scanning.

    Time Complexity: O(W * L) where W is number of words and L is max word length.
    Space Complexity: O(W * L) to construct the output list.

    Args:
        s: Input string containing space-separated words.

    Returns:
        List of vertical word strings without trailing spaces.

    Raises:
        TypeError: If s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")

    words = s.split()
    if not words:
        return []

    max_len = max(len(word) for word in words)
    columns: List[str] = []

    for col_idx in range(max_len):
        chars: List[str] = []
        for word in words:
            if col_idx < len(word):
                chars.append(word[col_idx])
            else:
                chars.append(" ")
        # Strip strictly trailing whitespace from right end of column
        columns.append("".join(chars).rstrip())

    return columns


def print_vertically_zip(s: str) -> List[str]:
    """
    Prints words vertically using itertools.zip_longest matrix transposition.

    Time Complexity: O(W * L).
    Space Complexity: O(W * L).

    Args:
        s: Input string containing words.

    Returns:
        List of vertical strings with trailing spaces removed.
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")

    words = s.split()
    if not words:
        return []

    return ["".join(col).rstrip() for col in zip_longest(*words, fillvalue=" ")]


def print_vertically_with_metrics(
    s: str,
) -> Tuple[List[str], Dict[str, Any]]:
    """
    Computes vertical words while tracking padding, trimming, and timing metrics.

    Args:
        s: Input sentence string.

    Returns:
        Tuple of (vertical_columns, metrics_dict).
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")

    t0 = time.perf_counter()
    words = s.split()
    if not words:
        return ([], {
            "word_count": 0,
            "max_word_length": 0,
            "total_chars": 0,
            "trailing_spaces_trimmed": 0,
            "time_seconds": time.perf_counter() - t0,
        })

    max_len = max(len(w) for w in words)
    num_words = len(words)
    columns: List[str] = []
    trimmed_spaces = 0

    for col_idx in range(max_len):
        raw = "".join(w[col_idx] if col_idx < len(w) else " " for w in words)
        trimmed = raw.rstrip()
        trimmed_spaces += len(raw) - len(trimmed)
        columns.append(trimmed)

    elapsed = time.perf_counter() - t0
    metrics = {
        "word_count": num_words,
        "max_word_length": max_len,
        "total_grid_cells": num_words * max_len,
        "trailing_spaces_trimmed": trimmed_spaces,
        "time_seconds": elapsed,
        "algorithm": "Column-Scan Matrix Transposition O(W*L)",
    }
    return (columns, metrics)


class Solution:
    """LeetCode 1324: Print Words Vertically solution wrapper."""

    def printVertically(self, s: str) -> List[str]:
        """Returns words vertically without trailing whitespace."""
        return print_vertically_zip(s)



# ─── 2. Streaming Generator, Grid Transformations & Round-Trip Reconstruction ───


def print_vertically_generator(s: str) -> Generator[str, None, None]:
    """
    Lazily yields each vertical word column one at a time.

    Avoids materializing the full transposed matrix in memory at once.

    Args:
        s: Space-separated input string.

    Yields:
        One stripped vertical column string per column index.
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")

    words = s.split()
    if not words:
        return

    max_len = max(len(w) for w in words)
    for col_idx in range(max_len):
        # Find last word index that has a character at col_idx to avoid building trailing spaces
        last_valid = -1
        for w_idx in range(len(words) - 1, -1, -1):
            if col_idx < len(words[w_idx]):
                last_valid = w_idx
                break

        if last_valid == -1:
            yield ""
        else:
            chars = [
                words[i][col_idx] if col_idx < len(words[i]) else " "
                for i in range(last_valid + 1)
            ]
            yield "".join(chars)


def print_vertically_bottom_up(s: str) -> List[str]:
    """
    Prints words vertically with word order reversed (bottom-to-top per column).

    Equivalent to rotating the word grid 90 degrees clockwise.

    Args:
        s: Space-separated string.

    Returns:
        List of bottom-up vertical column strings with trailing whitespace stripped.
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")

    words = s.split()
    if not words:
        return []

    reversed_words = words[::-1]
    return ["".join(col).rstrip() for col in zip_longest(*reversed_words, fillvalue=" ")]


def print_diagonal_words(s: str) -> List[str]:
    """
    Extracts anti-diagonal character streams across the rectangular word matrix.

    Diagonals follow the invariant: row + col == k for k = 0..(R + C - 2).

    Args:
        s: Space-separated string.

    Returns:
        List of anti-diagonal character strings with trailing whitespace removed.
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")

    words = s.split()
    if not words:
        return []

    rows = len(words)
    cols = max(len(w) for w in words)
    diagonals: List[str] = []

    for d in range(rows + cols - 1):
        chars: List[str] = []
        for r in range(rows):
            c = d - r
            if 0 <= c < cols:
                chars.append(words[r][c] if c < len(words[r]) else " ")
        diagonals.append("".join(chars).rstrip())

    return diagonals


def reconstruct_sentence_from_vertical(columns: List[str]) -> str:
    """
    Inverse operation: reconstructs the original horizontal sentence from vertical columns.

    Args:
        columns: List of vertical strings produced by print_vertically_*.

    Returns:
        Reconstructed space-separated sentence string.
    """
    if not isinstance(columns, list):
        raise TypeError(f"columns must be a list of strings, got {type(columns).__name__}")
    if not columns:
        return ""

    num_words = max(len(col) for col in columns)
    word_buffers: List[List[str]] = [[] for _ in range(num_words)]

    for col in columns:
        for w_idx in range(num_words):
            if w_idx < len(col):
                word_buffers[w_idx].append(col[w_idx])

    words = ["".join(buf).strip() for buf in word_buffers]
    return " ".join(w for w in words if w)



# ─── 3. ASCII Matrix Visualizer & Performance Benchmarking ────────────────────


def visualize_vertical_grid(s: str) -> str:
    """
    Renders an ASCII matrix showing word grid padding and vertical transposition.

    Args:
        s: Space-separated input string.

    Returns:
        Formatted ASCII string diagram.
    """
    words = s.split()
    if not words:
        return "Empty input string."

    max_len = max(len(w) for w in words)
    lines: List[str] = []
    lines.append(f"Vertical Grid Transposition for: '{s}'")
    lines.append("=" * 68)
    lines.append("1. Input Words Matrix ('.' indicates internal/trailing pad space):")

    col_header = "        " + " ".join(f"C{c}" for c in range(max_len))
    lines.append(col_header)
    lines.append("       +" + "--" * max_len + "+")

    for r, w in enumerate(words):
        row_cells = [w[c] if c < len(w) else "." for c in range(max_len)]
        lines.append(f"  W{r:<3} | " + " ".join(row_cells) + " |")

    lines.append("       +" + "--" * max_len + "+")
    lines.append("\n2. Transposed Vertical Columns (trailing spaces stripped):")
    cols = print_vertically_zip(s)
    for idx, col in enumerate(cols):
        lines.append(f"  Col {idx:<2}: \"{col}\"")

    lines.append("=" * 68)
    return "\n".join(lines)


def benchmark_vertical_algorithms(
    word_counts: Optional[List[int]] = None,
    word_len: int = 12,
    iterations: int = 20,
) -> Dict[str, Any]:
    """
    Benchmarks vertical word printing algorithms across varying input sizes.

    Args:
        word_counts: List of word counts to test.
        word_len: Maximum word length used in generated sentences.
        iterations: Runs per benchmark point.

    Returns:
        Structured benchmark metrics dictionary.
    """
    if word_counts is None:
        word_counts = [10, 50, 200, 1000]

    records: List[Dict[str, Any]] = []

    for count in word_counts:
        # Build synthetic test sentence with alternating lengths
        words = [("PYTHON" * 3)[: (i % word_len) + 1] for i in range(count)]
        sentence = " ".join(words)
        row: Dict[str, Any] = {"word_count": count}

        # 1. Column-Scan approach
        times: List[float] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            print_vertically_scan(sentence)
            times.append(time.perf_counter() - t0)
        row["scan"] = min(times)

        # 2. zip_longest approach
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            print_vertically_zip(sentence)
            times.append(time.perf_counter() - t0)
        row["zip_longest"] = min(times)

        # 3. Streaming generator
        times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            list(print_vertically_generator(sentence))
            times.append(time.perf_counter() - t0)
        row["generator"] = min(times)

        records.append(row)

    return {"records": records, "word_len": word_len, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """Formats the benchmark dictionary into an ASCII comparison table."""
    lines: List[str] = []
    lines.append("Print Words Vertically Performance Benchmark")
    lines.append("=" * 72)
    header = (
        f"{'Words':>8} | {'Column Scan':>18} | {'zip_longest':>18} | {'Lazy Generator':>18}"
    )
    lines.append(header)
    lines.append("-" * 72)

    def _fmt(val: float) -> str:
        us = val * 1_000_000.0
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['word_count']:>8} | "
            f"{_fmt(r['scan']):>18} | "
            f"{_fmt(r['zip_longest']):>18} | "
            f"{_fmt(r['generator']):>18}"
        )
        lines.append(line)

    lines.append("=" * 72)
    return "\n".join(lines)
