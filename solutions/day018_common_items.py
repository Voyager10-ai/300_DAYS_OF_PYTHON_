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
