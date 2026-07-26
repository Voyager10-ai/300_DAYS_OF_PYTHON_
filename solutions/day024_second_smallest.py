# Day 24: Second Smallest
#
# Problem:
#   Write a Python program to find the second smallest (and second largest) element in a list.
#   - Single-pass linear scan algorithm (O(n) time, O(1) space).
#   - Sorting-based selection algorithm (O(n log n)).
#   - Min-heap priority queue approach (O(n + k log n) using heapq).
#   - Key-based finding (using custom key functions e.g., string length or dict field).
#   - General K-th smallest / K-th largest distinct element finder.
#   - ASCII rank visualization diagram displaying sorted ranks and key highlights.
#   - Interactive CLI explorer with built-in test suites.
#
# This exercise covers linear scanning, sorting, heaps/priority queues,
# duplicate handling, custom key selection, ASCII visualizers, and CLI interactions.

import ast
import heapq


def find_second_smallest_linear(lst):
    """
    Find the second smallest distinct element using a single-pass O(n) scan.
    Time Complexity: O(n), Space Complexity: O(1).
    Returns None if fewer than 2 distinct elements exist.
    """
    if not lst or len(lst) < 2:
        return None

    first = float('inf')
    second = float('inf')

    for num in lst:
        if num < first:
            second = first
            first = num
        elif first < num < second:
            second = num

    return second if second != float('inf') else None


def find_second_largest_linear(lst):
    """
    Find the second largest distinct element using a single-pass O(n) scan.
    Time Complexity: O(n), Space Complexity: O(1).
    Returns None if fewer than 2 distinct elements exist.
    """
    if not lst or len(lst) < 2:
        return None

    first = float('-inf')
    second = float('-inf')

    for num in lst:
        if num > first:
            second = first
            first = num
        elif first > num > second:
            second = num

    return second if second != float('-inf') else None


def find_second_smallest_sorting(lst):
    """
    Find the second smallest distinct element by sorting unique elements.
    Time Complexity: O(n log n), Space Complexity: O(n).
    Returns None if fewer than 2 distinct elements exist.
    """
    if not lst:
        return None

    try:
        unique_elems = sorted(set(lst))
    except TypeError:
        # Fallback for unhashable elements
        unique_elems = []
        for item in lst:
            if item not in unique_elems:
                unique_elems.append(item)
        unique_elems.sort(key=lambda x: str(x))

    return unique_elems[1] if len(unique_elems) >= 2 else None


def find_second_smallest_heap(lst):
    """
    Find the second smallest element using a min-heap (heapq.nsmallest).
    Time Complexity: O(n + k log n), Space Complexity: O(n).
    Returns None if fewer than 2 distinct elements exist.
    """
    if not lst:
        return None

    try:
        unique_set = set(lst)
        two_smallest = heapq.nsmallest(2, unique_set)
    except TypeError:
        unique_elems = []
        for item in lst:
            if item not in unique_elems:
                unique_elems.append(item)
        two_smallest = heapq.nsmallest(2, unique_elems, key=lambda x: str(x))

    return two_smallest[1] if len(two_smallest) >= 2 else None


def find_second_smallest_by_key(lst, key=None):
    """
    Find the element corresponding to the second smallest value computed by key function.
    Returns the actual element or None if fewer than 2 distinct key values exist.
    """
    if not lst:
        return None

    if key is None:
        key = lambda x: x

    # Group elements by key or sort distinct key values
    key_map = {}
    for item in lst:
        k_val = key(item)
        if k_val not in key_map:
            key_map[k_val] = item

    sorted_keys = sorted(key_map.keys())
    return key_map[sorted_keys[1]] if len(sorted_keys) >= 2 else None


def find_kth_smallest(lst, k=2):
    """
    Find the K-th smallest distinct element in a list (1-indexed, default k=2).
    Returns the K-th smallest distinct element or None if insufficient elements exist.
    """
    if not lst or k <= 0:
        return None

    try:
        unique_sorted = sorted(set(lst))
    except TypeError:
        unique_elems = []
        for item in lst:
            if item not in unique_elems:
                unique_elems.append(item)
        unique_sorted = sorted(unique_elems, key=lambda x: str(x))

    return unique_sorted[k - 1] if len(unique_sorted) >= k else None


