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


# ---------- Statistical Subset Analysis ----------
def parity_subsets_stats(numbers):
    """Analyze even and odd subsets of numbers (sums, averages, min, max)."""
    evens_list = [n for n in numbers if n % 2 == 0]
    odds_list = [n for n in numbers if n % 2 != 0]

    e_count, e_sum = len(evens_list), sum(evens_list)
    o_count, o_sum = len(odds_list), sum(odds_list)

    print(f"\n   📈 Subset Statistics for: {numbers}")
    print(f"      🔵 Evens Count: {e_count} | Sum: {e_sum} | Avg: {e_sum/e_count if e_count > 0 else 0:.2f} | Min/Max: {min(evens_list) if e_count > 0 else 0}/{max(evens_list) if e_count > 0 else 0}")
    print(f"      🔴 Odds Count:  {o_count} | Sum: {o_sum} | Avg: {o_sum/o_count if o_count > 0 else 0:.2f} | Min/Max: {min(odds_list) if o_count > 0 else 0}/{max(odds_list) if o_count > 0 else 0}")
    return evens_list, odds_list


# ---------- Visual Distribution Representation ----------
def visualize_parity_distribution(numbers):
    """Draw a horizontal ASCII bar chart comparing even and odd count proportions."""
    evens = sum(1 for n in numbers if n % 2 == 0)
    odds = len(numbers) - evens
    total = len(numbers)

    print(f"\n   📊 Parity Chart (total {total} items):")
    if total == 0:
        print("      Empty list.")
        return

    max_width = 30
    e_width = int(evens / total * max_width) if total > 0 else 0
    o_width = int(odds / total * max_width) if total > 0 else 0

    # Ensure min width of 1 if count > 0
    if evens > 0 and e_width == 0: e_width = 1
    if odds > 0 and o_width == 0: o_width = 1

    print(f"      🔵 Evens: [{ '█' * e_width }{ '░' * (max_width - e_width) }] {evens} ({evens/total*100:.1f}%)")
    print(f"      🔴 Odds:  [{ '█' * o_width }{ '░' * (max_width - o_width) }] {odds} ({odds/total*100:.1f}%)")


# ---------- Interactive & Summary ----------
def interactive_parity_explorer():
    """Prompt the user to choose input type (numbers or a large number) and analyze."""
    print("\n   🤔 Parity Explorer:")
    print("      1. Analyze a list of numbers (separated by spaces)")
    print("      2. Analyze digits of a large number")
    choice = input("      Select option (1-2): ").strip()

    if choice == "1":
        val = input("      Enter numbers separated by spaces: ").strip()
        try:
            numbers = [int(x) for x in val.split()]
            if numbers:
                count_even_odd_sequence(numbers)
                parity_subsets_stats(numbers)
                visualize_parity_distribution(numbers)
            else:
                print("      Empty list.")
        except ValueError:
            print("      ❌ Invalid numbers entered.")
    elif choice == "2":
        val = input("      Enter a large integer: ").strip()
        try:
            num = int(val)
            count_digits_parity(num)
        except ValueError:
            print("      ❌ Invalid integer.")
    else:
        print("      No option selected.")


def show_parity_summary():
    """Print a beautiful parity summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "  🔵 EVEN ODD PARITY MASTERED! 🔴  ".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║" + "  Concepts: Parity detection, subset   ".ljust(width - 2) + "║")
    print("   ║" + "            statistics, digit parity,  ".ljust(width - 2) + "║")
    print("   ║" + "            proportional bar charts.   ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


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
    print()

    print(">>> Subset Statistics Demo <<<")
    parity_subsets_stats([12, 15, 22, 91, 104, 3, 7, 8])
    print()

    print(">>> Visual Parity Distribution <<<")
    visualize_parity_distribution([1, 1, 3, 5, 7, 9, 2, 4, 6])
    print()

    print(">>> Interactive Parity Explorer <<<")
    interactive_parity_explorer()
    show_parity_summary()


if __name__ == "__main__":
    main()





