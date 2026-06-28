# Day 6: Construct Number Pattern
#
# Problem:
#   Write a Python program that generates various number patterns
#   using nested loops.
#   - Simple increasing number triangle
#   - Floyd's triangle
#   - Pascal's triangle
#   - Number pyramid and diamond patterns
#   - Creative and artistic number arrangements
#
# This exercise covers nested loops, formatting, mathematical sequences,
# and pattern recognition.


# ---------- Basic Number Patterns ----------
def increasing_triangle(n=5):
    """Numbers increasing across rows: 1 / 1 2 / 1 2 3 / ..."""
    print(f"\n   📐 Increasing Triangle (n={n}):")
    for i in range(1, n + 1):
        row = " ".join(str(j) for j in range(1, i + 1))
        print(f"      {row}")


def repeated_number_triangle(n=5):
    """Each row repeats its row number: 1 / 2 2 / 3 3 3 / ..."""
    print(f"\n   📐 Repeated Number Triangle (n={n}):")
    for i in range(1, n + 1):
        row = " ".join(str(i) for _ in range(i))
        print(f"      {row}")


def right_aligned_triangle(n=5):
    """Right-aligned number triangle."""
    print(f"\n   📐 Right-Aligned Triangle (n={n}):")
    for i in range(1, n + 1):
        spaces = "  " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(f"      {spaces}{nums}")


def continuous_triangle(n=5):
    """Numbers flow continuously across rows: 1 / 2 3 / 4 5 6 / ..."""
    print(f"\n   📐 Continuous Number Triangle (n={n}):")
    num = 1
    for i in range(1, n + 1):
        row = []
        for _ in range(i):
            row.append(str(num))
            num += 1
        print(f"      {' '.join(row)}")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 6: CONSTRUCT NUMBER PATTERN")
    print("=" * 50)
    print()

    print(">>> Basic Number Patterns <<<")
    increasing_triangle()
    repeated_number_triangle()
    right_aligned_triangle()
    continuous_triangle()


if __name__ == "__main__":
    main()
