# Day 9: Count Even Odd
#
# Problem:
#   Write a Python program that counts the number of even and odd numbers
#   from a series of numbers or sequence.
#   - Count even/odd in a user-provided list or range
#   - Digits parity analyzer (counts even and odd digits in a large number)
#   - Separate statistical analysis for even and odd subsets (sums, averages)
#   - ASCII visualizer (bar chart comparing even/odd distribution)
#   - Interactive parity explorer
#
# This exercise covers loops, conditional logic, list processing, math stats,
# and console visualization.


# ---------- Basic Sequence Parity Counting ----------
def count_even_odd_sequence(numbers):
    """Count even and odd numbers in a given sequence."""
    evens = sum(1 for n in numbers if n % 2 == 0)
    odds = len(numbers) - evens

    print(f"\n   🔢 Sequence: {numbers[:15]}... (total {len(numbers)} items)" if len(numbers) > 15 else f"\n   🔢 Sequence: {numbers}")
    print(f"      🔵 Even numbers: {evens}")
    print(f"      🔴 Odd numbers:  {odds}")
    return evens, odds


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 9: COUNT EVEN ODD")
    print("=" * 50)
    print()

    print(">>> Basic Sequence Parity Demo <<<")
    count_even_odd_sequence([1, 2, 3, 4, 5, 6, 7, 8, 9])
    count_even_odd_sequence(list(range(10, 50, 3)))


if __name__ == "__main__":
    main()

