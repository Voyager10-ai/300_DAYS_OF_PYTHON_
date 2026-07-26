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
    """Render an ASCII rank visualization showing sorted order and key ranks."""
    pass


def parse_input_list(prompt_text):
    """Parse user input string into a list."""
    pass


def interactive_explorer():
    """Prompt user for input and display second smallest analysis results."""
    pass


def show_mastery_box():
    """Print an artistic summary box."""
    pass


def main():
    """Entry point for the program."""
    pass


if __name__ == "__main__":
    main()
