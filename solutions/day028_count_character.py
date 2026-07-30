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


def count_character_categories(s: str) -> Dict[str, int]:
    """
    Classifies characters into functional categories and returns count breakdown:
    - total_chars: Total length of string
    - alphabetic: Total letter characters
    - uppercase: Uppercase letter characters
    - lowercase: Lowercase letter characters
    - digits: Numeric digit characters (0-9)
    - vowels: Vowels (a, e, i, o, u case-insensitive)
    - consonants: Letters that are not vowels
    - whitespace: Space, tab, newline, return characters
    - punctuation: Standard punctuation characters (string.punctuation)
    - special: Characters that are non-alphanumeric and non-whitespace
    
    Time Complexity: O(n), Space Complexity: O(1).
    """
    vowels_set = set("aeiouAEIOU")
    stats = {
        "total_chars": len(s),
        "alphabetic": 0,
        "uppercase": 0,
        "lowercase": 0,
        "digits": 0,
        "vowels": 0,
        "consonants": 0,
        "whitespace": 0,
        "punctuation": 0,
        "special": 0,
    }
    
    for char in s:
        if char.isalpha():
            stats["alphabetic"] += 1
            if char.isupper():
                stats["uppercase"] += 1
            if char.islower():
                stats["lowercase"] += 1
            if char in vowels_set:
                stats["vowels"] += 1
            else:
                stats["consonants"] += 1
        elif char.isdigit():
            stats["digits"] += 1
            
        if char.isspace():
            stats["whitespace"] += 1
        if char in string.punctuation:
            stats["punctuation"] += 1
        if not char.isalnum() and not char.isspace():
            stats["special"] += 1
            
    return stats


def get_top_k_frequent(s: str, k: int = 3, ignore_spaces: bool = False) -> List[Tuple[str, int]]:
    """
    Returns the top K most frequently occurring characters sorted by count descending.
    Time Complexity: O(n + u log u), Space Complexity: O(u).
    
    Example:
      get_top_k_frequent("abracadabra", k=3) -> [('a', 5), ('b', 2), ('r', 2)]
    """
    freq = count_character_frequency(s, ignore_spaces=ignore_spaces)
    sorted_pairs = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    return sorted_pairs[:k]


def get_least_frequent(s: str, k: int = 3, ignore_spaces: bool = False) -> List[Tuple[str, int]]:
    """
    Returns the top K least frequently occurring characters sorted by count ascending.
    Time Complexity: O(n + u log u), Space Complexity: O(u).
    """
    freq = count_character_frequency(s, ignore_spaces=ignore_spaces)
    sorted_pairs = sorted(freq.items(), key=lambda item: (item[1], item[0]))
    return sorted_pairs[:k]


def find_first_non_repeating_char(s: str) -> Optional[str]:
    """
    Finds the first non-repeating (unique occurrence) character in a string.
    Returns None if all characters repeat or string is empty.
    Time Complexity: O(n), Space Complexity: O(u).
    
    Example:
      find_first_non_repeating_char("leetcode") -> "l"
      find_first_non_repeating_char("loveleetcode") -> "v"
    """
    counts = Counter(s)
    for char in s:
        if counts[char] == 1:
            return char
    return None


def count_unique_characters(s: str) -> int:
    """
    Returns total number of distinct/unique characters in the string.
    Time Complexity: O(n), Space Complexity: O(u).
    """
    return len(set(s))


def calculate_character_entropy(s: str) -> float:
    """
    Calculates the Shannon entropy (H in bits) of character distribution in a string.
    H = - sum(p(x) * log2(p(x)))
    Higher entropy indicates greater character diversity/randomness.
    Time Complexity: O(n), Space Complexity: O(u).
    """
    if not s:
        return 0.0
    
    n = len(s)
    freq = Counter(s)
    entropy = 0.0
    
    for count in freq.values():
        p = count / n
        entropy -= p * math.log2(p)
        
    return round(entropy, 4)


def calculate_char_distribution_percentage(s: str) -> Dict[str, float]:
    """
    Calculates the percentage contribution of each character in the string.
    Returns dictionary mapping char to float percentage rounded to 2 decimal places.
    Time Complexity: O(n), Space Complexity: O(u).
    """
    if not s:
        return {}
    n = len(s)
    freq = Counter(s)
    return {char: round((count / n) * 100, 2) for char, count in freq.items()}


