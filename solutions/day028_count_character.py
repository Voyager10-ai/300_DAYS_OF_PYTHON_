# Day 28: Count Character
#
# Problem:
#   Write a Python program to count character occurrences and analyze string character composition.
#   - Core Frequency Counting: Count occurrences of all characters in a given string.
#   - Target Character Search: Count occurrences of a specific character (case-sensitive/insensitive).
#   - Category Classification: Breakdown into vowels, consonants, digits, uppercase, lowercase, spaces, punctuation.
#   - Frequency Ranking: Find top K most frequent and least frequent characters.
#   - Unique & Non-Repeating Analysis: Identify first non-repeating character and total unique count.
#   - Information Metrics: Calculate character distribution percentages and Shannon entropy.
#   - ASCII Visualizer: Render horizontal frequency histograms and summary tables.
#   - Test Suite: Comprehensive unit tests and automated assertion checks.

import math
import string
from collections import Counter
from typing import Dict, List, Tuple, Optional, Any


def count_character_frequency(s: str, case_sensitive: bool = True, ignore_spaces: bool = False) -> Dict[str, int]:
    """
    Counts the frequency of each character in the given string.
    
    Args:
        s: Input string to analyze.
        case_sensitive: If False, converts characters to lowercase before counting.
        ignore_spaces: If True, excludes whitespace characters from count.
        
    Returns:
        Dictionary mapping characters to their integer occurrence counts.
        
    Time Complexity: O(n), Space Complexity: O(u) where u is unique characters.
    
    Example:
        count_character_frequency("google.com") -> {'g': 2, 'o': 3, 'l': 1, 'e': 1, '.': 1, 'c': 1, 'm': 1}
    """
    if not case_sensitive:
        s = s.lower()
    if ignore_spaces:
        s = "".join(s.split())
        
    freq: Dict[str, int] = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq


def count_specific_char(s: str, target: str, case_sensitive: bool = True) -> int:
    """
    Counts total occurrences of a specific target character or substring in a string.
    
    Args:
        s: Input string.
        target: Target character to search and count.
        case_sensitive: Whether match is case-sensitive.
        
    Returns:
        Integer count of occurrences.
        
    Time Complexity: O(n), Space Complexity: O(1) or O(n) depending on normalization.
    
    Example:
        count_specific_char("banana", "a") -> 3
        count_specific_char("Banana", "b", case_sensitive=False) -> 1
    """
    if not target:
        return 0
    if not case_sensitive:
        s = s.lower()
        target = target.lower()
    return s.count(target)

