# Day 17: Check a List Contains Sublist
#
# Problem:
#   Write a Python program that checks if a list contains another list as a sublist
#   (a contiguous subsequence in the same order).
#   - Check if sublist exists in a main list.
#   - Find all starting indices of the sublist in the main list.
#   - Implement two search methods: Naive Sliding Window and Knuth-Morris-Pratt (KMP) algorithm.
#   - Print a step-by-step sliding window comparison visualizer in the terminal.
#   - Provide an interactive terminal interface to input custom lists.
#
# This exercise covers list iteration, list slicing, pattern matching algorithms (KMP),
# visual console alignment, and user input validation.

import time


# ---------- Core Sublist Checking Algorithms ----------
def is_sublist_naive(main_list, sub_list):
    """
    Check if sub_list is a contiguous sublist of main_list using a naive sliding window.
    Returns (exists, occurrences_indices).
    """
    if not sub_list:
        return True, [0] # Empty list is technically a sublist at index 0
        
    n, m = len(main_list), len(sub_list)
    if m > n:
        return False, []
        
    occurrences = []
    # Slide the window
    for i in range(n - m + 1):
        if main_list[i:i+m] == sub_list:
            occurrences.append(i)
            
    exists = len(occurrences) > 0
    return exists, occurrences


def compute_kmp_lps(pattern):
    """Compute the Longest Prefix Suffix (LPS) array for KMP search."""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def is_sublist_kmp(main_list, sub_list):
    """
    Check if sub_list is a contiguous sublist of main_list using KMP algorithm.
    Returns (exists, occurrences_indices).
    """
    if not sub_list:
        return True, [0]
        
    n, m = len(main_list), len(sub_list)
    if m > n:
        return False, []
        
    lps = compute_kmp_lps(sub_list)
    occurrences = []
    
    i = 0 # Index for main_list
    j = 0 # Index for sub_list
    
    while i < n:
        if main_list[i] == sub_list[j]:
            i += 1
            j += 1
            
        if j == m:
            occurrences.append(i - j)
            j = lps[j - 1]
        elif i < n and main_list[i] != sub_list[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    exists = len(occurrences) > 0
    return exists, occurrences


# ---------- Visualizer ----------
def visualize_sublist_search(main_list, sub_list):
    """
    Perform naive sublist check and print step-by-step progress with ASCII pointers.
    Shows the sliding window comparison visually in the console.
    """
    print("\n   🎨 Naive Search Step-by-Step Visualizer:")
    print("      " + "-" * 55)
    
    n, m = len(main_list), len(sub_list)
    if m > n:
        print("      ❌ Error: Sublist is longer than the main list.")
        return False
        
    if not sub_list:
        print("      ✅ Match: Empty list is always a sublist.")
        return True
        
    matches = []
    
    # Render header representation of main list
    main_repr = " ".join(f"[{item}]" for item in main_list)
    print(f"      Main List:  {main_repr}")
    
    # Calculate spacing offsets for visual alignment
    # Each list element in the main_repr representation takes width of str(item) plus brackets and space
    element_positions = []
    current_pos = 18 # Starting horizontal offset for visual align
    
    for item in main_list:
        element_positions.append(current_pos)
        current_pos += len(f"[{item}]") + 1 # size of brackets + item + space
        
    for i in range(n - m + 1):
        window = main_list[i:i+m]
        is_match = window == sub_list
        match_symbol = "✅ MATCH" if is_match else "❌ NO"
        
        # Build alignment padding for the sub_list printout
        padding = " " * (element_positions[i] - 6) # offset adjustments
        sub_repr = " ".join(f" {item} " for item in sub_list)
        
        print(f"      Step {i+1:<2}: {match_symbol:<8} |{padding}{sub_repr}")
        if is_match:
            matches.append(i)
            
    print("      " + "-" * 55)
    if matches:
        print(f"      🎉 Found matches starting at indices: {matches}")
        return True
    else:
        print("      ❌ No matches found.")
        return False


# ---------- Interactive Features ----------
def parse_list_input(prompt_text):
    """Helper to parse a user-inputted comma-separated list into strings or integers."""
    raw = input(prompt_text).strip()
    if not raw:
        return []
    items = [item.strip() for item in raw.split(",") if item.strip()]
    
    # Try converting to integers where possible for cleaner number logic
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
    """Prompt user for main and sub lists, then execute validation and KMP/Naive results."""
    print("\n   === Sublist Detector Explorer ===")
    main_list = parse_list_input("      Enter elements of the MAIN list (comma-separated): ")
    sub_list = parse_list_input("      Enter elements of the SUBLIST list (comma-separated): ")
    
    if not main_list:
        print("      ⚠️  Main list cannot be empty.")
        return
        
    print(f"\n      Main List: {main_list}")
    print(f"      Sub List:  {sub_list}")
    
    print("\n      Select Search Method:")
    print("         1. Naive Sliding Window (Standard)")
    print("         2. Knuth-Morris-Pratt (KMP - Optimized)")
    print("         3. Visualizer Step-by-Step Mode")
    choice = input("\n      Select option (1-3, default 1): ").strip()
    
    if choice == "2":
        exists, indices = is_sublist_kmp(main_list, sub_list)
        method = "KMP Search"
    elif choice == "3":
        visualize_sublist_search(main_list, sub_list)
        return
    else:
        exists, indices = is_sublist_naive(main_list, sub_list)
        method = "Naive Window Search"
        
    print(f"\n   🔒 Results ({method}):")
    if exists:
        print(f"      ✅ YES! The sublist is present in the main list.")
        print(f"      - Starting indices: {indices}")
    else:
        print("      ❌ NO. The sublist does not exist as a contiguous segment.")


def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "  📋 SUBLIST CHECK COMPLETE! 📋  ".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║" + "  Algorithms: Naive Sliding Window,   ".ljust(width - 2) + "║")
    print("   ║" + "              KMP Pattern Matching,   ".ljust(width - 2) + "║")
    print("   ║" + "              LPS Failure Function    ".ljust(width - 2) + "║")
    print("   ║  Features: Visual Console Alignment,     ".ljust(width - 2) + "║")
    print("   ║            Index Tracking Demos          ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 17: CHECK IF A LIST CONTAINS A SUBLIST")
        print("=" * 50)
        print()
        print("   📂 Choose an option:")
        print("      1. Run interactive sublist detector")
        print("      2. Run built-in demos (integers, strings, overlaps)")
        print("      3. Exit")
        
        choice = input("\n      Select option (1-3): ").strip()
        if choice == "1":
            interactive_explorer()
        elif choice == "2":
            print("\n   >>> Running Built-in Demo Cases <<<")
            
            # Demo 1: Simple Integer Sublist
            list_a = [1, 2, 3, 4, 5, 6, 7]
            sub_a = [3, 4, 5]
            print(f"\n      Demo 1: Integers")
            print(f"      Main List: {list_a}")
            print(f"      Sub List:  {sub_a}")
            visualize_sublist_search(list_a, sub_a)
            
            # Demo 2: Character/String Sublist with multiple overlaps
            list_b = ["A", "B", "A", "B", "A", "B", "C"]
            sub_b = ["A", "B", "A"]
            print(f"\n      Demo 2: Strings with Overlap")
            print(f"      Main List: {list_b}")
            print(f"      Sub List:  {sub_b}")
            visualize_sublist_search(list_b, sub_b)
            
            # Demo 3: Match fail
            list_c = [10, 20, 30]
            sub_c = [20, 40]
            print(f"\n      Demo 3: Non-matching")
            print(f"      Main List: {list_c}")
            print(f"      Sub List:  {sub_c}")
            visualize_sublist_search(list_c, sub_c)
        elif choice == "3":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-3.")
            
    show_mastery_box()


if __name__ == "__main__":
    main()
