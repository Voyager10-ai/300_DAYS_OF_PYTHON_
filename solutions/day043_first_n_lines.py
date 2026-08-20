# Day 43: First N Lines
#
# Problem:
#   Write a Python program to read the first n lines of a file, supporting memory-efficient
#   streaming, generator iterators, custom line limits, multi-file inspection, predicate
#   filtering, line range slicing, robust encoding handling, unittest coverage, and
#   Java file line reading practice.

import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Union, Iterator


# ─── 1. Core First N Lines Reading Functions ──────────────────────────────────


def read_first_n_lines(
    file_path: Union[str, Path],
    n: int,
    encoding: str = "utf-8",
    strip_newline: bool = True,
) -> List[str]:
    """
    Reads the first n lines from a file.

    Args:
        file_path: Path to the file to read.
        n: Number of lines to read. Must be >= 0.
        encoding: File encoding (default: utf-8).
        strip_newline: If True, strips trailing newline characters (\\n or \\r\\n).

    Returns:
        List of line strings.

    Raises:
        ValueError: If n is negative.
        FileNotFoundError: If the specified file does not exist.
        IsADirectoryError: If path points to a directory.

    Example:
        >>> read_first_n_lines("sample.txt", 3)
        ['Line 1', 'Line 2', 'Line 3']
    """
    if n < 0:
        raise ValueError(f"Number of lines 'n' must be non-negative, got {n}.")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    lines: List[str] = []
    if n == 0:
        return lines

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for _ in range(n):
            line = f.readline()
            if not line:
                break
            if strip_newline:
                line = line.rstrip("\r\n")
            lines.append(line)

    return lines


def read_first_n_lines_as_text(
    file_path: Union[str, Path],
    n: int,
    encoding: str = "utf-8",
) -> str:
    """
    Reads the first n lines from a file and returns them joined as a single multiline string.

    Args:
        file_path: Path to the file.
        n: Number of lines to read.
        encoding: File encoding.

    Returns:
        Multiline string containing the first n lines.

    Example:
        >>> read_first_n_lines_as_text("sample.txt", 2)
        'Line 1\\nLine 2'
    """
    lines = read_first_n_lines(file_path, n, encoding=encoding, strip_newline=False)
    return "".join(lines)


def get_line_count(file_path: Union[str, Path], encoding: str = "utf-8") -> int:
    """
    Counts the total number of lines in a file efficiently.

    Args:
        file_path: Path to the file.
        encoding: File encoding.

    Returns:
        Total number of lines.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    count = 0
    with open(path, "r", encoding=encoding, errors="replace") as f:
        for _ in f:
            count += 1
    return count
