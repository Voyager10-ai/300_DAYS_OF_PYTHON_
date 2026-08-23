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


# ─── 6. Auto-Repair & Completion Utilities ────────────────────────────────────


def repair_unbalanced_parentheses(s: str) -> str:
    """
    Repairs an unbalanced string by removing orphan closing brackets and appending
    missing closing brackets for unclosed opening brackets.

    Args:
        s: Input string.

    Returns:
        Repaired string that is guaranteed to be valid/balanced.
    """
    open_to_close = {v: k for k, v in DEFAULT_BRACKET_PAIRS.items()}

    # First pass: Filter out unmatched closing brackets
    clean_chars: List[str] = []
    stack: List[str] = []

    for char in s:
        if char in OPENING_BRACKETS:
            stack.append(char)
            clean_chars.append(char)
        elif char in CLOSING_BRACKETS:
            if stack and stack[-1] == DEFAULT_BRACKET_PAIRS[char]:
                stack.pop()
                clean_chars.append(char)
            # Else ignore orphan closing bracket
        else:
            clean_chars.append(char)

    # Second pass: Append missing closing brackets for remaining unclosed open brackets
    missing_closing = [open_to_close[open_char] for open_char in reversed(stack)]
    return "".join(clean_chars) + "".join(missing_closing)


def complete_open_parentheses(s: str) -> str:
    """
    Appends only the required closing brackets to complete any unclosed opening brackets.

    Args:
        s: Expression string.

    Returns:
        Suffix string of missing closing brackets, or empty string if already complete/invalid.
    """
    open_to_close = {v: k for k, v in DEFAULT_BRACKET_PAIRS.items()}
    stack: List[str] = []

    for char in s:
        if char in OPENING_BRACKETS:
            stack.append(char)
        elif char in CLOSING_BRACKETS:
            if stack and stack[-1] == DEFAULT_BRACKET_PAIRS[char]:
                stack.pop()
            else:
                return ""

    missing_closing = [open_to_close[open_char] for open_char in reversed(stack)]
    return "".join(missing_closing)


# ─── 7. File-Based & Batch Parentheses Validator ──────────────────────────────


