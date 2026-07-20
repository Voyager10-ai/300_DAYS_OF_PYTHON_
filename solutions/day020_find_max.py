# Day 20: Find Max
#
# Problem:
#   Write a Python program that finds the maximum value in various types of lists/structures.
#   - Find maximum iteratively (standard linear scan).
#   - Find maximum recursively (divide and conquer or linear recursion).
#   - Find maximum in nested lists (flatten or traverse arbitrarily nested list/iterable structures).
#   - Find maximum with a custom key function (e.g., maximum by length, custom attributes, absolute values).
#   - Find the Top K elements (finding largest elements, e.g. using heaps).
#   - Render a custom ASCII visualization representing the maximum element in the dataset.
#   - Provide an interactive terminal exploration tool.
#
# This exercise covers standard loops, recursion, flattening, key parameters, heaps,
# and console visualization.

import heapq


# ---------- Core Find Max Algorithms ----------
def find_max_iterative(lst):
    """
    Find the maximum element in a flat list iteratively (manual linear scan).
    Raises ValueError if the list is empty.
    """
    if not lst:
        raise ValueError("Cannot find maximum of an empty list.")
    max_val = lst[0]
    for item in lst[1:]:
        if item > max_val:
            max_val = item
    return max_val


def find_max_recursive(lst):
    """
    Find the maximum element in a flat list recursively.
    Raises ValueError if the list is empty.
    """
    if not lst:
        raise ValueError("Cannot find maximum of an empty list.")
    
    def _helper(sub_lst):
        if len(sub_lst) == 1:
            return sub_lst[0]
        mid = len(sub_lst) // 2
        left_max = _helper(sub_lst[:mid])
        right_max = _helper(sub_lst[mid:])
        return left_max if left_max > right_max else right_max

    return _helper(lst)


def find_max_nested(lst):
    """
    Find the maximum element in an arbitrarily nested list/structure.
    Raises ValueError if no numbers/elements are found in the entire nested structure.
    """
    found = False
    max_val = None
    
    def traverse(item):
        nonlocal found, max_val
        if isinstance(item, (list, tuple, set)):
            for sub_item in item:
                traverse(sub_item)
        else:
            if isinstance(item, (int, float)):
                if not found or item > max_val:
                    max_val = item
                    found = True
                    
    traverse(lst)
    if not found:
        raise ValueError("No numbers found in the nested structure.")
    return max_val


# ---------- Custom Key & Top-K Finding ----------
def find_max_custom(lst, key_func):
    """
    Find the maximum element using a custom key function.
    Raises ValueError if the list is empty.
    """
    if not lst:
        raise ValueError("Cannot find maximum of an empty list.")
    max_item = lst[0]
    max_key = key_func(max_item)
    for item in lst[1:]:
        val = key_func(item)
        if val > max_key:
            max_key = val
            max_item = item
    return max_item


def find_top_k(lst, k):
    """
    Find the top K largest elements in a list.
    Returns a sorted list of top K elements (descending order).
    """
    if k <= 0:
        return []
    return heapq.nlargest(k, lst)


# ---------- ASCII Visualization ----------
def draw_max_visualization(lst, max_val):
    """
    Draw an ASCII bar chart or histogram representing the elements in lst,
    clearly highlighting the maximum value.
    """
    # Flatten/filter list to get numbers
    flat_nums = []
    def traverse(item):
        if isinstance(item, (list, tuple, set)):
            for sub in item:
                traverse(sub)
        elif isinstance(item, (int, float)):
            flat_nums.append(item)
            
    traverse(lst)
    
    if not flat_nums:
        print("      ⚠️  No numeric values to visualize.")
        return
        
    print("\n   📊 Dataset ASCII Visualization:")
    print("   " + "─" * 45)
    
    max_abs = max(abs(x) for x in flat_nums) if flat_nums else 1
    if max_abs == 0:
        max_abs = 1
    scale_width = 30
    
    for i, val in enumerate(flat_nums):
        is_max = (val == max_val)
        bar_len = int((abs(val) / max_abs) * scale_width)
        
        # Build bar representation
        bar_char = "█" if val >= 0 else "░"
        bar_str = bar_char * bar_len
        
        prefix = f"      [{val: >6}] "
        marker = " 👑 [MAX]" if is_max else ""
        
        if val >= 0:
            print(f"{prefix}{bar_str}{marker}")
        else:
            print(f"{prefix}-{bar_str}{marker}")
            
    print("   " + "─" * 45)


# ---------- Interactive Features ----------
import ast

