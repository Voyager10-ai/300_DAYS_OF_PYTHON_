# Day 32: Reverse Word in String
#
# Problem:
#   Write a Python program to reverse the words in a given string, sentence, or text block.
#   - Reverse Word Order: Reverses the sequence of words in a sentence.
#   - Reverse Each Word: Reverses the characters within each word while maintaining word order.

import re
import string
import sys
import io
from typing import List, Dict, Tuple, Optional, Any, Callable


def reverse_words(text: str) -> str:
    """
    Reverses the sequence of words in a given string.

    Args:
        text: Input sentence or paragraph.

    Returns:
        String with words in reverse order, joined by single spaces.

    Time Complexity: O(N) where N is string length.
    Space Complexity: O(N) for storing word tokens.

    Example:
        reverse_words("the sky is blue") -> "blue is sky"
        reverse_words("  hello world  ") -> "world hello"
    """
    if not text:
        return ""
    words = text.strip().split()
    return " ".join(reversed(words))


def reverse_each_word(text: str) -> str:
    """
    Reverses the characters of each word in a string while preserving original word placement.

    Args:
        text: Input string.

    Returns:
        String with every individual word character-reversed.

    Time Complexity: O(N) where N is string length.
    Space Complexity: O(N) for word token storage.

    Example:
        reverse_each_word("hello world") -> "olleh dlrow"
        reverse_each_word("Python Programming") -> "nohtyP gnimmargorP"
    """
    if not text:
        return ""
    words = text.split()
    reversed_words = [w[::-1] for w in words]
    return " ".join(reversed_words)


def reverse_words_custom_delimiter(text: str, delimiter: str = ",") -> str:
    """
    Reverses sequence of tokens delimited by a custom separator string.

    Args:
        text: Input string with custom delimiters.
        delimiter: Separator string between tokens.

    Returns:
        Delimited string with token order reversed.
    """
    if not text:
        return ""
    tokens = [t.strip() for t in text.split(delimiter)]
    return delimiter.join(reversed(tokens))


def reverse_words_preserve_whitespace(text: str) -> str:
    """
    Reverses word sequence while keeping original spacing/whitespace layout intact.

    Args:
        text: Input text containing spaces, tabs, or newlines.

    Returns:
        Reversed word order string matching identical whitespace slot locations.
    """
    if not text:
        return ""
    # Extract words and whitespace gaps using regex split
    tokens = re.split(r'(\s+)', text)
    words = [t for t in tokens if not t.isspace() and t != '']
    reversed_words = list(reversed(words))

    result = []
    word_idx = 0
    for t in tokens:
        if t == '':
            continue
        if t.isspace():
            result.append(t)
        else:
            result.append(reversed_words[word_idx])
            word_idx += 1
    return "".join(result)


def reverse_each_word_preserve_case(text: str) -> str:
    """
    Reverses characters of each word while maintaining capital letter positions.

    Args:
        text: Input string.

    Returns:
        Character-reversed string with original casing template preserved.

    Example:
        reverse_each_word_preserve_case("Hello World") -> "Olleh Dlrow"
    """
    def transform_word(w: str) -> str:
        casing_mask = [c.isupper() for c in w]
        raw_reversed = list(w[::-1].lower())
        for i, is_upper in enumerate(casing_mask):
            if is_upper:
                raw_reversed[i] = raw_reversed[i].upper()
        return "".join(raw_reversed)

    if not text:
        return ""
    words = text.split()
    return " ".join(transform_word(w) for w in words)


def reverse_words_preserve_punctuation(text: str) -> str:
    """
    Reverses word order while maintaining trailing/leading punctuation positions intact.

    Args:
        text: Sentence with punctuation marks.

    Returns:
        Sentence with words reversed but punctuation bound to structural slots.

    Example:
        reverse_words_preserve_punctuation("Hello, world!") -> "world, Hello!"
    """
    if not text:
        return ""

    # Tokenize words and non-word characters (punctuation/whitespace)
    tokens = re.findall(r'\w+|[^\w\s]+|\s+', text)

    words = [t for t in tokens if t.isalnum()]
    reversed_words = list(reversed(words))

    result = []
    word_idx = 0
    for t in tokens:
        if t.isalnum():
            result.append(reversed_words[word_idx])
            word_idx += 1
        else:
            result.append(t)

    return "".join(result)


def format_reversed_sentence(text: str, mode: str = "word_order") -> str:
    """
    High-level dispatcher for formatting reversed string outputs.

    Args:
        text: Input string.
        mode: Reversing mode ('word_order', 'char_in_word', 'both', 'preserve_punct').

    Returns:
        Formatted reversed string output based on selected mode.
    """
    if mode == "word_order":
        return reverse_words(text)
    elif mode == "char_in_word":
        return reverse_each_word(text)
    elif mode == "both":
        return reverse_words(reverse_each_word(text))
    elif mode == "preserve_punct":
        return reverse_words_preserve_punctuation(text)
    else:
        raise ValueError(f"Unknown reversing mode: {mode}")


