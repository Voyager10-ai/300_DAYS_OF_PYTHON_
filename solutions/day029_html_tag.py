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

