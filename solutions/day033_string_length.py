# Day 33: String Length
#
# Problem:
#   Write a Python program to calculate the length of a string using multiple algorithms and options.
#   - Iterative Character Count: Loop-based length counting without using len().
#   - Recursive Length: Divide-and-conquer recursive string length computation.
#   - Built-in Wrapper: Safe wrapper around standard len() with validation.

import sys
import io
import unicodedata
from typing import List, Dict, Tuple, Optional, Any, Callable


def calculate_length_iterative(s: str) -> int:
    """
    Calculates the length of a string by iterating through its characters without using len().

    Args:
        s: Input string.

    Returns:
        Integer count of characters in s.

    Time Complexity: O(N) where N is number of characters.
    Space Complexity: O(1).

    Example:
        calculate_length_iterative("Python") -> 6
        calculate_length_iterative("") -> 0
    """
    if not s:
        return 0
    count = 0
    for _ in s:
        count += 1
    return count


def calculate_length_recursive(s: str) -> int:
    """
    Recursively computes the length of a string.

    Args:
        s: Input string.

    Returns:
        Integer character count of s.

    Time Complexity: O(N) call depth.
    Space Complexity: O(N) call stack.

    Example:
        calculate_length_recursive("hello") -> 5
        calculate_length_recursive("") -> 0
    """
    if not s:
        return 0
    return 1 + calculate_length_recursive(s[1:])


def calculate_length_builtin(s: Optional[str]) -> int:
    """
    Safely retrieves the length of a string using Python's built-in len().

    Args:
        s: Input string or None.

    Returns:
        Length of s or 0 if s is None.
    """
    if s is None:
        return 0
    return len(s)


def calculate_byte_length(s: str, encoding: str = "utf-8") -> int:
    """
    Calculates the byte size of a string under a given text encoding format.

    Args:
        s: Input string.
        encoding: Character encoding format (e.g. 'utf-8', 'utf-16', 'ascii').

    Returns:
        Total number of encoded bytes.

    Example:
        calculate_byte_length("hello", "utf-8") -> 5
        calculate_byte_length("🚀", "utf-8") -> 4
    """
    if not s:
        return 0
    return len(s.encode(encoding, errors="replace"))


def calculate_unicode_code_points(s: str) -> int:
    """
    Calculates the total count of distinct Unicode code points in a string.

    Args:
        s: Input text string.

    Returns:
        Count of code points.
    """
    if not s:
        return 0
    return len([ord(c) for c in s])


