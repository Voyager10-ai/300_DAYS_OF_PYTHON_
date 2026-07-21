# Day 21: Frequency of Elements
#
# Problem:
#   Write a Python program that counts and analyzes element frequencies in lists and nested structures.
#   - Count element frequencies using standard dictionaries (manual count loop).
#   - Count element frequencies using collections.Counter.
#   - Count frequencies in arbitrarily nested lists/iterables (flattening/recursive traversal).
#   - Find top K most frequent and least frequent elements.
#   - Group elements by their frequency counts (inverted index mapping).
#   - Render a custom ASCII bar chart / histogram visualizing frequencies and relative percentages.
#   - Provide an interactive CLI explorer with built-in test suites.
#
# This exercise covers dictionary manipulation, collections module, recursion, data aggregation,
# histogram visualization, and CLI interactions.

import ast
from collections import Counter


# ---------- Core Frequency Algorithms ----------
def count_frequencies_dict(lst):
    """
    Count element frequencies using a standard Python dictionary loop.
    Returns a dictionary mapping elements to their count.
    """
    freq = {}
    for item in lst:
        freq[item] = freq.get(item, 0) + 1
    return freq


def count_frequencies_counter(lst):
    """
    Count element frequencies using collections.Counter.
    Returns a dictionary mapping elements to their count.
    """
    return dict(Counter(lst))


def count_frequencies_nested(lst):
    """
    Count element frequencies in an arbitrarily nested list/iterable structure.
    Traverses lists, tuples, sets recursively.
    """
    freq = {}

    def traverse(item):
        if isinstance(item, (list, tuple, set)):
            for sub in item:
                traverse(sub)
        else:
            freq[item] = freq.get(item, 0) + 1

    traverse(lst)
    return freq


# ---------- Frequency Analysis & Grouping ----------
def get_most_frequent(lst_or_freq, k=1):
    """
    Get the top K most frequent elements.
    Accepts either a list/nested structure or a frequency dictionary.
    Returns a list of tuples (element, count) sorted by count descending.
    """
    if isinstance(lst_or_freq, dict):
        freq_dict = lst_or_freq
    else:
        freq_dict = count_frequencies_nested(lst_or_freq)

    if not freq_dict or k <= 0:
        return []

    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:k]


def get_least_frequent(lst_or_freq, k=1):
    """
    Get the top K least frequent elements.
    Accepts either a list/nested structure or a frequency dictionary.
    Returns a list of tuples (element, count) sorted by count ascending.
    """
    if isinstance(lst_or_freq, dict):
        freq_dict = lst_or_freq
    else:
        freq_dict = count_frequencies_nested(lst_or_freq)

    if not freq_dict or k <= 0:
        return []

    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1])
    return sorted_items[:k]


def group_by_frequency(lst_or_freq):
    """
    Group elements by their frequency of occurrence.
    Returns a dictionary mapping frequency count -> list of elements with that count.
    """
    if isinstance(lst_or_freq, dict):
        freq_dict = lst_or_freq
    else:
        freq_dict = count_frequencies_nested(lst_or_freq)

    grouped = {}
    for elem, count in freq_dict.items():
        if count not in grouped:
            grouped[count] = []
        grouped[count].append(elem)
    return grouped


# ---------- ASCII Visualization ----------
def draw_frequency_histogram(lst_or_freq):
    """
    Draw an ASCII histogram representing frequency of elements.
    Highlights most frequent element(s) with 👑 [MODE].
    """
    if isinstance(lst_or_freq, dict):
        freq = lst_or_freq
    else:
        freq = count_frequencies_nested(lst_or_freq)

    if not freq:
        print("      ⚠️  No elements to visualize.")
        return

    total_count = sum(freq.values())
    max_count = max(freq.values())
    max_bar_width = 30

    print("\n   📊 Element Frequency Histogram:")
    print("   " + "─" * 58)

    # Sort by frequency descending, then element key ascending for display
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], str(x[0])))

    for item, count in sorted_items:
        bar_len = int((count / max_count) * max_bar_width) if max_count > 0 else 0
        bar_str = "█" * max(bar_len, 1)
        pct = (count / total_count) * 100

        is_mode = (count == max_count and max_count > 1)
        marker = " 👑 [MODE]" if is_mode else ""

        item_repr = f"'{item}'" if isinstance(item, str) else str(item)
        print(f"      {item_repr: >12} | {bar_str:<{max_bar_width}} {count: >3}x ({pct:5.1f}%){marker}")

    print("   " + "─" * 58)


