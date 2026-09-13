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
