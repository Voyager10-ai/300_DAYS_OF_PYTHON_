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
    """
    Parse user input string into a list.
    Supports Python list literal notation (e.g. [1, 2, 2, 'a', 'a']) or comma-separated string.
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
    """Prompt user for input list and display deduplication operations."""
    print("\n   === Duplicate Removal Explorer ===")
    print("      Enter elements (e.g. 1, 2, 2, 3, 1, 4 or [1, 'a', 'A', 'a', 2])")
    lst = parse_input_list("      Enter list: ")

    if not lst:
        print("      ⚠️  List cannot be empty.")
        return

    print(f"\n      Input List ({len(lst)} items): {lst}")

    print("\n      Select Operation:")
    print("         1. Preserve-Order Deduplication")
    print("         2. In-Place Sorted Deduplication (Two-pointer)")
    print("         3. In-Place Unsorted Deduplication")
    print("         4. Case-Insensitive Key Deduplication (for strings)")
    print("         5. Frequency Threshold Deduplication (Max K occurrences)")
    print("         6. Nested List Deep Deduplication")
    print("         7. Run All & Visualize Duplicate Stream")

    choice = input("\n      Select option (1-7, default 7): ").strip()

    if choice == "1":
        res = remove_duplicates_preserve_order(lst)
        print(f"\n      👉 Order-Preserved Deduplicated List: {res}")
    elif choice == "2":
        lst_copy = sorted(lst, key=lambda x: str(x))
        res = remove_duplicates_in_place_sorted(lst_copy)
        print(f"\n      👉 In-Place Sorted Result: {res}")
    elif choice == "3":
        lst_copy = list(lst)
        res = remove_duplicates_in_place_unsorted(lst_copy)
        print(f"\n      👉 In-Place Unsorted Result: {res}")
    elif choice == "4":
        res = remove_duplicates_by_key(lst, key=lambda x: str(x).lower())
        print(f"\n      👉 Case-Insensitive Key Deduplicated Result: {res}")
    elif choice == "5":
        k_str = input("         Enter max occurrences allowed K (default 2): ").strip()
        k = int(k_str) if k_str.isdigit() else 2
        res = remove_duplicates_max_occurrences(lst, max_k=k)
        print(f"\n      👉 Max {k} Occurrences Result: {res}")
    elif choice == "6":
        res = remove_duplicates_nested(lst)
        print(f"\n      👉 Nested Deep Deduplication Result: {res}")
    else:
        res = remove_duplicates_preserve_order(lst)
        res_k2 = remove_duplicates_max_occurrences(lst, max_k=2)
        print("\n      --- Deduplication Analysis Results ---")
        print(f"      👉 Original Count:               {len(lst)}")
        print(f"      👉 Unique Count (Preserved Order): {len(res)}")
        print(f"      👉 Deduplicated Result List:      {res}")
        print(f"      👉 Bounded (Max 2 Occurrences):   {res_k2}")

        visualize_duplicate_removal(lst)


def show_mastery_box():
    """Print an artistic summary box."""
    pass


def main():
    """Entry point for the program."""
    pass


if __name__ == "__main__":
    main()
