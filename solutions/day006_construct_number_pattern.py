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


# ---------- Famous Triangles ----------
def floyds_triangle(n=5):
    """Floyd's triangle: consecutive numbers in triangular form."""
    print(f"\n   📐 Floyd's Triangle (n={n}):")
    num = 1
    max_num = n * (n + 1) // 2
    width = len(str(max_num))
    for i in range(1, n + 1):
        row = []
        for _ in range(i):
            row.append(str(num).rjust(width))
            num += 1
        print(f"      {'  '.join(row)}")


def pascals_triangle(n=6):
    """Pascal's triangle using combinatorics."""
    print(f"\n   📐 Pascal's Triangle (n={n}):")
    triangle = []
    for i in range(n):
        row = [1]
        if triangle:
            last_row = triangle[-1]
            row.extend([last_row[j] + last_row[j + 1] for j in range(len(last_row) - 1)])
            row.append(1)
        triangle.append(row)

    max_width = len(" ".join(str(x) for x in triangle[-1]))
    for row in triangle:
        row_str = " ".join(str(x).center(4) for x in row)
        print(f"      {row_str.center(max_width)}")

    print(f"\n   💡 Row sums: {[sum(row) for row in triangle]}")
    print(f"   💡 These are powers of 2: {[2**i for i in range(n)]}")


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
    print()

    print(">>> Famous Triangles <<<")
    floyds_triangle()
    pascals_triangle()


if __name__ == "__main__":
    main()