def analyze_sentence_transformation(original_text: str) -> Dict[str, Any]:
    """
    Analyzes sentence properties before and after applying word reversing transformations.

    Args:
        original_text: Raw input string.

    Returns:
        Dictionary containing metric summaries and transformation outputs.
    """
    words = original_text.strip().split()
    word_count = len(words)
    char_count = len(original_text)
    palindromes = [w for w in words if w.lower() == w[::-1].lower()]

    rev_words = reverse_words(original_text)
    rev_each = reverse_each_word(original_text)

    return {
        "original_text": original_text,
        "word_count": word_count,
        "character_count": char_count,
        "palindrome_count": len(palindromes),
        "palindromes": palindromes,
        "reversed_words_order": rev_words,
        "reversed_each_word": rev_each,
        "is_sentence_palindrome": original_text.lower().replace(" ", "") == rev_words.lower().replace(" ", ""),
    }


def reverse_words_stream(stream_input: io.StringIO, mode: str = "word_order") -> str:
    """
    Processes line-by-line text stream and yields formatted reversed sentences.

    Args:
        stream_input: StringIO or file-like object.
        mode: Reversing mode to apply to each line.

    Returns:
        Multi-line string with transformed content.
    """
    output_lines = []
    for line in stream_input:
        cleaned_line = line.rstrip("\r\n")
        if cleaned_line:
            output_lines.append(format_reversed_sentence(cleaned_line, mode=mode))
        else:
            output_lines.append("")
    return "\n".join(output_lines)


def batch_reverse_lines(lines: List[str], mode: str = "word_order") -> List[str]:
    """
    Applies word reversing transformation to a list of sentence strings in bulk.

    Args:
        lines: List of sentences.
        mode: Reversing mode to apply.

    Returns:
        List of transformed sentence strings.
    """
    return [format_reversed_sentence(line, mode=mode) for line in lines]


import unittest


class TestReverseWordInString(unittest.TestCase):
    def test_reverse_words_basic(self):
        self.assertEqual(reverse_words("the sky is blue"), "blue is sky the")
        self.assertEqual(reverse_words("  hello world  "), "world hello")
        self.assertEqual(reverse_words("a"), "a")
        self.assertEqual(reverse_words(""), "")


    def test_reverse_each_word(self):
        self.assertEqual(reverse_each_word("hello world"), "olleh dlrow")
        self.assertEqual(reverse_each_word("Python"), "nohtyP")
        self.assertEqual(reverse_each_word(""), "")

    def test_custom_delimiter(self):
        self.assertEqual(reverse_words_custom_delimiter("apple,banana,cherry", ","), "cherry,banana,apple")
        self.assertEqual(reverse_words_custom_delimiter("a|b|c", "|"), "c|b|a")

    def test_preserve_whitespace(self):
        self.assertEqual(reverse_words_preserve_whitespace("one   two  three"), "three   two  one")

    def test_preserve_case(self):
        self.assertEqual(reverse_each_word_preserve_case("Hello World"), "Olleh Dlrow")

    def test_preserve_punctuation(self):
        self.assertEqual(reverse_words_preserve_punctuation("Hello, world!"), "world, Hello!")

    def test_format_reversed_sentence(self):
        self.assertEqual(format_reversed_sentence("hello world", mode="word_order"), "world hello")
        self.assertEqual(format_reversed_sentence("hello world", mode="char_in_word"), "olleh dlrow")
        self.assertEqual(format_reversed_sentence("hello world", mode="both"), "dlrow olleh")

    def test_analyze_sentence_transformation(self):
        res = analyze_sentence_transformation("radar cat level")
        self.assertEqual(res["word_count"], 3)
        self.assertEqual(res["palindrome_count"], 2)
        self.assertIn("radar", res["palindromes"])

    def test_batch_and_stream(self):
        lines = ["hello world", "python code"]
        res = batch_reverse_lines(lines)
        self.assertEqual(res, ["world hello", "code python"])

        stream_in = io.StringIO("alpha beta\ngamma delta")
        out = reverse_words_stream(stream_in)
        self.assertEqual(out, "beta alpha\ndelta gamma")


def main():
    print("=" * 60)
    print(" 🔄 Day 32: Reverse Word in String - Interactive CLI Demo")
    print("=" * 60)

    sample_sentence = "The quick brown fox jumps over the lazy dog."
    print(f"\nOriginal Sentence:\n  '{sample_sentence}'")

    print("\n1. Reversing Word Order:")
    print(f"  -> '{reverse_words(sample_sentence)}'")

    print("\n2. Reversing Characters in Each Word:")
    print(f"  -> '{reverse_each_word(sample_sentence)}'")

    print("\n3. Reversing Both Word Order and Characters:")
    print(f"  -> '{format_reversed_sentence(sample_sentence, mode='both')}'")

    print("\n4. Preserving Punctuation Slots:")
    print(f"  -> '{reverse_words_preserve_punctuation(sample_sentence)}'")

    print("\n5. Sentence Transformation Analysis:")
    metrics = analyze_sentence_transformation(sample_sentence)
    for key, value in metrics.items():
        print(f"  - {key}: {value}")

    print("\n" + "=" * 60)
    print(" Running Unit Tests...")
    print("=" * 60)
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    main()






