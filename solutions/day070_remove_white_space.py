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


# ─── 5. Collection Batch Whitespace Sanitizers ───────────────────────────────


def remove_whitespace_from_list(
    text_list: List[str],
    mode: str = "all",
) -> List[str]:
    """
    Sanitizes a list of strings by removing or trimming whitespace based on mode.

    Args:
        text_list: Input list of strings.
        mode: Sanitization mode ('all', 'trim', 'normalize').
              - 'all': strips all whitespace completely.
              - 'trim': strips leading and trailing whitespace.
              - 'normalize': collapses multiple spaces into single space.

    Returns:
        List of sanitized strings.

    Raises:
        TypeError: If text_list is not a list.
    """
    if not isinstance(text_list, list):
        raise TypeError(f"Expected list for text_list, got {type(text_list).__name__}")

    sanitized = []
    m = mode.lower().strip()

    for item in text_list:
        if not isinstance(item, str):
            raise TypeError(f"All list elements must be strings, got {type(item).__name__}")

        if m == "all":
            sanitized.append(remove_all_whitespace(item))
        elif m == "trim":
            sanitized.append(item.strip())
        elif m == "normalize":
            sanitized.append(normalize_whitespace(item))
        else:
            raise ValueError(f"Invalid mode '{mode}'. Choose from 'all', 'trim', 'normalize'.")

    return sanitized


def remove_whitespace_from_dict(
    data: Dict[str, Any],
    sanitize_keys: bool = True,
    sanitize_values: bool = True,
    mode: str = "all",
) -> Dict[str, Any]:
    """
    Sanitizes dictionary keys and/or string values by cleaning whitespace.

    Args:
        data: Target dictionary.
        sanitize_keys: If True, cleans whitespace in string keys.
        sanitize_values: If True, cleans whitespace in string values.
        mode: Sanitization mode ('all', 'trim', 'normalize').

    Returns:
        New dictionary with sanitized keys/values.

    Raises:
        TypeError: If data is not a dict.
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict for data, got {type(data).__name__}")

    new_dict: Dict[str, Any] = {}

    for k, v in data.items():
        key_str = str(k)
        new_k = remove_whitespace_from_list([key_str], mode=mode)[0] if sanitize_keys else k

        new_v = v
        if sanitize_values and isinstance(v, str):
            new_v = remove_whitespace_from_list([v], mode=mode)[0]

        new_dict[new_k] = new_v

    return new_dict


# ─── 6. Whitespace Replacement Masker & Code Indentation Normalizer ─────────


def replace_whitespace(text: str, replacement_char: str = "_") -> str:
    """
    Replaces all whitespace characters in a text with a replacement character.

    Args:
        text: Source text string.
        replacement_char: Character to substitute for whitespace (default '_').

    Returns:
        Transformed string.

    Raises:
        TypeError: If inputs are not strings.
    """
    if not isinstance(text, str) or not isinstance(replacement_char, str):
        raise TypeError("text and replacement_char must be strings.")

    return re.sub(r"\s", replacement_char, text)


def normalize_indentation(code_text: str, indent_spaces: int = 4) -> str:
    """
    Converts tab characters in indented code text to uniform space indentation.

    Args:
        code_text: Multiline code snippet string.
        indent_spaces: Number of spaces per tab level (default 4).

    Returns:
        Code string with normalized space indentation.

    Raises:
        TypeError: If code_text is not a string.
        ValueError: If indent_spaces is not positive.
    """
    if not isinstance(code_text, str):
        raise TypeError(f"Expected string for code_text, got {type(code_text).__name__}")
    if indent_spaces < 1:
        raise ValueError(f"indent_spaces must be positive, got {indent_spaces}")

    spaces = " " * indent_spaces
    lines = code_text.splitlines()
    normalized = []

    for line in lines:
        # Convert leading tabs to space indentation
        match = re.match(r"^[\t ]+", line)
        if match:
            leading = match.group(0)
            converted_leading = leading.replace("\t", spaces)
            rest = line[len(leading) :]
            normalized.append(converted_leading + rest)
        else:
            normalized.append(line)

    return "\n".join(normalized)





