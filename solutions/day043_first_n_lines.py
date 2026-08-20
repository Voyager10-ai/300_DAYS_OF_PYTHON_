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


# ─── 2. Memory-Efficient Streaming & Generator Iterators ───────────────────────


def stream_first_n_lines(
    file_path: Union[str, Path],
    n: int,
    encoding: str = "utf-8",
    strip_newline: bool = True,
) -> Iterator[str]:
    """
    Yields lines one-by-one from a file up to n lines without loading the full file into memory.

    Args:
        file_path: Path to the target file.
        n: Maximum number of lines to stream.
        encoding: Text encoding.
        strip_newline: If True, strips trailing newline characters.

    Yields:
        Line strings incrementally.

    Raises:
        ValueError: If n < 0.
        FileNotFoundError: If file is missing.
    """
    if n < 0:
        raise ValueError(f"Number of lines 'n' must be non-negative, got {n}.")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if n == 0:
        return

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for count, line in enumerate(f):
            if count >= n:
                break
            yield line.rstrip("\r\n") if strip_newline else line


def stream_lines_batch(
    file_path: Union[str, Path],
    batch_size: int = 10,
    max_batches: Optional[int] = None,
    encoding: str = "utf-8",
) -> Iterator[List[str]]:
    """
    Yields lines in batches (chunks of lines) up to an optional maximum number of batches.

    Args:
        file_path: Path to the file.
        batch_size: Size of each batch of lines. Must be > 0.
        max_batches: Optional ceiling on the number of batches to yield.
        encoding: Text encoding.

    Yields:
        Lists of line strings.
    """
    if batch_size <= 0:
        raise ValueError(f"batch_size must be positive, got {batch_size}.")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    batch_count = 0
    with open(path, "r", encoding=encoding, errors="replace") as f:
        current_batch: List[str] = []
        for line in f:
            current_batch.append(line.rstrip("\r\n"))
            if len(current_batch) == batch_size:
                yield current_batch
                batch_count += 1
                current_batch = []
                if max_batches is not None and batch_count >= max_batches:
                    return
        if current_batch:
            yield current_batch


# ─── 3. Head-like Formatting & Predicate Filtering ─────────────────────────────


def head_file(
    file_path: Union[str, Path],
    n: int = 10,
    include_line_numbers: bool = False,
    strip_trailing_whitespace: bool = False,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Emulates the Unix `head` command by formatting the first n lines of a file.

    Args:
        file_path: Path to file.
        n: Number of lines to preview (default: 10).
        include_line_numbers: If True, prefixes lines with '  1: ', '  2: ', etc.
        strip_trailing_whitespace: If True, strips trailing whitespace on each line.
        encoding: File encoding.

    Returns:
        List of formatted lines.
    """
    raw_lines = read_first_n_lines(file_path, n, encoding=encoding, strip_newline=True)
    result: List[str] = []

    for idx, line in enumerate(raw_lines, start=1):
        formatted_line = line.rstrip() if strip_trailing_whitespace else line
        if include_line_numbers:
            formatted_line = f"{idx:4d}: {formatted_line}"
        result.append(formatted_line)

    return result


def read_first_n_matching_lines(
    file_path: Union[str, Path],
    n: int,
    predicate: Callable[[str], bool],
    encoding: str = "utf-8",
) -> List[str]:
    """
    Reads the first n lines from a file that satisfy a given filter condition (predicate).

    Args:
        file_path: Path to the file.
        n: Target number of matching lines to return.
        predicate: Callable taking a line string and returning True if line matches.
        encoding: File encoding.

    Returns:
        List of matching line strings.

    Example:
        >>> read_first_n_matching_lines("log.txt", 3, lambda line: "ERROR" in line)
        ['ERROR: Out of memory', 'ERROR: Connection failed', 'ERROR: Timeout']
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}.")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    matching_lines: List[str] = []
    if n == 0:
        return matching_lines

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            clean_line = line.rstrip("\r\n")
            if predicate(clean_line):
                matching_lines.append(clean_line)
                if len(matching_lines) == n:
                    break

    return matching_lines


