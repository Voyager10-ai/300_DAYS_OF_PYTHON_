# Day 3: Calculate with Input
#
# Problem:
#   Write a Python program that takes numeric input from the user and
#   performs various calculations.
#   - Basic arithmetic operations (add, subtract, multiply, divide)
#   - Handle edge cases like division by zero
#   - Build a simple interactive calculator
#   - Demonstrate operator precedence and advanced math operations
#   - Create a unit converter using calculations
#
# This exercise covers arithmetic operators, math module, input handling,
# and building interactive programs.

import math


# ---------- Basic Arithmetic ----------
def basic_arithmetic():
    """Demonstrate all arithmetic operators with user input."""
    print("Enter two numbers for arithmetic operations:")
    a = float(input("  Number 1: "))
    b = float(input("  Number 2: "))

    print(f"\n📐 Arithmetic Results for {a} and {b}:")
    print(f"   Addition:        {a} + {b} = {a + b}")
    print(f"   Subtraction:     {a} - {b} = {a - b}")
    print(f"   Multiplication:  {a} × {b} = {a * b}")

    # Handle division by zero
    if b != 0:
        print(f"   Division:        {a} ÷ {b} = {a / b:.4f}")
        print(f"   Floor Division:  {a} // {b} = {a // b}")
        print(f"   Modulus:         {a} % {b} = {a % b}")
    else:
        print("   Division:        ❌ Cannot divide by zero!")
        print("   Floor Division:  ❌ Cannot divide by zero!")
        print("   Modulus:         ❌ Cannot divide by zero!")

    print(f"   Exponentiation:  {a} ** {b} = {a ** b}")

    return a, b


def demonstrate_operators():
    """Show all operators with hardcoded values (no input needed)."""
    print("📊 Operator Precedence Demo:")
    expressions = [
        ("2 + 3 * 4", 2 + 3 * 4),
        ("(2 + 3) * 4", (2 + 3) * 4),
        ("10 - 2 ** 3", 10 - 2 ** 3),
        ("15 // 4 + 7 % 3", 15 // 4 + 7 % 3),
        ("2 ** 3 ** 2", 2 ** 3 ** 2),
        ("(2 ** 3) ** 2", (2 ** 3) ** 2),
    ]
    print(f"   {'Expression':<25} {'Result':>10}")
    print(f"   {'-' * 25} {'-' * 10}")
    for expr, result in expressions:
        print(f"   {expr:<25} {result:>10}")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 3: CALCULATE WITH INPUT")
    print("=" * 50)
    print()

    print(">>> Basic Arithmetic <<<")
    basic_arithmetic()
    print()

    print(">>> Operator Precedence <<<")
    demonstrate_operators()


if __name__ == "__main__":
    main()
