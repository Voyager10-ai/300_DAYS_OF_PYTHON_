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
    """Find the second smallest distinct element by sorting."""
    pass


def find_second_smallest_heap(lst):
    """Find the second smallest element using a min-heap."""
    pass


def find_second_smallest_by_key(lst, key=None):
    """Find the second smallest element based on a custom key function."""
    pass


def find_kth_smallest(lst, k=2):
    """Find the K-th smallest distinct element in a list."""
    pass


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
