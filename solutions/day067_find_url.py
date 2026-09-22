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

# Robust URL matching pattern supporting http, https, ftp, ftps, with ports, paths, query, IP addresses, and fragments
URL_REGEX_PATTERN = r"(?i)\b(?:https?|ftp)://(?:[a-zA-Z0-9.\-]+(?::[a-zA-Z0-9.&%$-]+)*@)?(?:(?:\d{1,3}\.){3}\d{1,3}|localhost|(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})(?::\d+)?(?:/[^\s<>'\"`{}]*)?"



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


# ─── 3. URL Validation & Security Health Checker ─────────────────────────────


def is_valid_url(
    url: str,
    require_protocol: bool = True,
    allowed_schemes: Optional[Set[str]] = None,
) -> bool:
    """
    Validates whether a given string is a syntactically correct URL.

    Args:
        url: URL string to check.
        require_protocol: If True, requires explicit scheme (e.g. http:// or https://).
        allowed_schemes: Set of allowed schemes e.g. {'http', 'https'}.

    Returns:
        True if valid URL matching criteria, else False.

    Raises:
        TypeError: If url is not a string.
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected string, got {type(url).__name__}")
    if not url.strip():
        return False

    if allowed_schemes is None:
        allowed_schemes = {"http", "https", "ftp", "ftps"}

    if require_protocol:
        if "://" not in url:
            return False
        scheme = url.split("://")[0].lower()
        if scheme not in allowed_schemes:
            return False

    target = url if "://" in url else f"http://{url}"
    parsed = urlparse(target)

    # Validate hostname domain format
    hostname = parsed.hostname
    if not hostname:
        return False

    # Check IPv4 or domain syntax
    domain_pattern = r"^([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}$|^localhost$|^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    return bool(re.match(domain_pattern, hostname))


def validate_url_security(url: str) -> Dict[str, Any]:
    """
    Performs security risk assessment on a URL string.

    Args:
        url: URL string to inspect.

    Returns:
        Dict containing is_secure_protocol, is_ip_host, contains_credentials,
        has_suspicious_tld, potential_path_traversal, and security_score (0 to 100).

    Raises:
        TypeError: If url is not a string.
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected string, got {type(url).__name__}")

    components = parse_url_components(url)
    hostname = components["hostname"]
    scheme = components["scheme"].lower()

    is_https = scheme == "https"
    is_ip = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname))
    has_userinfo = components["userinfo"] is not None

    suspicious_tlds = {".zip", ".mov", ".top", ".xyz", ".work", ".click", ".country"}
    has_suspicious = any(hostname.lower().endswith(tld) for tld in suspicious_tlds)

    path = components["path"]
    has_traversal = "../" in path or "..\\" in path

    warnings = []
    score = 100

    if not is_https:
        warnings.append("Insecure protocol (HTTP/FTP)")
        score -= 20
    if is_ip:
        warnings.append("Raw IP address used instead of domain name")
        score -= 25
    if has_userinfo:
        warnings.append("Credentials embedded in URL userinfo")
        score -= 30
    if has_suspicious:
        warnings.append("Suspicious or high-risk TLD extension")
        score -= 15
    if has_traversal:
        warnings.append("Potential directory traversal pattern in path")
        score -= 40

    return {
        "url": url,
        "is_https": is_https,
        "is_ip_host": is_ip,
        "contains_credentials": has_userinfo,
        "has_suspicious_tld": has_suspicious,
        "potential_path_traversal": has_traversal,
        "warnings": warnings,
        "security_score": max(0, score),
    }


# ─── 4. Query String Builder & URL Normalizer ─────────────────────────────────


