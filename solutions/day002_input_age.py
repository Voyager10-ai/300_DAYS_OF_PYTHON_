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


# ---------- Validation & Error Handling ----------
def validate_age(age_str):
    """Validate that the input is a valid age. Returns (is_valid, age_or_error)."""
    # Check if it's a number at all
    try:
        age = int(age_str)
    except ValueError:
        return False, f"'{age_str}' is not a valid integer"

    # Check reasonable range
    if age < 0:
        return False, "Age cannot be negative"
    if age > 150:
        return False, "Age cannot exceed 150 (oldest recorded: 122)"
    return True, age


def get_validated_age():
    """Keep asking until the user provides a valid age."""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        age_str = input(f"Enter your age (attempt {attempt}/{max_attempts}): ")
        is_valid, result = validate_age(age_str)
        if is_valid:
            print(f"✅ Valid age: {result}")
            return result
        else:
            print(f"❌ Invalid: {result}")
    print("Too many invalid attempts. Using default age of 25.")
    return 25


def demonstrate_validation():
    """Show validation with various test cases (no user input needed)."""
    test_cases = ["25", "abc", "-5", "200", "0", "17", "3.5", ""]
    print(f"{'Input':<10} {'Valid?':<8} {'Result'}")
    print("-" * 40)
    for test in test_cases:
        is_valid, result = validate_age(test)
        status = "✅ Yes" if is_valid else "❌ No"
        print(f"{repr(test):<10} {status:<8} {result}")


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
    print()

    print(">>> Validation Demo <<<")
    demonstrate_validation()


if __name__ == "__main__":
    main()