# ---------- Interactive CLI Features ----------
def parse_element_input(prompt_text):
    """
    Parse user input string.
    Supports Python list literal syntax (e.g., [1, 'a', [2, 1]]) or comma-separated values.
    """
    raw = input(prompt_text).strip()
    if not raw:
        return []
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return parsed
        return [parsed]
    except (ValueError, SyntaxError):
        items = [item.strip() for item in raw.split(",") if item.strip()]
        converted = []
        for item in items:
            try:
                converted.append(int(item))
            except ValueError:
                try:
                    converted.append(float(item))
                except ValueError:
                    converted.append(item)
        return converted


def interactive_explorer():
    """Prompt user for input and display frequency analysis results."""
    print("\n   === Element Frequency Explorer ===")
    print("      Enter a list (e.g. 1, 2, 2, 3, a, b, a) or nested list (e.g. [1, [2, 'a'], 'a', 2])")
    lst = parse_element_input("      Enter elements: ")

    if not lst:
        print("      ⚠️  List cannot be empty.")
        return

    print(f"\n      Input List: {lst}")
    is_nested = any(isinstance(x, (list, tuple, set)) for x in lst)

    print("\n      Select Operation:")
    print("         1. Standard Dictionary Frequency")
    print("         2. Collections.Counter Frequency")
    print("         3. Nested List Frequency Analysis")
    print("         4. Top K Most & Least Frequent Elements")
    print("         5. Group Elements by Frequency")
    print("         6. Run All Analyses & ASCII Histogram")

    choice = input("\n      Select option (1-6, default 6): ").strip()

    if choice == "1":
        if is_nested:
            print("      ⚠️  Standard dict requires flat elements. Using nested frequency algorithm.")
            freq = count_frequencies_nested(lst)
        else:
            freq = count_frequencies_dict(lst)
        print(f"\n      👉 Frequency Dict: {freq}")
    elif choice == "2":
        if is_nested:
            print("      ⚠️  Counter requires flat hashable elements. Using nested frequency algorithm.")
            freq = count_frequencies_nested(lst)
        else:
            freq = count_frequencies_counter(lst)
        print(f"\n      👉 Counter Result: {freq}")
    elif choice == "3":
        freq = count_frequencies_nested(lst)
        print(f"\n      👉 Nested Frequency Dict: {freq}")
    elif choice == "4":
        freq = count_frequencies_nested(lst)
        k_str = input("         Enter K value (default 2): ").strip()
        k = int(k_str) if k_str.isdigit() else 2
        most = get_most_frequent(freq, k)
        least = get_least_frequent(freq, k)
        print(f"\n      👉 Top {k} Most Frequent:  {most}")
        print(f"      👉 Top {k} Least Frequent: {least}")
    elif choice == "5":
        freq = count_frequencies_nested(lst)
        grouped = group_by_frequency(freq)
        print(f"\n      👉 Grouped by Frequency: {grouped}")
    else:
        freq = count_frequencies_nested(lst)
        print("\n      --- Frequency Analysis Results ---")
        print(f"      👉 Frequency Dictionary: {freq}")
        print(f"      👉 Most Frequent (Mode): {get_most_frequent(freq, 1)}")
        print(f"      👉 Least Frequent:       {get_least_frequent(freq, 1)}")
        print(f"      👉 Grouped by Frequency: {group_by_frequency(freq)}")
        draw_frequency_histogram(freq)
