# Day 69: Remove Parenthesis
#
# Problem:
#   Write a Python program / module to strip or extract parentheses and enclosed text from strings.
#   Includes core removal, multi-bracket support ((), [], {}, <>), nested stack-based parsers,
#   expression simplifiers, structure analysis metrics, collection batch cleaners,
#   redaction masking, unit test suite, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Parenthesis Removal & Content Stripping ─────────────────────────


def remove_parentheses(text: str, remove_contents: bool = True) -> str:
    """
    Removes parentheses '()' from a string, optionally stripping the enclosed contents.

    Args:
        text: Target text string.
        remove_contents: If True, removes text inside parentheses e.g. "Hello (world)" -> "Hello ".
                         If False, removes only the parenthesis characters '(' and ')'.

    Returns:
        Cleaned string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text:
        return ""

    if remove_contents:
        # Regex to strip non-nested parentheses and their contents, repeated for simple multi-pair
        result = text
        while re.search(r"\([^()]*\)", result):
            result = re.sub(r"\([^()]*\)", "", result)
        # Collapse multiple spaces leftover into single space if needed
        return re.sub(r" +", " ", result).strip()

    return text.replace("(", "").replace(")", "")


def has_parentheses(text: str) -> bool:
    """
    Checks if a string contains any parenthesis characters '(' or ')'.

    Args:
        text: Target text string.

    Returns:
        True if text contains '(' or ')', else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    return "(" in text or ")" in text


# ─── 2. Multi-Bracket Remover & Content Extractor ────────────────────────────

BRACKET_PAIRS = {
    "()": (r"\(", r"\)"),
    "[]": (r"\[", r"\]"),
    "{}": (r"\{", r"\}"),
    "<>": (r"<", r">"),
}


def remove_custom_brackets(
    text: str,
    brackets: Optional[List[str]] = None,
    remove_contents: bool = True,
) -> str:
    """
    Strips specified bracket types e.g. '()', '[]', '{}', '<>' and optionally their contents.

    Args:
        text: Input string.
        brackets: List of bracket pair strings e.g. ['()', '[]']. Defaults to all.
        remove_contents: If True, removes text enclosed inside brackets.

    Returns:
        Cleaned output string.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If invalid bracket type provided.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text:
        return ""

    target_brackets = brackets or ["()", "[]", "{}", "<>"]
    result = text

    for b in target_brackets:
        if b not in BRACKET_PAIRS:
            raise ValueError(f"Unsupported bracket pair '{b}'. Choose from '()', '[]', '{{}}', '<>'.")
        open_b, close_b = BRACKET_PAIRS[b]

        if remove_contents:
            pattern = f"{open_b}[^{open_b}{close_b}]*{close_b}"
            while re.search(pattern, result):
                result = re.sub(pattern, "", result)
        else:
            raw_open, raw_close = b[0], b[1]
            result = result.replace(raw_open, "").replace(raw_close, "")

    return re.sub(r" +", " ", result).strip()


def extract_parenthetical_contents(text: str) -> List[str]:
    """
    Extracts all substrings enclosed inside parentheses.

    Args:
        text: Source text string.

    Returns:
        List of extracted string contents.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if not text:
        return []

    return re.findall(r"\(([^()]*)\)", text)


# ─── 3. Nested Parenthesis Stack Parser & Balance Checker ────────────────────


def remove_nested_parentheses(text: str, max_depth: Optional[int] = None) -> str:
    """
    Parses and strips nested parentheses up to a specified depth using a character stack.

    Args:
        text: Source string containing nested parentheses e.g. "a (b (c) d) e".
        max_depth: Maximum nesting depth to remove (None to remove all nested levels).

    Returns:
        Stripped output string.

    Raises:
        TypeError: If text is not a string.
        ValueError: If max_depth is negative.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if max_depth is not None and max_depth < 1:
        raise ValueError("max_depth must be positive integer >= 1")

    res = []
    current_depth = 0

    for char in text:
        if char == "(":
            current_depth += 1
            if max_depth is not None and current_depth > max_depth:
                res.append(char)
        elif char == ")":
            if max_depth is not None and current_depth > max_depth:
                res.append(char)
            if current_depth > 0:
                current_depth -= 1
        else:
            if current_depth == 0 or (max_depth is not None and current_depth > max_depth):
                res.append(char)

    return re.sub(r" +", " ", "".join(res)).strip()


def check_balanced_parentheses(text: str) -> Tuple[bool, int, List[int]]:
    """
    Validates if parentheses in text are properly balanced.

    Args:
        text: Target text string.

    Returns:
        Tuple of (is_balanced, max_depth, unbalanced_indices_list).

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    stack = []  # stores (index, char)
    max_depth = 0
    unbalanced_indices = []

    for idx, char in enumerate(text):
        if char == "(":
            stack.append((idx, char))
            if len(stack) > max_depth:
                max_depth = len(stack)
        elif char == ")":
            if stack:
                stack.pop()
            else:
                unbalanced_indices.append(idx)

    for idx, char in stack:
        unbalanced_indices.append(idx)

    unbalanced_indices.sort()
    is_balanced = len(unbalanced_indices) == 0

    return is_balanced, max_depth, unbalanced_indices


# ─── 4. Expression Simplifier & Structure Analysis Engine ────────────────────


def simplify_expression_parentheses(expr: str) -> str:
    """
    Removes redundant nested parentheses enclosing a mathematical or logical expression.
    e.g. "((a + b))" -> "(a + b)"

    Args:
        expr: Expression string to simplify.

    Returns:
        Simplified expression string.

    Raises:
        TypeError: If expr is not a string.
    """
    if not isinstance(expr, str):
        raise TypeError(f"Expected string, got {type(expr).__name__}")
    if not expr.strip():
        return ""

    res = expr.strip()
    while res.startswith("(") and res.endswith(")"):
        is_bal, _, _ = check_balanced_parentheses(res[1:-1])
        if is_bal:
            res = res[1:-1].strip()
        else:
            break

    return res


def analyze_parenthesis_structure(text: str) -> Dict[str, Any]:
    """
    Computes statistical and structural metrics for parentheses in a text.

    Args:
        text: Target text string.

    Returns:
        Dict containing open_count, close_count, is_balanced, max_depth,
        unbalanced_indices, total_enclosed_chars, and parenthetical_pairs_count.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    open_cnt = text.count("(")
    close_cnt = text.count(")")
    is_bal, max_depth, unbal_idx = check_balanced_parentheses(text)

    contents = extract_parenthetical_contents(text)
    total_enclosed = sum(len(c) for c in contents)

    return {
        "open_count": open_cnt,
        "close_count": close_cnt,
        "is_balanced": is_bal,
        "max_nesting_depth": max_depth,
        "unbalanced_indices": unbal_idx,
        "parenthetical_pairs_count": len(contents),
        "total_enclosed_chars": total_enclosed,
        "extracted_contents": contents,
    }