def add_query_params(url: str, params: Dict[str, Any]) -> str:
    """
    Appends or updates query parameters in a URL string.

    Args:
        url: Target URL string.
        params: Dictionary of parameters to add/update.

    Returns:
        Updated URL string with newly encoded query parameters.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected string for url, got {type(url).__name__}")
    if not isinstance(params, dict):
        raise TypeError(f"Expected dict for params, got {type(params).__name__}")
    if not params:
        return url

    parsed = urlparse(url)
    current_qs = parse_qs(parsed.query)

    for k, v in params.items():
        current_qs[k] = [str(v)]

    new_query = urlencode(current_qs, doseq=True)
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )


def remove_query_params(url: str, param_names: List[str]) -> str:
    """
    Removes specified query parameters from a URL string.

    Args:
        url: Target URL string.
        param_names: List of parameter keys to remove.

    Returns:
        Cleaned URL string without specified query keys.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected string for url, got {type(url).__name__}")
    if not isinstance(param_names, list):
        raise TypeError(f"Expected list for param_names, got {type(param_names).__name__}")

    parsed = urlparse(url)
    current_qs = parse_qs(parsed.query)

    for name in param_names:
        current_qs.pop(name, None)

    new_query = urlencode(current_qs, doseq=True)
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )


def normalize_url(
    url: str,
    strip_trailing_slash: bool = True,
    lowercase_domain: bool = True,
) -> str:
    """
    Normalizes a URL to a canonical standard form.

    Args:
        url: Input URL string.
        strip_trailing_slash: If True, strips trailing '/' from path.
        lowercase_domain: If True, converts scheme and domain to lowercase.

    Returns:
        Normalized URL string.

    Raises:
        TypeError: If url is not a string.
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected string, got {type(url).__name__}")

    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower() if lowercase_domain else parsed.scheme
    netloc = parsed.netloc.lower() if lowercase_domain else parsed.netloc

    path = parsed.path
    if strip_trailing_slash and path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    return urlunparse(
        (
            scheme,
            netloc,
            path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )


# ─── 5. Domain & TLD Analysis Utilities ───────────────────────────────────────


def extract_domain_info(url: str) -> Dict[str, str]:
    """
    Deconstructs a URL's hostname into subdomain, root domain, and TLD extension.

    Args:
        url: Input URL string.

    Returns:
        Dict containing full_hostname, subdomain, root_domain, and tld.

    Raises:
        TypeError: If url is not a string.
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected string, got {type(url).__name__}")

    components = parse_url_components(url)
    hostname = components["hostname"].lower()

    if not hostname:
        return {"full_hostname": "", "subdomain": "", "root_domain": "", "tld": ""}

    parts = hostname.split(".")
    if len(parts) == 1:
        return {"full_hostname": hostname, "subdomain": "", "root_domain": hostname, "tld": ""}

    # Common multi-part TLD extensions e.g., .co.uk, .com.au
    multi_tlds = {"co.uk", "com.au", "gov.uk", "edu.au", "co.in", "net.au"}

    if len(parts) >= 3 and f"{parts[-2]}.{parts[-1]}" in multi_tlds:
        tld = f"{parts[-2]}.{parts[-1]}"
        root_domain = f"{parts[-3]}.{tld}"
        subdomain = ".".join(parts[:-3])
    else:
        tld = parts[-1]
        root_domain = f"{parts[-2]}.{tld}"
        subdomain = ".".join(parts[:-2])

    return {
        "full_hostname": hostname,
        "subdomain": subdomain,
        "root_domain": root_domain,
        "tld": tld,
    }


def filter_urls_by_domain(
    urls: List[str],
    target_domain: str,
    include_subdomains: bool = True,
) -> List[str]:
    """
    Filters a list of URLs to keep only those belonging to target_domain.

    Args:
        urls: List of URL strings.
        target_domain: Target domain e.g. 'example.com'.
        include_subdomains: If True, matches subdomains like 'blog.example.com'.

    Returns:
        Filtered list of URL strings.

    Raises:
        TypeError: If inputs are invalid types.
    """
    if not isinstance(urls, list) or not isinstance(target_domain, str):
        raise TypeError("urls must be a list and target_domain must be a string.")

    target = target_domain.lower().strip()
    matching = []

    for u in urls:
        if not isinstance(u, str):
            continue
        info = extract_domain_info(u)
        host = info["full_hostname"]
        root = info["root_domain"]

        if include_subdomains:
            if host == target or host.endswith(f".{target}") or root == target:
                matching.append(u)
        else:
            if host == target or root == target:
                matching.append(u)

    return matching


