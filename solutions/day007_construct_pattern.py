# Day 7: Construct Pattern
#
# Problem:
#   Write a Python program that constructs various symbol and character patterns
#   using nested loops and string manipulations.
#   - Simple solid shapes (squares, right triangles)
#   - Symmetric shapes (pyramids, diamonds)
#   - Hollow patterns (hollow squares, hollow triangles)
#   - Complex symbols patterns (butterfly, checkerboard)
#   - Creative/advanced generative ASCII art and grids
#
# This exercise covers loops, conditional formatting, and grid coordinate mappings.


# ---------- Basic Solid Shapes ----------
def solid_square(size=5, symbol="*"):
    """Print a solid square pattern."""
    print(f"\n   ⏹️  Solid Square ({size}x{size}, symbol='{symbol}'):")
    for _ in range(size):
        print("      " + " ".join(symbol for _ in range(size)))


def right_triangle(size=5, symbol="*"):
    """Print a left-aligned right triangle."""
    print(f"\n   📐 Right Triangle (size={size}, symbol='{symbol}'):")
    for i in range(1, size + 1):
        print("      " + " ".join(symbol for _ in range(i)))


def inverted_right_triangle(size=5, symbol="*"):
    """Print an inverted right triangle."""
    print(f"\n   📐 Inverted Right Triangle (size={size}, symbol='{symbol}'):")
    for i in range(size, 0, -1):
        print("      " + " ".join(symbol for _ in range(i)))


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 7: CONSTRUCT PATTERN")
    print("=" * 50)
    print()

    print(">>> Basic Solid Shapes <<<")
    solid_square(5, "*")
    right_triangle(5, "#")
    inverted_right_triangle(5, "@")


if __name__ == "__main__":
    main()

