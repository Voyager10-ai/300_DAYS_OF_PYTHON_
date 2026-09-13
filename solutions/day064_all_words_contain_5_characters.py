# Day 64: All Words Contain 5 Characters
#
# Problem:
#   Write a Python program / module to check if all words in a given string or list contain exactly 5 characters.
#   Includes robust word tokenization, punctuation removal, length filtering, comprehensive analysis metrics,
#   5-letter word validation, custom length range constraints, unit tests, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Tokenization & Length Verification ──────────────────────────────


def tokenize_words(text: str, remove_punct: bool = True) -> List[str]:
    """
    Extracts words from a string input.

    Args:
        text: Input string to tokenize.
        remove_punct: If True, strips punctuation around words.

    Returns:
        List of extracted word strings.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")

    if not text.strip():
        return []

    if remove_punct:
        # Match sequences of word characters (alphanumeric + underscore)
        words = re.findall(r"\b\w+\b", text)
    else:
        words = text.strip().split()

    return words


def all_words_have_length(
    text_or_list: Union[str, List[str]],
    target_length: int = 5,
    clean_punctuation: bool = True,
) -> bool:
    """
    Checks if all words in a string or list have exactly target_length characters.

    Args:
        text_or_list: A string sentence or list of word strings.
        target_length: Required length for all words (default: 5).
        clean_punctuation: If True, strips punctuation from string input words.

    Returns:
        True if input is non-empty and ALL words have length == target_length, else False.

    Raises:
        TypeError: If input is invalid type or target_length is not an int.
        ValueError: If target_length < 1.
    """
    if not isinstance(target_length, int) or isinstance(target_length, bool):
        raise TypeError(f"target_length must be an integer, got {type(target_length).__name__}")
    if target_length < 1:
        raise ValueError(f"target_length must be positive, got {target_length}")

    if isinstance(text_or_list, str):
        words = tokenize_words(text_or_list, remove_punct=clean_punctuation)
    elif isinstance(text_or_list, list):
        words = text_or_list
    else:
        raise TypeError(f"Expected str or list of str, got {type(text_or_list).__name__}")

    if not words:
        return False

    for word in words:
        if not isinstance(word, str):
            raise TypeError(f"All list elements must be strings, got {type(word).__name__}")
        w = word.strip()
        if clean_punctuation and isinstance(text_or_list, list):
            w = re.sub(r"^\W+|\W+$", "", w)
        if len(w) != target_length:
            return False

    return True


# ─── 2. Word Filtering by Length Utility ─────────────────────────────────────


def filter_words_by_length(
    text_or_list: Union[str, List[str]],
    target_length: int = 5,
    clean_punctuation: bool = True,
) -> List[str]:
    """
    Filters and returns all words from text or list that have exact target_length characters.

    Args:
        text_or_list: Input string sentence or list of word strings.
        target_length: Required character length (default: 5).
        clean_punctuation: If True, strips surrounding punctuation.

    Returns:
        List of matching words of length target_length.

    Raises:
        TypeError: If input types are invalid.
        ValueError: If target_length < 1.
    """
    if not isinstance(target_length, int) or isinstance(target_length, bool):
        raise TypeError(f"target_length must be an integer, got {type(target_length).__name__}")
    if target_length < 1:
        raise ValueError(f"target_length must be positive, got {target_length}")

    if isinstance(text_or_list, str):
        words = tokenize_words(text_or_list, remove_punct=clean_punctuation)
    elif isinstance(text_or_list, list):
        words = text_or_list
    else:
        raise TypeError(f"Expected str or list of str, got {type(text_or_list).__name__}")

    matching = []
    for word in words:
        if not isinstance(word, str):
            raise TypeError(f"All list elements must be strings, got {type(word).__name__}")
        w = word.strip()
        if clean_punctuation and isinstance(text_or_list, list):
            w = re.sub(r"^\W+|\W+$", "", w)
        if len(w) == target_length:
            matching.append(w)

    return matching


# ─── 3. Detailed Word Length Analysis Engine ─────────────────────────────────


def analyze_word_lengths(
    text_or_list: Union[str, List[str]],
    target_length: int = 5,
    clean_punctuation: bool = True,
) -> Dict[str, Any]:
    """
    Analyzes word lengths in an input text or list, returning comprehensive metrics.

    Args:
        text_or_list: Input text or list of word strings.
        target_length: Target word length to analyze against (default: 5).
        clean_punctuation: If True, strips surrounding punctuation.

    Returns:
        Dictionary containing:
          - total_words: Total word count.
          - target_length_count: Number of words with length == target_length.
          - target_length_words: List of words with length == target_length.
          - all_match_target: Boolean, True if all words match target_length.
          - length_distribution: Dict mapping word_length -> list of words.
          - non_matching_words: List of (word, length) tuples for non-matching words.
    """
    if isinstance(text_or_list, str):
        words = tokenize_words(text_or_list, remove_punct=clean_punctuation)
    elif isinstance(text_or_list, list):
        words = text_or_list
    else:
        raise TypeError(f"Expected str or list of str, got {type(text_or_list).__name__}")

    cleaned_words = []
    for word in words:
        if not isinstance(word, str):
            raise TypeError(f"All elements must be strings, got {type(word).__name__}")
        w = word.strip()
        if clean_punctuation and isinstance(text_or_list, list):
            w = re.sub(r"^\W+|\W+$", "", w)
        if w:
            cleaned_words.append(w)

    total_words = len(cleaned_words)
    target_words = [w for w in cleaned_words if len(w) == target_length]
    target_count = len(target_words)
    all_match = total_words > 0 and total_words == target_count

    length_dist: Dict[int, List[str]] = {}
    non_matching = []

    for w in cleaned_words:
        l = len(w)
        length_dist.setdefault(l, []).append(w)
        if l != target_length:
            non_matching.append((w, l))

    return {
        "total_words": total_words,
        "target_length_count": target_count,
        "target_length_words": target_words,
        "all_match_target": all_match,
        "length_distribution": length_dist,
        "non_matching_words": non_matching,
    }


# ─── 4. 5-Letter Word Validator with Mismatch Breakdown ───────────────────────


def validate_five_letter_words(
    text_or_list: Union[str, List[str]]
) -> Tuple[bool, List[str], List[str]]:
    """
    Validates whether input contains exclusively 5-letter words.

    Args:
        text_or_list: String sentence or list of word strings.

    Returns:
        Tuple of (all_valid, valid_5_letter_words, invalid_words).
    """
    analysis = analyze_word_lengths(text_or_list, target_length=5)
    valid_words = analysis["target_length_words"]
    invalid_words = [w for w, _ in analysis["non_matching_words"]]
    all_valid = analysis["all_match_target"]

    return all_valid, valid_words, invalid_words


# ─── 5. Custom Length Range Constraint Checker ───────────────────────────────


def check_words_length_constraint(
    text_or_list: Union[str, List[str]],
    min_length: int = 5,
    max_length: int = 5,
    clean_punctuation: bool = True,
) -> Dict[str, Any]:
    """
    Checks if all words satisfy a min_length to max_length constraint.

    Args:
        text_or_list: Input string sentence or list of word strings.
        min_length: Minimum allowed word length.
        max_length: Maximum allowed word length.
        clean_punctuation: If True, strips surrounding punctuation.

    Returns:
        Dict with 'is_valid', 'violating_words', 'valid_words', and 'compliance_rate'.

    Raises:
        ValueError: If min_length > max_length or min_length < 1.
    """
    if min_length < 1 or max_length < 1:
        raise ValueError("min_length and max_length must be positive integers.")
    if min_length > max_length:
        raise ValueError(f"min_length ({min_length}) cannot exceed max_length ({max_length}).")

    if isinstance(text_or_list, str):
        words = tokenize_words(text_or_list, remove_punct=clean_punctuation)
    elif isinstance(text_or_list, list):
        words = text_or_list
    else:
        raise TypeError(f"Expected str or list of str, got {type(text_or_list).__name__}")

    valid_words = []
    violating_words = []

    for word in words:
        if not isinstance(word, str):
            raise TypeError(f"All elements must be strings, got {type(word).__name__}")
        w = word.strip()
        if clean_punctuation and isinstance(text_or_list, list):
            w = re.sub(r"^\W+|\W+$", "", w)
        if w:
            if min_length <= len(w) <= max_length:
                valid_words.append(w)
            else:
                violating_words.append((w, len(w)))

    total = len(valid_words) + len(violating_words)
    compliance_rate = (len(valid_words) / total * 100.0) if total > 0 else 0.0

    return {
        "is_valid": total > 0 and len(violating_words) == 0,
        "valid_words": valid_words,
        "violating_words": violating_words,
        "compliance_rate": round(compliance_rate, 2),
    }


# ─── 6. String Transformation & Masking Helpers ───────────────────────────────


def mask_non_five_letter_words(text: str, mask_char: str = "*") -> str:
    """
    Replaces words in text that do not have 5 characters with mask_char repeated.

    Args:
        text: Input string paragraph.
        mask_char: Single character to replace non-5-letter word characters (default '*').

    Returns:
        Transformed string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    def replace_word(match: re.Match) -> str:
        word = match.group(0)
        if len(word) == 5:
            return word
        return mask_char * len(word)

    return re.sub(r"\b\w+\b", replace_word, text)


