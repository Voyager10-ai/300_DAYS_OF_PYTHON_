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


# ---------- Row & Column Operations ----------
def matrix_statistics():
    """Calculate statistics for rows and columns."""
    scores = [
        [85, 92, 78, 90],  # Student 1
        [70, 88, 95, 82],  # Student 2
        [90, 76, 88, 94],  # Student 3
        [65, 80, 72, 85],  # Student 4
    ]
    subjects = ["Math", "Sci", "Eng", "Hist"]
    print_matrix(scores, "Student Scores (4 students × 4 subjects)")

    # Row statistics (per student)
    print(f"\n   📊 Per-Student Statistics:")
    print(f"   {'Student':<12} {'Sum':>6} {'Avg':>8} {'Min':>6} {'Max':>6}")
    print(f"   {'-' * 42}")
    for i, row in enumerate(scores):
        print(f"   Student {i + 1:<4} {sum(row):>6} {sum(row)/len(row):>8.1f} {min(row):>6} {max(row):>6}")

    # Column statistics (per subject)
    print(f"\n   📚 Per-Subject Statistics:")
    print(f"   {'Subject':<12} {'Sum':>6} {'Avg':>8} {'Min':>6} {'Max':>6}")
    print(f"   {'-' * 42}")
    for j, subj in enumerate(subjects):
        col = [scores[i][j] for i in range(len(scores))]
        print(f"   {subj:<12} {sum(col):>6} {sum(col)/len(col):>8.1f} {min(col):>6} {max(col):>6}")

    # Grand total
    total = sum(sum(row) for row in scores)
    count = sum(len(row) for row in scores)
    print(f"\n   🏆 Overall: Total = {total}, Average = {total / count:.1f}")


def search_in_matrix():
    """Search for elements in a 2D array."""
    matrix = [
        [15, 22, 38, 41],
        [50, 63, 77, 84],
        [91, 10, 25, 33],
    ]
    print_matrix(matrix, "Search Matrix")

    target = 77
    print(f"\n   🔍 Searching for {target}:")
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == target:
                print(f"   ✅ Found {target} at position [{i}][{j}]")

    # Find all values > 50
    print(f"\n   🔍 Values greater than 50:")
    found = [(i, j, matrix[i][j]) for i in range(len(matrix)) for j in range(len(matrix[i])) if matrix[i][j] > 50]
    for r, c, v in found:
        print(f"      [{r}][{c}] = {v}")



# ---------- Matrix Transformations ----------
def transpose_matrix(matrix):
    """Transpose a matrix (swap rows and columns)."""
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


def rotate_90_clockwise(matrix):
    """Rotate matrix 90 degrees clockwise."""
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]


def flip_horizontal(matrix):
    """Flip matrix horizontally (reverse each row)."""
    return [row[::-1] for row in matrix]


def flip_vertical(matrix):
    """Flip matrix vertically (reverse row order)."""
    return matrix[::-1]


def matrix_transformations():
    """Demonstrate various matrix transformations."""
    original = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    print_matrix(original, "Original")

    transposed = transpose_matrix(original)
    print_matrix(transposed, "Transposed (rows ↔ cols)")

    rotated = rotate_90_clockwise(original)
    print_matrix(rotated, "Rotated 90° Clockwise")

    h_flip = flip_horizontal(original)
    print_matrix(h_flip, "Flipped Horizontal ↔")

    v_flip = flip_vertical(original)
    print_matrix(v_flip, "Flipped Vertical ↕")

    # Non-square transpose
    rect = [[1, 2, 3, 4], [5, 6, 7, 8]]
    print_matrix(rect, "Rectangle (2×4)")
    print_matrix(transpose_matrix(rect), "Transposed (4×2)")


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
    print()

    print(">>> Matrix Statistics <<<")
    matrix_statistics()
    print()

    print(">>> Search in Matrix <<<")
    search_in_matrix()
    print()

    print(">>> Matrix Transformations <<<")
    matrix_transformations()
    print()

    print(">>> Advanced Operations <<<")
    advanced_operations()
    print()

    print(">>> Tic-Tac-Toe Board <<<")
    tic_tac_toe_display()


# ---------- Advanced Operations ----------
def spiral_order(matrix):
    """Traverse a matrix in spiral order."""
    if not matrix:
        return []
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    return result


def matrix_add(a, b):
    """Add two matrices element-wise."""
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def advanced_operations():
    """Demo spiral traversal and matrix arithmetic."""
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print_matrix(m, "Matrix")
    print(f"\n   🌀 Spiral Order: {spiral_order(m)}")

    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    print_matrix(a, "Matrix A")
    print_matrix(b, "Matrix B")
    print_matrix(matrix_add(a, b), "A + B")


# ---------- Creative: Tic-Tac-Toe Board ----------
def tic_tac_toe_display():
    """Display a Tic-Tac-Toe board using a 2D array."""
    board = [
        ["X", "O", "X"],
        ["O", "X", " "],
        [" ", "O", "X"],
    ]

    print("\n   🎮 Tic-Tac-Toe Board:")
    print()
    for i, row in enumerate(board):
        line = " | ".join(f" {cell} " for cell in row)
        print(f"      {line}")
        if i < 2:
            print(f"      {'-----+-------+-----'}")

    # Check winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            print(f"\n   🏆 Row {i + 1} wins: {board[i][0]}!")
            return
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != " ":
            print(f"\n   🏆 Column {j + 1} wins: {board[0][j]}!")
            return
    if board[0][0] == board[1][1] == board[2][2] != " ":
        print(f"\n   🏆 Diagonal wins: {board[1][1]}!")
        return
    if board[0][2] == board[1][1] == board[2][0] != " ":
        print(f"\n   🏆 Anti-diagonal wins: {board[1][1]}!")
        return
    print("\n   🤝 No winner yet — game in progress!")


if __name__ == "__main__":
    main()
