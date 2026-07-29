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
