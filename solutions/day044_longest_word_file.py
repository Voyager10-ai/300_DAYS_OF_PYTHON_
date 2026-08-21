# Day 44: Longest Word (File)
#
# Problem:
#   Write a Python program to find the longest word(s) in a text file.
#   Includes support for punctuation cleaning, case normalization, top-K ranking,
#   generator streaming for large files, regex tokenization, multi-file inspection,
#   unit tests, and Java practice.

import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List, Dict, Tuple, Set, Any, Callable, Optional, Union, Iterator
from collections import Counter


# ─── 1. Core Longest Word Retrieval Functions ─────────────────────────────────


def clean_word(word: str, strip_punctuation: bool = True) -> str:
    """
    Cleans a word token by optionally stripping surrounding and embedded punctuation.

    Args:
        word: Raw string token.
        strip_punctuation: If True, removes non-alphanumeric characters.

    Returns:
        Cleaned word string.
    """
    if not strip_punctuation:
        return word.strip()
    return re.sub(r"^[^\w]+|[^\w]+$", "", word)


def find_longest_word_in_file(
    file_path: Union[str, Path],
    strip_punctuation: bool = True,
    case_sensitive: bool = True,
    encoding: str = "utf-8",
) -> Optional[str]:
    """
    Finds and returns the first occurrence of the longest word in a file.

    Args:
        file_path: Path to the target file.
        strip_punctuation: If True, strips non-alphanumeric symbols.
        case_sensitive: If False, compares lengths on lowercased words.
        encoding: File encoding.

    Returns:
        The longest word string, or None if the file is empty/has no words.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If path points to a directory.
    """
    all_longest = find_all_longest_words_in_file(
        file_path,
        strip_punctuation=strip_punctuation,
        case_sensitive=case_sensitive,
        encoding=encoding,
    )
    return all_longest[0] if all_longest else None


