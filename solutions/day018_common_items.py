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
