# Day 66: Find Substring
#
# Problem:
#   Write a Python program / module to locate, match, and analyze substrings within text strings.
#   Includes core index finders, KMP (Knuth-Morris-Pratt) algorithm, Rabin-Karp rolling hash search,
#   longest common substring (LCS), longest repeated substring, regex locators, context window extractors,
#   substring replacement/highlighting, unit test suite, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Substring Search & Index Finders ─────────────────────────────────


def find_substring_index(
    text: str,
    sub: str,
    start: int = 0,
    case_sensitive: bool = True,
) -> int:
    """
    Finds the first starting index of substring sub in text.

    Args:
        text: Target text string to search within.
        sub: Substring pattern to find.
        start: Starting character position index for search (default 0).
        case_sensitive: If False, ignores letter casing.

    Returns:
        0-indexed integer position of first match, or -1 if not found.

    Raises:
        TypeError: If text or sub is not a string.
        ValueError: If start index is negative.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("Both text and sub must be strings.")
    if start < 0:
        raise ValueError(f"start index cannot be negative, got {start}")

    if not sub:
        return min(start, len(text))

    t = text if case_sensitive else text.lower()
    s = sub if case_sensitive else sub.lower()

    return t.find(s, start)


def find_all_substring_indices(
    text: str,
    sub: str,
    allow_overlap: bool = False,
    case_sensitive: bool = True,
) -> List[int]:
    """
    Finds starting indices of all occurrences of sub in text.

    Args:
        text: Source text string.
        sub: Substring pattern to search for.
        allow_overlap: If True, returns overlapping match positions.
        case_sensitive: If False, performs case-insensitive search.

    Returns:
        List of 0-indexed starting positions where sub occurs.

    Raises:
        TypeError: If inputs are not strings.
        ValueError: If sub is an empty string.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("Both text and sub must be strings.")
    if not sub:
        raise ValueError("Substring 'sub' cannot be empty.")

    t = text if case_sensitive else text.lower()
    s = sub if case_sensitive else sub.lower()

    indices = []
    start = 0
    step = 1 if allow_overlap else len(s)

    while True:
        pos = t.find(s, start)
        if pos == -1:
            break
        indices.append(pos)
        start = pos + step

    return indices


# ─── 2. Knuth-Morris-Pratt (KMP) Pattern Search ───────────────────────────────


def compute_lps_array(pattern: str) -> List[int]:
    """
    Computes the Longest Prefix Suffix (LPS) array for KMP algorithm.

    lps[i] stores the length of the longest proper prefix of pattern[0..i]
    that is also a suffix of pattern[0..i].

    Args:
        pattern: The search pattern string.

    Returns:
        List of integers representing the LPS lookup table.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str, case_sensitive: bool = True) -> List[int]:
    """
    Performs Knuth-Morris-Pratt (KMP) string matching algorithm in O(N + M) time complexity.

    Args:
        text: Target text string to search within.
        pattern: Pattern substring to find.
        case_sensitive: If False, performs case-insensitive KMP search.

    Returns:
        List of starting indices where pattern matches text.

    Raises:
        TypeError: If inputs are not strings.
        ValueError: If pattern is empty.
    """
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("Both text and pattern must be strings.")
    if not pattern:
        raise ValueError("Search pattern cannot be empty.")

    t = text if case_sensitive else text.lower()
    p = pattern if case_sensitive else pattern.lower()

    n = len(t)
    m = len(p)
    if m > n:
        return []

    lps = compute_lps_array(p)
    indices = []
    i = 0  # index for t
    j = 0  # index for p

    while i < n:
        if p[j] == t[i]:
            i += 1
            j += 1

        if j == m:
            indices.append(i - j)
            j = lps[j - 1]
        elif i < n and p[j] != t[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return indices

