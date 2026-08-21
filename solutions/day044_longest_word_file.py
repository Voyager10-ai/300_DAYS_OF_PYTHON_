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
