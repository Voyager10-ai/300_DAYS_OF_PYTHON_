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


# ─── 2. Detailed URL Parser & Component Decomposition Engine ─────────────────


def parse_url_components(url: str) -> Dict[str, Any]:
    """
    Decomposes a URL string into detailed constituent components.

    Args:
        url: Target URL string to parse.

    Returns:
        Dict containing scheme, netloc, domain, port, path, query_string,
        query_params (dict), fragment, and userinfo.

    Raises:
        TypeError: If url is not a string.
        ValueError: If url is empty.
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected string for url, got {type(url).__name__}")
    if not url.strip():
        raise ValueError("URL string cannot be empty.")

    # Ensure URL has protocol for urllib parsing if omitted
    parse_target = url if "://" in url else f"http://{url}"
    parsed = urlparse(parse_target)

    # Extract userinfo if present
    userinfo = None
    if parsed.username or parsed.password:
        userinfo = {
            "username": parsed.username,
            "password": parsed.password,
        }

    # Extract query parameters into dict
    raw_query = parse_qs(parsed.query)
    # Simplify query values list if single value
    query_params: Dict[str, Any] = {}
    for k, v in raw_query.items():
        query_params[k] = v[0] if len(v) == 1 else v

    # Extract port
    port = parsed.port
    hostname = parsed.hostname or ""

    return {
        "raw_url": url,
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "hostname": hostname,
        "port": port,
        "path": parsed.path or "/",
        "query_string": parsed.query,
        "query_params": query_params,
        "fragment": parsed.fragment,
        "userinfo": userinfo,
        "is_secure": parsed.scheme.lower() == "https",
    }