def draw_frequency_histogram(s: str, max_bar_width: int = 30) -> None:
    """
    Renders an ASCII horizontal bar chart visualizing character frequencies.
    """
    freq = count_character_frequency(s, ignore_spaces=False)
    if not freq:
        print("\n   [Empty string - no character frequency to display]\n")
        return

    total = len(s)
    max_count = max(freq.values())

    print("\n   ┌" + "─" * 62 + "┐")
    print("   │" + "📊 CHARACTER FREQUENCY HISTOGRAM".center(62) + "│")
    print("   ├" + "─" * 62 + "┤")

    sorted_items = sorted(freq.items(), key=lambda item: (-item[1], item[0]))

    for char, count in sorted_items:
        display_char = f"'{char}'" if char != " " else "'SPACE'"
        bar_len = int((count / max_count) * max_bar_width) if max_count > 0 else 0
        bar = "█" * bar_len
        pct = (count / total) * 100
        line = f"{display_char:>8} │ {bar:<30} {count:2d} ({pct:5.1f}%)"
        print("   │ " + line.ljust(60) + "│")

    print("   └" + "─" * 62 + "┘\n")


def draw_category_summary_table(s: str) -> None:
    """
    Renders an ASCII summary table detailing character classification stats.
    """
    stats = count_character_categories(s)
    entropy = calculate_character_entropy(s)
    unique_count = count_unique_characters(s)
    first_non_rep = find_first_non_repeating_char(s) or "None"

    print("   ┌" + "─" * 62 + "┐")
    print("   │" + "📋 CHARACTER COMPOSITION SUMMARY".center(62) + "│")
    print("   ├" + "─" * 62 + "┤")
    print("   │ " + f"Total String Length    : {stats['total_chars']}".ljust(60) + "│")
    print("   │ " + f"Unique Characters      : {unique_count}".ljust(60) + "│")
    print("   │ " + f"First Non-Repeating    : '{first_non_rep}'".ljust(60) + "│")
    print("   │ " + f"Shannon Entropy (bits) : {entropy}".ljust(60) + "│")
    print("   ├" + "─" * 62 + "┤")
    print("   │ " + f"Alphabetic (Letters)   : {stats['alphabetic']}".ljust(60) + "│")
    print("   │   - Uppercase Letters : " + f"{stats['uppercase']}".ljust(37) + "│")
    print("   │   - Lowercase Letters : " + f"{stats['lowercase']}".ljust(37) + "│")
    print("   │   - Vowels            : " + f"{stats['vowels']}".ljust(37) + "│")
    print("   │   - Consonants        : " + f"{stats['consonants']}".ljust(37) + "│")

    print("   │ " + f"Digits (0-9)           : {stats['digits']}".ljust(60) + "│")
    print("   │ " + f"Whitespace             : {stats['whitespace']}".ljust(60) + "│")
    print("   │ " + f"Punctuation Marks      : {stats['punctuation']}".ljust(60) + "│")
    print("   │ " + f"Special / Non-Alphanum  : {stats['special']}".ljust(60) + "│")
    print("   └" + "─" * 62 + "┘\n")


def run_demo_suite() -> None:
    """
    Runs demonstration suite over sample inputs and validates assertions.
    """
    print("\n" + "=" * 66)
    print(" 🚀 DAY 28: COUNT CHARACTER DEMONSTRATION SUITE")
    print("=" * 66)

    sample_strings = [
        "google.com",
        "Hello World! 123",
        "leetcode",
        "abracadabra",
    ]

    for sample in sample_strings:
        print(f"\n📌 Analyzing String: '{sample}'")
        draw_frequency_histogram(sample)
        draw_category_summary_table(sample)

    # Unit assertions validation
    assert count_character_frequency("google.com") == {'g': 2, 'o': 3, 'l': 1, 'e': 1, '.': 1, 'c': 1, 'm': 1}
    assert count_specific_char("banana", "a") == 3
    assert count_specific_char("Banana", "b", case_sensitive=False) == 1
    assert get_top_k_frequent("abracadabra", k=1) == [('a', 5)]
    assert find_first_non_repeating_char("leetcode") == "l"
    assert find_first_non_repeating_char("loveleetcode") == "v"
    assert count_unique_characters("abc") == 3
    assert calculate_character_entropy("") == 0.0

    cats = count_character_categories("Hello 123!")
    assert cats["total_chars"] == 10
    assert cats["alphabetic"] == 5
    assert cats["digits"] == 3
    assert cats["whitespace"] == 1
    assert cats["punctuation"] == 1

    print("─" * 66)
    print(" ✅ All test assertions passed successfully!")
    print("─" * 66 + "\n")


def main() -> None:
    """
    Main execution entry point.
    """
    run_demo_suite()


if __name__ == "__main__":
    main()






