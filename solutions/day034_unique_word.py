# Day 34: Unique Word
#
# Problem:
#   Write a Python program to extract and analyze unique words from a string or text corpus.
#   - Core Set-Based Extraction: Fast unordered unique word retrieval using set().
#   - Order-Preserving Unique Words: Retain word appearance sequence using dict.fromkeys() or set tracking.
#   - Case-Insensitive Extraction: Standardize text casing to find distinct semantic words.

import sys
import re
import unittest
from typing import List, Set, Dict, Tuple, Optional, Iterable, Iterator, Any


def get_unique_words_set(text: str) -> Set[str]:
    """
    Extracts unique words from text using an unordered set.

    Args:
        text: Input string.

    Returns:
        Set of unique space-delimited words.

    Time Complexity: O(N) where N is number of characters in text.
    Space Complexity: O(U) where U is number of unique words.

    Example:
        get_unique_words_set("apple banana apple cherry") -> {"apple", "banana", "cherry"}
    """
    if not text:
        return set()
    return set(text.split())


def get_unique_words_ordered(text: str) -> List[str]:
    """
    Extracts unique words from text while preserving their initial order of appearance.

    Args:
        text: Input string.

    Returns:
        List of unique words in first-seen order.

    Time Complexity: O(N).
    Space Complexity: O(U).

    Example:
        get_unique_words_ordered("apple banana apple cherry banana") -> ["apple", "banana", "cherry"]
    """
    if not text:
        return []
    words = text.split()
    return list(dict.fromkeys(words))


def get_unique_words_case_insensitive(text: str, preserve_first_case: bool = False) -> List[str]:
    """
    Extracts unique words ignoring case sensitivity.

    Args:
        text: Input string.
        preserve_first_case: If True, keeps the case of the word's first occurrence;
                             if False, returns all words in lowercase.

    Returns:
        List of unique words with normalized case matching.

    Example:
        get_unique_words_case_insensitive("Python python PYTHON") -> ["python"]
        get_unique_words_case_insensitive("Python python PYTHON", preserve_first_case=True) -> ["Python"]
    """
    if not text:
        return []
    
    words = text.split()
    seen: Set[str] = set()
    result: List[str] = []

    for word in words:
        lowered = word.lower()
        if lowered not in seen:
            seen.add(lowered)
            result.append(word if preserve_first_case else lowered)

    return result


def get_strictly_unique_words(text: str, case_sensitive: bool = False) -> List[str]:
    """
    Finds words that occur EXACTLY ONCE in the given text (hax legomena / singletons).

    Args:
        text: Input text string.
        case_sensitive: Whether to consider case when counting word frequencies.

    Returns:
        List of words appearing with frequency equal to 1.

    Example:
        get_strictly_unique_words("apple banana apple cherry") -> ["banana", "cherry"]
    """
    if not text:
        return []
    
    words = text.split()
    counts: Dict[str, int] = {}

    for word in words:
        key = word if case_sensitive else word.lower()
        counts[key] = counts.get(key, 0) + 1

    return [w for w in words if counts[w if case_sensitive else w.lower()] == 1]


def get_unique_words_cleaned(
    text: str,
    strip_punctuation: bool = True,
    min_length: int = 1,
    case_fold: bool = True
) -> List[str]:
    """
    Extracts unique words after stripping punctuation and filtering by minimum word length.

    Args:
        text: Input text string.
        strip_punctuation: If True, strips surrounding and embedded punctuation marks.
        min_length: Minimum character length for a word to be included.
        case_fold: If True, converts words to lowercase before comparison.

    Returns:
        List of cleaned, unique words in first-appearance order.

    Example:
        get_unique_words_cleaned("Hello, world! Hello... Python 3.10", min_length=2)
        -> ["hello", "world", "python"]
    """
    if not text:
        return []

    raw_tokens = re.findall(r'\b\w+\b', text) if strip_punctuation else text.split()
    seen: Set[str] = set()
    cleaned_unique: List[str] = []

    for token in raw_tokens:
        processed = token.lower() if case_fold else token
        if len(processed) >= min_length and processed not in seen:
            seen.add(processed)
            cleaned_unique.append(processed)

    return cleaned_unique


