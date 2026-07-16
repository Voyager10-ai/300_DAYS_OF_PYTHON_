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

