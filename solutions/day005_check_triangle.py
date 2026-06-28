# Day 5: Check Triangle
#
# Problem:
#   Write a Python program that checks whether three given sides
#   can form a valid triangle and determines the triangle type.
#   - Validate if three sides form a valid triangle
#   - Classify by sides: equilateral, isosceles, scalene
#   - Classify by angles: acute, right, obtuse
#   - Calculate area, perimeter, and other properties
#   - Visualize triangles with ASCII art
#
# This exercise covers conditional logic, mathematical operations,
# function design, and input validation.

import math


# ---------- Triangle Validation ----------
def is_valid_triangle(a, b, c):
    """Check if three sides can form a valid triangle using the triangle inequality theorem."""
    return a + b > c and a + c > b and b + c > a and a > 0 and b > 0 and c > 0


def validate_and_report(a, b, c):
    """Validate sides and print a detailed report."""
    print(f"\n   📐 Sides: a={a}, b={b}, c={c}")

    # Check positivity
    if a <= 0 or b <= 0 or c <= 0:
        print("   ❌ All sides must be positive numbers!")
        return False

    # Triangle inequality theorem
    checks = [
        (a + b > c, f"   a + b = {a + b} > {c} = c"),
        (a + c > b, f"   a + c = {a + c} > {b} = b"),
        (b + c > a, f"   b + c = {b + c} > {a} = a"),
    ]

    print("   🔍 Triangle Inequality Checks:")
    all_valid = True
    for valid, msg in checks:
        status = "✅" if valid else "❌"
        print(f"      {status} {msg} → {'PASS' if valid else 'FAIL'}")
        if not valid:
            all_valid = False

    if all_valid:
        print("   ✅ Valid triangle!")
    else:
        print("   ❌ NOT a valid triangle!")
    return all_valid


# ---------- Classification by Sides ----------
def classify_by_sides(a, b, c):
    """Classify triangle as equilateral, isosceles, or scalene."""
    if a == b == c:
        return "Equilateral", "All three sides are equal"
    elif a == b or b == c or a == c:
        return "Isosceles", "Exactly two sides are equal"
    else:
        return "Scalene", "All three sides are different"


def demonstrate_validation():
    """Show validation with multiple test cases."""
    test_cases = [
        (3, 4, 5, "Classic right triangle"),
        (5, 5, 5, "Equilateral"),
        (1, 1, 10, "Invalid — too short"),
        (7, 10, 5, "Valid scalene"),
        (0, 3, 4, "Invalid — zero side"),
        (6, 6, 3, "Isosceles"),
    ]

    print(f"   {'Sides':<15} {'Valid?':<8} {'Type':<15} {'Note'}")
    print(f"   {'-' * 55}")
    for a, b, c, note in test_cases:
        valid = is_valid_triangle(a, b, c)
        if valid:
            side_type, _ = classify_by_sides(a, b, c)
        else:
            side_type = "—"
        status = "✅ Yes" if valid else "❌ No"
        print(f"   ({a},{b},{c}){'':>7} {status:<8} {side_type:<15} {note}")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 5: CHECK TRIANGLE")
    print("=" * 50)
    print()

    print(">>> Triangle Validation <<<")
    validate_and_report(3, 4, 5)
    validate_and_report(1, 1, 10)
    print()

    print(">>> Classification Demo <<<")
    demonstrate_validation()


if __name__ == "__main__":
    main()
