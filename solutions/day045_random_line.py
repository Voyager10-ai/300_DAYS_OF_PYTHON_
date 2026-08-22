# Day 45: Random Line
#
# Problem:
#   Write a Python program to read a random line from a text file.
#   Includes support for Reservoir Sampling (Algorithm R), K-line sampling,
#   weighted selection, predicate/regex filtering, multi-file inspection,
#   fast O(1) byte-offset indexing (LineIndexer), unit tests, and Java practice.

import os
import re
import sys
import random
import tempfile
import unittest
from pathlib import Path
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Union, Iterator


# ─── 1. Core Random Line Selection Functions ──────────────────────────────────


def read_all_lines_random(
    file_path: Union[str, Path],
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Reads all lines from a file into memory and strips trailing newlines if requested.

    Args:
        file_path: Path to the target text file.
        strip_newline: If True, strips trailing newline characters (\\r\\n, \\n).
        encoding: Text file encoding.

    Returns:
        List of string lines.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the path is a directory.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    with open(path, "r", encoding=encoding, errors="replace") as f:
        if strip_newline:
            return [line.rstrip("\r\n") for line in f]
        return f.readlines()


def get_random_line(
    file_path: Union[str, Path],
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> Optional[str]:
    """
    Reads a random line from a text file.

    Args:
        file_path: Path to the file.
        strip_newline: If True, strips trailing newline characters.
        encoding: File encoding.

    Returns:
        A randomly chosen line string, or None if the file is empty.
    """
    lines = read_all_lines_random(file_path, strip_newline=strip_newline, encoding=encoding)
    if not lines:
        return None
    return random.choice(lines)


def get_random_line_with_index(
    file_path: Union[str, Path],
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> Optional[Tuple[int, str]]:
    """
    Reads a random line from a text file along with its 1-indexed line number.

    Args:
        file_path: Path to the file.
        strip_newline: If True, strips trailing newline characters.
        encoding: File encoding.

    Returns:
        Tuple of (line_number, line_content), or None if the file is empty.
    """
    lines = read_all_lines_random(file_path, strip_newline=strip_newline, encoding=encoding)
    if not lines:
        return None
    index = random.randint(0, len(lines) - 1)
    return (index + 1, lines[index])


# ─── 2. Reservoir Sampling for Memory-Efficient Selection ──────────────────────


def reservoir_sample_line(
    file_path: Union[str, Path],
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> Optional[Tuple[int, str]]:
    """
    Selects a random line from a file using Reservoir Sampling (Algorithm R).
    Operates in O(1) space and a single stream pass, making it ideal for huge files.

    Args:
        file_path: Path to the file.
        strip_newline: If True, strips trailing newline characters.
        encoding: File encoding.

    Returns:
        Tuple of (selected_line_number, selected_line_content), or None if file is empty.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    selected_line_num: Optional[int] = None
    selected_content: Optional[str] = None

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for i, line in enumerate(f, start=1):
            if strip_newline:
                line = line.rstrip("\r\n")
            # Select 1st element with prob 1, 2nd with 1/2, ith with 1/i
            if random.randint(1, i) == 1:
                selected_line_num = i
                selected_content = line

    if selected_line_num is None or selected_content is None:
        return None
    return (selected_line_num, selected_content)


def reservoir_sample_k_lines(
    file_path: Union[str, Path],
    k: int,
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> List[Tuple[int, str]]:
    """
    Selects K random lines from a file using Reservoir Sampling algorithm in a single pass.

    Args:
        file_path: Path to the file.
        k: Number of lines to sample. Must be > 0.
        strip_newline: If True, strips trailing newlines.
        encoding: File encoding.

    Returns:
        List of tuples (line_number, line_content). If total lines < k, returns all lines.
    """
    if k <= 0:
        raise ValueError("k must be greater than 0")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    reservoir: List[Tuple[int, str]] = []

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for i, line in enumerate(f, start=1):
            if strip_newline:
                line = line.rstrip("\r\n")

            if i <= k:
                reservoir.append((i, line))
            else:
                j = random.randint(1, i)
                if j <= k:
                    reservoir[j - 1] = (i, line)

    return reservoir