# ─── 6. HTML Link Tag Parser & URL Masker ─────────────────────────────────────


def extract_urls_from_html(
    html_content: str,
    base_url: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Parses HTML content to extract all link (href) and media (src) URLs.

    Args:
        html_content: String HTML document markup.
        base_url: Optional base URL to resolve relative link paths (e.g. '/about' -> 'https://site.com/about').

    Returns:
        List of dicts containing 'tag', 'attribute', 'raw_value', and 'absolute_url'.

    Raises:
        TypeError: If html_content is not a string.
    """
    if not isinstance(html_content, str):
        raise TypeError(f"Expected string for html_content, got {type(html_content).__name__}")

    tag_pattern = r'<(a|img|script|link|iframe|source)\s+[^>]*?(href|src)\s*=\s*["\']([^"\']+)["\'][^>]*>'
    matches = re.findall(tag_pattern, html_content, flags=re.IGNORECASE)

    extracted = []
    for tag, attr, raw_val in matches:
        val = raw_val.strip()
        if not val or val.startswith("javascript:") or val.startswith("mailto:"):
            continue

        abs_url = val
        if base_url:
            abs_url = urljoin(base_url, val)

        extracted.append(
            {
                "tag": tag.lower(),
                "attribute": attr.lower(),
                "raw_value": val,
                "absolute_url": abs_url,
            }
        )

    return extracted


def mask_urls_in_text(text: str, mask_str: str = "[URL REDACTED]") -> str:
    """
    Replaces all URLs in a text paragraph with a redaction mask.

    Args:
        text: Target text string.
        mask_str: Redaction label replacement string (default '[URL REDACTED]').

    Returns:
        Redacted text string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    urls = extract_urls(text)
    redacted = text

    for u in urls:
        redacted = redacted.replace(u, mask_str)

    return redacted


# ─── 7. Unit Test Suite ───────────────────────────────────────────────────────


class TestFindURL(unittest.TestCase):
    """Test suite for URL extraction, component parsing, validation, and domain analysis."""

    def test_extract_urls(self):
        text = "Visit https://google.com or http://github.com/repo for details."
        urls = extract_urls(text)
        self.assertEqual(urls, ["https://google.com", "http://github.com/repo"])
        self.assertTrue(has_url(text))
        self.assertFalse(has_url("No link here."))

        with self.assertRaises(TypeError):
            extract_urls(12345)

    def test_parse_url_components(self):
        url = "https://admin:pass@api.example.com:8080/v1/users?role=admin&active=true#section2"
        comp = parse_url_components(url)
        self.assertEqual(comp["scheme"], "https")
        self.assertEqual(comp["hostname"], "api.example.com")
        self.assertEqual(comp["port"], 8080)
        self.assertEqual(comp["path"], "/v1/users")
        self.assertEqual(comp["query_params"], {"role": "admin", "active": "true"})
        self.assertEqual(comp["fragment"], "section2")
        self.assertEqual(comp["userinfo"], {"username": "admin", "password": "pass"})
        self.assertTrue(comp["is_secure"])

    def test_is_valid_url_and_security(self):
        self.assertTrue(is_valid_url("https://example.com/test"))
        self.assertFalse(is_valid_url("invalid-url-string"))

        sec = validate_url_security("http://192.168.1.1/admin/../secret.txt")
        self.assertFalse(sec["is_https"])
        self.assertTrue(sec["is_ip_host"])
        self.assertTrue(sec["potential_path_traversal"])
        self.assertLess(sec["security_score"], 50)

    def test_query_params_and_normalization(self):
        url = "https://example.com/search?q=python"
        updated = add_query_params(url, {"page": 2, "sort": "asc"})
        self.assertIn("page=2", updated)
        self.assertIn("sort=asc", updated)

        cleaned = remove_query_params(updated, ["page"])
        self.assertNotIn("page=2", cleaned)
        self.assertIn("q=python", cleaned)

        norm = normalize_url("HTTPS://Example.com:80/path/to/page/")
        self.assertEqual(norm, "https://example.com:80/path/to/page")

    def test_domain_info_and_filtering(self):
        info = extract_domain_info("https://blog.sub.example.co.uk/post/1")
        self.assertEqual(info["full_hostname"], "blog.sub.example.co.uk")
        self.assertEqual(info["root_domain"], "example.co.uk")
        self.assertEqual(info["tld"], "co.uk")

        urls = [
            "https://example.com/p1",
            "https://blog.example.com/p2",
            "https://otherdomain.com/p3",
        ]
        filtered = filter_urls_by_domain(urls, "example.com", include_subdomains=True)
        self.assertEqual(filtered, ["https://example.com/p1", "https://blog.example.com/p2"])

    def test_html_parsing_and_masking(self):
        html = '<a href="/about">About</a><img src="https://cdn.site.com/logo.png">'
        links = extract_urls_from_html(html, base_url="https://site.com")
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]["absolute_url"], "https://site.com/about")

        text = "Contact us at https://support.site.com now."
        masked = mask_urls_in_text(text, mask_str="[REDACTED]")
        self.assertEqual(masked, "Contact us at [REDACTED] now.")


