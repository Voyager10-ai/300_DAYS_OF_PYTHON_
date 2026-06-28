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


# ---------- Digit Parity Counting ----------
def count_digits_parity(number):
    """Count even and odd digits within a large integer."""
    # Convert to string and filter out signs/decimals if any
    num_str = "".join(char for char in str(number) if char.isdigit())
    evens = 0
    odds = 0

    for digit_char in num_str:
        digit = int(digit_char)
        if digit % 2 == 0:
            evens += 1
        else:
            odds += 1

    print(f"\n   🔢 Number: {number}")
    print(f"      🔵 Even digits: {evens} (e.g. 0, 2, 4, 6, 8)")
    print(f"      🔴 Odd digits:  {odds} (e.g. 1, 3, 5, 7, 9)")
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
    print()

    print(">>> Digit Parity Demo <<<")
    count_digits_parity(45678)
    count_digits_parity(1357902468)


if __name__ == "__main__":
    main()


