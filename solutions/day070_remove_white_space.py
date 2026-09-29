# Day 70: Remove White Space
#
# Problem:
#   Write a Python program / module to strip, trim, normalize, and analyze whitespace characters in strings.
#   Includes core removal, trimming modes, whitespace normalization, multiline cleaner, selective category stripping,
#   metrics analysis engine, collection batch sanitizers, code indentation normalizer, unit test suite, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Whitespace Removal & Trimming Utilities ─────────────────────────


def remove_all_whitespace(text: str) -> str:
    """
    Strips all whitespace characters (spaces, tabs, newlines, carriage returns) from a string.

    Args:
        text: Target input string.

    Returns:
        String with all whitespace characters completely removed.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text:
        return ""

    return re.sub(r"\s+", "", text)


def trim_whitespace(text: str, mode: str = "both") -> str:
    """
    Trims whitespace from a string based on specified mode.

    Args:
        text: Target text string.
        mode: Trimming strategy ('both', 'leading', 'trailing', 'extra_spaces').
              - 'both': strips leading and trailing whitespace.
              - 'leading': strips only leading whitespace.
              - 'trailing': strips only trailing whitespace.
              - 'extra_spaces': collapses multiple interior spaces into a single space and trims edges.

    Returns:
        Trimmed string output.

    Raises:
        TypeError: If text is not a string.
        ValueError: If mode is invalid.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")

    m = mode.lower().strip()
    if m == "both":
        return text.strip()
    elif m == "leading":
        return text.lstrip()
    elif m == "trailing":
        return text.rstrip()
    elif m == "extra_spaces":
        return re.sub(r"\s+", " ", text).strip()
    else:
        raise ValueError(f"Invalid mode '{mode}'. Choose from 'both', 'leading', 'trailing', 'extra_spaces'.")


# ─── 2. Whitespace Normalizer & Multiline Text Cleaner ────────────────────────


def normalize_whitespace(text: str, single_space: bool = True) -> str:
    """
    Normalizes consecutive whitespace characters into a single space or standard newlines.

    Args:
        text: Source text string.
        single_space: If True, converts all consecutive whitespace (including newlines) into a single space.
                      If False, collapses consecutive spaces per line while preserving single line breaks.

    Returns:
        Normalized string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if not text:
        return ""

    if single_space:
        return re.sub(r"\s+", " ", text).strip()

    # Preserve line breaks but collapse horizontal spaces on each line
    lines = text.splitlines()
    normalized_lines = [re.sub(r"[ \t]+", " ", line).strip() for line in lines]
    return "\n".join(normalized_lines)


def clean_line_whitespace(multiline_text: str, remove_empty_lines: bool = True) -> str:
    """
    Trims leading and trailing whitespace from each line of a multiline text block.

    Args:
        multiline_text: Paragraph or multiline string.
        remove_empty_lines: If True, completely filters out blank or empty lines.

    Returns:
        Cleaned multiline string.

    Raises:
        TypeError: If multiline_text is not a string.
    """
    if not isinstance(multiline_text, str):
        raise TypeError(f"Expected string for multiline_text, got {type(multiline_text).__name__}")

    lines = multiline_text.splitlines()
    cleaned = []

    for line in lines:
        stripped = line.strip()
        if remove_empty_lines:
            if stripped:
                cleaned.append(stripped)
        else:
            cleaned.append(stripped)

    return "\n".join(cleaned)


# ─── 3. Selective Category Stripper & Excess Whitespace Detector ───────────────


def strip_whitespace_categories(
    text: str,
    remove_spaces: bool = True,
    remove_tabs: bool = True,
    remove_newlines: bool = True,
) -> str:
    """
    Selectively removes specific categories of whitespace (spaces, tabs, newlines).

    Args:
        text: Target text string.
        remove_spaces: If True, strips space characters ' '.
        remove_tabs: If True, strips tab characters '\t'.
        remove_newlines: If True, strips line break characters '\n' and '\r'.

    Returns:
        Filtered string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    res = text
    if remove_tabs:
        res = res.replace("\t", "")
    if remove_newlines:
        res = res.replace("\n", "").replace("\r", "")
    if remove_spaces:
        res = res.replace(" ", "")

    return res


def has_excess_whitespace(text: str) -> bool:
    """
    Detects if a string contains excess whitespace (leading, trailing, or multiple consecutive spaces).

    Args:
        text: Target text string.

    Returns:
        True if text has leading/trailing whitespace or multiple spaces, else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    if not text:
        return False

    if text != text.strip():
        return True

    return bool(re.search(r" {2,}|\t|\n", text))


# ─── 4. Whitespace Analysis & Distribution Metrics Engine ────────────────────


def analyze_whitespace_distribution(text: str) -> Dict[str, Any]:
    """
    Computes comprehensive statistics on whitespace distribution within a text string.

    Args:
        text: Target input string.

    Returns:
        Dict containing total_length, non_whitespace_count, total_whitespace_count,
        spaces_count, tabs_count, newlines_count, whitespace_ratio_percentage,
        and consecutive_space_blocks_count.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    total_len = len(text)
    spaces_cnt = text.count(" ")
    tabs_cnt = text.count("\t")
    newlines_cnt = text.count("\n") + text.count("\r")
    total_ws = sum(1 for c in text if c.isspace())
    non_ws = total_len - total_ws

    ratio = (total_ws / total_len * 100.0) if total_len > 0 else 0.0
    consecutive_blocks = len(re.findall(r"\s+", text))

    return {
        "total_length": total_len,
        "non_whitespace_count": non_ws,
        "total_whitespace_count": total_ws,
        "spaces_count": spaces_cnt,
        "tabs_count": tabs_cnt,
        "newlines_count": newlines_cnt,
        "whitespace_ratio_percentage": round(ratio, 2),
        "consecutive_space_blocks_count": consecutive_blocks,
        "has_excess_whitespace": has_excess_whitespace(text),
    }



