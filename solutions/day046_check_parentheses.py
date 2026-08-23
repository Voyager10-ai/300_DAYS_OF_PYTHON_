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


# ─── 2. Detailed Syntax Error Diagnostic Reporter ──────────────────────────────


@dataclass
class ParenthesesDiagnosticResult:
    """Detailed result structure for bracket validation diagnostic reporting."""

    is_valid: bool
    error_type: Optional[str] = None  # 'UNMATCHED_CLOSING', 'UNCLOSED_OPENING', 'MISMATCHED_BRACKET'
    error_position: Optional[int] = None
    found_char: Optional[str] = None
    expected_char: Optional[str] = None
    message: str = "Parentheses are balanced."


def validate_parentheses_with_diagnostics(s: str) -> ParenthesesDiagnosticResult:
    """
    Validates parentheses in a string and returns detailed diagnostic info on syntax errors.

    Args:
        s: Input string.

    Returns:
        ParenthesesDiagnosticResult containing error position, expected vs found tokens.
    """
    stack: List[Tuple[str, int]] = []  # Stores (bracket_char, index)

    for idx, char in enumerate(s):
        if char in OPENING_BRACKETS:
            stack.append((char, idx))
        elif char in CLOSING_BRACKETS:
            if not stack:
                matching_open = DEFAULT_BRACKET_PAIRS[char]
                return ParenthesesDiagnosticResult(
                    is_valid=False,
                    error_type="UNMATCHED_CLOSING",
                    error_position=idx,
                    found_char=char,
                    expected_char=matching_open,
                    message=f"Unmatched closing bracket '{char}' at index {idx} with no prior open bracket.",
                )
            top_open, top_idx = stack.pop()
            expected_close = {v: k for k, v in DEFAULT_BRACKET_PAIRS.items()}[top_open]
            if top_open != DEFAULT_BRACKET_PAIRS[char]:
                return ParenthesesDiagnosticResult(
                    is_valid=False,
                    error_type="MISMATCHED_BRACKET",
                    error_position=idx,
                    found_char=char,
                    expected_char=expected_close,
                    message=(
                        f"Mismatched bracket '{char}' at index {idx}; expected '{expected_close}' "
                        f"to match '{top_open}' opened at index {top_idx}."
                    ),
                )

    if stack:
        unclosed_char, unclosed_idx = stack[-1]
        expected_close = {v: k for k, v in DEFAULT_BRACKET_PAIRS.items()}[unclosed_char]
        return ParenthesesDiagnosticResult(
            is_valid=False,
            error_type="UNCLOSED_OPENING",
            error_position=unclosed_idx,
            found_char=unclosed_char,
            expected_char=expected_close,
            message=f"Unclosed opening bracket '{unclosed_char}' at index {unclosed_idx}; expected '{expected_close}'.",
        )

    return ParenthesesDiagnosticResult(is_valid=True)


# ─── 3. Custom Bracket Pair Mappings & Configuration ──────────────────────────


def build_bracket_mapping(pairs: List[Tuple[str, str]]) -> Dict[str, str]:
    """
    Builds a closing-to-opening bracket dictionary from a list of (open, close) tuple pairs.

    Args:
        pairs: List of tuples, e.g. [("(", ")"), ("<", ">"), ("«", "»")].

    Returns:
        Dictionary mapping closing char -> opening char.
    """
    return {close_char: open_char for open_char, close_char in pairs}


