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


def extract_html_tags(html_str: str) -> List[str]:
    """
    Extracts all tag names present in an HTML string in order of appearance.
    
    Args:
        html_str: HTML content string.
        
    Returns:
        List of lowercase tag names.
        
    Example:
        extract_html_tags('<div><h1>Title</h1><p>Text</p></div>') -> ['div', 'h1', 'h1', 'p', 'p', 'div']
    """
    tag_pattern = r'</?\s*([a-zA-Z0-9]+)[^>]*>'
    return [match.group(1).lower() for match in re.finditer(tag_pattern, html_str)]


def strip_html_tags(html_str: str) -> str:
    """
    Strips all HTML markup tags from a string, returning clean inner text content.
    
    Args:
        html_str: HTML content containing markup tags.
        
    Returns:
        Clean plain text with tags removed.
        
    Example:
        strip_html_tags('<p>Hello <b>World</b>!</p>') -> 'Hello World!'
    """
    clean_text = re.sub(r'<[^>]+>', '', html_str)
    return html.unescape(clean_text)


def parse_tag_attributes(tag_str: str) -> Dict[str, str]:
    """
    Parses key-value attribute pairs from an HTML opening tag string or full tag.
    
    Args:
        tag_str: Opening HTML tag string (e.g., '<a href="https://example.com" class="link">').
        
    Returns:
        Dictionary mapping attribute names to string values.
        
    Example:
        parse_tag_attributes('<img src="test.jpg" alt="Test Image" width="100">') 
        -> {'src': 'test.jpg', 'alt': 'Test Image', 'width': '100'}
    """
    tag_str = tag_str.strip()
    match = re.search(r'<([a-zA-Z0-9]+)([^>]*)>', tag_str)
    if not match:
        return {}
    
    attrs_raw = match.group(2)
    attr_pattern = r'([a-zA-Z0-9_-]+)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+)))?'
    
    attributes = {}
    for attr_match in re.finditer(attr_pattern, attrs_raw):
        attr_name = attr_match.group(1).lower()
        val = attr_match.group(2) or attr_match.group(3) or attr_match.group(4) or ""
        attributes[attr_name] = html.unescape(val)
        
    return attributes


def find_tags_by_name(html_str: str, tag_name: str) -> List[Dict[str, Any]]:
    """
    Finds all occurrences of a specified tag and returns a list of details including content and attributes.
    
    Args:
        html_str: HTML document string.
        tag_name: Target tag name to search (case-insensitive).
        
    Returns:
        List of dictionaries containing 'tag', 'attributes', 'inner_content', and 'full_match'.
    """
    target = tag_name.lower().strip()
    pattern = rf'<{target}([^>]*)>(.*?)</{target}>'
    matches = []
    
    for m in re.finditer(pattern, html_str, re.IGNORECASE | re.DOTALL):
        attrs_str = m.group(1)
        full_opening = f"<{target}{attrs_str}>"
        attrs = parse_tag_attributes(full_opening)
        content = m.group(2)
        matches.append({
            "tag": target,
            "attributes": attrs,
            "inner_content": content,
            "full_match": m.group(0)
        })
        
    return matches

HTML_VOID_TAGS: Set[str] = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr"
}

HTML_INLINE_TAGS: Set[str] = {
    "a", "b", "i", "em", "strong", "span", "code", "small", "sub",
    "sup", "mark", "ins", "del", "abbr", "label", "button", "input"
}

HTML_BLOCK_TAGS: Set[str] = {
    "div", "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li",
    "table", "tr", "td", "th", "form", "header", "footer", "section",
    "article", "nav", "aside", "main", "blockquote", "pre", "body", "html"
}


def is_valid_tag_name(tag_name: str) -> bool:
    """
    Checks if a tag name string is a syntactically valid HTML tag identifier.
    
    Args:
        tag_name: Tag name string.
        
    Returns:
        Boolean indicating validity.
    """
    if not tag_name or not isinstance(tag_name, str):
        return False
    clean = tag_name.strip().lower()
    return bool(re.match(r'^[a-z][a-z0-9-]*$', clean))


def get_tag_category(tag_name: str) -> str:
    """
    Determines the category type of an HTML tag.
    
    Returns one of: 'void', 'inline', 'block', or 'other'.
    """
    tag = tag_name.lower().strip()
    if tag in HTML_VOID_TAGS:
        return "void"
    if tag in HTML_INLINE_TAGS:
        return "inline"
    if tag in HTML_BLOCK_TAGS:
        return "block"
    return "other"


