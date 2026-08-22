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
