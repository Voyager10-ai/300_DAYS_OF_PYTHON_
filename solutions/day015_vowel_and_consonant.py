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
