# Day 16: Characters to String
#
# Problem:
#   Write a Python program that converts a list of characters into a single string,
#   and splits strings back into lists of characters with various processing filters.
#   - Convert a list/array of individual characters into a string.
#   - Support custom separators between characters (e.g. empty, space, hyphen, comma).
#   - Support character casing transformations during the joining process.
#   - Support the inverse operation: splitting a string back into character lists.
#   - Provide options to deduplicate, strip whitespace, or sort the character lists.
#   - Render a custom character distribution frequency ASCII chart.
#   - Provide an interactive terminal menu explorer.
#
# This exercise covers list manipulation, string joining, list comprehension,
# dictionary counting, custom sorting, and CLI dashboard construction.

import collections
import string