def draw_rank_visualization(lst):
    """
    Render an ASCII rank visualization showing sorted unique order,
    rank badges (1st Min, 2nd Min, 2nd Max, Max), and relative position bars.
    """
    print("\n   📊 Element Rank & Order Visualization:")
    print("   " + "─" * 58)

    if not lst:
        print("      (Empty list provided)")
        print("   " + "─" * 58)
        return

    try:
        unique_sorted = sorted(set(lst))
    except TypeError:
        unique_elems = []
        for item in lst:
            if item not in unique_elems:
                unique_elems.append(item)
        unique_sorted = sorted(unique_elems, key=lambda x: str(x))

    n_unique = len(unique_sorted)
    print(f"   Raw List      : {lst}")
    print(f"   Unique Count  : {n_unique} distinct element(s)")
    print("   " + "─" * 58)

    if n_unique < 2:
        print(f"   ⚠️  Need at least 2 distinct elements (found {n_unique}).")
        print("   " + "─" * 58)
        return

    first_min = unique_sorted[0]
    second_min = unique_sorted[1]
    second_max = unique_sorted[-2]
    first_max = unique_sorted[-1]

    # Render rank breakdown table
    print("   Rank breakdown:")
    for idx, val in enumerate(unique_sorted, 1):
        badges = []
        if val == first_min:
            badges.append("👑 [1st MIN]")
        if val == second_min:
            badges.append("🥈 [2nd MIN]")
        if val == second_max and n_unique > 2:
            badges.append("🥈 [2nd MAX]")
        if val == first_max:
            badges.append("👑 [1st MAX]")

        badge_str = " ".join(badges)

        # Bar width calculation for numbers
        if isinstance(val, (int, float)):
            max_v = max(abs(x) for x in unique_sorted if isinstance(x, (int, float))) or 1
            bar_len = int((abs(val) / max_v) * 20)
            bar_str = "█" * max(1, bar_len)
            val_str = f"{val: >8}"
        else:
            bar_str = "■" * min(20, len(str(val)))
            val_str = f"'{val}': >8"

        print(f"      Rank #{idx: >2}: {val_str} | {bar_str:<20} {badge_str}")

    print("   " + "─" * 58)


