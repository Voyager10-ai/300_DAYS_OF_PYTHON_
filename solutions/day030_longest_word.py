# Day 30: Longest Word
#
# Problem:
#   Write a Python program to find the longest word in a string, sentence, or list of words.
#   - Core Longest Word Search: Extract the single longest word from input text.
#   - Punctuation Sanitization: Clean leading/trailing punctuation and symbols.

import string
from typing import Optional, List, Dict, Any, Callable, Tuple


def clean_word(word: str) -> str:
    """
    Strips leading and trailing punctuation characters from a word token.

    Args:
        word: Single word token string.

    Returns:
        Cleaned word string with punctuation removed from boundaries.

    Example:
        clean_word("hello,") -> "hello"
        clean_word("...world!") -> "world"
    """
    return word.strip(string.punctuation)


def find_longest_word(text: str, strip_punctuation: bool = True) -> str:
    """
    Finds the first longest word in a given text string.

    Args:
        text: Input string or sentence.
        strip_punctuation: Whether to remove surrounding punctuation.

    Returns:
        The longest word found, or an empty string if input contains no valid words.

    Time Complexity: O(N) where N is number of characters.
    Space Complexity: O(W) where W is number of words.

    Example:
        find_longest_word("The quick brown fox jumps over the lazy dog") -> "jumps"
        find_longest_word("Comprehensive Python programming guide!") -> "Comprehensive"
    """
    if not text or not text.strip():
        return ""

    tokens = text.split()
    if strip_punctuation:
        cleaned_words = [clean_word(t) for t in tokens]
        words = [w for w in cleaned_words if w]
    else:
        words = tokens

    if not words:
        return ""

    return max(words, key=len)


def find_all_longest_words(text: str, strip_punctuation: bool = True) -> List[str]:
    """
    Finds all words in text that share the maximum word length.

    Args:
        text: Input text string.
        strip_punctuation: Whether to strip surrounding punctuation.

    Returns:
        List of distinct longest words in order of appearance.

    Example:
        find_all_longest_words("cat dog elephant dinosaur") -> ["elephant", "dinosaur"]
    """
    if not text or not text.strip():
        return []

    tokens = text.split()
    if strip_punctuation:
        cleaned_words = [clean_word(t) for t in tokens]
        words = [w for w in cleaned_words if w]
    else:
        words = tokens

    if not words:
        return []

    max_len = max(len(w) for w in words)
    longest_words = []
    seen = set()

    for w in words:
        if len(w) == max_len and w not in seen:
            longest_words.append(w)
            seen.add(w)

    return longest_words


def longest_word_by_criteria(text: str, filter_func: Callable[[str], bool]) -> Optional[str]:
    """
    Finds the longest word in text that satisfies a custom filter predicate.

    Args:
        text: Input text string.
        filter_func: Callable returning True if a word token meets criteria.

    Returns:
        Longest word matching criteria or None if no match is found.

    Example:
        longest_word_by_criteria("apple banana blueberry", lambda w: w.startswith('b')) -> "blueberry"
    """
    if not text or not text.strip():
        return None

    words = [clean_word(w) for w in text.split()]
    matching_words = [w for w in words if w and filter_func(w)]

    if not matching_words:
        return None

    return max(matching_words, key=len)


def word_length_analysis(text: str) -> Dict[str, Any]:
    """
    Generates detailed statistical analysis and frequency breakdown of word lengths in text.

    Args:
        text: Input string.

    Returns:
        Dictionary containing total_words, longest_words, max_length, average_length, length_distribution.
    """
    words = [clean_word(w) for w in text.split()]
    words = [w for w in words if w]

    if not words:
        return {
            "total_words": 0,
            "longest_words": [],
            "max_length": 0,
            "average_length": 0.0,
            "length_distribution": {},
        }

    lengths = [len(w) for w in words]
    max_len = max(lengths)
    distribution: Dict[int, int] = {}
    for l in lengths:
        distribution[l] = distribution.get(l, 0) + 1

    longest_words = find_all_longest_words(text)

    return {
        "total_words": len(words),
        "longest_words": longest_words,
        "max_length": max_len,
        "average_length": round(sum(lengths) / len(words), 2),
        "length_distribution": dict(sorted(distribution.items())),
    }


def find_longest_word_in_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Reads a file line-by-line and extracts the longest words without loading the entire file into memory.

    Args:
        file_path: Absolute or relative file path.
        encoding: File character encoding format (default: 'utf-8').

    Returns:
        Dictionary containing total_lines, total_words, longest_words, max_length.
    """
    max_len = 0
    longest_words = []
    seen = set()
    total_lines = 0
    total_words = 0

    with open(file_path, "r", encoding=encoding) as f:
        for line in f:
            total_lines += 1
            words = [clean_word(w) for w in line.split()]
            words = [w for w in words if w]
            total_words += len(words)

            for w in words:
                w_len = len(w)
                if w_len > max_len:
                    max_len = w_len
                    longest_words = [w]
                    seen = {w}
                elif w_len == max_len and w not in seen:
                    longest_words.append(w)
                    seen.add(w)

    return {
        "total_lines": total_lines,
        "total_words": total_words,
        "longest_words": longest_words,
        "max_length": max_len,
    }


def find_top_n_longest_words(text: str, n: int = 5) -> List[Tuple[str, int]]:
    """
    Extracts the top N longest unique words from input text sorted descending by word length.

    Args:
        text: Input text string.
        n: Number of top longest words to return.

    Returns:
        List of tuples (word, length) sorted by length descending.

    Example:
        find_top_n_longest_words("apple banana strawberry blueberry kiwi", 3) ->
        [('strawberry', 10), ('blueberry', 9), ('banana', 6)]
    """
    if not text or not text.strip() or n <= 0:
        return []

    words = [clean_word(w) for w in text.split()]
    unique_words = list(set(w for w in words if w))

    # Sort descending by length then alphabetically
    sorted_words = sorted(unique_words, key=lambda w: (-len(w), w.lower()))
    return [(w, len(w)) for w in sorted_words[:n]]





