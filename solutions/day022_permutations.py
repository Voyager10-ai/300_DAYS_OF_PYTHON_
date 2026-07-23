# Day 22: Permutations
#
# Problem:
#   Write a Python program to generate, analyze, and visualize permutations of lists and strings.
#   - Generate all permutations using classic recursive backtracking.
#   - Generate all permutations using Python's standard library itertools.permutations.
#   - Generate all permutations using Heap's Algorithm (efficient element swapping).
#   - Handle duplicate elements to generate unique permutations only.
#   - Generate k-length partial permutations P(n, k) from a set of n elements.
#   - Render a custom ASCII decision tree / search space diagram showing permutation choices.
#   - Provide an interactive CLI explorer with built-in test suites.
#
# This exercise covers recursion, backtracking, Heap's algorithm, set-based deduplication,
# combinatorics, tree visualization, and interactive CLI features.

import ast
import itertools


def permutations_backtracking(lst):
    """
    Generate all permutations of a list using recursive backtracking.
    Returns a list of lists representing all n! permutations.
    """
    if not lst:
        return [[]]
    res = []
    lst_copy = list(lst)

    def backtrack(start):
        if start == len(lst_copy):
            res.append(lst_copy[:])
            return
        for i in range(start, len(lst_copy)):
            lst_copy[start], lst_copy[i] = lst_copy[i], lst_copy[start]
            backtrack(start + 1)
            lst_copy[start], lst_copy[i] = lst_copy[i], lst_copy[start]

    backtrack(0)
    return res


def permutations_itertools(lst):
    """
    Generate all permutations using itertools.permutations.
    Returns a list of lists.
    """
    return [list(p) for p in itertools.permutations(lst)]


def permutations_heaps(lst):
    """
    Generate all permutations using Heap's Algorithm.
    Generates permutations by swapping elements efficiently.
    Returns a list of lists.
    """
    arr = list(lst)
    res = []
    n = len(arr)

    def generate(k):
        if k == 1:
            res.append(arr[:])
            return
        generate(k - 1)
        for i in range(k - 1):
            if k % 2 == 0:
                arr[i], arr[k - 1] = arr[k - 1], arr[i]
            else:
                arr[0], arr[k - 1] = arr[k - 1], arr[0]
            generate(k - 1)

    if n > 0:
        generate(n)
    else:
        res.append([])
    return res