# ─── 8. Interactive CLI Demonstration ─────────────────────────────────────────


def main() -> None:
    """Demonstrates all Day 67 URL extraction, parsing, and manipulation utilities."""
    print("=" * 65)
    print(" DAY 67: FIND URL & PARSER UTILITIES DEMONSTRATION")
    print("=" * 65)

    sample_paragraph = (
        "Check documentation at https://docs.python.org/3/library/urllib.parse.html "
        "or visit http://admin:secret@192.168.1.100:8080/dashboard?user=root#overview for dev stats."
    )

    print("\n1. Extracted URLs:")
    extracted = extract_urls(sample_paragraph)
    for u in extracted:
        print(f"   -> {u}")

    print("\n2. URL Component Breakdown (Complex URL):")
    target_url = "https://admin:secret@api.service.co.uk:9000/v2/items?category=tech&page=1#results"
    comp = parse_url_components(target_url)
    print(f"   Raw URL      : {comp['raw_url']}")
    print(f"   Scheme       : {comp['scheme']} (HTTPS: {comp['is_secure']})")
    print(f"   Hostname     : {comp['hostname']} (Port: {comp['port']})")
    print(f"   Path         : {comp['path']}")
    print(f"   Query Params : {comp['query_params']}")
    print(f"   Fragment     : {comp['fragment']}")
    print(f"   User Info    : {comp['userinfo']}")

    print("\n3. URL Security Health Assessment:")
    insecure_url = "http://192.168.1.1/admin/../etc/passwd"
    sec = validate_url_security(insecure_url)
    print(f"   Target URL     : {insecure_url}")
    print(f"   Security Score : {sec['security_score']}/100")
    print(f"   Warnings       : {sec['warnings']}")

    print("\n4. Query Parameter Manipulator & Normalizer:")
    base_link = "https://example.com/products?category=shoes"
    updated_link = add_query_params(base_link, {"discount": "20%", "sort": "price"})
    print(f"   Original Link : {base_link}")
    print(f"   Updated Link  : {updated_link}")
    print(f"   Normalized    : {normalize_url('HTTPS://EXAMPLE.COM:443/products/')}")

    print("\n5. Domain & TLD Deconstruction:")
    domain_info = extract_domain_info("https://sub.blog.example.co.uk/article")
    print(f"   Hostname    : {domain_info['full_hostname']}")
    print(f"   Subdomain   : {domain_info['subdomain']}")
    print(f"   Root Domain : {domain_info['root_domain']}")
    print(f"   TLD         : {domain_info['tld']}")

    print("\n6. HTML Link Extraction & Redaction Masking:")
    html_markup = '<a href="/login">Login</a> <img src="https://cdn.example.com/banner.png">'
    html_links = extract_urls_from_html(html_markup, base_url="https://example.com")
    print(f"   Extracted HTML Links: {html_links}")
    print(f"   Redacted Paragraph  : '{mask_urls_in_text(sample_paragraph)}'")

    print("\n" + "=" * 65)
    print(" Running Unit Test Suite...")
    print("=" * 65)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)


if __name__ == "__main__":
    main()