def analyze_multi_byte_characters(s: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Analyzes character composition and identifies single-byte vs multi-byte characters.

    Args:
        s: Input string.
        encoding: Character encoding format.

    Returns:
        Dictionary containing character count, byte count, and multi-byte breakdown.
    """
    if not s:
        return {
            "char_count": 0,
            "byte_count": 0,
            "single_byte_chars": 0,
            "multi_byte_chars": 0,
            "expansion_ratio": 1.0,
        }

    char_count = len(s)
    byte_count = calculate_byte_length(s, encoding=encoding)

    single_byte = 0
    multi_byte = 0
    for char in s:
        b_len = len(char.encode(encoding, errors="replace"))
        if b_len == 1:
            single_byte += 1
        else:
            multi_byte += 1

    ratio = round(byte_count / char_count, 2) if char_count > 0 else 1.0

    return {
        "char_count": char_count,
        "byte_count": byte_count,
        "single_byte_chars": single_byte,
        "multi_byte_chars": multi_byte,
        "expansion_ratio": ratio,
    }


def calculate_trimmed_length(s: str) -> int:
    """
    Calculates string length after stripping boundary whitespace.

    Args:
        s: Input string.

    Returns:
        Length of trimmed string.
    """
    if not s:
        return 0
    return len(s.strip())


def calculate_non_whitespace_length(s: str) -> int:
    """
    Calculates string length ignoring all whitespace characters (spaces, tabs, newlines).

    Args:
        s: Input text string.

    Returns:
        Count of non-whitespace characters.
    """
    if not s:
        return 0
    return len([c for c in s if not c.isspace()])


def calculate_filtered_length(s: str, predicate: Callable[[str], bool]) -> int:
    """
    Calculates length of string matching a custom condition predicate.

    Args:
        s: Input text string.
        predicate: Function taking a char string and returning boolean.

    Returns:
        Count of matching characters.

    Example:
        calculate_filtered_length("Py3.9!", str.isalpha) -> 2 ("Py")
    """
    if not s:
        return 0
    return len([c for c in s if predicate(c)])


def get_word_lengths(text: str) -> List[Tuple[str, int]]:
    """
    Splits text into words and calculates the length of each individual word.

    Args:
        text: Input sentence or paragraph.

    Returns:
        List of tuples containing (word, length).

    Example:
        get_word_lengths("hello world") -> [("hello", 5), ("world", 5)]
    """
    if not text:
        return []
    words = text.strip().split()
    return [(w, len(w)) for w in words]


def analyze_length_statistics(text: str) -> Dict[str, Any]:
    """
    Computes statistical metrics regarding word lengths in a given text body.

    Args:
        text: Input sentence or document text.

    Returns:
        Dictionary containing length metrics (min, max, average, median, distribution).
    """
    word_pairs = get_word_lengths(text)
    if not word_pairs:
        return {
            "total_words": 0,
            "min_length": 0,
            "max_length": 0,
            "average_length": 0.0,
            "median_length": 0.0,
            "length_distribution": {},
        }

    lengths = [length for _, length in word_pairs]
    total_words = len(lengths)
    min_len = min(lengths)
    max_len = max(lengths)
    avg_len = round(sum(lengths) / total_words, 2)

    sorted_lengths = sorted(lengths)
    mid = total_words // 2
    if total_words % 2 == 0:
        median_len = round((sorted_lengths[mid - 1] + sorted_lengths[mid]) / 2.0, 2)
    else:
        median_len = float(sorted_lengths[mid])

    freq: Dict[int, int] = {}
    for l in lengths:
        freq[l] = freq.get(l, 0) + 1

    return {
        "total_words": total_words,
        "min_length": min_len,
        "max_length": max_len,
        "average_length": avg_len,
        "median_length": median_len,
        "length_distribution": dict(sorted(freq.items())),
    }


def render_length_histogram(text: str, max_bar_width: int = 20) -> str:
    """
    Renders a formatted ASCII visual histogram of word length frequencies in text.

    Args:
        text: Input text string.
        max_bar_width: Maximum character width of visual frequency bar.

    Returns:
        Formatted multi-line ASCII chart string.
    """
    stats = analyze_length_statistics(text)
    dist = stats["length_distribution"]
    if not dist:
        return "No words found to render histogram."

    max_freq = max(dist.values())
    lines = ["Word Length Frequency Histogram:"]
    lines.append("-" * 40)
    lines.append(f"{'Length':<8} | {'Count':<6} | {'Distribution':<20}")
    lines.append("-" * 40)

    for word_len, count in dist.items():
        bar_len = int((count / max_freq) * max_bar_width) if max_freq > 0 else 0
        bar = "█" * max(bar_len, 1)
        lines.append(f"{word_len:<8} | {count:<6} | {bar}")

    lines.append("-" * 40)
    return "\n".join(lines)


def calculate_stream_line_lengths(stream_input: io.StringIO) -> List[Tuple[int, int]]:
    """
    Reads line-by-line text stream and computes character length per line.

    Args:
        stream_input: StringIO or file-like object.

    Returns:
        List of tuples (line_number, character_length).
    """
    results = []
    for line_no, line in enumerate(stream_input, start=1):
        cleaned = line.rstrip("\r\n")
        results.append((line_no, len(cleaned)))
    return results


def batch_calculate_lengths(strings: List[str]) -> Dict[str, int]:
    """
    Evaluates a collection of strings and maps each string to its character length.

    Args:
        strings: List of input string items.

    Returns:
        Dictionary mapping string text to character length.
    """
    return {s: len(s) for s in strings}


import unittest


class TestStringLength(unittest.TestCase):
    def test_iterative_and_recursive_length(self):
        self.assertEqual(calculate_length_iterative("Python"), 6)
        self.assertEqual(calculate_length_iterative(""), 0)
        self.assertEqual(calculate_length_recursive("Programming"), 11)
        self.assertEqual(calculate_length_recursive(""), 0)

    def test_builtin_and_null(self):
        self.assertEqual(calculate_length_builtin("test"), 4)
        self.assertEqual(calculate_length_builtin(None), 0)

    def test_byte_length_and_unicode(self):
        self.assertEqual(calculate_byte_length("hello", "utf-8"), 5)
        self.assertEqual(calculate_byte_length("🚀", "utf-8"), 4)
        self.assertEqual(calculate_unicode_code_points("abc"), 3)

        analysis = analyze_multi_byte_characters("a🚀b")
        self.assertEqual(analysis["char_count"], 3)
        self.assertEqual(analysis["single_byte_chars"], 2)
        self.assertEqual(analysis["multi_byte_chars"], 1)

    def test_trimmed_and_non_whitespace(self):
        self.assertEqual(calculate_trimmed_length("   hello   "), 5)
        self.assertEqual(calculate_non_whitespace_length("a b c d"), 4)

    def test_filtered_length(self):
        self.assertEqual(calculate_filtered_length("Py3.9!", str.isalpha), 2)
        self.assertEqual(calculate_filtered_length("Py3.9!", str.isdigit), 2)

    def test_word_lengths(self):
        pairs = get_word_lengths("cat elephant dog")
        self.assertEqual(pairs, [("cat", 3), ("elephant", 8), ("dog", 3)])

    def test_length_statistics(self):
        stats = analyze_length_statistics("one two three")
        self.assertEqual(stats["total_words"], 3)
        self.assertEqual(stats["min_length"], 3)
        self.assertEqual(stats["max_length"], 5)

    def test_histogram_rendering(self):
        chart = render_length_histogram("a bb ccc")
        self.assertIn("Word Length Frequency Histogram:", chart)
        self.assertIn("3", chart)

    def test_stream_and_batch(self):
        stream_in = io.StringIO("first line\nsecond line here")
        res = calculate_stream_line_lengths(stream_in)
        self.assertEqual(res, [(1, 10), (2, 16)])

        batch_res = batch_calculate_lengths(["cat", "elephant"])
        self.assertEqual(batch_res, {"cat": 3, "elephant": 8})


def main():
    print("=" * 60)
    print(" 📏 Day 33: String Length Calculation - Interactive CLI Demo")
    print("=" * 60)

    sample_text = "The quick brown fox 🚀 jumps over 123 lazy dogs!"
    print(f"\nSample Input Text:\n  '{sample_text}'")

    print("\n1. Basic Length Algorithms:")
    print(f"  - Iterative Length:  {calculate_length_iterative(sample_text)}")
    print(f"  - Recursive Length:  {calculate_length_recursive(sample_text)}")
    print(f"  - Built-in len():    {calculate_length_builtin(sample_text)}")

    print("\n2. Encoding & Multi-Byte Metrics:")
    print(f"  - UTF-8 Byte Size:   {calculate_byte_length(sample_text, 'utf-8')} bytes")
    print(f"  - Code Points Count: {calculate_unicode_code_points(sample_text)}")
    mb_analysis = analyze_multi_byte_characters(sample_text)
    print(f"  - Single-byte chars: {mb_analysis['single_byte_chars']}")
    print(f"  - Multi-byte chars:  {mb_analysis['multi_byte_chars']}")
    print(f"  - Expansion Ratio:   {mb_analysis['expansion_ratio']}")

    print("\n3. Filtered Lengths:")
    print(f"  - Trimmed Length:    {calculate_trimmed_length(sample_text)}")
    print(f"  - Non-whitespace:    {calculate_non_whitespace_length(sample_text)}")
    print(f"  - Alphabetic Chars:  {calculate_filtered_length(sample_text, str.isalpha)}")
    print(f"  - Numeric Digits:    {calculate_filtered_length(sample_text, str.isdigit)}")

    print("\n4. Length Frequency Histogram:")
    print(render_length_histogram(sample_text))

    print("\n" + "=" * 60)
    print(" Running Unit Tests...")
    print("=" * 60)
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    main()






