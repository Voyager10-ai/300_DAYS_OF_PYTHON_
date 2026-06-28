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


# ---------- Symmetric Shapes ----------
def symbol_pyramid(height=5, symbol="*"):
    """Print a centered pyramid pattern using the given symbol."""
    print(f"\n   🔺 Symbol Pyramid (height={height}, symbol='{symbol}'):")
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        row = " ".join(symbol for _ in range(2 * i - 1))
        print(f"      {spaces}{row}")


def symbol_diamond(height=5, symbol="*"):
    """Print a diamond pattern using the given symbol."""
    print(f"\n   💎 Symbol Diamond (height={height}, symbol='{symbol}'):")
    # Upper half
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        row = " ".join(symbol for _ in range(2 * i - 1))
        print(f"      {spaces}{row}")
    # Lower half
    for i in range(height - 1, 0, -1):
        spaces = " " * (height - i)
        row = " ".join(symbol for _ in range(2 * i - 1))
        print(f"      {spaces}{row}")


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
    print()

    print(">>> Symmetric Shapes <<<")
    symbol_pyramid(5, "*")
    symbol_diamond(4, "+")


if __name__ == "__main__":
    main()


