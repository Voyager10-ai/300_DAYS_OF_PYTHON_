# Day 35: Word Count
#
# Problem:
#   Write a Python program to calculate word counts and word frequencies from a text string or stream.
#   - Basic Word Counting: Space-delimited token counting.
#   - Frequency Analysis: Frequency map creation using collections.Counter and dicts.

import sys
import re
import unittest
from collections import Counter
from typing import List, Set, Dict, Tuple, Optional, Iterable, Iterator, Any


def count_words_basic(text: str) -> int:
    """
    Calculates total word count based on whitespace separation.

    Args:
        text: Input string.

    Returns:
        Integer count of words.

    Time Complexity: O(N) where N is number of characters.
    Space Complexity: O(W) where W is number of words.

    Example:
        count_words_basic("Hello world! Python is great.") -> 5
        count_words_basic("") -> 0
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


def get_word_frequencies(text: str, case_sensitive: bool = False) -> Dict[str, int]:
    """
    Generates a frequency map of words in the given text.

    Args:
        text: Input text string.
        case_sensitive: Whether to maintain word casing when counting frequencies.

    Returns:
        Dictionary mapping each word to its occurrence count.

    Example:
        get_word_frequencies("apple Banana apple") -> {"apple": 2, "banana": 1}
    """
    if not text or not text.strip():
        return {}

    words = text.split()
    processed_words = words if case_sensitive else [w.lower() for w in words]
    return dict(Counter(processed_words))


def count_words_regex(text: str, strip_punctuation: bool = True) -> int:
    """
    Counts words using regex pattern matching, ignoring punctuation marks and special symbols.

    Args:
        text: Input string.
        strip_punctuation: If True, uses word boundaries \\b\\w+\\b to isolate alphanumeric tokens.

    Returns:
        Number of valid word tokens.

    Example:
        count_words_regex("Hello, world! 123... test-case") -> 4
    """
    if not text or not text.strip():
        return 0

    if strip_punctuation:
        tokens = re.findall(r'\b\w+\b', text)
    else:
        tokens = text.split()

    return len(tokens)


def count_words_case_insensitive(text: str) -> Dict[str, int]:
    """
    Counts word occurrences case-insensitively after stripping punctuation.

    Args:
        text: Input string.

    Returns:
        Dictionary of lowercased word frequencies.

    Example:
        count_words_case_insensitive("Python python PYTHON!") -> {"python": 3}
    """
    if not text or not text.strip():
        return {}

    tokens = [w.lower() for w in re.findall(r'\b\w+\b', text)]
    return dict(Counter(tokens))


DEFAULT_STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "what",
    "which", "this", "that", "these", "those", "then", "just", "so", "than",
    "such", "both", "through", "about", "for", "is", "of", "to", "in", "it"
}


def count_words_filter_stopwords(
    text: str,
    custom_stopwords: Optional[Set[str]] = None,
    min_length: int = 1
) -> Dict[str, int]:
    """
    Counts word frequencies excluding common stop-words and short noise tokens.

    Args:
        text: Input text string.
        custom_stopwords: Set of stop-words to exclude (uses DEFAULT_STOPWORDS if None).
        min_length: Minimum word length threshold to count.

    Returns:
        Filtered dictionary of word frequencies.

    Example:
        count_words_filter_stopwords("The quick brown fox is fast") -> {"quick": 1, "brown": 1, "fox": 1, "fast": 1}
    """
    if not text or not text.strip():
        return {}

    stopwords = custom_stopwords if custom_stopwords is not None else DEFAULT_STOPWORDS
    raw_tokens = re.findall(r'\b\w+\b', text.lower())

    filtered_tokens = [
        word for word in raw_tokens
        if word not in stopwords and len(word) >= min_length
    ]
    return dict(Counter(filtered_tokens))


def get_word_length_distribution(text: str) -> Dict[int, int]:
    """
    Calculates the frequency distribution of word lengths (e.g. how many 3-letter, 4-letter words).

    Args:
        text: Input string.

    Returns:
        Dictionary mapping word_length -> count_of_words_with_that_length.

    Example:
        get_word_length_distribution("cat dog elephant") -> {3: 2, 8: 1}
    """
    if not text or not text.strip():
        return {}

    tokens = re.findall(r'\b\w+\b', text)
    lengths = [len(token) for token in tokens]
    return dict(Counter(lengths))


def get_ngram_frequencies(text: str, n: int = 2) -> Dict[Tuple[str, ...], int]:
    """
    Extracts N-gram word sequences (bigrams, trigrams, etc.) and computes their occurrence frequencies.

    Args:
        text: Input text string.
        n: Sequence length (2 for bigrams, 3 for trigrams, etc.).

    Returns:
        Dictionary mapping n-gram tuple of words -> count.

    Example:
        get_ngram_frequencies("deep learning artificial intelligence deep learning", n=2)
        -> {("deep", "learning"): 2, ("learning", "artificial"): 1, ("artificial", "intelligence"): 1, ("intelligence", "deep"): 1}
    """
    if not text or not text.strip() or n < 1:
        return {}

    tokens = [w.lower() for w in re.findall(r'\b\w+\b', text)]
    if len(tokens) < n:
        return {}

    ngrams = [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]
    return dict(Counter(ngrams))


def get_top_n_words(
    text: str,
    top_n: int = 5,
    exclude_stopwords: bool = True
) -> List[Tuple[str, int]]:
    """
    Retrieves the top N most frequent words from text.

    Args:
        text: Input text string.
        top_n: Number of top elements to return.
        exclude_stopwords: Whether to ignore stop-words.

    Returns:
        List of tuples (word, count) sorted by frequency in descending order.

    Example:
        get_top_n_words("python code python python data code", top_n=2)
        -> [("python", 3), ("code", 2)]
    """
    if exclude_stopwords:
        freq_map = count_words_filter_stopwords(text)
    else:
        freq_map = count_words_case_insensitive(text)

    counter = Counter(freq_map)
    return counter.most_common(top_n)


def count_words_stream(lines: Iterable[str], case_fold: bool = True) -> Counter:
    """
    Memory-efficient stream word counter that processes lines iteratively.

    Args:
        lines: Iterable yielding strings (e.g. open file handle).
        case_fold: Whether to standardize casing.

    Returns:
        collections.Counter containing accumulated word frequencies.
    """
    counter = Counter()
    for line in lines:
        tokens = re.findall(r'\b\w+\b', line)
        if case_fold:
            tokens = [t.lower() for t in tokens]
        counter.update(tokens)
    return counter


def count_words_chunked(text: str, chunk_size: int = 1000) -> Counter:
    """
    Splits text into chunks of specified character size and aggregates word counts.

    Args:
        text: Input string.
        chunk_size: Character limit per chunk.

    Returns:
        Combined Counter of all chunks.
    """
    if not text:
        return Counter()

    total_counter = Counter()
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        tokens = re.findall(r'\b\w+\b', chunk.lower())
        total_counter.update(tokens)

    return total_counter


class TestWordCount(unittest.TestCase):
    """Unit test suite for Day 35: Word Count algorithms."""

    def test_count_words_basic(self):
        self.assertEqual(count_words_basic("Hello world! Python is great."), 5)
        self.assertEqual(count_words_basic(""), 0)
        self.assertEqual(count_words_basic("   "), 0)

    def test_get_word_frequencies(self):
        self.assertEqual(get_word_frequencies("apple Banana apple"), {"apple": 2, "banana": 1})
        self.assertEqual(
            get_word_frequencies("apple Banana apple", case_sensitive=True),
            {"apple": 2, "Banana": 1}
        )

    def test_count_words_regex(self):
        self.assertEqual(count_words_regex("Hello, world! 123... test-case"), 5)
        self.assertEqual(count_words_regex(""), 0)

    def test_count_words_case_insensitive(self):
        self.assertEqual(count_words_case_insensitive("Python python PYTHON!"), {"python": 3})

    def test_count_words_filter_stopwords(self):
        freq = count_words_filter_stopwords("The quick brown fox is fast")
        self.assertIn("quick", freq)
        self.assertIn("brown", freq)
        self.assertNotIn("the", freq)
        self.assertNotIn("is", freq)

    def test_get_word_length_distribution(self):
        dist = get_word_length_distribution("cat dog elephant")
        self.assertEqual(dist[3], 2)
        self.assertEqual(dist[8], 1)

    def test_get_ngram_frequencies(self):
        ngrams = get_ngram_frequencies("deep learning deep learning artificial", n=2)
        self.assertEqual(ngrams[("deep", "learning")], 2)

    def test_get_top_n_words(self):
        top = get_top_n_words("python data python python data code", top_n=2, exclude_stopwords=False)
        self.assertEqual(top[0], ("python", 3))
        self.assertEqual(top[1], ("data", 2))

    def test_count_words_stream(self):
        lines = ["First line of text\n", "Second line of text\n"]
        counter = count_words_stream(lines)
        self.assertEqual(counter["text"], 2)
        self.assertEqual(counter["line"], 2)

    def test_count_words_chunked(self):
        text = "word " * 50
        counter = count_words_chunked(text, chunk_size=20)
        self.assertEqual(counter["word"], 50)


def main():
    print("=" * 60)
    print("🐍 300 Days of Python - Day 35: Word Count & Text Analytics")
    print("=" * 60)

    sample_text = (
        "Data science and machine learning with Python. "
        "Python makes data analysis fast, efficient, and readable! "
        "Machine learning models require clean data and robust Python code."
    )

    print("\n📝 Sample Input Text:")
    print(f"   \"{sample_text}\"")

    print("\n1️⃣ Basic Word Count (split):", count_words_basic(sample_text))
    print("2️⃣ Regex Alphanumeric Token Count:", count_words_regex(sample_text))

    print("\n3️⃣ Top 5 Most Frequent Words (excluding stop-words):")
    top_words = get_top_n_words(sample_text, top_n=5, exclude_stopwords=True)
    for word, count in top_words:
        print(f"   - {word:<15}: {count}")

    print("\n4️⃣ Bigram (2-gram) Frequencies:")
    bigrams = get_ngram_frequencies(sample_text, n=2)
    for ngram, count in list(bigrams.items())[:5]:
        print(f"   - {' '.join(ngram):<25}: {count}")

    print("\n5️⃣ Word Length Distribution:")
    length_dist = get_word_length_distribution(sample_text)
    for length in sorted(length_dist.keys()):
        print(f"   - {length}-letter words: {length_dist[length]}")

    print("\n🧪 Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWordCount)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("✅ All Day 35 unit tests passed successfully!")
    else:
        print("❌ Some unit tests failed.")


if __name__ == "__main__":
    main()






