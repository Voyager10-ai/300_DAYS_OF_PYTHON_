# Day 14: Triangle Types
#
# Problem:
#   Write a Python program that classifies triangles based on their side lengths.
#   - Check if the given side lengths form a valid triangle (triangle inequality theorem).
#   - Classify the triangle by sides: Equilateral, Isosceles, or Scalene.
#   - Classify the triangle by angles: Right, Acute, or Obtuse (using the Pythagorean theorem).
#   - Calculate the area (using Heron's formula) and perimeter.
#   - Render a custom ASCII triangle visualizer matching the classification.
#   - Provide an interactive exploration tool.
#
# This exercise covers conditional statements, mathematical formulas (Heron's), list sorting,
# validation logic, and ASCII rendering.

import math


# ---------- Triangle Calculations & Classification ----------
def is_valid_triangle(a, b, c):
    """Check if three side lengths satisfy the triangle inequality theorem."""
    return (a + b > c) and (a + c > b) and (b + c > a)


def classify_by_sides(a, b, c):
    """Classify the triangle as Equilateral, Isosceles, or Scalene."""
    if a == b == c:
        return "Equilateral"
    elif a == b or b == c or c == a:
        return "Isosceles"
    else:
        return "Scalene"


def classify_by_angles(a, b, c):
    """
    Classify the triangle as Right, Acute, or Obtuse.
    Applies the Pythagorean relation to sorted sides: x <= y <= z
    """
    sides = sorted([a, b, c])
    x, y, z = sides[0], sides[1], sides[2]
    
    # Using a tolerance for floating point comparisons
    lhs = x**2 + y**2
    rhs = z**2
    
    if math.isclose(lhs, rhs, rel_tol=1e-9):
        return "Right-angled"
    elif lhs > rhs:
        return "Acute-angled"
    else:
        return "Obtuse-angled"


def calculate_properties(a, b, c):
    """Calculate perimeter and area (Heron's Formula)."""
    perimeter = a + b + c
    s = perimeter / 2
    # Area = sqrt(s * (s-a) * (s-b) * (s-c))
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return perimeter, area


# ---------- ASCII Visualizations ----------
def draw_ascii_triangle(side_type, angle_type):
    """Draw a basic ASCII representation of the triangle shape."""
    print("\n   🎨 Visual Representative Shape:")
    if side_type == "Equilateral":
        print("          /\\")
        print("         /  \\")
        print("        /    \\")
        print("       /______\\")
    elif angle_type == "Right-angled":
        print("      |\\")
        print("      | \\")
        print("      |  \\")
        print("      |___\\")
    elif side_type == "Isosceles":
        print("          /\\")
        print("         /  \\")
        print("        /    \\")
        print("       /      \\")
        print("      /________\\")
    else: # Scalene / Obtuse / General
        print("        /\\")
        print("       /   \\_")
        print("      /______\\_")


# ---------- Interactive Features ----------
def analyze_triangle(a, b, c):
    """Analyze and display all details of the triangle."""
    print(f"\n   🔍 Analyzing sides: a = {a}, b = {b}, c = {c}")
    
    if not is_valid_triangle(a, b, c):
        print("      ❌ Invalid Triangle: These sides violate the triangle inequality theorem.")
        print("         Rule: The sum of any two sides must be strictly greater than the third side.")
        return False
        
    side_type = classify_by_sides(a, b, c)
    angle_type = classify_by_angles(a, b, c)
    perimeter, area = calculate_properties(a, b, c)
    
    print(f"      ✅ Valid Triangle found!")
    print(f"      - Classification (Sides):  {side_type}")
    print(f"      - Classification (Angles): {angle_type}")
    print(f"      - Perimeter:               {perimeter:.4f}")
    print(f"      - Area (Heron's Formula):  {area:.4f}")
    
    draw_ascii_triangle(side_type, angle_type)
    return True


def interactive_explorer():
    """Prompt user for inputs and display classification results."""
    print("\n   === Input Triangle Sides ===")
    try:
        a = float(input("      Enter side a: ").strip())
        b = float(input("      Enter side b: ").strip())
        c = float(input("      Enter side c: ").strip())
        
        if a <= 0 or b <= 0 or c <= 0:
            print("      ⚠️  Side lengths must be positive numbers.")
            return
            
        analyze_triangle(a, b, c)
    except ValueError:
        print("      ❌ Invalid input. Please enter valid numeric values.")


def show_mastery_box():
    """Print an artistic summary box."""
    width = 44
    print()
    print("   ╔" + "═" * (width - 2) + "╗")
    print("   ║" + "  📐 TRIANGLE TYPES CLASSIFIER DONE! 📐  ".center(width - 2) + "║")
    print("   ║" + " " * (width - 2) + "║")
    print("   ║" + "  Checks: Inequality Theorem,         ".ljust(width - 2) + "║")
    print("   ║" + "          Sides (Equi/Isos/Scale),    ".ljust(width - 2) + "║")
    print("   ║" + "          Angles (Right/Acute/Obtuse),".ljust(width - 2) + "║")
    print("   ║" + "          Area & Perimeter (Heron's), ".ljust(width - 2) + "║")
    print("   ║" + "          ASCII Representation        ".ljust(width - 2) + "║")
    print("   ╚" + "═" * (width - 2) + "╝")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 14: TRIANGLE TYPES & CLASSIFIER")
    print("=" * 50)
    
    # Run built-in demos
    print("\n>>> Built-in Classification Demos <<<")
    analyze_triangle(3, 4, 5)     # Right / Scalene
    analyze_triangle(5, 5, 5)     # Acute / Equilateral
    analyze_triangle(5, 5, 8)     # Obtuse / Isosceles
    analyze_triangle(1, 2, 4)     # Invalid
    
    # Run interactive explorer
    while True:
        print("\n" + "-" * 50)
        choice = input("      Would you like to try custom sides? (y/n): ").strip().lower()
        if choice == 'y':
            interactive_explorer()
        else:
            print("      Exiting.")
            break
            
    show_mastery_box()


if __name__ == "__main__":
    main()
