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
      swap_indices("code", 0, 2) -> "doce"
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


def swap_vowels(s: str) -> str:
    """
    Reverses the positions of all vowels (a, e, i, o, u, A, E, I, O, U) in a string
    while keeping non-vowel characters in place. Two-pointer technique.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      'hello' -> 'holle'
      'leetcode' -> 'leotcede'
    """
    vowels = set("aeiouAEIOU")
    chars = list(s)
    left, right = 0, len(chars) - 1
    
    while left < right:
        while left < right and chars[left] not in vowels:
            left += 1
        while left < right and chars[right] not in vowels:
            right -= 1
            
        if left < right:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1
            
    return "".join(chars)


def swap_first_last_vowel(s: str) -> str:
    """
    Swaps only the very first vowel and the very last vowel in a string.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      'python coding' -> 'pythan codong'
    """
    vowels = set("aeiouAEIOU")
    vowel_indices = [idx for idx, ch in enumerate(s) if ch in vowels]
    
    if len(vowel_indices) < 2:
        return s
    
    return swap_indices(s, vowel_indices[0], vowel_indices[-1])


def swap_consonants(s: str) -> str:
    """
    Reverses the positions of all consonants in a string while keeping vowels and numbers in place.
    Time Complexity: O(n), Space Complexity: O(n).
    """
    vowels = set("aeiouAEIOU")
    chars = list(s)
    left, right = 0, len(chars) - 1
    
    def is_consonant(ch: str) -> bool:
        return ch.isalpha() and ch not in vowels
    
    while left < right:
        while left < right and not is_consonant(chars[left]):
            left += 1
        while left < right and not is_consonant(chars[right]):
            right -= 1
            
        if left < right:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1
            
    return "".join(chars)


def swap_pairwise(s: str) -> str:
    """
    Exchanges adjacent character pairs (index 0 with 1, 2 with 3, etc.).
    If string length is odd, the trailing character remains unchanged.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      'python' -> 'ypto nh' -> 'yptonh'
      'abc'    -> 'bac'
    """
    chars = list(s)
    for idx in range(0, len(chars) - 1, 2):
        chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
    return "".join(chars)


def rotate_characters(s: str, k: int) -> str:
    """
    Cyclically rotates string characters by k positions.
    Positive k rotates right (e.g. k=2 shifts last 2 chars to front).
    Negative k rotates left.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      rotate_characters("python", 2)  -> "onpyth"
      rotate_characters("python", -1) -> "ythonp"
    """
    if not s:
        return s
    n = len(s)
    effective_k = k % n
    if effective_k == 0:
        return s
    return s[-effective_k:] + s[:-effective_k]


def swap_custom_mapping(s: str, mapping: Dict[str, str]) -> str:
    """
    Exchanges characters in the string according to a custom lookup dictionary.
    Simultaneously substitutes mapped characters to avoid chain replacements.
    Time Complexity: O(n), Space Complexity: O(n).
    
    Example:
      swap_custom_mapping("cat", {'c': 'b', 't': 's'}) -> "bas"
    """
    return "".join(mapping.get(ch, ch) for ch in s)


def draw_exchange_visualization(original: str, modified: str, title: str = "CHARACTER EXCHANGE VISUALIZATION") -> None:
    """
    Renders an ASCII visualization chart showing original string, index layout,
    swap indicators, and the resulting modified string.
    """
    print("\n   ┌" + "─" * 62 + "┐")
    print("   │" + f"🔀 {title}".center(62) + "│")
    print("   ├" + "─" * 62 + "┤")
    
    n = max(len(original), len(modified))
    if n == 0:
        print("   │" + " (empty string) ".center(62) + "│")
        print("   └" + "─" * 62 + "┘\n")
        return

    # Index header
    indices_str = " ".join(f"{i:2d}" for i in range(len(original)))
    orig_chars_str = " ".join(f" '{ch}'" if len(ch) == 1 else f"'{ch}'" for ch in original)
    mod_chars_str = " ".join(f" '{ch}'" if len(ch) == 1 else f"'{ch}'" for ch in modified)
    
    print("   │ Index:    " + indices_str.ljust(50) + "│")
    print("   │ Original: " + orig_chars_str.ljust(50) + "│")
    
    # Highlight changed positions
    diff_markers = []
    for i in range(max(len(original), len(modified))):
        c1 = original[i] if i < len(original) else ""
        c2 = modified[i] if i < len(modified) else ""
        diff_markers.append(" ↕ " if c1 != c2 else " │ ")
    
    markers_str = "".join(diff_markers)
    print("   │ Change:   " + markers_str.ljust(50) + "│")
    print("   │ Result:   " + mod_chars_str.ljust(50) + "│")
    print("   └" + "─" * 62 + "┘\n")


def run_demo_suite() -> None:
    """
    Executes comprehensive test suites demonstrating all character exchange algorithms.
    """
    print("\n" + "=" * 66)
    print(" 🚀 DAY 27: CHARACTER EXCHANGE DEMONSTRATION SUITE")
    print("=" * 66)

    test_cases = [
        ("python", "First & Last Exchange"),
        ("a", "Single Char String"),
        ("hello world python", "Per-Word First & Last Exchange"),
        ("leetcode", "Vowel Position Reversal"),
        ("code", "Index Swap (0, 2)"),
        ("123456", "Pairwise Adjacent Swap"),
        ("python", "Cyclic Rotation Right (k=2)"),
    ]

    for item, label in test_cases:
        print(f"\n📌 Case: {label}")
        if label == "First & Last Exchange":
            res = swap_first_last(item)
        elif label == "Single Char String":
            res = swap_first_last(item)
        elif label == "Per-Word First & Last Exchange":
            res = swap_first_last_words(item)
        elif label == "Vowel Position Reversal":
            res = swap_vowels(item)
        elif label == "Index Swap (0, 2)":
            res = swap_indices(item, 0, 2)
        elif label == "Pairwise Adjacent Swap":
            res = swap_pairwise(item)
        elif label == "Cyclic Rotation Right (k=2)":
            res = rotate_characters(item, 2)
        else:
            res = item

        draw_exchange_visualization(item, res, title=f"{label.upper()}")
        print(f"   Input : '{item}'")
        print(f"   Output: '{res}'")

    # Automated assertions validation
    assert swap_first_last("python") == "nythop"
    assert swap_first_last("a") == "a"
    assert swap_first_last_words("hello world") == "oellh dorlw"
    assert swap_indices("code", 0, 2) == "doce"
    assert swap_vowels("hello") == "holle"
    assert swap_pairwise("abcd") == "badc"
    assert rotate_characters("python", 2) == "onpyth"
    
    print("\n" + "─" * 66)
    print(" ✅ All test assertions passed successfully!")
    print("─" * 66 + "\n")


def main() -> None:
    """
    Main entry point for Day 27 executable script.
    """
    run_demo_suite()


if __name__ == "__main__":
    main()





