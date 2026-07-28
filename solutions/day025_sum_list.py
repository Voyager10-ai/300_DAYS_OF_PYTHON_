# Day 25: Sum List
#
# Problem:
#   Write a Python program to compute sums of list elements using multiple algorithms and techniques.
#   - Compute sum using an iterative loop accumulator.
#   - Compute sum using Python's built-in sum() function.
#   - Compute sum using functools.reduce() with operator.add.
#   - Compute sum recursively (head recursion and tail recursion approaches).
#   - Compute conditional / filtered sums (even-only, odd-only, positive-only, custom predicate).
#   - Compute cumulative (prefix) sums / running totals.
#   - Compute sum of nested / deeply-nested lists via recursive flattening.
#   - Compute pairwise sums of two lists (element-wise zip addition).
#   - Render an ASCII contribution breakdown visualizing each element's percentage share.
#   - Provide an interactive CLI explorer with built-in test suites.
#
# This exercise covers iteration, built-ins, functional programming (reduce),
# recursion, conditional filtering, prefix sums, nested structures,
# pairwise operations, ASCII visualization, and CLI interactions.

import ast
import functools
import operator


def sum_iterative(lst):
    """
    Compute sum using an iterative loop accumulator.
    Time Complexity: O(n), Space Complexity: O(1).
    """
    total = 0
    for item in lst:
        total += item
    return total


def sum_builtin(lst):
    """
    Compute sum using Python's built-in sum() function.
    Time Complexity: O(n), Space Complexity: O(1).
    """
    return sum(lst)


def sum_reduce(lst):
    """
    Compute sum using functools.reduce with operator.add.
    Time Complexity: O(n), Space Complexity: O(1).
    """
    if not lst:
        return 0
    return functools.reduce(operator.add, lst)


def sum_recursive(lst):
    """
    Compute sum recursively using head recursion.
    Time Complexity: O(n), Space Complexity: O(n) call stack depth.
    """
    if not lst:
        return 0
    return lst[0] + sum_recursive(lst[1:])


def sum_tail_recursive(lst, acc=0):
    """
    Compute sum recursively using tail-recursive style with accumulator.
    Time Complexity: O(n), Space Complexity: O(n) call stack depth.
    """
    if not lst:
        return acc
    return sum_tail_recursive(lst[1:], acc + lst[0])


def sum_filtered(lst, predicate=None):
    """
    Compute sum of elements matching a predicate function.
    If predicate is None, sums all elements.
    Time Complexity: O(n), Space Complexity: O(1).
    """
    if predicate is None:
        predicate = lambda x: True
    return sum(x for x in lst if predicate(x))


def sum_cumulative(lst):
    """
    Compute cumulative (prefix) sums / running totals for a list.
    Time Complexity: O(n), Space Complexity: O(n).
    Example: [1, 2, 3, 4] -> [1, 3, 6, 10]
    """
    running_total = 0
    prefix_sums = []
    for item in lst:
        running_total += item
        prefix_sums.append(running_total)
    return prefix_sums


def sum_nested(lst):
    """
    Compute total sum of elements in arbitrarily nested lists/tuples.
    Time Complexity: O(total elements), Space Complexity: O(recursion depth).
    Example: [1, [2, [3, 4], 5], 6] -> 21
    """
    total = 0
    if isinstance(lst, (list, tuple, set)):
        for item in lst:
            total += sum_nested(item)
    elif isinstance(lst, (int, float)):
        total += lst
    return total


def sum_pairwise(lst_a, lst_b):
    """
    Compute element-wise pairwise sums of two lists.
    Pads shorter list with 0 using itertools.zip_longest.
    Time Complexity: O(max(len(a), len(b))), Space Complexity: O(max(len(a), len(b))).
    Example: [1, 2, 3], [10, 20] -> [11, 22, 3]
    """
    import itertools
    return [a + b for a, b in itertools.zip_longest(lst_a, lst_b, fillvalue=0)]


