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


# ─── 3. Rabin-Karp Rolling Hash Search Algorithm ─────────────────────────────


def rabin_karp_search(
    text: str,
    pattern: str,
    prime: int = 101,
    case_sensitive: bool = True,
) -> List[int]:
    """
    Performs Rabin-Karp pattern search algorithm using rolling hash functions.

    Args:
        text: Source text string to search within.
        pattern: Pattern substring to match.
        prime: Prime number modulus for hash collision avoidance (default 101).
        case_sensitive: If False, ignores casing.

    Returns:
        List of 0-indexed starting positions where pattern occurs in text.

    Raises:
        TypeError: If text or pattern is not a string.
        ValueError: If pattern is empty.
    """
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("Both text and pattern must be strings.")
    if not pattern:
        raise ValueError("Pattern string cannot be empty.")

    t = text if case_sensitive else text.lower()
    p = pattern if case_sensitive else pattern.lower()

    n = len(t)
    m = len(p)
    if m > n:
        return []

    d = 256  # Number of characters in alphabet
    p_hash = 0
    t_hash = 0
    h = 1

    # h = pow(d, m-1) % prime
    for i in range(m - 1):
        h = (h * d) % prime

    # Calculate initial hash values
    for i in range(m):
        p_hash = (d * p_hash + ord(p[i])) % prime
        t_hash = (d * t_hash + ord(t[i])) % prime

    indices = []

    for i in range(n - m + 1):
        if p_hash == t_hash:
            # Check characters one by one on hash collision
            if t[i : i + m] == p:
                indices.append(i)

        if i < n - m:
            t_hash = (d * (t_hash - ord(t[i]) * h) + ord(t[i + m])) % prime
            if t_hash < 0:
                t_hash += prime

    return indices


# ─── 4. Longest Common & Repeated Substring Finders ───────────────────────────


def find_longest_common_substring(
    s1: str,
    s2: str,
    case_sensitive: bool = True,
) -> str:
    """
    Finds the longest contiguous common substring between two strings s1 and s2 using DP matrix.

    Args:
        s1: First string.
        s2: Second string.
        case_sensitive: If False, ignores casing.

    Returns:
        The longest common substring (from s1 original casing).

    Raises:
        TypeError: If s1 or s2 is not a string.
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Both s1 and s2 must be strings.")
    if not s1 or not s2:
        return ""

    str1 = s1 if case_sensitive else s1.lower()
    str2 = s2 if case_sensitive else s2.lower()

    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    max_len = 0
    end_pos_s1 = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos_s1 = i

    if max_len == 0:
        return ""

    start_pos_s1 = end_pos_s1 - max_len
    return s1[start_pos_s1:end_pos_s1]


def find_longest_repeated_substring(text: str) -> str:
    """
    Finds the longest substring that appears at least twice in text.

    Args:
        text: Source string to analyze.

    Returns:
        Longest repeated substring string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if len(text) < 2:
        return ""

    n = len(text)
    # Generate Suffix Array
    suffixes = sorted([(text[i:], i) for i in range(n)])

    lrs = ""
    for i in range(n - 1):
        s1, idx1 = suffixes[i]
        s2, idx2 = suffixes[i + 1]

        # Calculate Longest Common Prefix (LCP) between adjacent suffixes
        j = 0
        min_l = min(len(s1), len(s2))
        while j < min_l and s1[j] == s2[j]:
            j += 1

        if j > len(lrs):
            lrs = s1[:j]

    return lrs


# ─── 5. Regex Pattern Locator & Context Extractor ────────────────────────────


def find_substring_regex(
    text: str,
    pattern: str,
    case_sensitive: bool = True,
) -> List[Dict[str, Any]]:
    """
    Finds matches of regex pattern in text returning match detail dicts.

    Args:
        text: Source text string.
        pattern: Regex pattern string.
        case_sensitive: If False, uses re.IGNORECASE.

    Returns:
        List of dicts containing 'match', 'start', 'end', and 'span'.

    Raises:
        TypeError: If text or pattern is not a string.
        re.error: If regex pattern is invalid.
    """
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("Both text and pattern must be strings.")

    flags = 0 if case_sensitive else re.IGNORECASE
    matches = []

    for match in re.finditer(pattern, text, flags):
        matches.append(
            {
                "match": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "span": match.span(),
            }
        )

    return matches


