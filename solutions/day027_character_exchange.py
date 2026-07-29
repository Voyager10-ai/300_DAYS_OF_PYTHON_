# Day 27: Character Exchange
#
# Problem:
#   Write a Python program to swap/exchange characters in a string.
#   - Core Feature: Exchange the first and last characters of a given string.
#   - Word-level Exchange: Exchange first and last characters of each word in a sentence.
#   - Index Swapping: Swap characters at arbitrary indices (i, j) with index validation.
#   - Vowel Exchange: Reverse or swap positions of vowels while preserving consonants.
#   - Pairwise & Rotation: Adjacent pair swapping and cyclic character rotations.
#   - Custom Mapping: Key-based character replacement using mapping rules.
#   - ASCII Visualizer: Rich diagram showing original vs modified string and index maps.
#   - Interactive CLI & Comprehensive Demo Test Suite.

import re
import sys
from typing import List, Tuple, Dict, Optional


def swap_first_last(s: str) -> str:
    """
    Exchanges the first and last characters of a string.
    If string length is <= 1, returns the original string.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      'python' -> 'nythop'
      'a'      -> 'a'
      ''       -> ''
    """
    if not s or len(s) <= 1:
        return s
    return s[-1] + s[1:-1] + s[0]


def swap_first_last_words(sentence: str) -> str:
    """
    Exchanges the first and last character of each individual word in a sentence.
    Preserves original word boundaries and whitespace.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      'hello world python' -> 'oellh dorlw nythop'
    """
    if not sentence:
        return sentence

    # Split sentence into words and whitespace tokens preserving exact formatting
    tokens = re.split(r'(\s+)', sentence)
    result = []
    for token in tokens:
        if token.isspace() or not token:
            result.append(token)
        else:
            result.append(swap_first_last(token))
    return "".join(result)


def swap_indices(s: str, i: int, j: int) -> str:
    """
    Exchanges characters at specified 0-based indices i and j in a string.
    Supports negative index lookup (e.g. -1 for last character).
    Raises IndexError if either index is out of bounds.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      swap_indices("code", 0, 2) -> "dレスレット" wait: c and d swapped -> "doc-..." -> 'd' at 0, 'o' at 1, 'c' at 2, 'e' at 3 -> "doce"
    """
    n = len(s)
    if n <= 1:
        return s
    
    # Normalize negative indices
    actual_i = i if i >= 0 else n + i
    actual_j = j if j >= 0 else n + j
    
    if not (0 <= actual_i < n and 0 <= actual_j < n):
        raise IndexError(f"Indices ({i}, {j}) out of range for string of length {n}.")
    
    if actual_i == actual_j:
        return s
    
    chars = list(s)
    chars[actual_i], chars[actual_j] = chars[actual_j], chars[actual_i]
    return "".join(chars)

