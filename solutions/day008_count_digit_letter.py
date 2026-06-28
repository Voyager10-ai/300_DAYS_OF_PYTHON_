# Day 8: Count Digit Letter
#
# Problem:
#   Write a Python program that accepts a sentence and calculates the number of
#   letters and digits in it.
#   - Basic counting using built-in string methods (.isalpha(), .isdigit())
#   - Custom counting using ASCII value ranges
#   - Character frequency distribution (counts for each letter and digit)
#   - Visual representation (ASCII bar chart of character categories)
#   - Interactive input analyzer
#
# This exercise covers string manipulation, character classification, loops,
# dictionary usage, and visual data representation in terminal.


# ---------- Basic Counting ----------
def count_builtins(text):
    """Count letters and digits using standard string methods."""
    letters = sum(1 for char in text if char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    others = len(text) - letters - digits

    print(f"\n   📝 Analyzing: '{text}'")
    print(f"      🔤 Letters: {letters}")
    print(f"      🔢 Digits:  {digits}")
    print(f"      ✨ Others:  {others}")
    return letters, digits, others


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 8: COUNT DIGIT LETTER")
    print("=" * 50)
    print()

    print(">>> Basic Counting Demo <<<")
    count_builtins("hello world! 123")
    count_builtins("Python 3.10 is awesome!")


if __name__ == "__main__":
    main()

