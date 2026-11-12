# Day 94: Longest Common Prefix (LeetCode 14)
#
# Problem:
#   Write a function to find the longest common prefix string amongst an array
#   of strings. If there is no common prefix, return an empty string "".
#   Includes:
#     - Horizontal Scan O(S) where S is sum of all characters
#     - Vertical Column Scan O(S) with early termination on mismatch
#     - Divide-and-Conquer binary split LCP O(S)
#     - Binary Search over prefix length O(S * log(minLen))
#     - Lexicographical Sort-Endpoints O(N * L * log N)
#     - Prefix Tree (Trie) insertion & branch-stop traversal
#     - LeetCode 14 Solution wrapper
#     - Extensions: Longest Common Suffix & Pairwise LCP
#     - ASCII vertical alignment & divergence visualizer
#     - Multi-algorithm performance benchmark
#     - Comprehensive unit tests and Java practice code

import time
import unittest
from typing import List, Dict, Tuple, Any, Optional


# ─── 1. Horizontal, Vertical & Divide-and-Conquer LCP Solvers ─────────────────


def _validate_str_list(strs: List[str]) -> None:
    """Validates that strs is a list containing only string elements."""
    if not isinstance(strs, list):
        raise TypeError(f"strs must be a list of strings, got {type(strs).__name__}")
    for idx, item in enumerate(strs):
        if not isinstance(item, str):
            raise TypeError(f"Element at index {idx} must be a str, got {type(item).__name__}")


def lcp_horizontal_scan(strs: List[str]) -> str:
    """
    Finds Longest Common Prefix by iteratively shrinking prefix across strings.

    LCP(S1..Sn) = LCP(LCP(LCP(S1, S2), S3)...Sn)

    Time Complexity: O(S) where S is total characters across all strings.
    Space Complexity: O(1) auxiliary space (excluding result slice).

    Args:
        strs: List of strings.

    Returns:
        Longest common prefix string.
    """
    _validate_str_list(strs)
    if not strs:
        return ""

    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def lcp_vertical_scan(strs: List[str]) -> str:
    """
    Finds Longest Common Prefix by scanning character columns left-to-right.

    Stops immediately at the first character mismatch or shortest string boundary,
    making it optimal when the common prefix is short.

    Time Complexity: O(S) worst-case, O(N * minLen) best-case.
    Space Complexity: O(1) auxiliary space.

    Args:
        strs: List of strings.

    Returns:
        Longest common prefix string.
    """
    _validate_str_list(strs)
    if not strs:
        return ""

    first = strs[0]
    for col in range(len(first)):
        ch = first[col]
        for s in strs[1:]:
            if col == len(s) or s[col] != ch:
                return first[:col]
    return first


def _common_prefix_pair(left: str, right: str) -> str:
    """Computes LCP of two individual strings."""
    limit = min(len(left), len(right))
    for i in range(limit):
        if left[i] != right[i]:
            return left[:i]
    return left[:limit]


def lcp_divide_and_conquer(strs: List[str]) -> str:
    """
    Finds Longest Common Prefix using Divide-and-Conquer binary splitting.

    LCP(S[l..r]) = common_prefix(LCP(S[l..mid]), LCP(S[mid+1..r]))

    Time Complexity: O(S) total character comparisons.
    Space Complexity: O(m * log N) call stack frames (m = max string length).

    Args:
        strs: List of strings.

    Returns:
        Longest common prefix string.
    """
    _validate_str_list(strs)
    if not strs:
        return ""

    def _dnc_helper(lo: int, hi: int) -> str:
        if lo == hi:
            return strs[lo]
        mid = (lo + hi) // 2
        lcp_left = _dnc_helper(lo, mid)
        lcp_right = _dnc_helper(mid + 1, hi)
        return _common_prefix_pair(lcp_left, lcp_right)

    return _dnc_helper(0, len(strs) - 1)