def is_valid_parentheses_custom(
    s: str,
    pairs: Optional[List[Tuple[str, str]]] = None,
    allow_same_delimiters: bool = False,
) -> bool:
    """
    Validates parentheses using custom user-defined bracket pairs.

    Args:
        s: Input string.
        pairs: List of (open, close) pairs. Defaults to standard (), {}, [].
        allow_same_delimiters: If True, supports identical open/close delimiters (e.g. '|', '"').

    Returns:
        True if string is balanced according to custom rules, False otherwise.
    """
    if pairs is None:
        close_to_open = DEFAULT_BRACKET_PAIRS
    else:
        close_to_open = build_bracket_mapping(pairs)

    open_chars = set(close_to_open.values())
    close_chars = set(close_to_open.keys())

    stack: List[str] = []
    for char in s:
        if allow_same_delimiters and char in open_chars and char in close_chars:
            # Handle identical open/close pair (like quote or pipe "|")
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)
        elif char in open_chars:
            stack.append(char)
        elif char in close_chars:
            if not stack or stack[-1] != close_to_open[char]:
                return False
            stack.pop()

    return len(stack) == 0


# ─── 4. Quote & Comment Aware Code Bracket Parser ─────────────────────────────


def strip_comments_and_strings(code: str) -> str:
    """
    Strips string literals ("...", '...') and Python comments (# ...) from code text,
    replacing their contents with spaces to avoid false-positive bracket mismatches.

    Args:
        code: Source code string.

    Returns:
        Code string with strings and comments neutralized.
    """
    result: List[str] = []
    in_single_quote = False
    in_double_quote = False
    in_comment = False
    escape = False

    for char in code:
        if in_comment:
            if char == "\n":
                in_comment = False
                result.append("\n")
            else:
                result.append(" ")
            continue

        if in_single_quote:
            if escape:
                escape = False
                result.append(" ")
            elif char == "\\":
                escape = True
                result.append(" ")
            elif char == "'":
                in_single_quote = False
                result.append(" ")
            else:
                result.append(" ")
            continue

        if in_double_quote:
            if escape:
                escape = False
                result.append(" ")
            elif char == "\\":
                escape = True
                result.append(" ")
            elif char == '"':
                in_double_quote = False
                result.append(" ")
            else:
                result.append(" ")
            continue

        if char == "#":
            in_comment = True
            result.append(" ")
        elif char == "'":
            in_single_quote = True
            result.append(" ")
        elif char == '"':
            in_double_quote = True
            result.append(" ")
        else:
            result.append(char)

    return "".join(result)


def validate_parentheses_in_code(code: str) -> ParenthesesDiagnosticResult:
    """
    Validates bracket balance in source code, ignoring brackets embedded in strings or comments.

    Args:
        code: Python source code or structured text.

    Returns:
        ParenthesesDiagnosticResult containing detailed status.
    """
    clean_code = strip_comments_and_strings(code)
    return validate_parentheses_with_diagnostics(clean_code)


# ─── 5. Bracket Nesting Depth Analyzer ─────────────────────────────────────────


def get_max_nesting_depth(s: str) -> int:
    """
    Calculates the maximum nesting depth of parentheses/brackets in a string.

    Args:
        s: Input string.

    Returns:
        Maximum integer depth >= 0, or -1 if the parentheses are unbalanced.
    """
    max_depth = 0
    current_depth = 0
    stack: List[str] = []

    for char in s:
        if char in OPENING_BRACKETS:
            stack.append(char)
            current_depth += 1
            if current_depth > max_depth:
                max_depth = current_depth
        elif char in CLOSING_BRACKETS:
            if not stack or stack[-1] != DEFAULT_BRACKET_PAIRS[char]:
                return -1
            stack.pop()
            current_depth -= 1

    return max_depth if len(stack) == 0 else -1


def get_bracket_depth_profile(s: str) -> Tuple[List[int], int]:
    """
    Generates a depth profile mapping each character position to its current nesting depth.

    Args:
        s: Input string.

    Returns:
        Tuple of (depths_list, max_depth).
    """
    depths: List[int] = []
    current_depth = 0
    max_depth = 0

    for char in s:
        if char in OPENING_BRACKETS:
            current_depth += 1
            if current_depth > max_depth:
                max_depth = current_depth
            depths.append(current_depth)
        elif char in CLOSING_BRACKETS:
            depths.append(current_depth)
            current_depth = max(0, current_depth - 1)
        else:
            depths.append(current_depth)

    return (depths, max_depth)