def parse_input_list(prompt_text):
    """
    Parse user input string into a list.
    Supports Python list syntax (e.g., [5, 2, 8, 1, 9]) or comma-separated numbers/strings.
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
    """Prompt user for input list and execute second smallest operations."""
    print("\n   === Second Smallest Explorer ===")
    print("      Enter numbers or strings (e.g. 5, 2, 8, 1, 9, 2 or [10, 20, 5, 15])")
    lst = parse_input_list("      Enter list: ")

    if not lst:
        print("      ⚠️  List cannot be empty.")
        return

    print(f"\n      Input List ({len(lst)} items): {lst}")

    print("\n      Select Operation:")
    print("         1. Single-Pass Linear Search O(n)")
    print("         2. Sorting Approach O(n log n)")
    print("         3. Min-Heap Priority Queue Approach")
    print("         4. Key-Based Search (e.g. string length)")
    print("         5. General K-th Smallest Element")
    print("         6. Run All Algorithms & Render Rank Visualization")

    choice = input("\n      Select option (1-6, default 6): ").strip()

    if choice == "1":
        s_min = find_second_smallest_linear(lst)
        s_max = find_second_largest_linear(lst)
        print(f"\n      👉 Second Smallest (Linear): {s_min}")
        print(f"      👉 Second Largest  (Linear): {s_max}")
    elif choice == "2":
        s_min = find_second_smallest_sorting(lst)
        print(f"\n      👉 Second Smallest (Sorting): {s_min}")
    elif choice == "3":
        s_min = find_second_smallest_heap(lst)
        print(f"\n      👉 Second Smallest (Heap): {s_min}")
    elif choice == "4":
        s_min = find_second_smallest_by_key(lst, key=lambda x: len(str(x)))
        print(f"\n      👉 Second Smallest by Length Key: {s_min}")
    elif choice == "5":
        k_str = input("         Enter K value (default 2): ").strip()
        k = int(k_str) if k_str.isdigit() else 2
        kth = find_kth_smallest(lst, k)
        print(f"\n      👉 {k}-th Smallest Distinct Element: {kth}")
    else:
        s_min_lin = find_second_smallest_linear(lst)
        s_max_lin = find_second_largest_linear(lst)
        s_min_sort = find_second_smallest_sorting(lst)
        s_min_heap = find_second_smallest_heap(lst)

        print("\n      --- Second Smallest Analysis Results ---")
        print(f"      👉 Second Smallest (Linear O(n)): {s_min_lin}")
        print(f"      👉 Second Smallest (Sorting):    {s_min_sort}")
        print(f"      👉 Second Smallest (Heap):       {s_min_heap}")
        print(f"      👉 Second Largest  (Linear O(n)): {s_max_lin}")

        draw_rank_visualization(lst)


def show_mastery_box():
    """Print an artistic summary box."""
    width = 46
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "👑 SECOND SMALLEST MASTERED! 👑".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║  Methods: Single-pass linear scan O(n),       ".ljust(width - 2) + "║")
    print("   ║           Sorting-based selection O(n log n), ".ljust(width - 2) + "║")
    print("   ║           Min-heap priority queue heapq,      ".ljust(width - 2) + "║")
    print("   ║           Key-based custom finder,            ".ljust(width - 2) + "║")
    print("   ║           General K-th smallest retrieval,    ".ljust(width - 2) + "║")
    print("   ║           ASCII rank breakdown visualization  ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 24: SECOND SMALLEST")
        print("=" * 50)
        print()
        print("   📂 Choose an option:")
        print("      1. Run interactive second smallest explorer")
        print("      2. Run built-in demo cases")
        print("      3. Exit")

        choice = input("\n      Select option (1-3): ").strip()
        if choice == "1":
            interactive_explorer()
        elif choice == "2":
            print("\n   >>> Running Built-in Demo Cases <<<")

            # Demo 1: Unsorted numbers with duplicate min
            d1 = [12, 3, 1, 1, 5, 8, 3, 19]
            print(f"\n      Demo 1: Unsorted List with Duplicates {d1}")
            s_min1 = find_second_smallest_linear(d1)
            print(f"      👉 Second Smallest: {s_min1}")
            draw_rank_visualization(d1)

            # Demo 2: Floats / Negative numbers
            d2 = [-10.5, 0.0, -2.3, -10.5, 15.2, -5.0]
            print(f"\n      Demo 2: Negative & Float Numbers {d2}")
            s_min2 = find_second_smallest_heap(d2)
            s_max2 = find_second_largest_linear(d2)
            print(f"      👉 Second Smallest: {s_min2}")
            print(f"      👉 Second Largest : {s_max2}")
            draw_rank_visualization(d2)

            # Demo 3: Key-based search on strings
            d3 = ["cat", "apple", "banana", "kiwi", "fig"]
            print(f"\n      Demo 3: Strings by Length Key {d3}")
            s_min3 = find_second_smallest_by_key(d3, key=len)
            print(f"      👉 Second Shortest String: '{s_min3}' (len={len(s_min3)})")

            # Demo 4: K-th smallest elements
            d4 = [100, 40, 20, 50, 80, 10]
            print(f"\n      Demo 4: K-th Smallest Selection {d4}")
            print(f"      👉 1st Smallest: {find_kth_smallest(d4, 1)}")
            print(f"      👉 2nd Smallest: {find_kth_smallest(d4, 2)}")
            print(f"      👉 3rd Smallest: {find_kth_smallest(d4, 3)}")

        elif choice == "3":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-3.")

    show_mastery_box()


if __name__ == "__main__":
    main()
