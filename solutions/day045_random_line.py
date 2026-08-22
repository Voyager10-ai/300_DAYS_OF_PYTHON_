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


# ─── 3. Multiple Random Lines & Weighted Sampling ──────────────────────────────


def sample_k_random_lines(
    file_path: Union[str, Path],
    k: int,
    replace: bool = False,
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Samples K random lines from a file, either with or without replacement.

    Args:
        file_path: Path to the file.
        k: Number of lines to sample. Must be >= 0.
        replace: If True, samples with replacement. If False, samples without replacement.
        strip_newline: If True, strips trailing newlines.
        encoding: File encoding.

    Returns:
        List of selected random line strings.

    Raises:
        ValueError: If k < 0 or if k > total lines when replace=False.
    """
    if k < 0:
        raise ValueError("k must be non-negative")

    lines = read_all_lines_random(file_path, strip_newline=strip_newline, encoding=encoding)
    if k == 0 or not lines:
        return []

    if replace:
        return random.choices(lines, k=k)
    else:
        if k > len(lines):
            raise ValueError(f"Cannot sample {k} lines without replacement from a file with {len(lines)} lines")
        return random.sample(lines, k)


def weighted_random_line(
    file_path: Union[str, Path],
    weight_func: Optional[Callable[[str], float]] = None,
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> Optional[str]:
    """
    Selects a random line weighted by a given weight function (default: line length).

    Args:
        file_path: Path to the file.
        weight_func: Callable returning non-negative weight for a line string.
                     If None, defaults to len(line).
        strip_newline: If True, strips trailing newlines.
        encoding: File encoding.

    Returns:
        A randomly chosen line weighted by weight_func, or None if file is empty.
    """
    lines = read_all_lines_random(file_path, strip_newline=strip_newline, encoding=encoding)
    if not lines:
        return None

    if weight_func is None:
        weight_func = lambda line: float(len(line))

    weights = [max(0.0, float(weight_func(line))) for line in lines]
    total_weight = sum(weights)

    if total_weight <= 0:
        # Fall back to uniform choice if all weights are 0
        return random.choice(lines)

    return random.choices(lines, weights=weights, k=1)[0]


# ─── 4. Filtered Random Line Selection ─────────────────────────────────────────


def random_line_matching_predicate(
    file_path: Union[str, Path],
    predicate: Callable[[str], bool],
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> Optional[str]:
    """
    Selects a random line from a file that satisfies a predicate function.

    Args:
        file_path: Path to the file.
        predicate: Callable returning True for valid candidate lines.
        strip_newline: If True, strips trailing newlines.
        encoding: File encoding.

    Returns:
        A randomly chosen matching line, or None if no lines match.
    """
    lines = read_all_lines_random(file_path, strip_newline=strip_newline, encoding=encoding)
    matching = [line for line in lines if predicate(line)]
    if not matching:
        return None
    return random.choice(matching)


def random_line_matching_regex(
    file_path: Union[str, Path],
    pattern: str,
    flags: int = 0,
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> Optional[str]:
    """
    Selects a random line from a file that matches a regular expression pattern.

    Args:
        file_path: Path to the file.
        pattern: Regex pattern string.
        flags: Regex flags (e.g., re.IGNORECASE).
        strip_newline: If True, strips trailing newlines.
        encoding: File encoding.

    Returns:
        A randomly chosen regex-matching line, or None if no match found.
    """
    compiled_regex = re.compile(pattern, flags)
    return random_line_matching_predicate(
        file_path,
        predicate=lambda line: bool(compiled_regex.search(line)),
        strip_newline=strip_newline,
        encoding=encoding,
    )


def random_non_empty_line(
    file_path: Union[str, Path],
    strip_whitespace: bool = True,
    encoding: str = "utf-8",
) -> Optional[str]:
    """
    Selects a random non-empty line from a text file.

    Args:
        file_path: Path to the file.
        strip_whitespace: If True, considers whitespace-only lines as empty.
        encoding: File encoding.

    Returns:
        A random non-empty line, or None if file contains only empty lines.
    """
    if strip_whitespace:
        predicate = lambda line: bool(line.strip())
    else:
        predicate = lambda line: bool(line)

    return random_line_matching_predicate(
        file_path,
        predicate=predicate,
        strip_newline=True,
        encoding=encoding,
    )


# ─── 5. Multi-File & Directory Random Line Sampler ─────────────────────────────


def random_line_from_files(
    file_paths: List[Union[str, Path]],
    strip_newline: bool = True,
    encoding: str = "utf-8",
) -> Optional[Tuple[Path, int, str]]:
    """
    Selects a random line uniformly across multiple target text files.

    Args:
        file_paths: List of file paths.
        strip_newline: If True, strips trailing newlines.
        encoding: File encoding.

    Returns:
        Tuple of (selected_file_path, line_number, line_content), or None if no valid lines.
    """
    all_candidates: List[Tuple[Path, int, str]] = []

    for fp in file_paths:
        path = Path(fp)
        if not path.is_file():
            continue
        try:
            with open(path, "r", encoding=encoding, errors="replace") as f:
                for line_num, line in enumerate(f, start=1):
                    if strip_newline:
                        line = line.rstrip("\r\n")
                    all_candidates.append((path, line_num, line))
        except Exception:
            continue

    if not all_candidates:
        return None

    return random.choice(all_candidates)


def random_line_from_directory(
    directory_path: Union[str, Path],
    file_extension: str = ".txt",
    recursive: bool = False,
    encoding: str = "utf-8",
) -> Optional[Tuple[Path, int, str]]:
    """
    Scans a directory for matching files and selects a random line uniformly.

    Args:
        directory_path: Directory path to scan.
        file_extension: File extension filter (e.g., '.txt', '.py').
        recursive: If True, recursively scans subdirectories.
        encoding: File encoding.

    Returns:
        Tuple of (selected_file_path, line_number, line_content), or None if no files/lines found.
    """
    dir_path = Path(directory_path)
    if not dir_path.exists() or not dir_path.is_dir():
        raise NotADirectoryError(f"Directory not found: {directory_path}")

    pattern = f"**/*{file_extension}" if recursive else f"*{file_extension}"
    target_files = [f for f in dir_path.glob(pattern) if f.is_file()]

    if not target_files:
        return None

    return random_line_from_files(target_files, encoding=encoding)


# ─── 6. Fast Line Indexing & Byte-Offset Random Access ─────────────────────────


class LineIndexer:
    """
    Scans a text file once to index line start byte offsets.
    Enables O(1) random line retrieval without loading the whole file content into memory.
    """

    def __init__(self, file_path: Union[str, Path], encoding: str = "utf-8"):
        self.file_path = Path(file_path)
        self.encoding = encoding
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if self.file_path.is_dir():
            raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

        self.offsets: List[int] = []
        self._build_index()

    def _build_index(self) -> None:
        """Scans file in binary mode to record byte offset of each line's start."""
        self.offsets = []
        with open(self.file_path, "rb") as f:
            offset = 0
            self.offsets.append(offset)
            while True:
                line = f.readline()
                if not line:
                    break
                offset += len(line)
                self.offsets.append(offset)
        # Remove the final EOF offset if file is non-empty
        if len(self.offsets) > 1 and self.offsets[-1] == self.offsets[-2]:
            self.offsets.pop()

    @property
    def total_lines(self) -> int:
        """Returns total number of lines indexed in the file."""
        return max(0, len(self.offsets) - 1)

    def get_line_at(self, line_number: int, strip_newline: bool = True) -> str:
        """
        Retrieves line at 1-indexed line number in O(1) time using byte seeking.

        Args:
            line_number: 1-indexed line number (1 to total_lines).
            strip_newline: If True, strips trailing newline characters.

        Returns:
            Line string at the given position.

        Raises:
            IndexError: If line_number is out of bounds.
        """
        if line_number < 1 or line_number > self.total_lines:
            raise IndexError(f"Line number {line_number} out of range (1-{self.total_lines})")

        start_offset = self.offsets[line_number - 1]
        with open(self.file_path, "r", encoding=self.encoding, errors="replace") as f:
            f.seek(start_offset)
            line = f.readline()
            if strip_newline:
                return line.rstrip("\r\n")
            return line

    def get_random_line(self, strip_newline: bool = True) -> Optional[str]:
        """Returns a random line using indexed byte offsets."""
        if self.total_lines == 0:
            return None
        rand_idx = random.randint(1, self.total_lines)
        return self.get_line_at(rand_idx, strip_newline=strip_newline)

    def get_random_line_with_index(self, strip_newline: bool = True) -> Optional[Tuple[int, str]]:
        """Returns (line_number, line_content) of a randomly indexed line."""
        if self.total_lines == 0:
            return None
        rand_idx = random.randint(1, self.total_lines)
        return (rand_idx, self.get_line_at(rand_idx, strip_newline=strip_newline))


# ─── 7. Test Asset Helpers & Safe Encoding Fallbacks ──────────────────────────


def create_dummy_text_file(
    path: Union[str, Path],
    num_lines: int = 10,
    line_prefix: str = "Line",
    encoding: str = "utf-8",
) -> Path:
    """
    Creates a temporary dummy text file with N numbered lines for testing.

    Args:
        path: Path where the file should be created.
        num_lines: Number of lines to write.
        line_prefix: Prefix for each line.
        encoding: File encoding.

    Returns:
        Path object of created file.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding=encoding) as f:
        for i in range(1, num_lines + 1):
            f.write(f"{line_prefix} #{i}: Sample line text entry for testing.\n")
    return file_path


def clean_up_temp_file(path: Union[str, Path]) -> None:
    """Safely removes a test file if it exists."""
    file_path = Path(path)
    if file_path.exists() and file_path.is_file():
        try:
            file_path.unlink()
        except OSError:
            pass


def safe_get_random_line(
    file_path: Union[str, Path],
    encodings: Optional[List[str]] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Attempts to read a random line using a list of fallback encodings.

    Args:
        file_path: Path to the file.
        encodings: List of encodings to attempt in order (default: ['utf-8', 'latin-1', 'cp1252']).

    Returns:
        Tuple of (selected_line, encoding_used). Returns (None, None) if file read fails or file is empty.
    """
    if encodings is None:
        encodings = ["utf-8", "latin-1", "cp1252"]

    path = Path(file_path)
    if not path.exists() or path.is_dir():
        return (None, None)

    for enc in encodings:
        try:
            line = get_random_line(path, encoding=enc)
            return (line, enc)
        except (UnicodeDecodeError, Exception):
            continue

    return (None, None)


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestRandomLineOperations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)

        self.file_sample = self.dir_path / "sample.txt"
        self.sample_lines = [
            "Alpha entry line one",
            "Beta entry line two with extra text",
            "Gamma line three",
            "Delta line four with special characters !@#",
            "Epsilon final line five",
        ]
        with open(self.file_sample, "w", encoding="utf-8") as f:
            for line in self.sample_lines:
                f.write(f"{line}\n")

        self.file_empty = self.dir_path / "empty.txt"
        self.file_empty.touch()

        self.file_single = self.dir_path / "single.txt"
        with open(self.file_single, "w", encoding="utf-8") as f:
            f.write("Sole single line in file\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_random_line(self):
        line = get_random_line(self.file_sample)
        self.assertIsNotNone(line)
        self.assertIn(line, self.sample_lines)

    def test_get_random_line_with_index(self):
        result = get_random_line_with_index(self.file_sample)
        self.assertIsNotNone(result)
        line_num, line_content = result
        self.assertTrue(1 <= line_num <= len(self.sample_lines))
        self.assertEqual(self.sample_lines[line_num - 1], line_content)

    def test_empty_file_returns_none(self):
        self.assertIsNone(get_random_line(self.file_empty))
        self.assertIsNone(get_random_line_with_index(self.file_empty))
        self.assertIsNone(reservoir_sample_line(self.file_empty))
        self.assertEqual(reservoir_sample_k_lines(self.file_empty, k=3), [])

    def test_single_line_file(self):
        self.assertEqual(get_random_line(self.file_single), "Sole single line in file")
        res = get_random_line_with_index(self.file_single)
        self.assertEqual(res, (1, "Sole single line in file"))

    def test_reservoir_sample_line(self):
        result = reservoir_sample_line(self.file_sample)
        self.assertIsNotNone(result)
        line_num, line_content = result
        self.assertTrue(1 <= line_num <= len(self.sample_lines))
        self.assertEqual(self.sample_lines[line_num - 1], line_content)

    def test_reservoir_sample_k_lines(self):
        k_samples = reservoir_sample_k_lines(self.file_sample, k=3)
        self.assertEqual(len(k_samples), 3)
        for num, content in k_samples:
            self.assertTrue(1 <= num <= len(self.sample_lines))
            self.assertEqual(self.sample_lines[num - 1], content)

    def test_sample_k_random_lines(self):
        # Without replacement
        samples_no_rep = sample_k_random_lines(self.file_sample, k=3, replace=False)
        self.assertEqual(len(samples_no_rep), 3)
        self.assertEqual(len(set(samples_no_rep)), 3)

        # With replacement
        samples_rep = sample_k_random_lines(self.file_sample, k=10, replace=True)
        self.assertEqual(len(samples_rep), 10)

        # Exceeding k without replacement
        with self.assertRaises(ValueError):
            sample_k_random_lines(self.file_sample, k=10, replace=False)

    def test_weighted_random_line(self):
        line = weighted_random_line(self.file_sample)
        self.assertIsNotNone(line)
        self.assertIn(line, self.sample_lines)

    def test_filtered_random_lines(self):
        # Predicate
        pred_line = random_line_matching_predicate(
            self.file_sample, predicate=lambda l: "Beta" in l
        )
        self.assertEqual(pred_line, "Beta entry line two with extra text")

        # Regex
        regex_line = random_line_matching_regex(self.file_sample, pattern=r"special")
        self.assertEqual(regex_line, "Delta line four with special characters !@#")

        # Non-empty
        non_empty = random_non_empty_line(self.file_sample)
        self.assertIsNotNone(non_empty)

    def test_line_indexer(self):
        indexer = LineIndexer(self.file_sample)
        self.assertEqual(indexer.total_lines, 5)
        self.assertEqual(indexer.get_line_at(1), "Alpha entry line one")
        self.assertEqual(indexer.get_line_at(5), "Epsilon final line five")

        rand_line = indexer.get_random_line()
        self.assertIn(rand_line, self.sample_lines)

        with self.assertRaises(IndexError):
            indexer.get_line_at(0)
        with self.assertRaises(IndexError):
            indexer.get_line_at(6)

    def test_multi_file_and_directory_sampling(self):
        f2 = self.dir_path / "sample2.txt"
        with open(f2, "w", encoding="utf-8") as f:
            f.write("Sample2 standalone line\n")

        res_files = random_line_from_files([self.file_sample, f2])
        self.assertIsNotNone(res_files)
        path, num, content = res_files
        self.assertTrue(path in [self.file_sample, f2])

        res_dir = random_line_from_directory(self.dir_path, file_extension=".txt")
        self.assertIsNotNone(res_dir)

    def test_nonexistent_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            get_random_line(self.dir_path / "nonexistent.txt")