def validate_html_structure(html_str: str) -> Dict[str, Any]:
    """
    Validates whether an HTML string has balanced and properly matched opening/closing tags.
    
    Args:
        html_str: HTML content string to validate.
        
    Returns:
        Dictionary containing:
        - 'is_valid': bool indicating if HTML is properly balanced
        - 'errors': list of error message strings if invalid
        - 'max_depth': integer representing maximum tag nesting depth reached
        
    Example:
        validate_html_structure('<div><p>Ok</p></div>') -> {'is_valid': True, 'errors': [], 'max_depth': 2}
        validate_html_structure('<div><p>Error</div>') -> {'is_valid': False, 'errors': [...], 'max_depth': 2}
    """
    tag_regex = r'<(/?)s*([a-zA-Z0-9-]+)([^>]*)>'
    stack: List[Tuple[str, int]] = []
    errors: List[str] = []
    max_depth = 0
    
    # Clean out comments and doctype
    cleaned_html = re.sub(r'<!--.*?-->', '', html_str, flags=re.DOTALL)
    cleaned_html = re.sub(r'<!DOCTYPE[^>]*>', '', cleaned_html, flags=re.IGNORECASE)
    
    for match in re.finditer(tag_regex, cleaned_html):
        is_closing = bool(match.group(1))
        tag_name = match.group(2).lower()
        attributes_raw = match.group(3)
        
        # Check if self-closing tag indicated by trailing slash (e.g. <br/> or <div />)
        is_self_closing = attributes_raw.strip().endswith('/') or tag_name in HTML_VOID_TAGS
        
        if is_self_closing:
            continue
            
        if not is_closing:
            stack.append((tag_name, match.start()))
            if len(stack) > max_depth:
                max_depth = len(stack)
        else:
            if not stack:
                errors.append(f"Unexpected closing tag </{tag_name}> at index {match.start()} with no matching opening tag.")
            elif stack[-1][0] != tag_name:
                expected_tag, expected_idx = stack[-1]
                errors.append(
                    f"Mismatched closing tag </{tag_name}> at index {match.start()}. "
                    f"Expected closing tag </{expected_tag}> for opening tag at index {expected_idx}."
                )
                # Pop matching tag if found higher up in stack
                stack_tags = [t[0] for t in stack]
                if tag_name in stack_tags:
                    while stack and stack[-1][0] != tag_name:
                        stack.pop()
                    if stack:
                        stack.pop()
            else:
                stack.pop()
                
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "max_depth": max_depth
    }


class HTMLNode:
    """
    Represents an HTML DOM Element node with tag, text, attributes, and child nodes.
    """
    def __init__(
        self,
        tag: str = "root",
        text: str = "",
        attributes: Optional[Dict[str, str]] = None,
        children: Optional[List['HTMLNode']] = None
    ):
        self.tag = tag.strip().lower()
        self.text = text
        self.attributes = attributes or {}
        self.children = children or []

    def add_child(self, child: 'HTMLNode') -> 'HTMLNode':
        """Appends a child HTMLNode."""
        self.children.append(child)
        return child

    def to_html(self) -> str:
        """Serializes the HTMLNode tree back to an HTML string."""
        if self.tag == "root":
            inner = "".join(child.to_html() for child in self.children)
            return f"{self.text}{inner}"
            
        attrs_str = format_attributes(self.attributes)
        if self.tag in HTML_VOID_TAGS:
            return f"<{self.tag}{attrs_str} />"
            
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{attrs_str}>{self.text}{children_html}</{self.tag}>"

    def find(self, tag_name: str) -> Optional['HTMLNode']:
        """Finds first child/descendant node matching given tag_name."""
        target = tag_name.lower()
        if self.tag == target:
            return self
        for child in self.children:
            found = child.find(target)
            if found:
                return found
        return None

    def find_all(self, tag_name: str) -> List['HTMLNode']:
        """Finds all child/descendant nodes matching given tag_name."""
        target = tag_name.lower()
        results = []
        if self.tag == target:
            results.append(self)
        for child in self.children:
            results.extend(child.find_all(target))
        return results

    def __repr__(self) -> str:
        return f"<HTMLNode <{self.tag}> children={len(self.children)} text='{self.text[:15]}'>"


def parse_html_to_dom(html_str: str) -> HTMLNode:
    """
    Parses a simple HTML snippet into a hierarchical DOM tree of HTMLNode instances.
    
    Args:
        html_str: Input HTML markup string.
        
    Returns:
        Root HTMLNode containing document tree.
    """
    root = HTMLNode(tag="root")
    stack: List[HTMLNode] = [root]
    
    # Tokenize tags and text
    token_pattern = r'(<!--.*?-->|<[^>]+>|[^<]+)'
    tokens = [t for t in re.findall(token_pattern, html_str, re.DOTALL) if t.strip()]
    
    tag_regex = r'^<(/?)s*([a-zA-Z0-9-]+)([^>]*)>$'
    
    for token in tokens:
        if token.startswith('<!--') or token.startswith('<!DOCTYPE'):
            continue
            
        tag_match = re.match(tag_regex, token)
        if tag_match:
            is_closing = bool(tag_match.group(1))
            tag_name = tag_match.group(2).lower()
            attrs_raw = tag_match.group(3)
            
            is_void = tag_name in HTML_VOID_TAGS or attrs_raw.strip().endswith('/')
            
            if is_closing:
                if len(stack) > 1 and stack[-1].tag == tag_name:
                    stack.pop()
            else:
                attrs = parse_tag_attributes(token)
                node = HTMLNode(tag=tag_name, attributes=attrs)
                stack[-1].add_child(node)
                if not is_void:
                    stack.append(node)
        else:
            # Text content
            cleaned_text = html.unescape(token.strip())
            if cleaned_text:
                if len(stack) > 1:
                    stack[-1].text += ( " " + cleaned_text if stack[-1].text else cleaned_text )
                else:
                    root.add_child(HTMLNode(tag="text", text=cleaned_text))
                    
    return root


