# Day 15: Vowel and Consonant
#
# Problem:
#   Write a Python program that analyzes string input to count, analyze, and highlight
#   vowels and consonants.
#   - Count the total number of vowels and consonants in a text.
#   - Provide a percentage breakdown of vowels and consonants.
#   - Generate a character frequency distribution chart for vowels and consonants.
#   - Provide a visual highlighter in the console showing vowels and consonants.
#   - Offer options to strip vowels/consonants or replace them with custom symbols.
#   - Support analyzing either direct user input or text from a file.
#
# This exercise covers string manipulation, character iteration, dictionaries, math
# proportions, list comprehensions, and interactive terminal interface design.

import collections
import os

# ---------- Constants ----------
VOWELS = set("aeiouAEIOU")
CONSONANTS = set("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ")


# ---------- Core Analysis Logic ----------
def analyze_text(text):
    """
    Analyze the text and return statistics.
    Returns a dictionary of counts, frequencies, and ratios.
    """
    stats = {
        "vowel_count": 0,
        "consonant_count": 0,
        "digit_count": 0,
        "space_count": 0,
        "special_count": 0,
        "total_chars": len(text),
        "vowel_freq": collections.Counter(),
        "consonant_freq": collections.Counter()
    }
    
    for char in text:
        if char in VOWELS:
            stats["vowel_count"] += 1
            stats["vowel_freq"][char.lower()] += 1
        elif char in CONSONANTS:
            stats["consonant_count"] += 1
            stats["consonant_freq"][char.lower()] += 1
        elif char.isdigit():
            stats["digit_count"] += 1
        elif char.isspace():
            stats["space_count"] += 1
        else:
            stats["special_count"] += 1
            
    return stats


# ---------- Text Transformation ----------
def highlight_characters(text, highlight_mode):
    """
    Highlight characters based on mode.
    Modes:
      - 'vowels': Wraps vowels in square brackets like [a]
      - 'consonants': Wraps consonants in square brackets like [b]
      - 'color': Wraps vowels in cyan color and consonants in yellow color (ANSI codes)
    """
    result = []
    
    # ANSI escape sequences for coloring
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    
    for char in text:
        if highlight_mode == "vowels":
            if char in VOWELS:
                result.append(f"[{char}]")
            else:
                result.append(char)
        elif highlight_mode == "consonants":
            if char in CONSONANTS:
                result.append(f"[{char}]")
            else:
                result.append(char)
        elif highlight_mode == "color":
            if char in VOWELS:
                result.append(f"{CYAN}{char}{RESET}")
            elif char in CONSONANTS:
                result.append(f"{YELLOW}{char}{RESET}")
            else:
                result.append(char)
        else:
            result.append(char)
            
    return "".join(result)


def transform_text(text, op_type, replace_char="*"):
    """Transform text based on operation type."""
    if op_type == "strip_vowels":
        return "".join(c for c in text if c not in VOWELS)
    elif op_type == "strip_consonants":
        return "".join(c for c in text if c not in CONSONANTS)
    elif op_type == "replace_vowels":
        return "".join(replace_char if c in VOWELS else c for c in text)
    elif op_type == "replace_consonants":
        return "".join(replace_char if c in CONSONANTS else c for c in text)
    return text
