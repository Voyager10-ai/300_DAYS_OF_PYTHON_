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


# ─── 5. Collection Batch Sanitizer & List Cleaner ─────────────────────────────


def remove_parentheses_from_list(
    text_list: List[str],
    remove_contents: bool = True,
) -> List[str]:
    """
    Sanitizes a list of strings by stripping parentheses and optionally their contents.

    Args:
        text_list: List of input string items.
        remove_contents: If True, removes text inside parentheses.

    Returns:
        List of sanitized strings.

    Raises:
        TypeError: If text_list is not a list.
    """
    if not isinstance(text_list, list):
        raise TypeError(f"Expected list for text_list, got {type(text_list).__name__}")

    sanitized = []
    for item in text_list:
        if not isinstance(item, str):
            raise TypeError(f"All list elements must be strings, got {type(item).__name__}")
        sanitized.append(remove_parentheses(item, remove_contents=remove_contents))

    return sanitized


def remove_parentheses_from_dict(
    data: Dict[str, Any],
    sanitize_keys: bool = True,
    sanitize_values: bool = True,
) -> Dict[str, Any]:
    """
    Sanitizes dictionary keys and/or string values by stripping parentheses.

    Args:
        data: Target dictionary.
        sanitize_keys: If True, strips parentheses from string keys.
        sanitize_values: If True, strips parentheses from string values.

    Returns:
        New dictionary with sanitized keys and values.

    Raises:
        TypeError: If data is not a dict.
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict for data, got {type(data).__name__}")

    new_dict: Dict[str, Any] = {}

    for k, v in data.items():
        new_k = remove_parentheses(str(k)) if sanitize_keys else k
        new_v = v
        if sanitize_values and isinstance(v, str):
            new_v = remove_parentheses(v)
        new_dict[new_k] = new_v

    return new_dict


# ─── 6. Parenthesis Redaction Masker & Tag Transformer ────────────────────────


def mask_parentheses_contents(text: str, mask_str: str = "[REDACTED]") -> str:
    """
    Replaces all text inside parentheses with a redaction mask label.

    Args:
        text: Source text string.
        mask_str: Redaction label string (default '[REDACTED]').

    Returns:
        Redacted text string.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(text, str) or not isinstance(mask_str, str):
        raise TypeError("text and mask_str must be strings.")
    if not text:
        return ""

    return re.sub(r"\([^()]*\)", f"({mask_str})", text)


def transform_parentheses_tags(
    text: str,
    new_open: str = "[",
    new_close: str = "]",
) -> str:
    """
    Replaces parenthesis characters '()' with alternative open/close brackets e.g. '[]' or '{}'.

    Args:
        text: Target string.
        new_open: New opening character/string (default '[').
        new_close: New closing character/string (default ']').

    Returns:
        Transformed string.

    Raises:
        TypeError: If inputs are not strings.
    """
    if not isinstance(text, str) or not isinstance(new_open, str) or not isinstance(new_close, str):
        raise TypeError("Inputs must be strings.")

    return text.replace("(", new_open).replace(")", new_close)


# ─── 7. Unit Test Suite ───────────────────────────────────────────────────────


class TestRemoveParenthesis(unittest.TestCase):
    """Test suite for parenthesis removal, content stripping, nested stack parsing, and structure analysis."""

    def test_core_remove_parentheses(self):
        self.assertEqual(remove_parentheses("Hello (world) Python"), "Hello Python")
        self.assertEqual(remove_parentheses("Hello (world) Python", remove_contents=False), "Hello world Python")
        self.assertEqual(remove_parentheses(""), "")
        self.assertTrue(has_parentheses("Text (note)"))
        self.assertFalse(has_parentheses("Text note"))

        with self.assertRaises(TypeError):
            remove_parentheses(12345)

    def test_remove_custom_brackets_and_contents(self):
        text = "Alpha (one) [two] {three} <four>"
        self.assertEqual(remove_custom_brackets(text, brackets=["()", "[]"]), "Alpha {three} <four>")
        self.assertEqual(extract_parenthetical_contents("Py (first) and (second)"), ["first", "second"])

    def test_nested_stack_parser_and_balance(self):
        nested = "A (B (C) D) E"
        self.assertEqual(remove_nested_parentheses(nested), "A E")
        self.assertEqual(remove_nested_parentheses(nested, max_depth=1), "A (C) E")

        is_bal, max_d, unbal = check_balanced_parentheses("((a + b))")
        self.assertTrue(is_bal)
        self.assertEqual(max_d, 2)
        self.assertEqual(unbal, [])

        is_bal_fail, _, unbal_fail = check_balanced_parentheses("((a + b)")
        self.assertFalse(is_bal_fail)
        self.assertEqual(unbal_fail, [0])

    def test_expression_simplifier_and_structure(self):
        self.assertEqual(simplify_expression_parentheses("((x + y))"), "x + y")
        self.assertEqual(simplify_expression_parentheses("(a + b) * (c + d)"), "(a + b) * (c + d)")

        struct = analyze_parenthesis_structure("Val (1) + (2)")
        self.assertEqual(struct["open_count"], 2)
        self.assertEqual(struct["parenthetical_pairs_count"], 2)
        self.assertEqual(struct["extracted_contents"], ["1", "2"])

    def test_collection_sanitizers(self):
        lst = ["Alpha (v1)", "Beta (v2)"]
        self.assertEqual(remove_parentheses_from_list(lst), ["Alpha", "Beta"])

        d = {"key(1)": "val(2)", "num": 100}
        san_d = remove_parentheses_from_dict(d)
        self.assertIn("key", san_d)
        self.assertEqual(san_d["key"], "val")

    def test_masking_and_tag_transformation(self):
        self.assertEqual(mask_parentheses_contents("User (secret) data"), "User ([REDACTED]) data")
        self.assertEqual(transform_parentheses_tags("Func(x, y)", "[", "]"), "Func[x, y]")






