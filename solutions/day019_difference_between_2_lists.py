# Day 19: Difference Between 2 Lists
#
# Problem:
#   Write a Python program that finds the differences between two lists.
#   - Find relative difference (elements in A but not in B: Set Difference, i.e., A - B).
#   - Find symmetric difference (elements in A or B but not both: i.e., A ^ B).
#   - Find relative difference preserving order of A (elements of A not in B, preserving duplicate occurrences and original order in A).
#   - Find multiset difference (elements of A not in B, accounting for frequency: e.g., if 'x' is 3 times in A and 1 time in B, it remains 2 times in the result: Counter(A) - Counter(B)).
#   - Render a custom ASCII diagram/visualization representing the difference.
#   - Provide an interactive terminal exploration tool.
#
# This exercise covers lists, sets, collections.Counter, mathematical set theory,
# alignment-based ASCII rendering, and CLI input parsing.

import collections


# ---------- Core List Difference Algorithms ----------
def find_unique_difference(list_a, list_b):
    """
    Find unique elements in list_a that are not in list_b (Set Difference A - B).
    Returns a sorted list of unique elements.
    """
    set_a = set(list_a)
    set_b = set(list_b)
    return sorted(list(set_a - set_b), key=lambda x: str(x))


def find_symmetric_difference(list_a, list_b):
    """
    Find unique elements that are in either list_a or list_b but not both (A ^ B).
    Returns a sorted list of unique elements.
    """
    set_a = set(list_a)
    set_b = set(list_b)
    return sorted(list(set_a ^ set_b), key=lambda x: str(x))


def find_ordered_difference(list_a, list_b):
    """
    Find elements in list_a that are not in list_b, preserving the original order
    and keeping any duplicates present in list_a (as long as they are not in list_b).
    """
    set_b = set(list_b)
    return [item for item in list_a if item not in set_b]


def find_multiset_difference(list_a, list_b):
    """
    Find elements of list_a after subtracting frequency of occurrences in list_b.
    E.g. If 'x' appears 3 times in list_a and 1 time in list_b, it will appear
    2 times in the output.
    """
    count_a = collections.Counter(list_a)
    count_b = collections.Counter(list_b)
    diff = count_a - count_b
    return list(diff.elements())


# ---------- ASCII Visualization ----------
def draw_difference_visualization(list_a, list_b):
    """Draw an ASCII representation showing relative difference and symmetric difference."""
    set_a = set(list_a)
    set_b = set(list_b)
    
    only_a = set_a - set_b
    only_b = set_b - set_a
    common = set_a.intersection(set_b)
    
    print("\n   📊 Set Difference & Overlap Diagram:")
    print(f"      List A (Unique: {len(set_a)})         List B (Unique: {len(set_b)})")
    print("       ┌───────────┐            ┌───────────┐")
    print("       │           │            │           │")
    print(f"       │  Only A   │            │  Only B   │")
    print(f"       │    ({len(only_a):<2})    │            │    ({len(only_b):<2})    │")
    print("       │           │            │           │")
    print("       └─────┬─────┘            └─────┬─────┘")
    print("             │                        │")
    print("             │      ┌───────────┐     │")
    print("             │      │  Common   │     │")
    print(f"             └─────►│    ({len(common):<2})    │◄────┘")
    print("                    │           │")
    print("                    └───────────┘")
    print(f"\n      👉 Relative Difference (A - B):  {sorted(list(only_a), key=lambda x: str(x))}")
    print(f"      👉 Relative Difference (B - A):  {sorted(list(only_b), key=lambda x: str(x))}")
    print(f"      👉 Symmetric Difference (A ^ B): {sorted(list(only_a ^ only_b), key=lambda x: str(x))}")


