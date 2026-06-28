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


# ---------- Classification by Angles ----------
def calculate_angles(a, b, c):
    """Calculate all three angles in degrees using the cosine rule."""
    angle_A = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
    angle_B = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
    angle_C = 180 - angle_A - angle_B
    return round(angle_A, 2), round(angle_B, 2), round(angle_C, 2)


def classify_by_angles(a, b, c):
    """Classify triangle as acute, right, or obtuse."""
    sides = sorted([a, b, c])
    a2, b2, c2 = sides[0]**2, sides[1]**2, sides[2]**2

    if abs(a2 + b2 - c2) < 1e-9:
        return "Right (90°)", "🔺"
    elif a2 + b2 > c2:
        return "Acute (all < 90°)", "🔻"
    else:
        return "Obtuse (one > 90°)", "🔶"


def angle_analysis():
    """Analyze angles for various triangles."""
    triangles = [
        (3, 4, 5, "3-4-5"),
        (5, 5, 5, "Equilateral"),
        (7, 10, 5, "Scalene"),
        (3, 4, 6, "Obtuse"),
        (6, 8, 10, "Scaled 3-4-5"),
    ]

    for a, b, c, name in triangles:
        if not is_valid_triangle(a, b, c):
            continue
        angles = calculate_angles(a, b, c)
        angle_type, emoji = classify_by_angles(a, b, c)
        side_type, _ = classify_by_sides(a, b, c)
        print(f"\n   {emoji} Triangle '{name}' ({a}, {b}, {c}):")
        print(f"      Sides:  {side_type}")
        print(f"      Angles: {angle_type}")
        print(f"      A={angles[0]}°, B={angles[1]}°, C={angles[2]}°")
        print(f"      Sum of angles: {sum(angles)}°")


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
    print()

    print(">>> Angle Analysis <<<")
    angle_analysis()
    print()

    print(">>> Triangle Properties <<<")
    triangle_properties(3, 4, 5)
    triangle_properties(5, 5, 5)
    triangle_properties(7, 10, 12)


# ---------- Triangle Properties ----------
def triangle_properties(a, b, c):
    """Calculate and display all properties of a triangle."""
    if not is_valid_triangle(a, b, c):
        print(f"\n   ❌ ({a}, {b}, {c}) is not a valid triangle!")
        return

    # Perimeter
    perimeter = a + b + c
    s = perimeter / 2  # semi-perimeter

    # Area using Heron's formula
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))

    # Heights (from each side)
    h_a = 2 * area / a
    h_b = 2 * area / b
    h_c = 2 * area / c

    # Inradius and circumradius
    inradius = area / s
    circumradius = (a * b * c) / (4 * area)

    side_type, _ = classify_by_sides(a, b, c)
    angle_type, emoji = classify_by_angles(a, b, c)
    angles = calculate_angles(a, b, c)

    print(f"\n   {emoji} Triangle ({a}, {b}, {c}) — {side_type} {angle_type}")
    print(f"   {'─' * 45}")
    print(f"   {'Perimeter:':<20} {perimeter:.2f}")
    print(f"   {'Semi-perimeter:':<20} {s:.2f}")
    print(f"   {'Area (Heron):':<20} {area:.4f}")
    print(f"   {'Height from a:':<20} {h_a:.4f}")
    print(f"   {'Height from b:':<20} {h_b:.4f}")
    print(f"   {'Height from c:':<20} {h_c:.4f}")
    print(f"   {'Inradius:':<20} {inradius:.4f}")
    print(f"   {'Circumradius:':<20} {circumradius:.4f}")
    print(f"   {'Angles:':<20} {angles[0]}°, {angles[1]}°, {angles[2]}°")


if __name__ == "__main__":
    main()
