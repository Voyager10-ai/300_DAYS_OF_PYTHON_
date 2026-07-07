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


# ---------- Character Analysis & Visualization ----------
def draw_freq_chart(input_string, max_bars=10, bar_length=20):
    """
    Generate and print an ASCII bar chart of character frequencies in the input string.
    Removes whitespaces for cleaner display.
    """
    if not input_string:
        print("      No text to analyze.")
        return
        
    filtered = [c for c in input_string if not c.isspace()]
    if not filtered:
        print("      Text contains only whitespace.")
        return
        
    counts = collections.Counter(filtered)
    total_non_space = len(filtered)
    most_common = counts.most_common(max_bars)
    
    print("\n   📊 Character Frequency Analysis (Excluding Spaces):")
    print("      " + "-" * 50)
    for char, count in most_common:
        # Format display for readability (like quotes for symbols/punctuation)
        display_char = f"'{char}'"
        pct = (count / total_non_space) * 100
        filled = int((count / total_non_space) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"      {display_char:<6} {bar} {count:>3} ({pct:.1f}%)")
    print("      " + "-" * 50)


# ---------- Interactive Flow Functions ----------
def interactive_join_flow():
    """Run the interactive flow for joining characters into a string."""
    print("\n   === Character Joining Explorer ===")
    print("      Enter characters/strings one by one. Leave blank when finished.")
    char_list = []
    while True:
        char = input(f"      Item {len(char_list) + 1}: ")
        if char == "":
            break
        char_list.append(char)
        
    if not char_list:
        print("      ⚠️  No items entered.")
        return
        
    print(f"\n      Entered items: {char_list}")
    sep = input("      Enter custom separator (default: empty): ")
    
    print("\n      Choose casing transformation:")
    print("         1. None")
    print("         2. Lowercase")
    print("         3. Uppercase")
    print("         4. Capitalize (first character only)")
    print("         5. Titlecase (first letter of each word)")
    print("         6. Swapcase (invert upper/lower)")
    case_choice = input("      Select casing option (1-6, default 1): ").strip()
    
    case_map = {"1": "none", "2": "lower", "3": "upper", "4": "capitalize", "5": "title", "6": "swap"}
    casing = case_map.get(case_choice, "none")
    
    result = join_characters(char_list, sep, casing)
    print("\n   ✨ Resulting String:")
    print(f"      👉 \"{result}\"")
    print(f"      - String Length: {len(result)}")


def interactive_split_flow():
    """Run the interactive flow for splitting a string into characters."""
    print("\n   === String Splitting Explorer ===")
    text = input("      Enter the string to split: ")
    if not text:
        print("      ⚠️  Input string cannot be empty.")
        return
        
    strip_sp = input("      Strip whitespace characters? (y/n, default n): ").strip().lower() == "y"
    uniq = input("      Keep unique characters only? (y/n, default n): ").strip().lower() == "y"
    
    print("\n      Choose sorting option:")
    print("         1. None (keep original order)")
    print("         2. Ascending order")
    print("         3. Descending order")
    print("         4. Sort by occurrence frequency")
    sort_choice = input("      Select option (1-4, default 1): ").strip()
    
    sort_map = {"1": "none", "2": "asc", "3": "desc", "4": "frequency"}
    sorting = sort_map.get(sort_choice, "none")
    
    result = split_string_to_characters(text, strip_sp, uniq, sorting)
    print("\n   ✨ Resulting Character List:")
    print(f"      👉 {result}")
    print(f"      - List Count: {len(result)}")
    
    draw_freq_chart(text)