def escape_html_entities(text: str) -> str:
    """
    Escapes special HTML characters (&, <, >, ", ') into corresponding HTML entities.
    
    Args:
        text: Plain text string.
        
    Returns:
        HTML entity escaped string.
        
    Example:
        escape_html_entities('1 < 2 & "quote"') -> '1 &lt; 2 &amp; &quot;quote&quot;'
    """
    return html.escape(text, quote=True)


def unescape_html_entities(text: str) -> str:
    """
    Converts HTML entity references back to standard plain text characters.
    
    Args:
        text: HTML entity string.
        
    Returns:
        Decoded plain text string.
        
    Example:
        unescape_html_entities('1 &lt; 2') -> '1 < 2'
    """
    return html.unescape(text)


def sanitize_html(
    html_str: str,
    allowed_tags: Optional[Set[str]] = None,
    allowed_attributes: Optional[Set[str]] = None
) -> str:
    """
    Sanitizes HTML string by removing disallowed/dangerous tags (e.g., <script>, <iframe>)
    and dangerous event handler attributes (e.g., onclick=, onload=) to prevent XSS attacks.
    
    Args:
        html_str: Raw un-sanitized HTML string.
        allowed_tags: Optional set of allowed tag names. Defaults to safe semantic HTML tags.
        allowed_attributes: Optional set of allowed attribute names. Defaults to standard safe attributes.
        
    Returns:
        Sanitized safe HTML string.
    """
    if allowed_tags is None:
        allowed_tags = {
            "p", "b", "i", "em", "strong", "a", "span", "div", "h1", "h2", "h3",
            "h4", "h5", "h6", "ul", "ol", "li", "br", "hr", "img", "code", "pre"
        }
        
    if allowed_attributes is None:
        allowed_attributes = {"href", "src", "alt", "title", "class", "id", "width", "height"}

    # Remove script and style blocks entirely
    cleaned = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html_str, flags=re.IGNORECASE | re.DOTALL)
    
    def replace_tag(match: re.Match) -> str:
        is_closing = bool(match.group(1))
        tag_name = match.group(2).lower()
        raw_attrs = match.group(3)
        
        if tag_name not in allowed_tags:
            return ""
            
        if is_closing:
            return f"</{tag_name}>"
            
        # Parse attributes and filter
        parsed_attrs = parse_tag_attributes(match.group(0))
        safe_attrs = {}
        for attr, val in parsed_attrs.items():
            if attr.lower() in allowed_attributes and not attr.lower().startswith('on'):
                # Block javascript: URLs
                if attr.lower() in ('href', 'src') and val.strip().lower().startswith('javascript:'):
                    continue
                safe_attrs[attr] = val
                
        is_self_closing = raw_attrs.strip().endswith('/') or tag_name in HTML_VOID_TAGS
        if is_self_closing:
            return create_self_closing_tag(tag_name, safe_attrs)
        else:
            attrs_str = format_attributes(safe_attrs)
            return f"<{tag_name}{attrs_str}>"
            
    tag_regex = r'<(/?)s*([a-zA-Z0-9-]+)([^>]*)>'
    return re.sub(tag_regex, replace_tag, cleaned)


def get_html_stats(html_str: str) -> Dict[str, Any]:
    """
    Analyzes an HTML string and compiles a comprehensive statistical report.
    
    Args:
        html_str: HTML document string.
        
    Returns:
        Dictionary containing counts, ratios, unique tags, frequencies, and structure metrics.
    """
    total_len = len(html_str)
    plain_text = strip_html_tags(html_str)
    text_len = len(plain_text)
    
    all_tags = extract_html_tags(html_str)
    tag_freq = dict(Counter(all_tags))
    unique_tags = len(tag_freq)
    total_tags = len(all_tags)
    
    void_count = sum(count for tag, count in tag_freq.items() if tag in HTML_VOID_TAGS)
    validation = validate_html_structure(html_str)
    
    text_ratio = round((text_len / total_len * 100), 2) if total_len > 0 else 0.0
    
    return {
        "total_length": total_len,
        "text_length": text_len,
        "text_ratio_percent": text_ratio,
        "total_tags_count": total_tags,
        "unique_tags_count": unique_tags,
        "void_tags_count": void_count,
        "tag_frequency": tag_freq,
        "is_valid_structure": validation["is_valid"],
        "max_nesting_depth": validation["max_depth"],
        "validation_errors": validation["errors"]
    }



