# Day 67: Find URL
#
# Problem:
#   Write a Python program / module to extract, parse, validate, and manipulate URLs within text or HTML.
#   Includes regex URL extraction, component decomposition, security validation, query parameter manipulation,
#   domain/TLD analysis, HTML link tag parsing, URL masking, unit test suite, and Java practice.

import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, urljoin


# ─── 1. Core Regex URL Extractors & Link Finders ─────────────────────────────

# Robust URL matching pattern supporting http, https, ftp, ftps, with ports, paths, query, and fragments
URL_REGEX_PATTERN = r"(?i)\b(?:https?|ftp)://(?:[a-zA-Z0-9.\-]+(?::[a-zA-Z0-9.&%$-]+)*@)?(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(?::\d+)?(?:/[^\s<>'\"`{}]*)?"


def extract_urls(
    text: str,
    protocols: Optional[List[str]] = None,
) -> List[str]:
    """
    Extracts all URLs matching specified protocols from a string paragraph or document.

    Args:
        text: Input string text to search.
        protocols: List of allowed schemes e.g. ['http', 'https', 'ftp']. If None, all are allowed.

    Returns:
        List of extracted URL strings.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string for text, got {type(text).__name__}")
    if not text.strip():
        return []

    raw_matches = re.findall(URL_REGEX_PATTERN, text)
    cleaned_urls = []

    for match in raw_matches:
        # Strip trailing punctuation marks that might attach to URLs in prose (e.g. "Visit https://site.com.")
        url = re.sub(r"[.,;:!?)]+$", "", match)
        if protocols:
            scheme = url.split("://")[0].lower()
            if scheme not in [p.lower() for p in protocols]:
                continue
        cleaned_urls.append(url)

    return cleaned_urls


def has_url(text: str) -> bool:
    """
    Checks whether a string contains at least one valid URL.

    Args:
        text: Target text string.

    Returns:
        True if text contains a URL, else False.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    return bool(extract_urls(text))
