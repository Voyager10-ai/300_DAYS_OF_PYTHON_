# Day 52: Reverse Word
#
# Problem:
#   Write a Python program / module to reverse words in a string.
#   Includes word-order reversal, character reversal per word, punctuation preservation,
#   casing preservation, custom delimiters, predicate filtering, batch processing, unit tests, and Java practice.

import re
import string
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union, Callable


# ─── 1. Core Word Reversing Algorithms ─────────────────────────────────────────


def reverse_words_order(s: str) -> str:
    """
    Reverses the order of words in a string, preserving single space separation.
    For example: 'The quick brown fox' -> 'fox brown quick The'.

    Args:
        s: Input text string.

    Returns:
        String with words in reverse order.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")
    words = s.split()
    return " ".join(reversed(words))


def reverse_each_word(s: str) -> str:
    """
    Reverses the characters of each individual word while maintaining word order.
    For example: 'hello world' -> 'olleh dlrow'.

    Args:
        s: Input text string.

    Returns:
        String with characters of each word reversed.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")
    words = s.split(" ")
    return " ".join(w[::-1] for w in words)


def reverse_entire_string(s: str) -> str:
    """
    Reverses the entire string completely from end to start.
    For example: 'Hello World' -> 'dlroW olleH'.

    Args:
        s: Input text string.

    Returns:
        Reversed string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")
    return s[::-1]


# ─── 2. Punctuation & Position Preserving Word Reverser ───────────────────────


def reverse_words_preserve_punctuation(s: str) -> str:
    """
    Reverses alphabetical characters within each word token while keeping punctuation,
    digits, and whitespace symbols in their exact original indices.
    For example: 'Hello, World!' -> 'Olleh, Dlrow!'.

    Args:
        s: Input text string.

    Returns:
        String with word characters reversed while punctuation remains in-place.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    def reverse_token(token: str) -> str:
        letters = [ch for ch in token if ch.isalpha()]
        letters.reverse()
        result = []
        letter_idx = 0
        for ch in token:
            if ch.isalpha():
                result.append(letters[letter_idx])
                letter_idx += 1
            else:
                result.append(ch)
        return "".join(result)

    # Tokenize by word bounds using regex while keeping spaces/punctuation intact
    tokens = re.split(r"(\s+)", s)
    return "".join(reverse_token(tok) for tok in tokens)


# ─── 3. Case-Preserving Word Reverser ──────────────────────────────────────────


def reverse_words_preserve_casing(s: str) -> str:
    """
    Reverses characters of each word while preserving the original capitalization pattern.
    For example: 'Python' -> 'Nohtyp' (index 0 was uppercase 'P', so new index 0 'N' becomes 'N').

    Args:
        s: Input text string.

    Returns:
        String with reversed words adhering to original casing map.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    def apply_casing(word: str) -> str:
        reversed_chars = list(word[::-1].lower())
        result = []
        for orig_ch, rev_ch in zip(word, reversed_chars):
            if orig_ch.isupper():
                result.append(rev_ch.upper())
            else:
                result.append(rev_ch.lower())
        return "".join(result)

    words = s.split(" ")
    return " ".join(apply_casing(w) for w in words)


# ─── 4. Custom Delimiter & Regex Token Reverser ───────────────────────────────


def reverse_by_delimiter(s: str, delimiter: str = ",") -> str:
    """
    Reverses the sequence of tokens separated by a specific delimiter string.
    For example: 'apple,banana,cherry' with delimiter=',' -> 'cherry,banana,apple'.

    Args:
        s: Input text string.
        delimiter: Delimiter token.

    Returns:
        Reversed delimited string.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")
    tokens = s.split(delimiter)
    return delimiter.join(reversed(tokens))


def reverse_tokens_by_regex(s: str, pattern: str = r"\b\w+\b") -> str:
    """
    Reverses all token matches found by a regex pattern while preserving surrounding non-matching text.

    Args:
        s: Input text string.
        pattern: Regex pattern for tokens to reverse.

    Returns:
        String with regex matched tokens reversed in-place.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    def replacer(match: re.Match) -> str:
        return match.group(0)[::-1]

    return re.sub(pattern, replacer, s)


# ─── 5. Predicate-Filtered Word Reverser ───────────────────────────────────────


def reverse_matching_words(
    s: str,
    condition: Optional[Callable[[str], bool]] = None,
    min_length: int = 0,
) -> str:
    """
    Reverses only words in a string that satisfy a given filter predicate function or minimum length.
    Words that do not match the predicate are left untouched.

    Args:
        s: Input text string.
        condition: Callable returning True for words that should be reversed.
        min_length: Minimum word character length threshold for reversal.

    Returns:
        String with conditionally reversed words.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    if condition is None:
        condition = lambda w: len(w) >= min_length

    words = s.split(" ")
    result = []
    for w in words:
        clean_w = w.strip(string.punctuation)
        if condition(clean_w):
            result.append(w[::-1])
        else:
            result.append(w)

    return " ".join(result)


# ─── 6. Batch Word Reverser & Sentence Collection Processor ───────────────────


class BatchWordReverser:
    """
    Manages a collection of sentences/paragraphs and batch processes them with selectable reversal strategies.
    """

    def __init__(self, initial_texts: Optional[List[str]] = None):
        self.texts: List[str] = list(initial_texts) if initial_texts else []

    def add_text(self, text: str) -> None:
        self.texts.append(str(text))

    def add_texts(self, texts: List[str]) -> None:
        self.texts.extend([str(t) for t in texts])

    def process_all(self, mode: str = "words_order") -> List[str]:
        """
        Processes all collected texts using specified reversal mode.

        Args:
            mode: Reversal strategy: 'words_order', 'each_word', 'entire_string',
                  'preserve_punctuation', or 'preserve_casing'.

        Returns:
            List of processed strings.
        """
        mode_map: Dict[str, Callable[[str], str]] = {
            "words_order": reverse_words_order,
            "each_word": reverse_each_word,
            "entire_string": reverse_entire_string,
            "preserve_punctuation": reverse_words_preserve_punctuation,
            "preserve_casing": reverse_words_preserve_casing,
        }

        func = mode_map.get(mode, reverse_words_order)
        return [func(txt) for txt in self.texts]