def calculate_vocabulary_richness(text: str, case_fold: bool = True) -> Dict[str, Any]:
    """
    Calculates Type-Token Ratio (TTR) and word metrics for linguistic vocabulary richness.

    TTR = Number of Unique Words (Types) / Total Number of Words (Tokens)

    Args:
        text: Input text corpus.
        case_fold: Whether to standardize case when identifying types.

    Returns:
        Dictionary containing total_tokens, unique_types, ttr_ratio, and hapax_legomena.

    Example:
        calculate_vocabulary_richness("the quick brown fox jumps over the lazy dog")
        -> {'total_tokens': 9, 'unique_types': 8, 'ttr_ratio': 0.8889, ...}
    """
    if not text or not text.strip():
        return {
            "total_tokens": 0,
            "unique_types": 0,
            "ttr_ratio": 0.0,
            "hapax_legomena_count": 0,
            "hapax_legomena_ratio": 0.0
        }

    tokens = re.findall(r'\b\w+\b', text)
    if not tokens:
        return {
            "total_tokens": 0,
            "unique_types": 0,
            "ttr_ratio": 0.0,
            "hapax_legomena_count": 0,
            "hapax_legomena_ratio": 0.0
        }

    processed_tokens = [t.lower() for t in tokens] if case_fold else tokens
    total_tokens = len(processed_tokens)
    
    freq_map: Dict[str, int] = {}
    for token in processed_tokens:
        freq_map[token] = freq_map.get(token, 0) + 1

    unique_types = len(freq_map)
    hapax_count = sum(1 for count in freq_map.values() if count == 1)

    return {
        "total_tokens": total_tokens,
        "unique_types": unique_types,
        "ttr_ratio": round(unique_types / total_tokens, 4),
        "hapax_legomena_count": hapax_count,
        "hapax_legomena_ratio": round(hapax_count / unique_types, 4) if unique_types > 0 else 0.0
    }


def get_unique_words_from_stream(lines: Iterable[str], case_fold: bool = True) -> Iterator[str]:
    """
    Memory-efficient generator that yields unique words as they appear in a text stream or file line iterable.

    Args:
        lines: Iterable of text lines (e.g., file handle or list of strings).
        case_fold: If True, yields lowercase unique words.

    Yields:
        Unique words in order of appearance across the stream.
    """
    seen: Set[str] = set()
    for line in lines:
        tokens = re.findall(r'\b\w+\b', line)
        for token in tokens:
            processed = token.lower() if case_fold else token
            if processed not in seen:
                seen.add(processed)
                yield processed


class TestUniqueWord(unittest.TestCase):
    """Unit test suite for Day 34: Unique Word solutions."""

    def test_get_unique_words_set(self):
        self.assertEqual(get_unique_words_set("apple banana apple cherry"), {"apple", "banana", "cherry"})
        self.assertEqual(get_unique_words_set(""), set())

    def test_get_unique_words_ordered(self):
        self.assertEqual(
            get_unique_words_ordered("apple banana apple cherry banana"),
            ["apple", "banana", "cherry"]
        )
        self.assertEqual(get_unique_words_ordered(""), [])

    def test_get_unique_words_case_insensitive(self):
        self.assertEqual(
            get_unique_words_case_insensitive("Python python PYTHON"),
            ["python"]
        )
        self.assertEqual(
            get_unique_words_case_insensitive("Python python PYTHON", preserve_first_case=True),
            ["Python"]
        )

    def test_get_strictly_unique_words(self):
        self.assertEqual(
            get_strictly_unique_words("apple banana apple cherry banana date"),
            ["cherry", "date"]
        )
        self.assertEqual(get_strictly_unique_words(""), [])

    def test_get_unique_words_cleaned(self):
        result = get_unique_words_cleaned("Hello, world! Hello... Python 3.10", min_length=2)
        self.assertIn("hello", result)
        self.assertIn("world", result)
        self.assertIn("python", result)
        self.assertNotIn("3", result)

    def test_calculate_vocabulary_richness(self):
        metrics = calculate_vocabulary_richness("the quick brown fox jumps over the lazy dog")
        self.assertEqual(metrics["total_tokens"], 9)
        self.assertEqual(metrics["unique_types"], 8)
        self.assertAlmostEqual(metrics["ttr_ratio"], 0.8889, places=4)

    def test_get_unique_words_from_stream(self):
        stream_data = ["First line with words\n", "Second line with unique words\n"]
        unique_stream = list(get_unique_words_from_stream(stream_data))
        self.assertEqual(unique_stream, ["first", "line", "with", "words", "second", "unique"])


def main():
    print("=" * 60)
    print("🐍 300 Days of Python - Day 34: Unique Word Extraction")
    print("=" * 60)

    sample_text = (
        "Python is amazing, python is versatile! "
        "Learning Python daily builds consistency. "
        "Consistency leads to mastery in Python and programming."
    )

    print("\n📝 Sample Input Text:")
    print(f"   \"{sample_text}\"")

    print("\n1️⃣ Unordered Unique Words (set):")
    print("  ", get_unique_words_set(sample_text))

    print("\n2️⃣ Order-Preserving Unique Words (list):")
    print("  ", get_unique_words_ordered(sample_text))

    print("\n3️⃣ Case-Insensitive Unique Words:")
    print("  ", get_unique_words_case_insensitive(sample_text))

    print("\n4️⃣ Cleaned & Filtered Unique Words (min length = 4):")
    print("  ", get_unique_words_cleaned(sample_text, min_length=4))

    print("\n5️⃣ Strictly Unique Words (Frequency == 1):")
    print("  ", get_strictly_unique_words(sample_text))

    print("\n📊 Vocabulary Richness Metrics (TTR):")
    metrics = calculate_vocabulary_richness(sample_text)
    for k, v in metrics.items():
        print(f"   - {k}: {v}")

    print("\n🧪 Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUniqueWord)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("✅ All Day 34 unit tests passed successfully!")
    else:
        print("❌ Some unit tests failed.")


if __name__ == "__main__":
    main()