def lcp_with_metrics(strs: List[str]) -> Tuple[str, Dict[str, Any]]:
    """
    Computes LCP via vertical scan while recording character comparison counts and timing.

    Args:
        strs: List of strings.

    Returns:
        Tuple of (lcp_result, metrics_dict).
    """
    _validate_str_list(strs)
    t0 = time.perf_counter()

    if not strs:
        return ("", {
            "num_strings": 0,
            "lcp_length": 0,
            "comparisons": 0,
            "time_seconds": time.perf_counter() - t0,
        })

    comparisons = 0
    first = strs[0]
    result = first

    for col in range(len(first)):
        ch = first[col]
        mismatch = False
        for s in strs[1:]:
            comparisons += 1
            if col == len(s) or s[col] != ch:
                result = first[:col]
                mismatch = True
                break
        if mismatch:
            break

    elapsed = time.perf_counter() - t0
    metrics = {
        "num_strings": len(strs),
        "min_length": min(len(s) for s in strs),
        "lcp_length": len(result),
        "comparisons": comparisons,
        "time_seconds": elapsed,
        "algorithm": "Vertical Column Scan O(S)",
    }
    return (result, metrics)



# ─── 2. Binary Search, Lexicographical Sort, Trie & LeetCode Solution ─────────


def lcp_binary_search(strs: List[str]) -> str:
    """
    Finds Longest Common Prefix via binary search over the prefix length space.

    Searches length mid in [1, min_len]. If all strings share prefix[:mid],
    searches upper half [mid + 1, high]; otherwise searches lower half.

    Time Complexity: O(S * log(minLen)) where S is total characters.
    Space Complexity: O(1) auxiliary space.

    Args:
        strs: List of strings.

    Returns:
        Longest common prefix string.
    """
    _validate_str_list(strs)
    if not strs:
        return ""

    min_len = min(len(s) for s in strs)
    if min_len == 0:
        return ""

    def _is_common_prefix(length: int) -> bool:
        candidate = strs[0][:length]
        return all(s.startswith(candidate) for s in strs[1:])

    low, high = 1, min_len
    while low <= high:
        mid = (low + high) // 2
        if _is_common_prefix(mid):
            low = mid + 1
        else:
            high = mid - 1

    return strs[0][: (low + high) // 2]


def lcp_sort_endpoints(strs: List[str]) -> str:
    """
    Finds Longest Common Prefix by lexicographically sorting and comparing extremes.

    In a lexicographically sorted array, the two strings with maximum divergence
    are guaranteed to be the very first and very last elements. Any prefix shared
    between strs[0] and strs[-1] is shared by all strings between them.

    Time Complexity: O(N * L * log N) dominated by string sorting.
    Space Complexity: O(N) for sorted list reference copy.

    Args:
        strs: List of strings.

    Returns:
        Longest common prefix string.
    """
    _validate_str_list(strs)
    if not strs:
        return ""

    ordered = sorted(strs)
    return _common_prefix_pair(ordered[0], ordered[-1])


class _TrieNode:
    """Internal Trie node tracking child branches and word termination."""

    def __init__(self) -> None:
        self.children: Dict[str, "_TrieNode"] = {}
        self.is_end: bool = False


def lcp_trie(strs: List[str]) -> str:
    """
    Finds Longest Common Prefix using a Prefix Tree (Trie).

    Inserts all strings into a Trie, then walks down from the root while each
    node has strictly 1 child and is not a word termination boundary.

    Time Complexity: O(S) to build and walk the Trie.
    Space Complexity: O(S) for Trie node storage.

    Args:
        strs: List of strings.

    Returns:
        Longest common prefix string.
    """
    _validate_str_list(strs)
    if not strs:
        return ""

    root = _TrieNode()
    for word in strs:
        if word == "":
            return ""
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.is_end = True

    prefix_chars: List[str] = []
    curr = root
    while len(curr.children) == 1 and not curr.is_end:
        ch, next_node = next(iter(curr.children.items()))
        prefix_chars.append(ch)
        curr = next_node

    return "".join(prefix_chars)


class Solution:
    """LeetCode 14: Longest Common Prefix solution wrapper."""

    def longestCommonPrefix(self, strs: List[str]) -> str:
        """Returns the longest common prefix string among strs."""
        return lcp_sort_endpoints(strs)
