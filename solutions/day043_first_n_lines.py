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


# ─── 4. Multi-File Operations & Directory Head Previews ───────────────────────


def read_first_n_lines_multiple_files(
    file_paths: List[Union[str, Path]],
    n: int,
    encoding: str = "utf-8",
) -> Dict[str, List[str]]:
    """
    Reads the first n lines from multiple files and returns a dictionary mapping file path strings to line lists.

    Args:
        file_paths: List of file paths to process.
        n: Number of lines per file.
        encoding: File encoding.

    Returns:
        Dict mapping filename/path to first n lines.
    """
    results: Dict[str, List[str]] = {}
    for fp in file_paths:
        path = Path(fp)
        if path.exists() and path.is_file():
            results[str(path)] = read_first_n_lines(path, n, encoding=encoding)
    return results


def preview_directory_files_head(
    directory_path: Union[str, Path],
    n: int = 5,
    file_extension: Optional[str] = None,
    encoding: str = "utf-8",
) -> Dict[str, List[str]]:
    """
    Scans a directory and returns the first n lines of files, optionally filtering by extension.

    Args:
        directory_path: Target directory to scan.
        n: Number of lines to preview per file.
        file_extension: Optional file extension filter (e.g. '.py', '.txt').
        encoding: File encoding.

    Returns:
        Dict mapping file names to line lists.
    """
    dir_path = Path(directory_path)
    if not dir_path.exists() or not dir_path.is_dir():
        raise NotADirectoryError(f"Directory not found or invalid: {directory_path}")

    previews: Dict[str, List[str]] = {}
    for entry in sorted(dir_path.iterdir()):
        if entry.is_file():
            if file_extension and not entry.name.endswith(file_extension):
                continue
            try:
                previews[entry.name] = read_first_n_lines(entry, n, encoding=encoding)
            except Exception:
                continue

    return previews


# ─── 5. Line Slicing, Header Skipping & File Tail ─────────────────────────────


def read_line_range(
    file_path: Union[str, Path],
    start_line: int,
    end_line: int,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Reads lines from index start_line to end_line (1-indexed, inclusive).

    Args:
        file_path: Path to file.
        start_line: Starting line number (1-based, >= 1).
        end_line: Ending line number (1-based, >= start_line).
        encoding: File encoding.

    Returns:
        List of line strings within the range.

    Raises:
        ValueError: If line ranges are invalid.
    """
    if start_line < 1:
        raise ValueError(f"start_line must be >= 1, got {start_line}.")
    if end_line < start_line:
        raise ValueError(
            f"end_line ({end_line}) must be >= start_line ({start_line})."
        )

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    selected: List[str] = []
    with open(path, "r", encoding=encoding, errors="replace") as f:
        for current_idx, line in enumerate(f, start=1):
            if current_idx > end_line:
                break
            if current_idx >= start_line:
                selected.append(line.rstrip("\r\n"))

    return selected


def skip_header_and_read_n_lines(
    file_path: Union[str, Path],
    header_lines: int,
    n: int,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Skips a designated number of header lines, then reads the next n lines.

    Args:
        file_path: Path to the file.
        header_lines: Number of header lines to skip (>= 0).
        n: Number of data lines to read (>= 0).
        encoding: File encoding.

    Returns:
        List of n lines after header.
    """
    if header_lines < 0 or n < 0:
        raise ValueError("header_lines and n must be non-negative.")

    return read_line_range(
        file_path,
        start_line=header_lines + 1,
        end_line=header_lines + n,
        encoding=encoding,
    )


def read_last_n_lines(
    file_path: Union[str, Path],
    n: int,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Reads the last n lines of a file (emulates Unix `tail`).

    Args:
        file_path: Path to the file.
        n: Number of lines from the end to read.
        encoding: File encoding.

    Returns:
        List of last n line strings.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}.")
    if n == 0:
        return []

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    from collections import deque

    with open(path, "r", encoding=encoding, errors="replace") as f:
        last_lines = deque(f, maxlen=n)

    return [line.rstrip("\r\n") for line in last_lines]


# ─── 6. Dummy File Generation & File Helpers ─────────────────────────────────


def create_dummy_file_with_lines(
    file_path: Union[str, Path],
    lines_content: List[str],
    encoding: str = "utf-8",
) -> Path:
    """
    Creates a text file containing specified line contents for testing/demonstration.

    Args:
        file_path: Destination path.
        lines_content: List of string lines to write.
        encoding: File encoding.

    Returns:
        Path object to created file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        for line in lines_content:
            f.write(f"{line}\n")
    return path


def create_sample_file_with_n_generated_lines(
    file_path: Union[str, Path],
    count: int,
    prefix: str = "Sample Line",
) -> Path:
    """
    Generates a sample file with 'count' sequentially numbered lines.

    Args:
        file_path: Destination path.
        count: Number of lines to generate.
        prefix: Line text prefix.

    Returns:
        Path object to created file.
    """
    lines = [f"{prefix} #{i + 1}" for i in range(count)]
    return create_dummy_file_with_lines(file_path, lines)


def validate_file_line_count(
    file_path: Union[str, Path],
    expected_count: int,
) -> bool:
    """
    Validates whether a file contains exactly the expected line count.

    Args:
        file_path: Path to the file.
        expected_count: Expected number of lines.

    Returns:
        True if line count matches expected_count, False otherwise.
    """
    try:
        actual = get_line_count(file_path)
        return actual == expected_count
    except (FileNotFoundError, IsADirectoryError):
        return False


def safe_delete_file(file_path: Union[str, Path]) -> bool:
    """
    Safely deletes a file if it exists.

    Args:
        file_path: Path to the file.

    Returns:
        True if deleted, False if file did not exist or failed to delete.
    """
    try:
        path = Path(file_path)
        if path.exists() and path.is_file():
            path.unlink()
            return True
        return False
    except OSError:
        return False