def permutations_unique(lst):
    """
    Generate unique permutations for a list that may contain duplicate elements.
    Uses sorting and backtracking with boolean used array to avoid duplicates.
    """
    arr = list(lst)
    try:
        arr.sort()
    except TypeError:
        arr = sorted(arr, key=str)

    res = []
    used = [False] * len(arr)

    def backtrack(path):
        if len(path) == len(arr):
            res.append(path[:])
            return
        for i in range(len(arr)):
            if used[i]:
                continue
            if i > 0 and arr[i] == arr[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(arr[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return res


def permutations_k_length(lst, k):
    """
    Generate partial permutations P(n, k) of length k from list lst.
    Returns a list of lists.
    """
    if k < 0 or k > len(lst):
        return []
    return [list(p) for p in itertools.permutations(lst, k)]


def draw_permutation_tree(lst, max_depth=3):
    """
    Draw an ASCII decision search tree visualizing permutation branching.
    Shows chosen prefix paths and remaining choices.
    """
    print("\n   🌳 Permutation Decision Tree Diagram:")
    print("   " + "─" * 58)

    arr = list(lst)
    if not arr:
        print("      (Empty list)")
        print("   " + "─" * 58)
        return

    print(f"   ROOT: {arr}")

    def build_tree(path, remaining, depth, prefix_str):
        if not remaining or depth > max_depth:
            if not remaining:
                print(f"{prefix_str}└── 🎯 Permutation: {path}")
            else:
                print(f"{prefix_str}└── ... (depth limit reached)")
            return

        count = len(remaining)
        for idx, item in enumerate(remaining):
            is_last = (idx == count - 1)
            connector = "└── " if is_last else "├── "
            child_prefix = prefix_str + ("    " if is_last else "│   ")

            next_path = path + [item]
            next_remaining = remaining[:idx] + remaining[idx + 1:]

            print(f"{prefix_str}{connector}Pick [{item}] -> Path: {next_path} (Remaining: {next_remaining})")
            build_tree(next_path, next_remaining, depth + 1, child_prefix)

    build_tree([], arr, 1, "   ")
    print("   " + "─" * 58)


def parse_input_list(prompt_text):
    """
    Parse input into a list of elements.
    Supports list literal format (e.g. [1, 2, 3]) or comma-separated elements.
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
    """Prompt user for input and run selected permutation algorithms."""
    print("\n   === Permutations Explorer ===")
    print("      Enter elements (e.g. 1, 2, 3 or A, B, C or [1, 'a', 2])")
    lst = parse_input_list("      Enter elements: ")

    if not lst:
        print("      ⚠️  List cannot be empty.")
        return

    print(f"\n      Input Elements: {lst} (n = {len(lst)})")

    print("\n      Select Operation:")
    print("         1. Backtracking Permutations")
    print("         2. Itertools Permutations")
    print("         3. Heap's Algorithm Permutations")
    print("         4. Unique Permutations (handles duplicates)")
    print("         5. K-length Permutations P(n, k)")
    print("         6. Run All Algorithms & Draw Decision Tree")

    choice = input("\n      Select option (1-6, default 6): ").strip()

    if choice == "1":
        perms = permutations_backtracking(lst)
        print(f"\n      👉 Backtracking Result ({len(perms)} total): {perms}")
    elif choice == "2":
        perms = permutations_itertools(lst)
        print(f"\n      👉 Itertools Result ({len(perms)} total): {perms}")
    elif choice == "3":
        perms = permutations_heaps(lst)
        print(f"\n      👉 Heap's Algorithm Result ({len(perms)} total): {perms}")
    elif choice == "4":
        perms = permutations_unique(lst)
        print(f"\n      👉 Unique Permutations ({len(perms)} total): {perms}")
    elif choice == "5":
        k_str = input("         Enter K value (length of permutations): ").strip()
        k = int(k_str) if k_str.isdigit() else min(2, len(lst))
        perms = permutations_k_length(lst, k)
        print(f"\n      👉 P({len(lst)}, {k}) Permutations ({len(perms)} total): {perms}")
    else:
        p_backtrack = permutations_backtracking(lst)
        p_itertools = permutations_itertools(lst)
        p_heaps = permutations_heaps(lst)
        p_unique = permutations_unique(lst)

        print("\n      --- Permutations Analysis Results ---")
        print(f"      👉 Total Expected Permutations n!: {len(p_backtrack)}")
        print(f"      👉 Backtracking Output Count:       {len(p_backtrack)}")
        print(f"      👉 Itertools Output Count:          {len(p_itertools)}")
        print(f"      👉 Heap's Algorithm Count:          {len(p_heaps)}")
        print(f"      👉 Unique Permutations Count:       {len(p_unique)}")
        print(f"      👉 Sample Unique Permutations:      {p_unique[:6]}")

        draw_permutation_tree(lst)


def show_mastery_box():
    """Print an artistic summary box."""
    width = 46
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "👑 PERMUTATIONS MASTERED! 👑".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║  Methods: Backtracking recursion,             ".ljust(width - 2) + "║")
    print("   ║           Itertools permutations,             ".ljust(width - 2) + "║")
    print("   ║           Heap's algorithm swapping,          ".ljust(width - 2) + "║")
    print("   ║           Unique duplicate-safe generation,   ".ljust(width - 2) + "║")
    print("   ║           Partial P(n, k) permutations,       ".ljust(width - 2) + "║")
    print("   ║           ASCII Tree Search Visualization     ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    while True:
        print("\n" + "=" * 50)
        print("  DAY 22: PERMUTATIONS")
        print("=" * 50)
        print()
        print("   📂 Choose an option:")
        print("      1. Run interactive permutations explorer")
        print("      2. Run built-in demo cases")
        print("      3. Exit")

        choice = input("\n      Select option (1-3): ").strip()
        if choice == "1":
            interactive_explorer()
        elif choice == "2":
            print("\n   >>> Running Built-in Demo Cases <<<")

            # Demo 1: Distinct integer elements
            d1 = [1, 2, 3]
            print(f"\n      Demo 1: Distinct Elements {d1}")
            p1 = permutations_backtracking(d1)
            print(f"      👉 All Permutations ({len(p1)} total): {p1}")
            draw_permutation_tree(d1)

            # Demo 2: Elements with duplicates
            d2 = [1, 1, 2]
            print(f"\n      Demo 2: Duplicate Elements {d2}")
            p2_all = permutations_itertools(d2)
            p2_unique = permutations_unique(d2)
            print(f"      👉 All (incl. duplicates) ({len(p2_all)} total): {p2_all}")
            print(f"      👉 Unique Permutations ({len(p2_unique)} total): {p2_unique}")

            # Demo 3: String elements with partial permutations P(4, 2)
            d3 = ["A", "B", "C", "D"]
            print(f"\n      Demo 3: String Elements {d3} with K=2")
            p3 = permutations_k_length(d3, 2)
            print(f"      👉 P(4, 2) Permutations ({len(p3)} total): {p3}")

        elif choice == "3":
            print("\n      Goodbye!")
            break
        else:
            print("      ⚠️  Invalid selection. Please choose 1-3.")

    show_mastery_box()


if __name__ == "__main__":
    main()