def validate_file_parentheses(
    file_path: Union[str, Path],
    encoding: str = "utf-8",
) -> Dict[int, ParenthesesDiagnosticResult]:
    """
    Validates parentheses line by line in a target text file.

    Args:
        file_path: Path to the target file.
        encoding: File encoding.

    Returns:
        Dictionary mapping line_number (1-indexed) to diagnostic results for invalid lines.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    invalid_lines: Dict[int, ParenthesesDiagnosticResult] = {}

    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line_num, line in enumerate(f, start=1):
            diag = validate_parentheses_in_code(line)
            if not diag.is_valid:
                invalid_lines[line_num] = diag

    return invalid_lines


def validate_batch_expressions(expressions: List[str]) -> List[Tuple[str, bool]]:
    """
    Validates a list of math/code expressions in batch.

    Args:
        expressions: List of input string expressions.

    Returns:
        List of tuples (expression, is_valid).
    """
    return [(expr, is_valid_parentheses(expr)) for expr in expressions]


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestCheckParenthesesOperations(unittest.TestCase):
    def test_is_valid_parentheses_standard(self):
        self.assertTrue(is_valid_parentheses("()"))
        self.assertTrue(is_valid_parentheses("()[]{}"))
        self.assertTrue(is_valid_parentheses("{[()]}"))
        self.assertTrue(is_valid_parentheses("a * (b + c) - [d / {e}]"))
        self.assertFalse(is_valid_parentheses("(]"))
        self.assertFalse(is_valid_parentheses("([)]"))
        self.assertFalse(is_valid_parentheses("{"))
        self.assertFalse(is_valid_parentheses(")"))

    def test_is_balanced_simple(self):
        self.assertTrue(is_balanced_simple("((()))"))
        self.assertTrue(is_balanced_simple("()()()"))
        self.assertFalse(is_balanced_simple("((()"))
        self.assertFalse(is_balanced_simple(")("))

    def test_validate_parentheses_with_diagnostics(self):
        # Valid
        res_valid = validate_parentheses_with_diagnostics("{[()]}")
        self.assertTrue(res_valid.is_valid)

        # Unmatched closing
        res_unmatched = validate_parentheses_with_diagnostics("()")
        self.assertTrue(res_unmatched.is_valid)
        res_orphan = validate_parentheses_with_diagnostics("())")
        self.assertFalse(res_orphan.is_valid)
        self.assertEqual(res_orphan.error_type, "UNMATCHED_CLOSING")
        self.assertEqual(res_orphan.error_position, 2)

        # Mismatched bracket
        res_mismatch = validate_parentheses_with_diagnostics("(]")
        self.assertFalse(res_mismatch.is_valid)
        self.assertEqual(res_mismatch.error_type, "MISMATCHED_BRACKET")

        # Unclosed opening
        res_unclosed = validate_parentheses_with_diagnostics("{[(")
        self.assertFalse(res_unclosed.is_valid)
        self.assertEqual(res_unclosed.error_type, "UNCLOSED_OPENING")

    def test_custom_bracket_pairs(self):
        custom_pairs = [("<", ">"), ("«", "»")]
        self.assertTrue(is_valid_parentheses_custom("<«text»>", pairs=custom_pairs))
        self.assertFalse(is_valid_parentheses_custom("<«text>", pairs=custom_pairs))

    def test_code_quote_comment_awareness(self):
        code_sample = "x = '([)]' # comment with unmatched (\nprint(arr[0])"
        diag = validate_parentheses_in_code(code_sample)
        self.assertTrue(diag.is_valid)

    def test_nesting_depth(self):
        self.assertEqual(get_max_nesting_depth("((()))"), 3)
        self.assertEqual(get_max_nesting_depth("{[()]}"), 3)
        self.assertEqual(get_max_nesting_depth("(]"), -1)

        profile, max_d = get_bracket_depth_profile("a(b[c]d)e")
        self.assertEqual(max_d, 2)
        self.assertEqual(len(profile), len("a(b[c]d)e"))

    def test_repair_and_complete(self):
        self.assertEqual(repair_unbalanced_parentheses("((()"), "((()))")
        self.assertEqual(repair_unbalanced_parentheses(")(]"), "()")
        self.assertEqual(repair_unbalanced_parentheses("{[("), "{[()]}")

        self.assertEqual(complete_open_parentheses("function(arr[i"), "])")
        self.assertEqual(complete_open_parentheses("()"), "")

    def test_batch_expressions(self):
        batch = ["()", "([)]", "{[()]}"]
        results = validate_batch_expressions(batch)
        self.assertEqual(results, [("()", True), ("([)]", False), ("{[()]}", True)])


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" 🧩 Day 46: Parentheses & Bracket Validator - Interactive Demo")
    print("=" * 60)

    # 1. Batch Expression Check
    sample_exprs = [
        "a * (b + c) - [d / {e}]",
        "((x + y) * z",
        "function([x, y]) { return (x + y); }",
        "invalid_mismatch = (a + b]",
    ]
    print("\n1. Batch Parentheses Validation:")
    for expr in sample_exprs:
        valid = is_valid_parentheses(expr)
        status = "✅ VALID" if valid else "❌ INVALID"
        print(f"   [{status}] {expr}")

    # 2. Detailed Diagnostics
    invalid_sample = "def test(x):\n    arr = [1, 2, (3 + 4]\n    return arr"
    print("\n2. Detailed Diagnostic Reporting for Mismatched Code:")
    diag = validate_parentheses_with_diagnostics(invalid_sample)
    print(f"   Diagnostic Output: {diag.message}")
    print(f"   Error Type       : {diag.error_type}")
    print(f"   Error Position   : Index {diag.error_position}")

    # 3. Nesting Depth & Profile
    nested_str = "{ a : [ b + ( c * ( d + e ) ) ] }"
    depth = get_max_nesting_depth(nested_str)
    print(f"\n3. Nesting Depth Analysis:")
    print(f"   Expression : '{nested_str}'")
    print(f"   Max Depth  : {depth}")

    # 4. Auto-Repair Demonstration
    unbalanced_str = "((a + b) * [c - d"
    repaired_str = repair_unbalanced_parentheses(unbalanced_str)
    print(f"\n4. Auto-Repair Demonstration:")
    print(f"   Original Unbalanced : '{unbalanced_str}'")
    print(f"   Repaired Output     : '{repaired_str}'")

    # 5. Unit Test Suite Execution
    print("\n5. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCheckParenthesesOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








