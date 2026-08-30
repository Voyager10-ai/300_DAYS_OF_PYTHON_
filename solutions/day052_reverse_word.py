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


# ─── 7. Reversal Statistics & Comparison Utilities ───────────────────────────


def analyze_word_reversal_stats(s: str) -> Dict[str, Any]:
    """
    Analyzes character, word, and palindrome metrics before and after word reversal.

    Args:
        s: Input text string.

    Returns:
        Dictionary of text analysis statistics.
    """
    words = s.split()
    total_words = len(words)
    palindromes = [w for w in words if w.lower() == w[::-1].lower() and len(w) > 1]

    return {
        "original_text": s,
        "character_count": len(s),
        "word_count": total_words,
        "palindrome_words_count": len(palindromes),
        "palindrome_words": palindromes,
        "reversed_words_order": reverse_words_order(s),
        "reversed_each_word": reverse_each_word(s),
        "reversed_entire_string": reverse_entire_string(s),
    }


def compare_reversal_methods(s: str) -> Dict[str, str]:
    """
    Executes all reversal algorithms on string s and returns a mapping of method_name -> result.

    Args:
        s: Input text string.

    Returns:
        Dictionary mapping method names to reversed outputs.
    """
    return {
        "Word Order Reversed": reverse_words_order(s),
        "Each Word Reversed": reverse_each_word(s),
        "Entire String Reversed": reverse_entire_string(s),
        "Preserve Punctuation": reverse_words_preserve_punctuation(s),
        "Preserve Casing": reverse_words_preserve_casing(s),
    }


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestReverseWordOperations(unittest.TestCase):
    def test_reverse_words_order(self):
        self.assertEqual(reverse_words_order("The quick brown fox"), "fox brown quick The")
        self.assertEqual(reverse_words_order("Python"), "Python")
        self.assertEqual(reverse_words_order(""), "")

    def test_reverse_each_word(self):
        self.assertEqual(reverse_each_word("hello world"), "olleh dlrow")
        self.assertEqual(reverse_each_word("a b c"), "a b c")

    def test_reverse_entire_string(self):
        self.assertEqual(reverse_entire_string("Hello World"), "dlroW olleH")

    def test_reverse_preserve_punctuation(self):
        self.assertEqual(reverse_words_preserve_punctuation("Hello, World!"), "olleH, dlroW!")
        self.assertEqual(reverse_words_preserve_punctuation("123 test!"), "123 tset!")

    def test_reverse_preserve_casing(self):
        self.assertEqual(reverse_words_preserve_casing("Python Code"), "Nohtyp Edoc")

    def test_reverse_by_delimiter_and_regex(self):
        self.assertEqual(reverse_by_delimiter("apple,banana,orange", ","), "orange,banana,apple")
        self.assertEqual(reverse_tokens_by_regex("abc 123 def"), "cba 321 fed")

    def test_reverse_matching_words(self):
        res = reverse_matching_words("cat elephant dog", min_length=5)
        self.assertEqual(res, "cat tnahpele dog")

    def test_batch_and_stats(self):
        batch = BatchWordReverser(["hello world", "foo bar"])
        res = batch.process_all("each_word")
        self.assertEqual(res, ["olleh dlrow", "oof rab"])

        stats = analyze_word_reversal_stats("level racecar hello")
        self.assertEqual(stats["word_count"], 3)
        self.assertEqual(stats["palindrome_words_count"], 2)


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" 🔄 Day 52: Reverse Word Utilities - Interactive Demo")
    print("=" * 60)

    sample_text = "The quick brown fox jumps over the lazy dog!"
    print(f"\nSample Input Text:\n  '{sample_text}'")

    print("\n1. Comparison of Reversal Algorithms:")
    comparison = compare_reversal_methods(sample_text)
    for name, result in comparison.items():
        print(f"   {name:<24} : '{result}'")

    print("\n2. CSV Delimiter Reversal:")
    csv_str = "Python,Java,C++,JavaScript,Rust"
    print(f"   Original CSV : '{csv_str}'")
    print(f"   Reversed CSV : '{reverse_by_delimiter(csv_str, ',')}'")

    print("\n3. Text Reversal Statistics:")
    stats = analyze_word_reversal_stats("level racecar madam python code")
    print(f"   Word Count       : {stats['word_count']}")
    print(f"   Palindrome Words : {stats['palindrome_words']}")

    # 4. Unit Test Suite Execution
    print("\n4. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReverseWordOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








