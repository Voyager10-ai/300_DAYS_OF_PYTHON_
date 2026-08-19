# Day 42: File Size
#
# Problem:
#   Write a Python program to calculate, inspect, and analyze file sizes, directory totals,
#   human-readable representations (B, KB, MB, GB, TB), byte-level statistics, recursive
#   directory breakdowns, file size filtering, chunk streaming, disk space usage,
#   unit testing, and Java File size practice.

import os
import sys
import math
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Union


# ─── 1. Core File Size Retrieval & Formatting ──────────────────────────────────


def get_file_size_bytes(file_path: Union[str, Path]) -> int:
    """
    Returns the size of a file in bytes.

    Args:
        file_path: Path to the file.

    Returns:
        File size in bytes.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If path points to a directory instead of a file.

    Example:
        get_file_size_bytes("sample.txt") -> 1024
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise ValueError(f"Path is a directory, not a file: {file_path}")
    return path.stat().st_size


def format_file_size(size_in_bytes: int, binary: bool = False, decimal_places: int = 2) -> str:
    """
    Formats a byte count into a human-readable string (e.g., '1.02 KB' or '1.00 MiB').

    Args:
        size_in_bytes: Number of bytes.
        binary: If True, uses binary units (1024 base: KiB, MiB, GiB);
                if False, uses SI decimal units (1000 base: KB, MB, GB).
        decimal_places: Number of decimal places to round.

    Returns:
        Formatted human-readable string.

    Example:
        format_file_size(1048576) -> '1.05 MB'
        format_file_size(1048576, binary=True) -> '1.00 MiB'
    """
    if size_in_bytes < 0:
        raise ValueError("File size cannot be negative.")
    if size_in_bytes == 0:
        return "0 B"

    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"] if binary else ["B", "KB", "MB", "GB", "TB", "PB"]
    base = 1024.0 if binary else 1000.0

    exponent = min(int(math.log(size_in_bytes, base)), len(units) - 1)
    if exponent == 0:
        return f"{size_in_bytes} B"

    size_value = size_in_bytes / (base ** exponent)
    return f"{size_value:.{decimal_places}f} {units[exponent]}"


def get_formatted_file_size(
    file_path: Union[str, Path], binary: bool = False, decimal_places: int = 2
) -> str:
    """
    Utility function combining file size retrieval and human-readable formatting.

    Args:
        file_path: Path to the file.
        binary: If True, uses binary units (KiB, MiB); else decimal (KB, MB).
        decimal_places: Number of decimal places.

    Returns:
        Formatted file size string.

    Example:
        get_formatted_file_size("README.md") -> '1.20 KB'
    """
    bytes_size = get_file_size_bytes(file_path)
    return format_file_size(bytes_size, binary=binary, decimal_places=decimal_places)


# ─── 2. Multi-File & Directory Size Calculations ──────────────────────────────


def get_directory_total_size(dir_path: Union[str, Path], recursive: bool = True) -> int:
    """
    Calculates total size in bytes of all files in a directory.

    Args:
        dir_path: Path to the directory.
        recursive: If True, recursively scans subdirectories.

    Returns:
        Total size in bytes.

    Example:
        get_directory_total_size("solutions") -> 450123
    """
    path = Path(dir_path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {dir_path}")

    total = 0
    pattern = "**/*" if recursive else "*"
    for item in path.glob(pattern):
        if item.is_file() and not item.is_symlink():
            total += item.stat().st_size
    return total


def get_files_total_size(file_paths: List[Union[str, Path]]) -> int:
    """
    Calculates the aggregate size of a list of file paths.

    Args:
        file_paths: List of file paths.

    Returns:
        Combined total size in bytes.

    Example:
        get_files_total_size(["file1.txt", "file2.txt"]) -> 2048
    """
    total = 0
    for file_p in file_paths:
        p = Path(file_p)
        if p.is_file():
            total += p.stat().st_size
    return total


def get_directory_size_breakdown(dir_path: Union[str, Path]) -> Dict[str, int]:
    """
    Returns a dictionary mapping immediate subfolder and file names in a directory to their byte sizes.

    Args:
        dir_path: Path to directory.

    Returns:
        Dictionary {item_name: size_in_bytes}.

    Example:
        get_directory_size_breakdown(".") -> {"README.md": 1195, "solutions": 450123}
    """
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid directory path: {dir_path}")

    breakdown = {}
    for item in path.iterdir():
        if item.is_file() and not item.is_symlink():
            breakdown[item.name] = item.stat().st_size
        elif item.is_dir() and not item.is_symlink():
            breakdown[item.name] = get_directory_total_size(item, recursive=True)
    return breakdown