def extract_substring_context(
    text: str,
    sub: str,
    window: int = 15,
    case_sensitive: bool = True,
) -> List[str]:
    """
    Extracts text snippets surrounding every occurrence of sub with a context window.

    Args:
        text: Source text string.
        sub: Substring to locate.
        window: Number of context characters before and after match (default 15).
        case_sensitive: If False, ignores letter case.

    Returns:
        List of snippet strings formatted like '...context [sub] context...'.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If window is negative or sub is empty.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("Both text and sub must be strings.")
    if window < 0:
        raise ValueError(f"window size cannot be negative, got {window}")
    if not sub:
        raise ValueError("Substring 'sub' cannot be empty.")

    indices = find_all_substring_indices(text, sub, allow_overlap=False, case_sensitive=case_sensitive)
    snippets = []
    sub_len = len(sub)

    for idx in indices:
        start = max(0, idx - window)
        end = min(len(text), idx + sub_len + window)

        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(text) else ""

        match_str = text[idx : idx + sub_len]
        left_ctx = text[start:idx]
        right_ctx = text[idx + sub_len : end]

        snippets.append(f"{prefix}{left_ctx}[{match_str}]{right_ctx}{suffix}")

    return snippets


# ─── 6. Substring Replacement & Highlight Helpers ─────────────────────────────


def replace_substring_occurrences(
    text: str,
    sub: str,
    replacement: str,
    count: Optional[int] = None,
    case_sensitive: bool = True,
) -> str:
    """
    Replaces occurrences of sub with replacement string (with optional case insensitivity).

    Args:
        text: Source text string.
        sub: Substring to be replaced.
        replacement: Replacement text.
        count: Max replacements to make (or None for all).
        case_sensitive: If False, performs case-insensitive replacement.

    Returns:
        Transformed output string.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If sub is empty string.
    """
    if not isinstance(text, str) or not isinstance(sub, str) or not isinstance(replacement, str):
        raise TypeError("text, sub, and replacement must all be strings.")
    if not sub:
        raise ValueError("Substring 'sub' cannot be empty.")

    if case_sensitive:
        if count is None:
            return text.replace(sub, replacement)
        return text.replace(sub, replacement, count)

    # Case-insensitive replacement using regex
    pattern = re.escape(sub)
    c = 0 if count is None else count
    return re.sub(pattern, replacement, text, count=c, flags=re.IGNORECASE)


def highlight_substring_occurrences(
    text: str,
    sub: str,
    left_tag: str = "<<",
    right_tag: str = ">>",
    case_sensitive: bool = True,
) -> str:
    """
    Wraps all occurrences of sub in text with custom tags like <<substr>>.

    Args:
        text: Source text.
        sub: Substring to highlight.
        left_tag: Prefix tag label (default '<<').
        right_tag: Suffix tag label (default '>>').
        case_sensitive: If False, ignores letter case while preserving original text.

    Returns:
        Highlighted text string.

    Raises:
        TypeError: If inputs are not strings.
        ValueError: If sub is empty.
    """
    if not isinstance(text, str) or not isinstance(sub, str):
        raise TypeError("text and sub must be strings.")
    if not sub:
        raise ValueError("Substring 'sub' cannot be empty.")

    if case_sensitive:
        return text.replace(sub, f"{left_tag}{sub}{right_tag}")

    pattern = re.escape(sub)

    def replacer(match: re.Match) -> str:
        return f"{left_tag}{match.group(0)}{right_tag}"

    return re.sub(pattern, replacer, text, flags=re.IGNORECASE)


# ─── 7. Unit Test Suite ───────────────────────────────────────────────────────


class TestFindSubstring(unittest.TestCase):
    """Test suite for substring find, match, KMP, Rabin-Karp, and analysis utilities."""

    def test_core_substring_index(self):
        self.assertEqual(find_substring_index("hello world", "world"), 6)
        self.assertEqual(find_substring_index("hello world", "WORLD", case_sensitive=False), 6)
        self.assertEqual(find_substring_index("hello world", "python"), -1)
        self.assertEqual(find_all_substring_indices("abababa", "aba", allow_overlap=False), [0, 4])
        self.assertEqual(find_all_substring_indices("abababa", "aba", allow_overlap=True), [0, 2, 4])

        with self.assertRaises(TypeError):
            find_substring_index(12345, "1")

    def test_kmp_search(self):
        text = "ABABDABACDABABCABAB"
        pattern = "ABABCABAB"
        indices = kmp_search(text, pattern)
        self.assertEqual(indices, [10])

        self.assertEqual(kmp_search("aaaaa", "aa"), [0, 1, 2, 3])

        with self.assertRaises(ValueError):
            kmp_search("hello", "")

    def test_rabin_karp_search(self):
        text = "GEEKS FOR GEEKS"
        pattern = "GEEK"
        self.assertEqual(rabin_karp_search(text, pattern), [0, 10])
        self.assertEqual(rabin_karp_search("python code", "CODE", case_sensitive=False), [7])

    def test_lcs_and_lrs(self):
        self.assertEqual(find_longest_common_substring("abcdef", "zbcdf"), "bcd")
        self.assertEqual(find_longest_common_substring("Hello World", "world", case_sensitive=False), "World")

        self.assertEqual(find_longest_repeated_substring("banana"), "ana")
        self.assertEqual(find_longest_repeated_substring("abcdef"), "")

    def test_regex_and_context(self):
        text = "Python 3.9 and Python 3.10 and Python 3.11"
        matches = find_substring_regex(text, r"Python \d+\.\d+")
        self.assertEqual(len(matches), 3)
        self.assertEqual(matches[0]["match"], "Python 3.9")

        text_ctx = "The fast brown fox jumped over the lazy sleeping dog"
        snippets = extract_substring_context(text_ctx, "fox", window=10)
        self.assertEqual(len(snippets), 1)
        self.assertIn("[fox]", snippets[0])

    def test_replace_and_highlight(self):
        text = "Apple, apple, APPLE"
        replaced = replace_substring_occurrences(text, "apple", "fruit", case_sensitive=False)
        self.assertEqual(replaced, "fruit, fruit, fruit")

        highlighted = highlight_substring_occurrences("Hello Python!", "Python", left_tag="[", right_tag="]")
        self.assertEqual(highlighted, "Hello [Python]!")






