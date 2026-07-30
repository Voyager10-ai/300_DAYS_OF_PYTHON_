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
