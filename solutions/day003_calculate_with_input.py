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


# ---------- Interactive Calculator ----------
def interactive_calculator():
    """A menu-driven calculator that runs until the user quits."""
    operations = {
        "1": ("Addition (+)", lambda a, b: a + b),
        "2": ("Subtraction (-)", lambda a, b: a - b),
        "3": ("Multiplication (×)", lambda a, b: a * b),
        "4": ("Division (÷)", lambda a, b: a / b if b != 0 else "ERROR: Division by zero"),
        "5": ("Power (^)", lambda a, b: a ** b),
        "6": ("Modulus (%)", lambda a, b: a % b if b != 0 else "ERROR: Division by zero"),
    }

    print("🧮 Interactive Calculator")
    print("   Select an operation:")
    for key, (name, _) in operations.items():
        print(f"   [{key}] {name}")
    print("   [q] Quit")

    choice = input("\n   Your choice: ").strip().lower()
    if choice == "q":
        print("   Calculator closed. 👋")
        return

    if choice not in operations:
        print("   ❌ Invalid choice!")
        return

    try:
        a = float(input("   Enter first number:  "))
        b = float(input("   Enter second number: "))
    except ValueError:
        print("   ❌ Invalid number input!")
        return

    name, func = operations[choice]
    result = func(a, b)

    if isinstance(result, str):
        print(f"\n   ❌ {result}")
    else:
        print(f"\n   ✅ {name}")
        print(f"   {a} → {name.split('(')[1][0]} ← {b}")
        print(f"   Result: {result}")
        if isinstance(result, float) and result != int(result):
            print(f"   Rounded: {round(result, 4)}")



# ---------- Advanced Math (math module) ----------
def advanced_math_demo():
    """Demonstrate Python's math module with practical examples."""
    num = float(input("Enter a positive number for math operations: "))

    print(f"\n🔬 Advanced Math for {num}:")
    print(f"   Square root:     √{num} = {math.sqrt(abs(num)):.4f}")
    print(f"   Ceiling:         ⌈{num}⌉ = {math.ceil(num)}")
    print(f"   Floor:           ⌊{num}⌋ = {math.floor(num)}")
    print(f"   Absolute:        |{num}| = {abs(num)}")
    print(f"   Factorial of {min(int(abs(num)), 20)}:  {math.factorial(min(int(abs(num)), 20))}")

    print(f"\n📐 Trigonometry (angle = {num}°):")
    radians = math.radians(num)
    print(f"   sin({num}°) = {math.sin(radians):.6f}")
    print(f"   cos({num}°) = {math.cos(radians):.6f}")
    print(f"   tan({num}°) = {math.tan(radians):.6f}" if num % 90 != 0 or num % 180 == 0 else f"   tan({num}°) = undefined")

    if num > 0:
        print(f"\n📈 Logarithms:")
        print(f"   log₂({num})  = {math.log2(num):.4f}")
        print(f"   log₁₀({num}) = {math.log10(num):.4f}")
        print(f"   ln({num})    = {math.log(num):.4f}")

    print(f"\n🔢 Math Constants:")
    print(f"   π (pi)    = {math.pi}")
    print(f"   e (euler) = {math.e}")
    print(f"   τ (tau)   = {math.tau}")
    print(f"   ∞ (inf)   = {math.inf}")


def compound_interest():
    """Calculate compound interest — a practical financial calculation."""
    print("💰 Compound Interest Calculator:")
    principal = float(input("   Principal amount (₹): "))
    rate = float(input("   Annual interest rate (%): ")) / 100
    years = int(input("   Number of years: "))
    compounds = int(input("   Compounding frequency per year (e.g., 12 for monthly): "))

    amount = principal * (1 + rate / compounds) ** (compounds * years)
    interest_earned = amount - principal

    print(f"\n   📊 Investment Summary:")
    print(f"   {'Principal:':<25} ₹{principal:>12,.2f}")
    print(f"   {'Rate:':<25} {rate * 100:>11.2f}%")
    print(f"   {'Duration:':<25} {years:>10} years")
    print(f"   {'Compounding:':<25} {compounds:>10}x/year")
    print(f"   {'-' * 40}")
    print(f"   {'Final Amount:':<25} ₹{amount:>12,.2f}")
    print(f"   {'Interest Earned:':<25} ₹{interest_earned:>12,.2f}")
    print(f"   {'Growth:':<25} {(amount / principal - 1) * 100:>11.2f}%")


def main():

# ---------- Unit Converter ----------
def unit_converter():
    """A multi-category unit converter."""
    categories = {
        "1": "Temperature",
        "2": "Length",
        "3": "Weight",
    }

    print("🔄 Unit Converter")
    for key, name in categories.items():
        print(f"   [{key}] {name}")

    choice = input("   Select category: ").strip()

    if choice == "1":
        # Temperature
        temp = float(input("   Enter temperature: "))
        unit = input("   From (C/F/K): ").strip().upper()

        if unit == "C":
            f = temp * 9 / 5 + 32
            k = temp + 273.15
            print(f"\n   🌡️  {temp}°C = {f:.2f}°F = {k:.2f}K")
        elif unit == "F":
            c = (temp - 32) * 5 / 9
            k = c + 273.15
            print(f"\n   🌡️  {temp}°F = {c:.2f}°C = {k:.2f}K")
        elif unit == "K":
            c = temp - 273.15
            f = c * 9 / 5 + 32
            print(f"\n   🌡️  {temp}K = {c:.2f}°C = {f:.2f}°F")
        else:
            print("   ❌ Invalid unit!")

    elif choice == "2":
        # Length
        value = float(input("   Enter length in meters: "))
        print(f"\n   📏 {value} meters =")
        print(f"      {value * 100:.2f} centimeters")
        print(f"      {value * 1000:.2f} millimeters")
        print(f"      {value / 1000:.6f} kilometers")
        print(f"      {value * 3.28084:.4f} feet")
        print(f"      {value * 39.3701:.4f} inches")
        print(f"      {value * 1.09361:.4f} yards")
        print(f"      {value * 0.000621371:.6f} miles")

    elif choice == "3":
        # Weight
        value = float(input("   Enter weight in kilograms: "))
        print(f"\n   ⚖️  {value} kg =")
        print(f"      {value * 1000:.2f} grams")
        print(f"      {value * 2.20462:.4f} pounds")
        print(f"      {value * 35.274:.4f} ounces")
        print(f"      {value * 0.157473:.6f} stones")

    else:
        print("   ❌ Invalid category!")


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
    print()

    print(">>> Interactive Calculator <<<")
    interactive_calculator()
    print()

    print(">>> Advanced Math <<<")
    advanced_math_demo()
    print()

    print(">>> Compound Interest <<<")
    compound_interest()
    print()

    print(">>> Unit Converter <<<")
    unit_converter()
if __name__ == "__main__":
    main()
