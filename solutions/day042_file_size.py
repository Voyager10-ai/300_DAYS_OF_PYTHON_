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


# ─── 3. File Size Filtering & Search Functions ────────────────────────────────


def filter_files_by_size(
    dir_path: Union[str, Path],
    min_bytes: Optional[int] = None,
    max_bytes: Optional[int] = None,
    recursive: bool = True,
) -> List[str]:
    """
    Filters files in a directory matching specified byte size boundaries [min_bytes, max_bytes].

    Args:
        dir_path: Directory to search.
        min_bytes: Minimum size in bytes (inclusive), if any.
        max_bytes: Maximum size in bytes (inclusive), if any.
        recursive: If True, searches subdirectories.

    Returns:
        List of matching file path strings.

    Example:
        filter_files_by_size("solutions", min_bytes=10000, max_bytes=20000)
    """
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid directory path: {dir_path}")

    pattern = "**/*" if recursive else "*"
    matched = []
    for item in path.glob(pattern):
        if item.is_file() and not item.is_symlink():
            size = item.stat().st_size
            if min_bytes is not None and size < min_bytes:
                continue
            if max_bytes is not None and size > max_bytes:
                continue
            matched.append(str(item))
    return matched


def find_largest_file(dir_path: Union[str, Path], recursive: bool = True) -> Optional[Tuple[str, int]]:
    """
    Finds the largest file in a directory.

    Args:
        dir_path: Directory path.
        recursive: If True, scans recursively.

    Returns:
        Tuple of (file_path_str, size_in_bytes) or None if directory is empty.

    Example:
        find_largest_file("solutions") -> ("solutions/day029_html_tag.py", 26065)
    """
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        return None

    pattern = "**/*" if recursive else "*"
    largest: Optional[Tuple[str, int]] = None
    for item in path.glob(pattern):
        if item.is_file() and not item.is_symlink():
            size = item.stat().st_size
            if largest is None or size > largest[1]:
                largest = (str(item), size)
    return largest


def find_smallest_file(dir_path: Union[str, Path], recursive: bool = True) -> Optional[Tuple[str, int]]:
    """
    Finds the smallest file in a directory.

    Args:
        dir_path: Directory path.
        recursive: If True, scans recursively.

    Returns:
        Tuple of (file_path_str, size_in_bytes) or None if directory is empty.

    Example:
        find_smallest_file("solutions") -> ("solutions/day031_remove_nth_character.py", 378)
    """
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        return None

    pattern = "**/*" if recursive else "*"
    smallest: Optional[Tuple[str, int]] = None
    for item in path.glob(pattern):
        if item.is_file() and not item.is_symlink():
            size = item.stat().st_size
            if smallest is None or size < smallest[1]:
                smallest = (str(item), size)
    return smallest


# ─── 4. Chunk-Based Streaming & File Comparison Utilities ────────────────────


def count_bytes_by_streaming(file_path: Union[str, Path], chunk_size: int = 8192) -> int:
    """
    Calculates file size by physically reading byte chunks from disk.

    Args:
        file_path: Path to the file.
        chunk_size: Size of chunk buffer in bytes (default 8KB).

    Returns:
        Total bytes read.

    Example:
        count_bytes_by_streaming("README.md") -> 1195
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    total_bytes = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
    return total_bytes


def count_line_and_char_byte_stats(file_path: Union[str, Path]) -> Dict[str, Union[int, float]]:
    """
    Returns detailed text file size statistics including bytes, chars, lines, and avg bytes per line.

    Args:
        file_path: Path to text file.

    Returns:
        Dict with keys: 'bytes', 'chars', 'lines', 'avg_bytes_per_line'.

    Example:
        count_line_and_char_byte_stats("README.md")
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    total_bytes = path.stat().st_size
    lines = 0
    chars = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            lines += 1
            chars += len(line)

    avg_bytes = (total_bytes / lines) if lines > 0 else 0.0
    return {
        "bytes": total_bytes,
        "chars": chars,
        "lines": lines,
        "avg_bytes_per_line": round(avg_bytes, 2),
    }


def compare_file_sizes(
    file_path1: Union[str, Path], file_path2: Union[str, Path]
) -> Dict[str, Any]:
    """
    Compares the size of two files.

    Args:
        file_path1: Path to first file.
        file_path2: Path to second file.

    Returns:
        Dict with comparison statistics: 'size1', 'size2', 'difference', 'larger_file'.

    Example:
        compare_file_sizes("fileA.txt", "fileB.txt")
    """
    s1 = get_file_size_bytes(file_path1)
    s2 = get_file_size_bytes(file_path2)

    diff = abs(s1 - s2)
    larger = (
        str(file_path1) if s1 > s2 else (str(file_path2) if s2 > s1 else "equal")
    )
    return {
        "size1": s1,
        "size2": s2,
        "difference_bytes": diff,
        "larger_file": larger,
        "ratio": round(s1 / s2, 2) if s2 > 0 else float("inf"),
    }


