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



# ─── 3. Extensions, Visualizer & Performance Benchmarking ─────────────────────


def longest_common_suffix(strs: List[str]) -> str:
    """
    Finds the Longest Common Suffix across a list of strings.

    Args:
        strs: List of strings.

    Returns:
        Longest common suffix string.
    """
    _validate_str_list(strs)
    if not strs:
        return ""

    reversed_strs = [s[::-1] for s in strs]
    return lcp_vertical_scan(reversed_strs)[::-1]


def longest_common_prefix_k_strings(strs: List[str], k: int) -> str:
    """
    Finds the longest prefix shared by at least k strings in strs.

    Uses a frequency-annotated Trie to find the deepest node visited >= k times.

    Args:
        strs: List of strings.
        k: Minimum number of strings sharing the prefix (1 <= k <= len(strs)).

    Returns:
        Longest prefix string shared by >= k strings.
    """
    _validate_str_list(strs)
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")
    if len(strs) < k:
        return ""

    # Node structure: [children_dict, visit_count]
    root: Dict[str, Any] = {"children": {}, "count": 0}
    for word in strs:
        node = root
        for ch in word:
            if ch not in node["children"]:
                node["children"][ch] = {"children": {}, "count": 0}
            node = node["children"][ch]
            node["count"] += 1

    best_prefix = ""

    def _dfs(node: Dict[str, Any], path: List[str]) -> None:
        nonlocal best_prefix
        if len(path) > len(best_prefix):
            best_prefix = "".join(path)
        for ch, child in node["children"].items():
            if child["count"] >= k:
                path.append(ch)
                _dfs(child, path)
                path.pop()

    _dfs(root, [])
    return best_prefix


def visualize_lcp_vertical_scan(strs: List[str]) -> str:
    """
    Renders an ASCII vertical alignment diagram highlighting matching prefix vs divergence.

    Args:
        strs: List of strings to visualize.

    Returns:
        Formatted ASCII diagram string.
    """
    _validate_str_list(strs)
    if not strs:
        return "Empty string list."

    lcp = lcp_vertical_scan(strs)
    lcp_len = len(lcp)
    max_len = max(len(s) for s in strs)

    lines: List[str] = []
    lines.append(f"Longest Common Prefix Alignment (Result: '{lcp}', Length: {lcp_len})")
    lines.append("=" * 68)

    idx_header = "        " + " ".join(f"{i:<2}" for i in range(max_len))
    lines.append(idx_header)
    lines.append("       +" + "---" * max_len + "+")

    for r, word in enumerate(strs):
        padded = "  ".join(word[c] if c < len(word) else "." for c in range(max_len))
        lines.append(f"  S{r:<3} | {padded}  |")

    lines.append("       +" + "---" * max_len + "+")
    marker_cells = [
        "==" if c < lcp_len else ("^^" if c == lcp_len else "  ")
        for c in range(max_len)
    ]
    lines.append("  Match  " + " ".join(marker_cells))
    lines.append("=" * 68)
    return "\n".join(lines)


def benchmark_lcp_algorithms(
    dataset_sizes: Optional[List[int]] = None,
    prefix_len: int = 20,
    iterations: int = 10,
) -> Dict[str, Any]:
    """
    Benchmarks all 6 LCP strategies across datasets of growing sizes.

    Args:
        dataset_sizes: List of string counts per dataset.
        prefix_len: Shared prefix length in synthetic dataset.
        iterations: Trials per data point.

    Returns:
        Structured benchmark metrics dictionary.
    """
    if dataset_sizes is None:
        dataset_sizes = [20, 100, 500, 2000]

    records: List[Dict[str, Any]] = []
    shared = "a" * prefix_len

    for count in dataset_sizes:
        # Synthetic strings with shared prefix and varying suffix
        words = [f"{shared}suffix_{i % 50}_{'x' * (i % 10)}" for i in range(count)]
        row: Dict[str, Any] = {"count": count}

        algos = [
            ("horizontal", lcp_horizontal_scan),
            ("vertical", lcp_vertical_scan),
            ("dnc", lcp_divide_and_conquer),
            ("binary_search", lcp_binary_search),
            ("sort_endpoints", lcp_sort_endpoints),
            ("trie", lcp_trie),
        ]

        for key, fn in algos:
            times: List[float] = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                fn(words)
                times.append(time.perf_counter() - t0)
            row[key] = min(times)

        records.append(row)

    return {"records": records, "prefix_len": prefix_len, "iterations": iterations}


def format_benchmark_table(benchmark_data: Dict[str, Any]) -> str:
    """Formats the LCP benchmark output into an ASCII table."""
    lines: List[str] = []
    lines.append("Longest Common Prefix Algorithms Performance Benchmark")
    lines.append("=" * 94)
    header = (
        f"{'Strings':>8} | {'Horiz':>11} | {'Vertical':>11} | {'Div & Conq':>12} | "
        f"{'BinSearch':>11} | {'SortEnds':>11} | {'Trie':>11}"
    )
    lines.append(header)
    lines.append("-" * 94)

    def _fmt(val: float) -> str:
        us = val * 1_000_000.0
        if us < 1000.0:
            return f"{us:.2f} µs"
        return f"{us / 1000.0:.2f} ms"

    for r in benchmark_data["records"]:
        line = (
            f"{r['count']:>8} | "
            f"{_fmt(r['horizontal']):>11} | "
            f"{_fmt(r['vertical']):>11} | "
            f"{_fmt(r['dnc']):>12} | "
            f"{_fmt(r['binary_search']):>11} | "
            f"{_fmt(r['sort_endpoints']):>11} | "
            f"{_fmt(r['trie']):>11}"
        )
        lines.append(line)

    lines.append("=" * 94)
    return "\n".join(lines)



