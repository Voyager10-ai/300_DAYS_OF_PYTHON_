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



# ---------- Multi-line & Special Characters ----------
def multiline_print():
    """Demonstrate multi-line strings and escape characters."""
    # Triple-quoted multi-line string
    poem = """Roses are red,
Violets are blue,
Python is great,
And so are you!"""
    print(poem)
    print()

    # Escape characters
    print("Tab\tseparated\tvalues")
    print("Line1\nLine2\nLine3")
    print("She said, \"Hello!\"")
    print('It\'s a beautiful day')

    # Raw string (no escape processing)
    print(r"Raw string: \n is not a newline here")


# ---------- Creative & Artistic Printing ----------
def creative_print():
    """Demonstrate string repetition, centering, and artistic output."""
    # String repetition
    print("*" * 40)
    print("Python".center(40, "-"))
    print("*" * 40)
    print()

    # Box drawing
    width = 30
    print("+" + "-" * (width - 2) + "+")
    print("|" + "300 Days of Python".center(width - 2) + "|")
    print("|" + "Day 1: Print String".center(width - 2) + "|")
    print("+" + "-" * (width - 2) + "+")
    print()

    # Emoji-style art with Unicode
    print("\U0001F40D Python is amazing! \U0001F680")


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
    print()

    print(">>> Multi-line & Special Characters <<<")
    multiline_print()
    print()

    print(">>> Creative & Artistic <<<")
    creative_print()


if __name__ == "__main__":
    main()