# ─── 5. Extension Breakdown & Size Statistics ─────────────────────────────────


def get_size_by_file_extension(
    dir_path: Union[str, Path], recursive: bool = True
) -> Dict[str, int]:
    """
    Groups total accumulated file size by extension (e.g. '.py', '.txt', '.java').

    Args:
        dir_path: Directory path.
        recursive: If True, scans recursively.

    Returns:
        Dict mapping extension (e.g. '.py') to total size in bytes.

    Example:
        get_size_by_file_extension("solutions") -> {".py": 450123}
    """
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid directory path: {dir_path}")

    pattern = "**/*" if recursive else "*"
    ext_sizes: Dict[str, int] = {}
    for item in path.glob(pattern):
        if item.is_file() and not item.is_symlink():
            ext = item.suffix.lower() if item.suffix else "no_extension"
            ext_sizes[ext] = ext_sizes.get(ext, 0) + item.stat().st_size
    return ext_sizes


def get_file_size_distribution(
    dir_path: Union[str, Path], recursive: bool = True
) -> Dict[str, int]:
    """
    Categorizes files in a directory into standard size bins.

    Bins:
        '< 1 KB'
        '1 KB - 100 KB'
        '100 KB - 1 MB'
        '1 MB - 10 MB'
        '> 10 MB'

    Args:
        dir_path: Directory path.
        recursive: If True, scans recursively.

    Returns:
        Dict mapping category name to count of matching files.

    Example:
        get_file_size_distribution("solutions")
    """
    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid directory path: {dir_path}")

    bins = {
        "< 1 KB": 0,
        "1 KB - 100 KB": 0,
        "100 KB - 1 MB": 0,
        "1 MB - 10 MB": 0,
        "> 10 MB": 0,
    }

    pattern = "**/*" if recursive else "*"
    for item in path.glob(pattern):
        if item.is_file() and not item.is_symlink():
            size = item.stat().st_size
            if size < 1024:
                bins["< 1 KB"] += 1
            elif size < 100 * 1024:
                bins["1 KB - 100 KB"] += 1
            elif size < 1024 * 1024:
                bins["100 KB - 1 MB"] += 1
            elif size < 10 * 1024 * 1024:
                bins["1 MB - 10 MB"] += 1
            else:
                bins["> 10 MB"] += 1
    return bins


# ─── 6. Dummy File Creation & Size Integrity Validation ───────────────────────


