# Day 29: HTML Tag
#
# Problem:
#   Write a Python program to parse, manipulate, validate, sanitize, and visualize HTML tags and documents.
#   - Tag Wrapping & Generation: Wrap text in single/nested HTML tags, format self-closing tags.
#   - Tag Extraction & Parsing: Extract tag names, strip HTML tags to raw text, parse attributes.
#   - Structure Validation: Check balanced tag matching using stack data structures.
#   - DOM Object Model: Build HTMLNode hierarchy tree and render back to HTML string.
#   - Sanitization & Security: Clean forbidden tags/attributes (XSS mitigation) and escape entities.
#   - Analytics & Metrics: Count total/unique tags, nesting depth, text-to-tag ratio.
#   - AST Visualizer & Formatter: Render ASCII DOM tree diagrams and auto-format unindented HTML.
#   - Test Suite: Comprehensive unit tests and interactive CLI explorer.

import re
import html
from collections import Counter
from typing import Dict, List, Tuple, Optional, Set, Any, Union


def format_attributes(attributes: Optional[Dict[str, str]] = None) -> str:
    """
    Formats a dictionary of HTML attribute key-value pairs into a string space-separated representation.
    
    Args:
        attributes: Dictionary mapping attribute names to string values.
        
    Returns:
        Formatted attribute string starting with a space if non-empty, otherwise empty string.
        
    Example:
        format_attributes({"class": "btn", "id": "main"}) -> ' class="btn" id="main"'
    """
    if not attributes:
        return ""
    formatted_pairs = []
    for key, val in attributes.items():
        escaped_val = html.escape(str(val), quote=True)
        formatted_pairs.append(f'{key}="{escaped_val}"')
    return " " + " ".join(formatted_pairs)


def add_html_tag(tag: str, content: str = "", attributes: Optional[Dict[str, str]] = None) -> str:
    """
    Wraps text content inside an HTML opening and closing tag with optional attributes.
    
    Args:
        tag: HTML tag name (e.g., 'p', 'h1', 'div').
        content: Text or HTML content inside the tag.
        attributes: Optional dictionary of attributes.
        
    Returns:
        Formatted HTML string.
        
    Example:
        add_html_tag('i', 'Python') -> '<i>Python</i>'
        add_html_tag('a', 'Click Here', {'href': 'https://python.org'}) -> '<a href="https://python.org">Click Here</a>'
    """
    clean_tag = tag.strip().lower().lstrip('<').rstrip('>').split()[0]
    attrs_str = format_attributes(attributes)
    return f"<{clean_tag}{attrs_str}>{content}</{clean_tag}>"


def wrap_html_tags(tags: List[Union[str, Tuple[str, Dict[str, str]]]], content: str) -> str:
    """
    Wraps content in multiple nested HTML tags applied in sequential order.
    
    Args:
        tags: List of tag names or tuples of (tag_name, attributes_dict).
        content: Inner text content to wrap.
        
    Returns:
        Nested HTML tag string.
        
    Example:
        wrap_html_tags(['b', 'i'], 'Hello') -> '<b><i>Hello</i></b>'
    """
    result = content
    for item in reversed(tags):
        if isinstance(item, tuple):
            tag_name, attrs = item
            result = add_html_tag(tag_name, result, attrs)
        else:
            result = add_html_tag(item, result)
    return result


def create_self_closing_tag(tag: str, attributes: Optional[Dict[str, str]] = None) -> str:
    """
    Creates a self-closing (void) HTML tag string.
    
    Args:
        tag: Void tag name (e.g. 'img', 'br', 'hr', 'input').
        attributes: Optional attribute key-value pairs.
        
    Returns:
        Self-closing HTML tag string.
        
    Example:
        create_self_closing_tag('img', {'src': 'pic.jpg', 'alt': 'Photo'}) -> '<img src="pic.jpg" alt="Photo" />'
    """
    clean_tag = tag.strip().lower().lstrip('<').rstrip('>').split()[0]
    attrs_str = format_attributes(attributes)
    return f"<{clean_tag}{attrs_str} />"


