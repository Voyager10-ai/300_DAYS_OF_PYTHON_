# Day 21: Frequency of Elements
#
# Problem:
#   Write a Python program that counts and analyzes element frequencies in lists and nested structures.
#   - Count element frequencies using standard dictionaries (manual count loop).
#   - Count element frequencies using collections.Counter.
#   - Count frequencies in arbitrarily nested lists/iterables (flattening/recursive traversal).
#   - Find top K most frequent and least frequent elements.
#   - Group elements by their frequency counts (inverted index mapping).
#   - Render a custom ASCII bar chart / histogram visualizing frequencies and relative percentages.
#   - Provide an interactive CLI explorer with built-in test suites.
#
# This exercise covers dictionary manipulation, collections module, recursion, data aggregation,
# histogram visualization, and CLI interactions.

import ast
from collections import Counter


# ---------- Core Frequency Algorithms ----------
def count_frequencies_dict(lst):
    """
    Count element frequencies using a standard Python dictionary loop.
    Returns a dictionary mapping elements to their count.
    """
    freq = {}
    for item in lst:
        freq[item] = freq.get(item, 0) + 1
    return freq


def count_frequencies_counter(lst):
    """
    Count element frequencies using collections.Counter.
    Returns a dictionary mapping elements to their count.
    """
    return dict(Counter(lst))


def count_frequencies_nested(lst):
    """
    Count element frequencies in an arbitrarily nested list/iterable structure.
    Traverses lists, tuples, sets recursively.
    """
    freq = {}

    def traverse(item):
        if isinstance(item, (list, tuple, set)):
            for sub in item:
                traverse(sub)
        else:
            freq[item] = freq.get(item, 0) + 1

    traverse(lst)
    return freq


# ---------- Frequency Analysis & Grouping ----------
def get_most_frequent(lst_or_freq, k=1):
    """
    Get the top K most frequent elements.
    Accepts either a list/nested structure or a frequency dictionary.
    Returns a list of tuples (element, count) sorted by count descending.
    """
    pass


def get_least_frequent(lst_or_freq, k=1):
    """
    Get the top K least frequent elements.
    Accepts either a list/nested structure or a frequency dictionary.
    Returns a list of tuples (element, count) sorted by count ascending.
    """
    pass


def group_by_frequency(lst_or_freq):
    """
    Group elements by their frequency of occurrence.
    Returns a dictionary mapping frequency count -> list of elements with that count.
    """
    pass


# ---------- ASCII Visualization ----------
def draw_frequency_histogram(lst_or_freq):
    """
    Draw an ASCII histogram representing frequency of elements.
    Highlights most frequent element(s) with 👑 [MODE].
    """
    pass