def parse_list_input(prompt_text):
    """
    Parse user input. Supports:
    1. Python list literal syntax (e.g., [1, [2, 3], 4]) for nested lists.
    2. Plain comma-separated list of items.
    """
    raw = input(prompt_text).strip()
    if not raw:
        return []
    
    # Try ast.literal_eval for nested lists or list literals
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return parsed
        return [parsed]
    except (ValueError, SyntaxError):
        # Fallback to comma-separated values
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
    """Prompt user for data and run various max-finding operations."""
    print("\n   === Find Max Explorer ===")
    print("      Supports flat lists (e.g., 5, -2, 10, 3) or nested lists (e.g., [5, [12, -3], 8])")
    lst = parse_list_input("      Enter list or nested list: ")
    
    if not lst:
        print("      ⚠️  List cannot be empty.")
        return
        
    print(f"\n      Input Structure: {lst}")
    
    print("\n      Select Operation:")
    print("         1. Find Max Iteratively")
    print("         2. Find Max Recursively")
    print("         3. Find Max in Nested Lists")
    print("         4. Find Max by custom criteria (absolute value)")
    print("         5. Find Top K elements")
    print("         6. Run All Operations & Visualization")
    
    choice = input("\n      Select option (1-6, default 6): ").strip()
    
    is_nested = any(isinstance(x, (list, tuple, set)) for x in lst)
    
    def flatten(item):
        res = []
        if isinstance(item, (list, tuple, set)):
            for sub in item:
                res.extend(flatten(sub))
        else:
            res.append(item)
        return res
    
    flat_lst = flatten(lst)
    flat_nums = [x for x in flat_lst if isinstance(x, (int, float))]
    
    if choice == "1":
        if is_nested:
            print("      ⚠️  Iterative search requires flat list. Using flattened version.")
        try:
            res = find_max_iterative(flat_nums)
            print(f"\n      👉 Iterative Max: {res}")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    elif choice == "2":
        if is_nested:
            print("      ⚠️  Recursive search requires flat list. Using flattened version.")
        try:
            res = find_max_recursive(flat_nums)
            print(f"\n      👉 Recursive Max: {res}")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    elif choice == "3":
        try:
            res = find_max_nested(lst)
            print(f"\n      👉 Nested Max: {res}")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    elif choice == "4":
        if is_nested:
            print("      ⚠️  Custom search uses flattened version.")
        try:
            res = find_max_custom(flat_nums, abs)
            print(f"\n      👉 Custom Max (by absolute value): {res}")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    elif choice == "5":
        if is_nested:
            print("      ⚠️  Top K uses flattened version.")
        try:
            k_input = input("         Enter K: ").strip()
            k = int(k_input) if k_input.isdigit() else 3
            res = find_top_k(flat_nums, k)
            print(f"\n      👉 Top {k} elements: {res}")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    else:
        print("\n      --- Results ---")
        try:
            print(f"      👉 Iterative Max (flat): {find_max_iterative(flat_nums) if flat_nums else 'N/A'}")
        except Exception as e:
            print(f"      Iterative Max failed: {e}")
        try:
            print(f"      👉 Recursive Max (flat): {find_max_recursive(flat_nums) if flat_nums else 'N/A'}")
        except Exception as e:
            print(f"      Recursive Max failed: {e}")
        try:
            print(f"      👉 Nested Max:          {find_max_nested(lst)}")
        except Exception as e:
            print(f"      Nested Max failed: {e}")
        try:
            print(f"      👉 Custom Max (abs):    {find_max_custom(flat_nums, abs) if flat_nums else 'N/A'}")
        except Exception as e:
            print(f"      Custom Max failed: {e}")
        try:
            print(f"      👉 Top 3 Elements:      {find_top_k(flat_nums, 3)}")
        except Exception as e:
            print(f"      Top K failed: {e}")
            
        if flat_nums:
            try:
                draw_max_visualization(lst, find_max_nested(lst))
            except Exception as e:
                print(f"      Visualization failed: {e}")


# ---------- Mastery Summary & Entry Point ----------
def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "👑 MAXIMUM FINDER MASTERED! 👑".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║  Methods: Iterative Scan, Recursive search, ".ljust(width - 2) + "║")
    print("   ║           Nested List traversal,           ".ljust(width - 2) + "║")
    print("   ║           Custom key (absolute value),    ".ljust(width - 2) + "║")
    print("   ║           Top K finding (via Heap),        ".ljust(width - 2) + "║")
    print("   ║           ASCII Bar Chart visualization    ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 20: FIND THE MAXIMUM VALUE")
        print("=" * 50)
        print()
        print("   📂 Choose an option:")
        print("      1. Run interactive max finder")
        print("      2. Run built-in demo cases")
        print("      3. Exit")
        
        choice = input("\n      Select option (1-3): ").strip()
        if choice == "1":
            interactive_explorer()
        elif choice == "2":
            print("\n   >>> Running Built-in Demo Cases <<<")
            
            # Demo 1: Simple list with positive/negative numbers
            d1 = [10, -5, 25, 42, 0, 18]
            print(f"\n      Demo 1: Flat List {d1}")
            print(f"      👉 Iterative Max: {find_max_iterative(d1)}")
            print(f"      👉 Recursive Max: {find_max_recursive(d1)}")
            print(f"      👉 Top 3 elements: {find_top_k(d1, 3)}")
            draw_max_visualization(d1, 42)
            
            # Demo 2: Nested list
            d2 = [3, [12, 5], [[99, 45], -10], 8]
            print(f"\n      Demo 2: Nested List {d2}")
            m2 = find_max_nested(d2)
            print(f"      👉 Nested Max: {m2}")
            draw_max_visualization(d2, m2)
            
            # Demo 3: Custom keys (by string length)
            d3 = ["apple", "banana", "kiwi", "watermelon", "cherry"]
            print(f"\n      Demo 3: Strings (custom key = len) {d3}")
            print(f"      👉 Longest word: '{find_max_custom(d3, len)}'")
            
        elif choice == "3":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-3.")
            
    show_mastery_box()


if __name__ == "__main__":
    main()
