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