# ---------- Interactive Features ----------
def parse_list_input(prompt_text):
    """Helper to parse comma-separated string/numeric inputs into a list."""
    raw = input(prompt_text).strip()
    if not raw:
        return []
    items = [item.strip() for item in raw.split(",") if item.strip()]
    
    # Try parsing integers or floats for cleaner representation
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
    """Prompt user for two lists and run various operations."""
    print("\n   === List Difference Explorer ===")
    list_a = parse_list_input("      Enter elements of List A (comma-separated): ")
    list_b = parse_list_input("      Enter elements of List B (comma-separated): ")
    
    if not list_a and not list_b:
        print("      ⚠️  At least one list must have elements.")
        return
        
    print(f"\n      List A: {list_a} (Size: {len(list_a)})")
    print(f"      List B: {list_b} (Size: {len(list_b)})")
    
    print("\n      Select Operation:")
    print("         1. Unique Difference (A - B)")
    print("         2. Symmetric Difference (A ^ B)")
    print("         3. Ordered Difference (A - B preserving order of A)")
    print("         4. Multiset Difference (A - B accounting for frequency)")
    print("         5. Run All Operations & Visualization")
    choice = input("\n      Select option (1-5, default 5): ").strip()
    
    if choice == "1":
        res = find_unique_difference(list_a, list_b)
        print(f"\n      👉 Unique Difference (A - B): {res}")
    elif choice == "2":
        res = find_symmetric_difference(list_a, list_b)
        print(f"\n      👉 Symmetric Difference (A ^ B): {res}")
    elif choice == "3":
        res = find_ordered_difference(list_a, list_b)
        print(f"\n      👉 Ordered Difference (A - B): {res}")
    elif choice == "4":
        res = find_multiset_difference(list_a, list_b)
        print(f"\n      👉 Multiset Difference (A - B): {res}")
    else:
        print(f"\n      👉 Unique Difference (A - B):    {find_unique_difference(list_a, list_b)}")
        print(f"      👉 Symmetric Difference (A ^ B): {find_symmetric_difference(list_a, list_b)}")
        print(f"      👉 Ordered Difference (A - B):   {find_ordered_difference(list_a, list_b)}")
        print(f"      👉 Multiset Difference (A - B):  {find_multiset_difference(list_a, list_b)}")
        draw_difference_visualization(list_a, list_b)


# ---------- Mastery Summary & Entry Point ----------
def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "🤝 LIST DIFFERENCE MASTERED! 🤝".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║  Methods: Set-based Unique Difference,  ".ljust(width - 2) + "║")
    print("   ║           Symmetric Difference,          ".ljust(width - 2) + "║")
    print("   ║           Order-Preserving Difference,   ".ljust(width - 2) + "║")
    print("   ║           Multiset (Frequency) Difference,".ljust(width - 2) + "║")
    print("   ║           ASCII Overlap Diagram Render   ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 19: FIND DIFFERENCES BETWEEN TWO LISTS")
        print("=" * 50)
        print()
        print("   📂 Choose an option:")
        print("      1. Run interactive list comparator")
        print("      2. Run built-in demo cases (numbers & duplicates)")
        print("      3. Exit")
        
        choice = input("\n      Select option (1-3): ").strip()
        if choice == "1":
            interactive_explorer()
        elif choice == "2":
            print("\n   >>> Running Built-in Demo Cases <<<")
            
            # Demo 1: Numbers with duplicates
            a = [1, 2, 2, 3, 4, 4, 5]
            b = [2, 4, 4, 5, 6, 7]
            print(f"\n      Demo 1: Integers & Duplicates")
            print(f"      List A: {a}")
            print(f"      List B: {b}")
            print(f"      👉 Unique Difference (A - B):    {find_unique_difference(a, b)}")
            print(f"      👉 Symmetric Difference (A ^ B): {find_symmetric_difference(a, b)}")
            print(f"      👉 Ordered Difference (A - B):   {find_ordered_difference(a, b)}")
            print(f"      👉 Multiset Difference (A - B):  {find_multiset_difference(a, b)}")
            draw_difference_visualization(a, b)
            
            # Demo 2: Strings
            x = ["apple", "banana", "orange", "grape"]
            y = ["pear", "grape", "banana", "kiwi"]
            print(f"\n      Demo 2: Strings")
            print(f"      List A: {x}")
            print(f"      List B: {y}")
            print(f"      👉 Unique Difference (A - B):    {find_unique_difference(x, y)}")
            print(f"      👉 Symmetric Difference (x ^ y): {find_symmetric_difference(x, y)}")
            draw_difference_visualization(x, y)
        elif choice == "3":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-3.")
            
    show_mastery_box()


if __name__ == "__main__":
    main()


