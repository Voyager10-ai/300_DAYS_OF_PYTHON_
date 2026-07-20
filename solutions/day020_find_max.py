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
    pass
