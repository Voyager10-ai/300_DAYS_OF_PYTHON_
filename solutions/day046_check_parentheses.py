# Day 46: Check Parentheses
#
# Problem:
#   Write a Python program to check if a string of parentheses/brackets is valid and balanced.
#   Includes support for standard brackets (), {}, [], detailed syntax error diagnostics,
#   custom delimiter pairs, quote/comment aware code parsing, nesting depth analyzer,
#   auto-repair utilities, file-based validation, unit tests, and Java practice.

import os
import sys
import re
import unittest
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Stack-Based Parentheses Validation ───────────────────────────────


DEFAULT_BRACKET_PAIRS: Dict[str, str] = {
    ")": "(",
    "}": "{",
    "]": "[",
}

OPENING_BRACKETS: Set[str] = set(DEFAULT_BRACKET_PAIRS.values())
CLOSING_BRACKETS: Set[str] = set(DEFAULT_BRACKET_PAIRS.keys())


def is_valid_parentheses(s: str) -> bool:
    """
    Checks if a string has valid and balanced parentheses/brackets.
    Supports (), {}, and []. Ignores non-bracket characters.

    Args:
        s: Input string.

    Returns:
        True if all brackets are properly opened and closed in correct order, False otherwise.
    """
    stack: List[str] = []
    for char in s:
        if char in OPENING_BRACKETS:
            stack.append(char)
        elif char in CLOSING_BRACKETS:
            if not stack or stack[-1] != DEFAULT_BRACKET_PAIRS[char]:
                return False
            stack.pop()
    return len(stack) == 0


def is_balanced_simple(s: str) -> bool:
    """
    Checks if a string of only round parentheses '(' and ')' is balanced.

    Args:
        s: Input string.

    Returns:
        True if balanced, False otherwise.
    """
    count = 0
    for char in s:
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
            if count < 0:
                return False
    return count == 0