def find_all_longest_words_in_file(
    file_path: Union[str, Path],
    strip_punctuation: bool = True,
    case_sensitive: bool = True,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Finds and returns all unique words in a file that share the maximum word length.

    Args:
        file_path: Path to the file.
        strip_punctuation: If True, strips non-alphanumeric symbols.
        case_sensitive: If False, returns lowercased unique words.
        encoding: File encoding.

    Returns:
        List of unique words sharing the maximum length found in the file.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    max_len = 0
    longest_words: Set[str] = set()

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            tokens = line.split()
            for token in tokens:
                cleaned = clean_word(token, strip_punctuation=strip_punctuation)
                if not cleaned:
                    continue
                target_word = cleaned if case_sensitive else cleaned.lower()
                word_len = len(target_word)

                if word_len > max_len:
                    max_len = word_len
                    longest_words = {target_word}
                elif word_len == max_len:
                    longest_words.add(target_word)

    return sorted(list(longest_words))


def get_max_word_length_in_file(
    file_path: Union[str, Path],
    strip_punctuation: bool = True,
    encoding: str = "utf-8",
) -> int:
    """
    Returns the length of the longest word in the file.

    Args:
        file_path: Path to the file.
        strip_punctuation: If True, cleans punctuation before measuring.
        encoding: File encoding.

    Returns:
        Integer length of the longest word (0 if file contains no words).
    """
    words = find_all_longest_words_in_file(
        file_path, strip_punctuation=strip_punctuation, encoding=encoding
    )
    return len(words[0]) if words else 0


# ─── 2. Top-K Longest Words & Word Length Statistics ──────────────────────────


def find_top_k_longest_words(
    file_path: Union[str, Path],
    k: int = 5,
    strip_punctuation: bool = True,
    encoding: str = "utf-8",
) -> List[Tuple[str, int]]:
    """
    Returns the top-K longest unique words in a file along with their lengths.

    Args:
        file_path: Path to the file.
        k: Maximum number of top words to return.
        strip_punctuation: If True, cleans punctuation from tokens.
        encoding: File encoding.

    Returns:
        List of (word, length) tuples sorted in descending order of length.
    """
    if k <= 0:
        return []

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    word_set: Set[str] = set()

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            for token in line.split():
                cleaned = clean_word(token, strip_punctuation=strip_punctuation)
                if cleaned:
                    word_set.add(cleaned)

    # Sort by length descending, then alphabetically ascending
    sorted_words = sorted(word_set, key=lambda w: (-len(w), w.lower()))
    return [(w, len(w)) for w in sorted_words[:k]]


def get_word_length_statistics(
    file_path: Union[str, Path],
    encoding: str = "utf-8",
) -> Dict[str, Any]:
    """
    Calculates word length statistics (total words, min length, max length, average length).

    Args:
        file_path: Path to the file.
        encoding: File encoding.

    Returns:
        Dict containing statistical metrics.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    lengths: List[int] = []

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            for token in line.split():
                cleaned = clean_word(token, strip_punctuation=True)
                if cleaned:
                    lengths.append(len(cleaned))

    if not lengths:
        return {
            "total_words": 0,
            "min_length": 0,
            "max_length": 0,
            "avg_length": 0.0,
        }

    return {
        "total_words": len(lengths),
        "min_length": min(lengths),
        "max_length": max(lengths),
        "avg_length": round(sum(lengths) / len(lengths), 2),
    }


def get_word_length_distribution(
    file_path: Union[str, Path],
    encoding: str = "utf-8",
) -> Dict[int, int]:
    """
    Computes a histogram distribution of word lengths in a file.

    Args:
        file_path: Path to the file.
        encoding: File encoding.

    Returns:
        Dict mapping length -> frequency count.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    freq: Counter = Counter()
    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            for token in line.split():
                cleaned = clean_word(token, strip_punctuation=True)
                if cleaned:
                    freq[len(cleaned)] += 1

    return dict(sorted(freq.items()))



# ─── 3. Streaming & Chunk-based Memory-Efficient Iterators ────────────────────


def stream_words_from_file(
    file_path: Union[str, Path],
    chunk_size: int = 65536,
    encoding: str = "utf-8",
) -> Iterator[str]:
    """
    Streams individual cleaned words from a potentially huge file using chunked byte buffer reading.

    Args:
        file_path: Path to the file.
        chunk_size: Size of chunk buffer in bytes (default: 64 KB).
        encoding: File encoding.

    Yields:
        Cleaned word strings incrementally.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    remainder = ""
    with open(path, "r", encoding=encoding, errors="replace") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                if remainder:
                    cleaned = clean_word(remainder, strip_punctuation=True)
                    if cleaned:
                        yield cleaned
                break

            text = remainder + chunk
            tokens = text.split()

            # The last token might be incomplete across chunk boundaries
            if not chunk.endswith((" ", "\n", "\r", "\t")):
                remainder = tokens.pop() if tokens else ""
            else:
                remainder = ""

            for token in tokens:
                cleaned = clean_word(token, strip_punctuation=True)
                if cleaned:
                    yield cleaned


def stream_longest_word_in_file(
    file_path: Union[str, Path],
    chunk_size: int = 65536,
    encoding: str = "utf-8",
) -> Tuple[Optional[str], int]:
    """
    Finds the longest word by streaming without loading the entire file into memory.

    Args:
        file_path: Path to the file.
        chunk_size: Chunk size in bytes.
        encoding: File encoding.

    Returns:
        Tuple of (longest_word, max_length).
    """
    longest_word: Optional[str] = None
    max_len = 0

    for word in stream_words_from_file(file_path, chunk_size=chunk_size, encoding=encoding):
        if len(word) > max_len:
            max_len = len(word)
            longest_word = word

    return longest_word, max_len


# ─── 4. Regex Tokenization & Filtering ────────────────────────────────────────


def find_longest_word_with_regex(
    file_path: Union[str, Path],
    pattern: str = r"\b[A-Za-z0-9'-]+\b",
    encoding: str = "utf-8",
) -> List[str]:
    """
    Extracts longest words matched by a custom regular expression pattern.

    Args:
        file_path: Path to the file.
        pattern: Regex pattern matching valid words.
        encoding: File encoding.

    Returns:
        List of unique longest words matching the pattern.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    regex = re.compile(pattern)
    max_len = 0
    longest_words: Set[str] = set()

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            matches = regex.findall(line)
            for m in matches:
                word_len = len(m)
                if word_len > max_len:
                    max_len = word_len
                    longest_words = {m}
                elif word_len == max_len and max_len > 0:
                    longest_words.add(m)

    return sorted(list(longest_words))


def find_longest_word_matching_predicate(
    file_path: Union[str, Path],
    predicate: Callable[[str], bool],
    encoding: str = "utf-8",
) -> Optional[str]:
    """
    Finds the longest word in a file that satisfies a custom filter predicate.

    Args:
        file_path: Path to the file.
        predicate: Callable function returning True if a word is eligible.
        encoding: File encoding.

    Returns:
        The longest word satisfying predicate, or None if none match.

    Example:
        >>> find_longest_word_matching_predicate("data.txt", lambda w: w.startswith("a"))
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    longest_word: Optional[str] = None
    max_len = 0

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            for token in line.split():
                cleaned = clean_word(token, strip_punctuation=True)
                if cleaned and predicate(cleaned):
                    if len(cleaned) > max_len:
                        max_len = len(cleaned)
                        longest_word = cleaned

    return longest_word


def filter_words_by_length_range(
    file_path: Union[str, Path],
    min_length: int = 1,
    max_length: Optional[int] = None,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Finds all unique words in a file whose length falls within [min_length, max_length].

    Args:
        file_path: Path to the file.
        min_length: Minimum length (inclusive).
        max_length: Optional maximum length (inclusive).
        encoding: File encoding.

    Returns:
        List of unique words sorted by length descending then alphabetically.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    matching_words: Set[str] = set()

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            for token in line.split():
                cleaned = clean_word(token, strip_punctuation=True)
                if not cleaned:
                    continue
                w_len = len(cleaned)
                if w_len >= min_length and (max_length is None or w_len <= max_length):
                    matching_words.add(cleaned)

    return sorted(matching_words, key=lambda w: (-len(w), w.lower()))


# ─── 5. Multi-File & Directory Longest Word Analysis ──────────────────────────


def find_longest_words_across_files(
    file_paths: List[Union[str, Path]],
    encoding: str = "utf-8",
) -> Dict[str, Optional[str]]:
    """
    Finds the longest word in each file from a list of file paths.

    Args:
        file_paths: List of target file paths.
        encoding: File encoding.

    Returns:
        Dict mapping file path string -> longest word found.
    """
    results: Dict[str, Optional[str]] = {}
    for fp in file_paths:
        p = Path(fp)
        if p.exists() and p.is_file():
            results[str(p)] = find_longest_word_in_file(p, encoding=encoding)
    return results


def find_overall_longest_word_in_directory(
    directory_path: Union[str, Path],
    file_extension: Optional[str] = None,
    encoding: str = "utf-8",
) -> Tuple[Optional[str], Optional[str], int]:
    """
    Scans a directory to find the overall longest word across all matching files.

    Args:
        directory_path: Path to directory.
        file_extension: Optional extension filter (e.g., '.py', '.txt').
        encoding: File encoding.

    Returns:
        Tuple of (longest_word, source_file_path, length).
    """
    dir_path = Path(directory_path)
    if not dir_path.exists() or not dir_path.is_dir():
        raise NotADirectoryError(f"Invalid directory path: {directory_path}")

    overall_longest: Optional[str] = None
    source_file: Optional[str] = None
    max_len = 0

    for entry in dir_path.iterdir():
        if entry.is_file():
            if file_extension and not entry.name.endswith(file_extension):
                continue
            try:
                word = find_longest_word_in_file(entry, encoding=encoding)
                if word and len(word) > max_len:
                    max_len = len(word)
                    overall_longest = word
                    source_file = entry.name
            except Exception:
                continue

    return overall_longest, source_file, max_len


# ─── 6. Dummy File Generation & File Helpers ─────────────────────────────────


def create_dummy_file_with_text(
    file_path: Union[str, Path],
    text: str,
    encoding: str = "utf-8",
) -> Path:
    """
    Creates a text file containing specified text for testing.

    Args:
        file_path: Destination path.
        text: Text string to write.
        encoding: File encoding.

    Returns:
        Path object to created file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(text)
    return path


def create_dummy_file_with_words(
    file_path: Union[str, Path],
    words: List[str],
    encoding: str = "utf-8",
) -> Path:
    """
    Creates a file containing space-separated words.

    Args:
        file_path: Destination path.
        words: List of word strings.
        encoding: File encoding.

    Returns:
        Path object to created file.
    """
    return create_dummy_file_with_text(file_path, " ".join(words), encoding=encoding)


def safe_delete_file(file_path: Union[str, Path]) -> bool:
    """
    Safely deletes a file if it exists.

    Args:
        file_path: Target file path.

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



# ─── 7. Safe File Opening & Encoding Fallbacks ────────────────────────────────


def safe_find_longest_word_in_file(
    file_path: Union[str, Path],
    candidate_encodings: Optional[List[str]] = None,
) -> Tuple[Optional[str], str]:
    """
    Attempts to read a file and find the longest word using a list of candidate encodings.

    Args:
        file_path: Path to target file.
        candidate_encodings: List of candidate encodings (default: ['utf-8', 'latin-1', 'cp1252']).

    Returns:
        Tuple of (longest_word, working_encoding_name).
    """
    if candidate_encodings is None:
        candidate_encodings = ["utf-8", "latin-1", "cp1252", "ascii"]

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    for enc in candidate_encodings:
        try:
            word = find_longest_word_in_file(path, encoding=enc)
            return word, enc
        except (UnicodeDecodeError, UnicodeError):
            continue

    # Fallback with error replacement
    word = find_longest_word_in_file(path, encoding="utf-8")
    return word, "utf-8 (replace)"


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestLongestWordFileOperations(unittest.TestCase):
    """Unit test suite for Day 44 Longest Word in File operations."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)

        # Sample test files
        self.file_sample = self.dir_path / "sample.txt"
        create_dummy_file_with_text(
            self.file_sample,
            "The quick brown fox jumps over the lazy dog.\n"
            "Python programming language is extraordinarily versatile and powerful!",
        )

        self.file_ties = self.dir_path / "ties.txt"
        create_dummy_file_with_words(self.file_ties, ["cat", "dog", "bat", "rat", "elephant", "dinosaur"])

        self.file_empty = self.dir_path / "empty.txt"
        create_dummy_file_with_text(self.file_empty, "")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_longest_word_in_file(self):
        longest = find_longest_word_in_file(self.file_sample)
        self.assertEqual(longest, "extraordinarily")

    def test_find_all_longest_words_in_file(self):
        ties = find_all_longest_words_in_file(self.file_ties)
        self.assertEqual(ties, ["dinosaur", "elephant"])

    def test_get_max_word_length_in_file(self):
        max_len = get_max_word_length_in_file(self.file_sample)
        self.assertEqual(max_len, 15)  # "extraordinarily" = 15 chars

    def test_empty_file_returns_none(self):
        self.assertIsNone(find_longest_word_in_file(self.file_empty))
        self.assertEqual(find_all_longest_words_in_file(self.file_empty), [])
        self.assertEqual(get_max_word_length_in_file(self.file_empty), 0)

    def test_find_top_k_longest_words(self):
        top3 = find_top_k_longest_words(self.file_sample, k=3)
        self.assertEqual(len(top3), 3)
        self.assertEqual(top3[0], ("extraordinarily", 15))
        self.assertEqual(top3[1], ("programming", 11))

    def test_word_length_statistics(self):
        stats = get_word_length_statistics(self.file_sample)
        self.assertGreater(stats["total_words"], 0)
        self.assertEqual(stats["max_length"], 15)
        self.assertGreater(stats["avg_length"], 0.0)

    def test_stream_longest_word_in_file(self):
        word, length = stream_longest_word_in_file(self.file_sample, chunk_size=16)
        self.assertEqual(word, "extraordinarily")
        self.assertEqual(length, 15)

    def test_find_longest_word_with_regex(self):
        matches = find_longest_word_with_regex(self.file_sample, pattern=r"\b[a-z]{1,5}\b")
        self.assertTrue(all(len(w) <= 5 for w in matches))

    def test_find_longest_word_matching_predicate(self):
        p_word = find_longest_word_matching_predicate(
            self.file_sample, predicate=lambda w: w.startswith("p")
        )
        self.assertEqual(p_word, "programming")

    def test_filter_words_by_length_range(self):
        filtered = filter_words_by_length_range(self.file_sample, min_length=10, max_length=12)
        self.assertIn("programming", filtered)

    def test_nonexistent_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            find_longest_word_in_file(self.dir_path / "missing.txt")


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" 🔍 Day 44: Longest Word in File Finder - Interactive Demo")
    print("=" * 60)

    # 1. Project README Analysis
    readme_path = Path("README.md")
    if readme_path.exists():
        longest = find_longest_word_in_file(readme_path)
        all_longest = find_all_longest_words_in_file(readme_path)
        max_len = get_max_word_length_in_file(readme_path)
        print(f"\n1. README.md Longest Word Analysis:")
        print(f"   Single Longest Word: '{longest}' ({max_len} chars)")
        print(f"   All Max Length Words: {all_longest}")

        print("\n2. Top 5 Longest Words in README.md:")
        top5 = find_top_k_longest_words(readme_path, k=5)
        for rank, (w, length) in enumerate(top5, start=1):
            print(f"   #{rank}: {w:<25} ({length} chars)")

        print("\n3. Word Length Statistics for README.md:")
        stats = get_word_length_statistics(readme_path)
        for key, val in stats.items():
            print(f"   {key:<15} : {val}")

    # 2. Solutions Directory Analysis
    solutions_dir = Path("solutions")
    if solutions_dir.exists():
        print("\n4. Overall Longest Word across 'solutions/' Directory:")
        word, source, length = find_overall_longest_word_in_directory(solutions_dir, file_extension=".py")
        print(f"   Longest Word : '{word}' ({length} chars)")
        print(f"   Found in File: {source}")

    # 3. Unit Test Suite Execution
    print("\n5. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLongestWordFileOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








