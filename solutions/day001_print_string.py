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


# ---------- String Formatting ----------
def formatted_print():
    """Demonstrate Python's three string formatting approaches."""
    name = "Pradnyesh"
    age = 21
    gpa = 9.85

    # f-string (Python 3.6+) — the modern, preferred way
    print(f"Name: {name}, Age: {age}, GPA: {gpa:.1f}")

    # .format() method
    print("Name: {}, Age: {}, GPA: {:.1f}".format(name, age, gpa))

    # % formatting (old-style, C-like)
    print("Name: %s, Age: %d, GPA: %.1f" % (name, age, gpa))

    # f-string with expressions
    print(f"{name.upper()} will be {age + 5} in 5 years")



def main():
    print("=" * 50)
    print("  DAY 1: PRINT STRING")
    print("=" * 50)
    print()

    print(">>> Basic Print <<<")
    basic_print()
    print()

    print(">>> Formatted Print <<<")
    formatted_print()


if __name__ == "__main__":
    main()
