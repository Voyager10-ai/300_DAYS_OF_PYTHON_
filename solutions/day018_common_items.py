# Day 18: Common Items
#
# Problem:
#   Write a Python program that finds common elements between two lists (intersection)
#   and demonstrates set operations and list comparisons.
#   - Find unique common elements (Set Intersection).
#   - Find common elements preserving duplicates (Multi-set Intersection).
#   - Find common elements preserving order of appearance.
#   - Calculate difference and symmetric difference between two lists.
#   - Render a custom ASCII Venn Diagram representing the overlap of the two sets.
#   - Provide an interactive terminal exploration tool.
#
# This exercise covers lists, sets, collections.Counter, mathematical set theory,
# alignment-based ASCII rendering, and CLI input parsing.

import collections


# ---------- Core List Intersection Algorithms ----------
def find_unique_common(list_a, list_b):
    """
    Find unique common elements using set intersection.
    Returns a sorted list of unique common elements.
    """
    set_a = set(list_a)
    set_b = set(list_b)
    # Return sorted list of intersection
    return sorted(list(set_a.intersection(set_b)), key=lambda x: str(x))


def find_ordered_common(list_a, list_b):
    """
    Find common elements retaining the relative order of appearance in list_a.
    Duplicate values from list_a are only kept if they appear in list_b,
    and are kept exactly as many times as they are present in list_a.
    """
    set_b = set(list_b)
    return [item for item in list_a if item in set_b]


def find_multiset_common(list_a, list_b):
    """
    Find common elements preserving duplicates.
    E.g. If 'x' appears 3 times in list_a and 2 times in list_b,
    it will appear 2 times (min of both counts) in the result.
    """
    count_a = collections.Counter(list_a)
    count_b = collections.Counter(list_b)
    
    intersection_counter = count_a & count_b # Multiset intersection in Counter
    return list(intersection_counter.elements())


def find_relative_difference(list_a, list_b):
    """Find unique elements in list_a that are not in list_b."""
    return sorted(list(set(list_a) - set(list_b)), key=lambda x: str(x))


def find_symmetric_difference(list_a, list_b):
    """Find unique elements that are in either list_a or list_b but not both."""
    return sorted(list(set(list_a) ^ set(list_b)), key=lambda x: str(x))


# ---------- ASCII Visualization ----------
def draw_ascii_venn(list_a, list_b):
    """Draw a text-based ASCII Venn Diagram representing sizes and overlap."""
    set_a = set(list_a)
    set_b = set(list_b)
    
    unique_a = len(set_a - set_b)
    common = len(set_a.intersection(set_b))
    unique_b = len(set_b - set_a)
    
    print("\n   📊 Set Overlap Visualization (Unique Elements):")
    print(f"      List A (Unique: {len(set_a)})         List B (Unique: {len(set_b)})")
    print("       ┌───────────┐            ┌───────────┐")
    print("       │           │            │           │")
    print(f"       │  Only A   │    ({common:<2})    │  Only B   │")
    print(f"       │    ({unique_a:<2})    ├────────────┤    ({unique_b:<2})    │")
    print("       │           │   Common   │           │")
    print("       │           │            │           │")
    print("       └───────────┘            └───────────┘")


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
    print("\n   === Common Items Finder Explorer ===")
    list_a = parse_list_input("      Enter elements of List A (comma-separated): ")
    list_b = parse_list_input("      Enter elements of List B (comma-separated): ")
    
    if not list_a or not list_b:
        print("      ⚠️  Both lists must have elements.")
        return
        
    print(f"\n      List A: {list_a} (Size: {len(list_a)})")
    print(f"      List B: {list_b} (Size: {len(list_b)})")
    
    print("\n      Select Operation:")
    print("         1. Unique Common Items (Set Intersection)")
    print("         2. Common Items Preserving Order (of List A)")
    print("         3. Common Items Preserving Duplicates (Multi-set)")
    print("         4. Difference (A - B)")
    print("         5. Symmetric Difference (A ^ B)")
    print("         6. Run All Operations")
    choice = input("\n      Select option (1-6, default 1): ").strip()
    
    if choice == "2":
        res = find_ordered_common(list_a, list_b)
        print(f"\n      👉 Ordered Intersection: {res}")
    elif choice == "3":
        res = find_multiset_common(list_a, list_b)
        print(f"\n      👉 Multi-set Intersection: {res}")
    elif choice == "4":
        res = find_relative_difference(list_a, list_b)
        print(f"\n      👉 Difference (A - B): {res}")
    elif choice == "5":
        res = find_symmetric_difference(list_a, list_b)
        print(f"\n      👉 Symmetric Difference (A ^ B): {res}")
    elif choice == "6":
        print(f"\n      👉 Unique Common Items:    {find_unique_common(list_a, list_b)}")
        print(f"      👉 Ordered Intersection:   {find_ordered_common(list_a, list_b)}")
        print(f"      👉 Multi-set Intersection: {find_multiset_common(list_a, list_b)}")
        print(f"      👉 Difference (A - B):     {find_relative_difference(list_a, list_b)}")
        print(f"      👉 Symmetric Difference:   {find_symmetric_difference(list_a, list_b)}")
    else:
        res = find_unique_common(list_a, list_b)
        print(f"\n      👉 Unique Common Items: {res}")
        
    draw_ascii_venn(list_a, list_b)


# ---------- Mastery Summary & Entry Point ----------
def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "  🤝 COMMON ITEMS FINDER COMPLETE! 🤝  ".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║  Methods: Set-based Unique Intersection, ".ljust(width - 2) + "║")
    print("   ║           Order-Preserving Intersection, ".ljust(width - 2) + "║")
    print("   ║           Multi-set (Duplicate) Intersect,".ljust(width - 2) + "║")
    print("   ║           Symmetric & Relative Diff,     ".ljust(width - 2) + "║")
    print("   ║           ASCII Venn Diagram Render      ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 18: FIND COMMON ELEMENTS & SET MATH")
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
            print(f"      👉 Unique Common Items:    {find_unique_common(a, b)}")
            print(f"      👉 Ordered Intersection:   {find_ordered_common(a, b)}")
            print(f"      👉 Multi-set Intersection: {find_multiset_common(a, b)}")
            draw_ascii_venn(a, b)
            
            # Demo 2: Strings
            x = ["apple", "banana", "orange", "grape"]
            y = ["pear", "grape", "banana", "kiwi"]
            print(f"\n      Demo 2: Strings")
            print(f"      List A: {x}")
            print(f"      List B: {y}")
            print(f"      👉 Unique Common:          {find_unique_common(x, y)}")
            print(f"      👉 Symmetric Diff (A ^ B): {find_symmetric_difference(x, y)}")
            draw_ascii_venn(x, y)
        elif choice == "3":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-3.")
            
    show_mastery_box()


if __name__ == "__main__":
    main()
