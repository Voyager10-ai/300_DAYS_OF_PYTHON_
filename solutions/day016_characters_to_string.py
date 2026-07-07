# Day 16: Characters to String
#
# Problem:
#   Write a Python program that converts a list of characters into a single string,
#   and splits strings back into lists of characters with various processing filters.
#   - Convert a list/array of individual characters into a string.
#   - Support custom separators between characters (e.g. empty, space, hyphen, comma).
#   - Support character casing transformations during the joining process.
#   - Support the inverse operation: splitting a string back into character lists.
#   - Provide options to deduplicate, strip whitespace, or sort the character lists.
#   - Render a custom character distribution frequency ASCII chart.
#   - Provide an interactive terminal menu explorer.
#
# This exercise covers list manipulation, string joining, list comprehension,
# dictionary counting, custom sorting, and CLI dashboard construction.

import collections
import string


# ---------- Core Character-to-String Joining ----------
def join_characters(char_list, separator="", casing="none"):
    """
    Join a list of characters/strings using the specified separator
    and apply the chosen casing transformation.
    """
    if not char_list:
        return ""
        
    # Convert all items to string representations just in case
    str_list = [str(item) for item in char_list]
    joined = separator.join(str_list)
    
    if casing == "lower":
        return joined.lower()
    elif casing == "upper":
        return joined.upper()
    elif casing == "capitalize":
        return joined.capitalize()
    elif casing == "title":
        return joined.title()
    elif casing == "swap":
        return joined.swapcase()
    else:
        return joined


# ---------- Core String-to-Characters Splitting ----------
def split_string_to_characters(input_string, strip_spaces=False, unique=False, sort_list="none"):
    """
    Split a string back into a list of characters with optional filtering
    for unique characters, whitespace trimming, and sorting.
    """
    if not input_string:
        return []
        
    chars = list(input_string)
    
    if strip_spaces:
        chars = [c for c in chars if not c.isspace()]
        
    if unique:
        # Preserve insertion order for unique characters
        seen = set()
        unique_chars = []
        for c in chars:
            if c not in seen:
                seen.add(c)
                unique_chars.append(c)
        chars = unique_chars
        
    if sort_list == "asc":
        chars.sort()
    elif sort_list == "desc":
        chars.sort(reverse=True)
    elif sort_list == "frequency":
        counts = collections.Counter(chars)
        # Sort by frequency descending, then alphabetically ascending
        chars.sort(key=lambda x: (-counts[x], x))
        
    return chars