def create_dummy_file_with_size(file_path: Union[str, Path], target_size_bytes: int) -> str:
    """
    Creates a file with exact specified byte size for testing.

    Args:
        file_path: Destination file path.
        target_size_bytes: Target byte size.

    Returns:
        Absolute string path to created file.

    Example:
        create_dummy_file_with_size("test_1024.dat", 1024)
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.seek(max(0, target_size_bytes - 1))
        f.write(b"\0" if target_size_bytes > 0 else b"")
    return str(path.resolve())


def verify_file_size_integrity(file_path: Union[str, Path], expected_bytes: int) -> bool:
    """
    Verifies if a file exists and matches the exact expected size in bytes.

    Args:
        file_path: Path to the file.
        expected_bytes: Expected byte count.

    Returns:
        True if file exists and size matches expected_bytes, False otherwise.

    Example:
        verify_file_size_integrity("README.md", 1195) -> True
    """
    try:
        actual_size = get_file_size_bytes(file_path)
        return actual_size == expected_bytes
    except (FileNotFoundError, ValueError):
        return False


def safe_delete_file(file_path: Union[str, Path]) -> bool:
    """
    Safely deletes a file if it exists.

    Args:
        file_path: Path to file.

    Returns:
        True if file was deleted, False if file did not exist.
    """
    path = Path(file_path)
    if path.is_file():
        path.unlink()
        return True
    return False


# ─── 7. Disk Usage & Partition Space Inspection ───────────────────────────────


def get_disk_usage_stats(path: Union[str, Path] = ".") -> Dict[str, Union[int, str, float]]:
    """
    Returns disk usage statistics for the filesystem partition containing `path`.

    Args:
        path: Path in the filesystem (default current directory '.').

    Returns:
        Dict with keys: 'total_bytes', 'used_bytes', 'free_bytes', 'percent_used',
                        'total_formatted', 'used_formatted', 'free_formatted'.

    Example:
        get_disk_usage_stats(".")
    """
    usage = shutil.disk_usage(path)
    total = usage.total
    used = usage.used
    free = usage.free
    pct = round((used / total * 100), 2) if total > 0 else 0.0

    return {
        "total_bytes": total,
        "used_bytes": used,
        "free_bytes": free,
        "percent_used": pct,
        "total_formatted": format_file_size(total),
        "used_formatted": format_file_size(used),
        "free_formatted": format_file_size(free),
    }


def get_file_size_percentage_of_disk(
    file_path: Union[str, Path], disk_path: Union[str, Path] = "."
) -> float:
    """
    Calculates percentage of total disk partition space occupied by a single file.

    Args:
        file_path: Path to target file.
        disk_path: Disk partition path.

    Returns:
        Percentage float (0.0 to 100.0).

    Example:
        get_file_size_percentage_of_disk("README.md") -> 0.000002
    """
    file_size = get_file_size_bytes(file_path)
    total_disk = shutil.disk_usage(disk_path).total
    if total_disk == 0:
        return 0.0
    return round((file_size / total_disk) * 100, 6)


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestFileSizeOperations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Create dummy test files
        self.file_100b = create_dummy_file_with_size(self.temp_path / "file100.txt", 100)
        self.file_2000b = create_dummy_file_with_size(self.temp_path / "file2000.bin", 2000)
        self.sub_dir = self.temp_path / "sub"
        self.sub_dir.mkdir()
        self.file_sub = create_dummy_file_with_size(self.sub_dir / "file_sub.py", 500)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_file_size_and_format(self):
        self.assertEqual(get_file_size_bytes(self.file_100b), 100)
        self.assertEqual(format_file_size(0), "0 B")
        self.assertEqual(format_file_size(500), "500 B")
        self.assertEqual(format_file_size(1000), "1.00 KB")
        self.assertEqual(format_file_size(1024, binary=True), "1.00 KiB")

    def test_directory_size_and_breakdown(self):
        # 100 + 2000 + 500 = 2600 bytes
        total_size = get_directory_total_size(self.temp_path, recursive=True)
        self.assertEqual(total_size, 2600)
        breakdown = get_directory_size_breakdown(self.temp_path)
        self.assertIn("file100.txt", breakdown)
        self.assertEqual(breakdown["file100.txt"], 100)
        self.assertIn("sub", breakdown)
        self.assertEqual(breakdown["sub"], 500)

    def test_filtering_and_search(self):
        files_over_1k = filter_files_by_size(self.temp_path, min_bytes=1000)
        self.assertEqual(len(files_over_1k), 1)
        self.assertTrue(files_over_1k[0].endswith("file2000.bin"))

        largest = find_largest_file(self.temp_path)
        self.assertIsNotNone(largest)
        self.assertEqual(largest[1], 2000)

        smallest = find_smallest_file(self.temp_path)
        self.assertIsNotNone(smallest)
        self.assertEqual(smallest[1], 100)

    def test_streaming_and_comparison(self):
        streamed_bytes = count_bytes_by_streaming(self.file_2000b, chunk_size=256)
        self.assertEqual(streamed_bytes, 2000)

        comp = compare_file_sizes(self.file_2000b, self.file_100b)
        self.assertEqual(comp["size1"], 2000)
        self.assertEqual(comp["size2"], 100)
        self.assertEqual(comp["difference_bytes"], 1900)

    def test_extension_and_distribution(self):
        ext_sizes = get_size_by_file_extension(self.temp_path)
        self.assertEqual(ext_sizes[".txt"], 100)
        self.assertEqual(ext_sizes[".bin"], 2000)
        self.assertEqual(ext_sizes[".py"], 500)

        dist = get_file_size_distribution(self.temp_path)
        self.assertEqual(dist["< 1 KB"], 2)  # 100b and 500b
        self.assertEqual(dist["1 KB - 100 KB"], 1)  # 2000b

    def test_integrity_and_disk_usage(self):
        self.assertTrue(verify_file_size_integrity(self.file_100b, 100))
        self.assertFalse(verify_file_size_integrity(self.file_100b, 999))

        disk_stats = get_disk_usage_stats(".")
        self.assertIn("total_bytes", disk_stats)
        self.assertGreater(disk_stats["total_bytes"], 0)

        pct = get_file_size_percentage_of_disk(self.file_100b)
        self.assertGreaterEqual(pct, 0.0)







