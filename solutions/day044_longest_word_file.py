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