# ─── 4. Comprehensive Unit Test Suite ────────────────────────────────────────


class TestLongestCommonPrefix(unittest.TestCase):
    """Exhaustive unit test suite verifying all 6 LCP engines and extensions."""

    def test_consistency_across_all_engines(self) -> None:
        """Verifies all LCP implementations return identical results across test cases."""
        cases = [
            (["flower", "flow", "flight"], "fl"),
            (["dog", "racecar", "car"], ""),
            (["interspecies", "interstellar", "interstate"], "inters"),
            (["a"], "a"),
            (["ab", "a"], "a"),
            (["", "b"], ""),
            (["same", "same", "same"], "same"),
            ([], ""),
        ]
        sol = Solution()
        engines = [
            lcp_horizontal_scan,
            lcp_vertical_scan,
            lcp_divide_and_conquer,
            lcp_binary_search,
            lcp_sort_endpoints,
            lcp_trie,
            sol.longestCommonPrefix,
        ]
        for strs, expected in cases:
            for engine in engines:
                with self.subTest(strs=strs, engine=engine.__name__):
                    self.assertEqual(engine(strs), expected)

    def test_longest_common_suffix(self) -> None:
        """Tests longest common suffix extraction."""
        self.assertEqual(longest_common_suffix(["running", "jogging", "walking"]), "ing")
        self.assertEqual(longest_common_suffix(["cat", "dog"]), "")
        self.assertEqual(longest_common_suffix([]), "")

    def test_lcp_k_strings(self) -> None:
        """Tests k-string shared prefix discovery."""
        words = ["apple", "app", "apricot", "banana", "band"]
        self.assertEqual(longest_common_prefix_k_strings(words, 3), "ap")
        self.assertIn(longest_common_prefix_k_strings(words, 2), ["app", "ban"])
        self.assertEqual(longest_common_prefix_k_strings(words, 6), "")
        with self.assertRaises(ValueError):
            longest_common_prefix_k_strings(words, 0)

    def test_metrics_structure(self) -> None:
        """Verifies metrics dictionary accuracy."""
        res, m = lcp_with_metrics(["flower", "flow", "flight"])
        self.assertEqual(res, "fl")
        self.assertEqual(m["lcp_length"], 2)
        self.assertEqual(m["num_strings"], 3)
        self.assertGreater(m["comparisons"], 0)

    def test_type_validation(self) -> None:
        """Ensures non-list or non-string elements raise TypeError."""
        with self.assertRaises(TypeError):
            lcp_vertical_scan("not a list")  # type: ignore
        with self.assertRaises(TypeError):
            lcp_vertical_scan(["ok", 123])  # type: ignore



# ─── 5. Interactive CLI Demonstration ────────────────────────────────────────


def main() -> None:
    """Demonstrates LCP algorithms, extensions, visualizer, and benchmarks."""
    print("=" * 80)
    print("              DAY 94: LONGEST COMMON PREFIX (LEETCODE 14)               ")
    print("=" * 80)

    words = ["flower", "flow", "flight"]
    print(f"\n[1] Algorithm Consistency for {words}:")
    print(f"    - Horizontal Scan     : '{lcp_horizontal_scan(words)}'")
    print(f"    - Vertical Scan       : '{lcp_vertical_scan(words)}'")
    print(f"    - Divide & Conquer    : '{lcp_divide_and_conquer(words)}'")
    print(f"    - Binary Search       : '{lcp_binary_search(words)}'")
    print(f"    - Sort Endpoints      : '{lcp_sort_endpoints(words)}'")
    print(f"    - Prefix Tree (Trie)  : '{lcp_trie(words)}'")

    print("\n[2] Extensions (Suffix & k-String Prefix):")
    print(f"    - Longest Common Suffix(['running', 'jogging', 'walking']) -> '{longest_common_suffix(['running', 'jogging', 'walking'])}'")
    print(f"    - Prefix shared by >= 3 of ['apple', 'app', 'apricot', 'banana'] -> '{longest_common_prefix_k_strings(['apple', 'app', 'apricot', 'banana'], 3)}'")

    print("\n[3] Vertical Alignment & Divergence Visualizer:")
    print(visualize_lcp_vertical_scan(words))

    print("\n[4] Multi-Algorithm Performance Benchmark:")
    bench = benchmark_lcp_algorithms([20, 100, 500, 1500], prefix_len=20, iterations=5)
    print(format_benchmark_table(bench))

    print("\n" + "=" * 80)
    print("                      DEMONSTRATION COMPLETE                                   ")
    print("=" * 80)


if __name__ == "__main__":
    main()
