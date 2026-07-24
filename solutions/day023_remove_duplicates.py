# Day 23: Remove Duplicates
#
# Problem:
#   Write a Python program to remove duplicate elements from lists and complex data structures.
#   - Remove duplicates while preserving original element insertion order.
#   - Perform in-place deduplication for sorted arrays (two-pointer technique, O(1) space).
#   - Perform in-place deduplication for unsorted arrays.
#   - Deduplicate elements based on a custom key function (e.g., case-insensitive, field selection).
#   - Bounded frequency deduplication (allow up to K occurrences of each element).
#   - Perform deep deduplication on arbitrarily nested lists/structures.
#   - Render an ASCII duplicate removal visualizer with detailed reduction metrics.
#   - Provide an interactive CLI explorer with built-in test suites.
#
# This exercise covers list manipulation, set/dict lookups, two-pointer approach,
# higher-order key functions, recursive structure handling, ASCII visualization, and CLI interactions.

import ast
from collections import Counter


def remove_duplicates_preserve_order(lst):
    """
    Remove duplicate elements while preserving original insertion order.
    Handles hashable and unhashable elements gracefully.
    Returns a new list with unique elements in first-seen order.
    """
    seen = set()
    seen_unhashable = []
    result = []

    for item in lst:
        try:
            if item not in seen:
                seen.add(item)
                result.append(item)
        except TypeError:
            # Fallback for unhashable types (lists, dicts, etc.)
            if item not in seen_unhashable:
                seen_unhashable.append(item)
                result.append(item)

    return result


def remove_duplicates_in_place_sorted(lst):
    """
    Remove duplicates in-place from a sorted list using the two-pointer technique.
    Modifies the list in-place and truncates it to unique elements.
    Returns the modified list.
    """
    if not lst:
        return lst

    write_idx = 1
    for read_idx in range(1, len(lst)):
        if lst[read_idx] != lst[read_idx - 1]:
            lst[write_idx] = lst[read_idx]
            write_idx += 1

    del lst[write_idx:]
    return lst


def remove_duplicates_in_place_unsorted(lst):
    """
    Remove duplicates in-place from an unsorted list while preserving order.
    Modifies the list in-place and returns it.
    """
    seen = set()
    write_idx = 0

    for read_idx in range(len(lst)):
        item = lst[read_idx]
        try:
            if item not in seen:
                seen.add(item)
                lst[write_idx] = item
                write_idx += 1
        except TypeError:
            # Fallback for unhashable items
            if item not in lst[:write_idx]:
                lst[write_idx] = item
                write_idx += 1

    del lst[write_idx:]
    return lst


def remove_duplicates_by_key(lst, key=None):
    """
    Remove duplicates based on a custom key function (e.g. key=str.lower, key=lambda x: x['id']).
    If key is None, behaves like standard preserve-order deduplication.
    Returns a new list with unique items according to the key.
    """
    if key is None:
        key = lambda x: x

    seen_keys = set()
    seen_unhashable_keys = []
    result = []

    for item in lst:
        k = key(item)
        try:
            if k not in seen_keys:
                seen_keys.add(k)
                result.append(item)
        except TypeError:
            if k not in seen_unhashable_keys:
                seen_unhashable_keys.append(k)
                result.append(item)

    return result


def remove_duplicates_max_occurrences(lst, max_k=1):
    """
    Filter list to allow at most `max_k` occurrences of each element while preserving order.
    Returns a new list containing up to max_k copies of each distinct element.
    """
    if max_k <= 0:
        return []

    counts = {}
    result = []

    for item in lst:
        try:
            current = counts.get(item, 0)
            if current < max_k:
                counts[item] = current + 1
                result.append(item)
        except TypeError:
            # Fallback for unhashable elements
            unhashable_count = sum(1 for x in result if x == item)
            if unhashable_count < max_k:
                result.append(item)

    return result


def remove_duplicates_nested(lst):
    """
    Recursively process nested lists, tuples, and sets to remove duplicate items at every level
    while preserving structure and first-seen element ordering.
    """
    if not isinstance(lst, (list, tuple, set)):
        return lst

    processed_elements = []
    for item in lst:
        if isinstance(item, (list, tuple, set)):
            processed_elements.append(remove_duplicates_nested(item))
        else:
            processed_elements.append(item)

    # Now deduplicate the current level
    result = remove_duplicates_preserve_order(processed_elements)

    if isinstance(lst, tuple):
        return tuple(result)
    elif isinstance(lst, set):
        return set(result)
    return result


def visualize_duplicate_removal(lst):
    """
    Render ASCII visualization showing original vs deduplicated list, element status,
    and reduction statistics.
    """
    print("\n   📊 Duplicate Removal Analysis & Visualization:")
    print("   " + "─" * 58)

    if not lst:
        print("      (Empty list provided)")
        print("   " + "─" * 58)
        return

    dedup = remove_duplicates_preserve_order(lst)
    orig_len = len(lst)
    dedup_len = len(dedup)
    removed_count = orig_len - dedup_len
    reduction_pct = (removed_count / orig_len * 100) if orig_len > 0 else 0.0

    print(f"   Original List  ({orig_len:2d} items): {lst}")
    print(f"   Unique List    ({dedup_len:2d} items): {dedup}")
    print("   " + "─" * 58)

    # Element tracking
    seen = set()
    tracking_str = []
    for item in lst:
        try:
            if item in seen:
                tracking_str.append(f"❌[{item}]")
            else:
                seen.add(item)
                tracking_str.append(f"✅[{item}]")
        except TypeError:
            tracking_str.append(f"?[{item}]")

    print("   Element Stream (✅ = Keep / ❌ = Duplicate Removed):")
    print("      " + " → ".join(tracking_str))

    # Metrics summary
    print("\n   📈 Metrics:")
    orig_bar = "█" * min(30, orig_len)
    dedup_bar = "█" * min(30, dedup_len)

    print(f"      Original Count : {orig_bar:<30} {orig_len}")
    print(f"      Unique Count   : {dedup_bar:<30} {dedup_len}")
    print(f"      Duplicates Off : {removed_count} item(s) removed ({reduction_pct:.1f}% reduction)")
    print("   " + "─" * 58)


def parse_input_list(prompt_text):
    """Parse user input string into a list."""
    pass


def interactive_explorer():
    """Prompt user for input and display deduplication analysis results."""
    pass


def show_mastery_box():
    """Print an artistic summary box."""
    pass


def main():
    """Entry point for the program."""
    pass


if __name__ == "__main__":
    main()