def highlight_five_letter_words(text: str, tag: str = "FIVE") -> str:
    """
    Wraps all 5-letter words in text with a tag like [FIVE:apple].

    Args:
        text: Input text.
        tag: Tag label to prefix word with.

    Returns:
        Tagged string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    def tag_word(match: re.Match) -> str:
        word = match.group(0)
        if len(word) == 5:
            return f"[{tag}:{word}]"
        return word

    return re.sub(r"\b\w+\b", tag_word, text)


# ─── 7. Unit Test Suite ───────────────────────────────────────────────────────


class TestFiveCharacterWords(unittest.TestCase):
    """Test suite for 5-character word detection and analysis functions."""

    def test_tokenize_words(self):
        text = "Hello, world! Python is cool."
        words = tokenize_words(text, remove_punct=True)
        self.assertEqual(words, ["Hello", "world", "Python", "is", "cool"])

        with self.assertRaises(TypeError):
            tokenize_words(12345)

    def test_all_words_have_length_true(self):
        # All 5-letter words
        words_list = ["apple", "grape", "peach", "lemon", "berry"]
        self.assertTrue(all_words_have_length(words_list, target_length=5))

        sentence = "apple grape peach lemon berry"
        self.assertTrue(all_words_have_length(sentence, target_length=5))

    def test_all_words_have_length_false(self):
        sentence = "The quick brown fox jumps"
        self.assertFalse(all_words_have_length(sentence, target_length=5))

        with self.assertRaises(ValueError):
            all_words_have_length("apple", target_length=0)

    def test_filter_words_by_length(self):
        text = "apple pie, fresh grape and lemon juice!"
        fives = filter_words_by_length(text, target_length=5)
        self.assertEqual(fives, ["apple", "fresh", "grape", "lemon", "juice"])

    def test_analyze_word_lengths(self):
        words = ["apple", "banana", "peach", "pear"]
        analysis = analyze_word_lengths(words, target_length=5)

        self.assertEqual(analysis["total_words"], 4)
        self.assertEqual(analysis["target_length_count"], 2)
        self.assertEqual(analysis["target_length_words"], ["apple", "peach"])
        self.assertFalse(analysis["all_match_target"])
        self.assertIn(6, analysis["length_distribution"])

    def test_validate_five_letter_words(self):
        valid_sentence = "train plane truck"
        all_val, valid, invalid = validate_five_letter_words(valid_sentence)
        self.assertTrue(all_val)
        self.assertEqual(valid, ["train", "plane", "truck"])
        self.assertEqual(invalid, [])

        mixed = "car train bicycle truck"
        all_val, valid, invalid = validate_five_letter_words(mixed)
        self.assertFalse(all_val)
        self.assertEqual(valid, ["train", "truck"])
        self.assertEqual(invalid, ["car", "bicycle"])

    def test_check_words_length_constraint(self):
        words = ["apple", "peach", "grape"]
        res = check_words_length_constraint(words, min_length=5, max_length=5)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["compliance_rate"], 100.0)

        with self.assertRaises(ValueError):
            check_words_length_constraint(words, min_length=6, max_length=5)

    def test_mask_and_highlight(self):
        text = "an apple a day keeps doctors away"
        masked = mask_non_five_letter_words(text, mask_char="*")
        self.assertIn("apple", masked)
        self.assertIn("**", masked)

        tagged = highlight_five_letter_words(text)
        self.assertIn("[FIVE:apple]", tagged)


# ─── 8. Interactive CLI Demonstration ─────────────────────────────────────────


def main() -> None:
    """Demonstrates all Day 64 5-character word detection utilities."""
    print("=" * 65)
    print(" DAY 64: ALL WORDS CONTAIN 5 CHARACTERS DEMONSTRATION")
    print("=" * 65)

    sample1 = ["apple", "grape", "peach", "lemon", "berry"]
    sample2 = "The quick brown fox jumps over the lazy dog"
    sample3 = "train plane truck clock chair"

    print("\n1. All Words Have 5 Characters Check:")
    print(f"   Sample 1 (List): {sample1}")
    print(f"   -> Result: {all_words_have_length(sample1, 5)}")

    print(f"\n   Sample 2 (Sentence): '{sample2}'")
    print(f"   -> Result: {all_words_have_length(sample2, 5)}")

    print(f"\n   Sample 3 (Sentence): '{sample3}'")
    print(f"   -> Result: {all_words_have_length(sample3, 5)}")

    print("\n2. Filter 5-Letter Words:")
    print(f"   Input text: '{sample2}'")
    fives = filter_words_by_length(sample2, 5)
    print(f"   -> 5-letter words found: {fives}")

    print("\n3. Comprehensive Length Analysis:")
    analysis = analyze_word_lengths("An apple a day keeps the doctor away from house", target_length=5)
    print(f"   Total Words       : {analysis['total_words']}")
    print(f"   5-Letter Count    : {analysis['target_length_count']}")
    print(f"   5-Letter Words    : {analysis['target_length_words']}")
    print(f"   All Match 5       : {analysis['all_match_target']}")
    print(f"   Length Frequency  : {[(l, len(words)) for l, words in sorted(analysis['length_distribution'].items())]}")

    print("\n4. 5-Letter Word Validation:")
    all_val, val_w, inval_w = validate_five_letter_words(sample3)
    print(f"   Sample 3 -> Valid: {all_val}, 5-Letter Words: {val_w}, Invalid: {inval_w}")

    print("\n5. Custom Length Constraint Check (min=4, max=6):")
    constraint = check_words_length_constraint(sample2, min_length=4, max_length=6)
    print(f"   Is Valid (4-6 chars): {constraint['is_valid']}")
    print(f"   Compliance Rate     : {constraint['compliance_rate']}%")

    print("\n6. Masking & Tagging Transformations:")
    text_demo = "an apple a day keeps the doctor away from house"
    print(f"   Original Text: '{text_demo}'")
    print(f"   Masked Text  : '{mask_non_five_letter_words(text_demo)}'")
    print(f"   Tagged Text  : '{highlight_five_letter_words(text_demo)}'")

    print("\n" + "=" * 65)
    print(" Running Unit Test Suite...")
    print("=" * 65)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)


if __name__ == "__main__":
    main()