def draw_contribution_chart(lst, max_bar_width=30):
    """
    Render ASCII contribution breakdown showing each element's percentage share of the sum.
    """
    if not lst:
        print("      [Empty List - No chart available]")
        return

    total = sum(lst)
    print("\n   ┌" + "─" * 60 + "┐")
    print("   │" + "📊 ELEMENT CONTRIBUTION BREAKDOWN CHART".center(60) + "│")
    print("   ├" + "─" * 60 + "┤")
    print(f"   │ Total Sum: {total:<47} │")
    print("   ├" + "─" * 60 + "┤")

    if total == 0:
        for idx, val in enumerate(lst):
            print(f"   │ Index [{idx:2d}]: Val={val:<6} | Share:  0.0% [N/A]                 │")
    else:
        abs_sum = sum(abs(x) for x in lst)
        for idx, val in enumerate(lst):
            share = (val / total) * 100
            bar_len = int((abs(val) / (abs_sum if abs_sum != 0 else 1)) * max_bar_width)
            bar_char = "█" if val >= 0 else "░"
            bar = bar_char * bar_len
            print(f"   │ Index [{idx:2d}]: Val={val:<6} | {share:6.1f}% {bar:<{max_bar_width}} │")

    print("   └" + "─" * 60 + "┘")


def parse_input_list(prompt_text):
    """
    Parse user input string into a list of numbers or elements.
    Supports Python list literal format [1, 2, 3] and space/comma separated inputs.
    """
    raw_input = input(prompt_text).strip()
    if not raw_input:
        return []

    try:
        parsed = ast.literal_eval(raw_input)
        if isinstance(parsed, (list, tuple)):
            return list(parsed)
        elif isinstance(parsed, (int, float)):
            return [parsed]
    except (ValueError, SyntaxError):
        pass

    # Fallback: parse comma or space separated numbers
    clean_str = raw_input.replace(",", " ")
    parts = clean_str.split()
    elements = []
    for p in parts:
        try:
            if "." in p:
                elements.append(float(p))
            else:
                elements.append(int(p))
        except ValueError:
            elements.append(p)
    return elements


def interactive_explorer():
    """Prompt user for input list and display comprehensive sum analysis results."""
    print("\n" + "=" * 50)
    print("   🧮 INTERACTIVE SUM LIST EXPLORER")
    print("=" * 50)

    user_list = parse_input_list("\n   Enter a list of numbers (e.g., [10, 20, 30, 40] or 5, 10, 15): ")
    if not user_list:
        print("   ⚠️  No elements provided.")
        return

    # Check if elements are purely numeric
    numeric_list = [x for x in user_list if isinstance(x, (int, float))]
    if len(numeric_list) != len(user_list):
        print(f"   ⚠️  List contains non-numeric elements: {user_list}")
        print(f"   Filtered numeric elements: {numeric_list}")
        user_list = numeric_list

    if not user_list:
        return

    print(f"\n   📋 Input List: {user_list}")
    print("   " + "─" * 45)
    print(f"   🔹 Iterative Accumulator Sum : {sum_iterative(user_list)}")
    print(f"   🔹 Built-in sum()            : {sum_builtin(user_list)}")
    print(f"   🔹 functools.reduce() Sum    : {sum_reduce(user_list)}")
    print(f"   🔹 Recursive Head Sum        : {sum_recursive(user_list)}")
    print(f"   🔹 Recursive Tail Sum        : {sum_tail_recursive(user_list)}")
    print(f"   🔹 Filtered Even-only Sum    : {sum_filtered(user_list, lambda x: x % 2 == 0)}")
    print(f"   🔹 Filtered Odd-only Sum     : {sum_filtered(user_list, lambda x: x % 2 != 0)}")
    print(f"   🔹 Filtered Positive Sum     : {sum_filtered(user_list, lambda x: x > 0)}")
    print(f"   🔹 Cumulative (Prefix) Sums  : {sum_cumulative(user_list)}")

    draw_contribution_chart(user_list)


def show_mastery_box():
    """Print an artistic summary box."""
    pass


def main():
    """Entry point for the program."""
    pass


if __name__ == "__main__":
    main()
