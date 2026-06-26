# Day 4: 2 Dimensional Array
#
# Problem:
#   Write a Python program that demonstrates working with 2D arrays
#   (lists of lists) in Python.
#   - Create and initialize 2D arrays
#   - Access elements by row and column
#   - Perform row/column operations (sum, average, search)
#   - Transpose, rotate, and reshape matrices
#   - Build a practical grid-based application
#
# This exercise covers nested lists, list comprehensions, iteration
# patterns, and matrix operations in Python.


# ---------- Creating & Displaying 2D Arrays ----------
def print_matrix(matrix, title="Matrix"):
    """Pretty-print a 2D array with aligned columns."""
    print(f"\n   {title}:")
    if not matrix:
        print("   (empty)")
        return
    col_width = max(len(str(val)) for row in matrix for val in row) + 2
    for row in matrix:
        print("   " + "".join(str(val).center(col_width) for val in row))


def create_2d_arrays():
    """Demonstrate different ways to create 2D arrays."""
    # Method 1: Direct initialization
    grid_3x3 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    print_matrix(grid_3x3, "Direct Init (3×3)")

    # Method 2: List comprehension
    zeros = [[0 for _ in range(4)] for _ in range(3)]
    print_matrix(zeros, "Zeros (3×4)")

    # Method 3: Multiplication table
    mult_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
    print_matrix(mult_table, "Multiplication Table (5×5)")

    # Method 4: Identity matrix
    size = 4
    identity = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    print_matrix(identity, f"Identity Matrix ({size}×{size})")

    return grid_3x3, mult_table


def access_elements():
    """Show how to access rows, columns, and individual elements."""
    matrix = [
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90],
    ]
    print_matrix(matrix, "Sample Matrix")

    print(f"\n   📍 Accessing Elements:")
    print(f"      matrix[0][0] = {matrix[0][0]}  (top-left)")
    print(f"      matrix[1][1] = {matrix[1][1]}  (center)")
    print(f"      matrix[2][2] = {matrix[2][2]}  (bottom-right)")
    print(f"      matrix[0]    = {matrix[0]}  (first row)")
    print(f"      matrix[-1]   = {matrix[-1]}  (last row)")

    # Access a column
    col_1 = [row[1] for row in matrix]
    print(f"      column[1]    = {col_1}  (middle column)")

    # Diagonal
    diagonal = [matrix[i][i] for i in range(len(matrix))]
    print(f"      diagonal     = {diagonal}  (main diagonal)")


def main():
    """Entry point for the program."""
    print("=" * 50)
    print("  DAY 4: 2 DIMENSIONAL ARRAY")
    print("=" * 50)
    print()

    print(">>> Creating 2D Arrays <<<")
    create_2d_arrays()
    print()

    print(">>> Accessing Elements <<<")
    access_elements()


if __name__ == "__main__":
    main()
