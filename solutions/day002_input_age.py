# Day 2: Input Age
#
# Problem:
#   Write a Python program that takes a user's age as input and performs
#   various operations on it.
#   - Take age as input from the user
#   - Validate the input (ensure it's a valid age)
#   - Calculate birth year, days lived, and future milestones
#   - Classify the age into life stages
#   - Display fun facts and statistics based on the age
#
# This exercise covers Python's input() function, type conversion,
# validation, and conditional logic.

from datetime import datetime


# ---------- Basic Input ----------
def basic_input():
    """Demonstrate simple input() and type conversion."""
    # input() always returns a string
    age_str = input("Enter your age: ")
    print(f"You entered: {age_str} (type: {type(age_str).__name__})")

    # Convert to integer
    age = int(age_str)
    print(f"Converted:  {age} (type: {type(age).__name__})")

    return age


def get_age_from_birth_year():
    """Calculate age from birth year input."""
    birth_year = int(input("Enter your birth year: "))
    current_year = datetime.now().year
    age = current_year - birth_year
    print(f"Born in {birth_year} → You are approximately {age} years old")
    return age


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 2: INPUT AGE")
    print("=" * 50)
    print()

    print(">>> Basic Input <<<")
    age = basic_input()
    print()

    print(">>> Age from Birth Year <<<")
    get_age_from_birth_year()


if __name__ == "__main__":
    main()
