# Day 1: Print String
#
# Problem:
#   Write a Python program that demonstrates different ways to print strings.
#   - Print a simple string
#   - Print multiple strings on the same line
#   - Print formatted strings using f-strings, .format(), and % formatting
#   - Print multi-line strings
#   - Print strings with special characters (newline, tab, etc.)
#
# This exercise covers Python's print() function and string formatting basics.

# ---------- Basic Print ----------
def basic_print():
    """Demonstrate simple print() usage."""
    # Simple string
    print("Hello, World!")

    # Multiple arguments
    print("Python", "is", "awesome")

    # Custom separator
    print("2026", "06", "24", sep="-")

    # Custom end character (no newline)
    print("Loading", end="... ")
    print("Done!")


def main():
    print("=" * 50)
    print("  DAY 1: PRINT STRING")
    print("=" * 50)
    print()

    print(">>> Basic Print <<<")
    basic_print()


if __name__ == "__main__":
    main()
