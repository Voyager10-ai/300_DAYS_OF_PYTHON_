# Day 75: Array Rotate
#
# Problem:
#   Write a Python program / module to perform array rotation operations (left, right, in-place reversal).
#   Includes core rotation solvers, in-place reversal, block swap & juggling algorithms, 2D matrix rotation,
#   rotation cycle analysis engine, batch processors, rotation search & equivalence checkers, unit test suite, and Java practice.

import math
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Left & Right Array Rotation Solvers ─────────────────────────────


def rotate_array(arr: List[Any], k: int, direction: str = "right") -> List[Any]:
    """
    Rotates an array left or right by k positions using array slicing.

    Args:
        arr: Input list.
        k: Number of positions to rotate.
        direction: Rotation direction ('right' or 'left').

    Returns:
        New rotated list.

    Raises:
        TypeError: If inputs are invalid types.
        ValueError: If direction is invalid.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")
    if not isinstance(direction, str):
        raise TypeError(f"Expected str for direction, got {type(direction).__name__}")

    d = direction.lower().strip()
    if d not in ("right", "left"):
        raise ValueError(f"Invalid direction '{direction}'. Choose 'right' or 'left'.")

    n = len(arr)
    if n == 0:
        return []

    shift = k % n
    if shift == 0:
        return list(arr)

    if d == "right":
        return list(arr[-shift:] + arr[:-shift])
    else:  # left
        return list(arr[shift:] + arr[:shift])


def _reverse_slice(arr: List[Any], start: int, end: int) -> None:
    """Helper to reverse elements in arr[start:end+1] in-place."""
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1


def rotate_array_inplace(arr: List[Any], k: int, direction: str = "right") -> None:
    """
    Rotates an array in-place using the 3-step reversal algorithm (O(1) auxiliary space).

    Args:
        arr: Input list to mutate in-place.
        k: Number of positions to rotate.
        direction: Rotation direction ('right' or 'left').

    Raises:
        TypeError: If inputs are invalid.
        ValueError: If direction is invalid.
    """
    if not isinstance(arr, list):
        raise TypeError(f"Expected list for in-place mutation, got {type(arr).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")

    d = direction.lower().strip()
    if d not in ("right", "left"):
        raise ValueError(f"Invalid direction '{direction}'. Choose 'right' or 'left'.")

    n = len(arr)
    if n <= 1:
        return

    shift = k % n
    if shift == 0:
        return

    if d == "right":
        # 1. Reverse entire array
        _reverse_slice(arr, 0, n - 1)
        # 2. Reverse first k elements
        _reverse_slice(arr, 0, shift - 1)
        # 3. Reverse remaining elements
        _reverse_slice(arr, shift, n - 1)
    else:  # left
        # 1. Reverse first k elements
        _reverse_slice(arr, 0, shift - 1)
        # 2. Reverse remaining elements
        _reverse_slice(arr, shift, n - 1)
        # 3. Reverse entire array
        _reverse_slice(arr, 0, n - 1)


# ─── 2. Advanced Rotation Algorithms (Block Swap & Juggling) ─────────────────


def rotate_array_juggling(arr: List[Any], k: int) -> List[Any]:
    """
    Rotates an array left by k positions using the Juggling Algorithm (GCD cycles).

    Args:
        arr: Input list.
        k: Number of left rotation steps.

    Returns:
        New rotated list.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")

    n = len(arr)
    if n <= 1:
        return list(arr)

    shift = k % n
    if shift == 0:
        return list(arr)

    res = list(arr)
    num_cycles = math.gcd(shift, n)

    for i in range(num_cycles):
        temp = res[i]
        j = i
        while True:
            d = (j + shift) % n
            if d == i:
                break
            res[j] = res[d]
            j = d
        res[j] = temp

    return res


def _swap_blocks(arr: List[Any], fi: int, si: int, d: int) -> None:
    """Swaps d elements starting at index fi with d elements starting at index si."""
    for i in range(d):
        arr[fi + i], arr[si + i] = arr[si + i], arr[fi + i]


def rotate_array_block_swap(arr: List[Any], k: int) -> List[Any]:
    """
    Rotates an array left by k positions using the Block Swap Algorithm.

    Args:
        arr: Input list.
        k: Left rotation count.

    Returns:
        New rotated list.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")

    n = len(arr)
    if n <= 1:
        return list(arr)

    d = k % n
    if d == 0:
        return list(arr)

    res = list(arr)
    i = d
    j = n - d

    while i != j:
        if i < j:
            _swap_blocks(res, d - i, d + j - i, i)
            j -= i
        else:
            _swap_blocks(res, d - i, d, j)
            i -= j

    _swap_blocks(res, d - i, d, i)
    return res


# ─── 3. 2D Matrix Rotation & Multidimensional Transform Helpers ─────────────


def rotate_matrix_90(matrix: List[List[Any]], direction: str = "clockwise") -> List[List[Any]]:
    """
    Rotates a 2D matrix (M x N) by 90 degrees clockwise or counterclockwise.

    Args:
        matrix: 2D list of lists.
        direction: 'clockwise' or 'counterclockwise' / 'anti-clockwise'.

    Returns:
        New rotated 2D matrix.

    Raises:
        TypeError: If matrix format is invalid.
        ValueError: If direction is invalid.
    """
    if not isinstance(matrix, (list, tuple)):
        raise TypeError(f"Expected list or tuple for matrix, got {type(matrix).__name__}")
    if not matrix:
        return []

    for row in matrix:
        if not isinstance(row, (list, tuple)):
            raise TypeError(f"Each row must be a list or tuple, got {type(row).__name__}")

    d = direction.lower().strip()
    if d in ("clockwise", "cw"):
        # Transpose then reverse rows
        return [list(col[::-1]) for col in zip(*matrix)]
    elif d in ("counterclockwise", "anti-clockwise", "ccw"):
        # Transpose then reverse cols (reverse overall rows)
        return [list(col) for col in zip(*matrix)][::-1]
    else:
        raise ValueError(f"Invalid direction '{direction}'. Choose 'clockwise' or 'counterclockwise'.")


def rotate_matrix_inplace(matrix: List[List[Any]], direction: str = "clockwise") -> None:
    """
    Rotates an N x N square matrix in-place by 90 degrees.

    Args:
        matrix: Square 2D list of lists to mutate.
        direction: 'clockwise' or 'counterclockwise'.

    Raises:
        TypeError: If matrix is invalid.
        ValueError: If matrix is not square (N x N) or direction is invalid.
    """
    if not isinstance(matrix, list):
        raise TypeError(f"Expected list for matrix, got {type(matrix).__name__}")

    n = len(matrix)
    if n == 0:
        return

    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError("In-place rotation requires a square matrix (N x N).")

    d = direction.lower().strip()
    if d not in ("clockwise", "cw", "counterclockwise", "ccw"):
        raise ValueError(f"Invalid direction '{direction}'.")

    # Step 1: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse rows or columns based on direction
    if d in ("clockwise", "cw"):
        for i in range(n):
            matrix[i].reverse()
    else:
        matrix.reverse()


# ─── 4. Array Rotation Metrics & Cycle Analysis Engine ───────────────────────


def analyze_array_rotation(arr: List[Any], k: int, direction: str = "right") -> Dict[str, Any]:
    """
    Analyzes displacement, effective shift, full cycles, and rotational symmetry of an array.

    Args:
        arr: Target input array.
        k: Shift steps.
        direction: Rotation direction ('right' or 'left').

    Returns:
        Dictionary of rotation metrics.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    if not isinstance(k, int):
        raise TypeError(f"Expected int for k, got {type(k).__name__}")

    n = len(arr)
    if n == 0:
        return {
            "array_length": 0,
            "requested_shift": k,
            "effective_shift": 0,
            "direction": direction,
            "is_full_cycle": True,
            "full_rotations_completed": 0,
            "element_displacement_distance": 0,
            "rotated_array": [],
            "is_symmetric_under_rotation": True,
        }

    effective_shift = k % n
    full_cycles = abs(k) // n
    rotated = rotate_array(arr, k, direction=direction)
    is_symmetric = (rotated == list(arr))

    return {
        "array_length": n,
        "requested_shift": k,
        "effective_shift": effective_shift,
        "direction": direction,
        "is_full_cycle": (effective_shift == 0),
        "full_rotations_completed": full_cycles,
        "element_displacement_distance": effective_shift,
        "rotated_array": rotated,
        "is_symmetric_under_rotation": is_symmetric,
    }


# ─── 5. Batch Collection Processors & Rotation Filters ──────────────────────


def batch_rotate_arrays(
    datasets: List[List[Any]], k: int, direction: str = "right"
) -> List[List[Any]]:
    """
    Applies rotation to a collection of array datasets.

    Args:
        datasets: List of lists.
        k: Shift positions.
        direction: 'right' or 'left'.

    Returns:
        List of rotated lists.

    Raises:
        TypeError: If datasets is not a list or tuple.
    """
    if not isinstance(datasets, (list, tuple)):
        raise TypeError(f"Expected list or tuple of datasets, got {type(datasets).__name__}")

    return [rotate_array(arr, k, direction=direction) for arr in datasets]


def filter_arrays_by_rotation_equivalence(
    datasets: List[List[Any]], target: List[Any]
) -> List[List[Any]]:
    """
    Filters datasets returning only those arrays that are cyclic rotations of target.

    Args:
        datasets: List of candidate arrays.
        target: Reference target array.

    Returns:
        List of qualifying arrays that match target under rotation.

    Raises:
        TypeError: If inputs are invalid.
    """
    if not isinstance(datasets, (list, tuple)):
        raise TypeError(f"Expected list or tuple for datasets, got {type(datasets).__name__}")
    if not isinstance(target, (list, tuple)):
        raise TypeError(f"Expected list or tuple for target, got {type(target).__name__}")

    qualifying: List[List[Any]] = []
    for candidate in datasets:
        if isinstance(candidate, (list, tuple)):
            is_rot, _ = is_rotation_of(candidate, target)
            if is_rot:
                qualifying.append(list(candidate))
    return qualifying


# ─── 6. Rotation Search & Array Equivalence Checkers ─────────────────────────


def is_rotation_of(arr1: List[Any], arr2: List[Any]) -> Tuple[bool, int]:
    """
    Checks whether arr2 is a rotated version of arr1 and returns the shift count.

    Args:
        arr1: Original reference list.
        arr2: Candidate rotated list.

    Returns:
        Tuple of (is_rotation: bool, shift_count: int). If False, shift_count is -1.

    Raises:
        TypeError: If inputs are not lists or tuples.
    """
    if not isinstance(arr1, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr1, got {type(arr1).__name__}")
    if not isinstance(arr2, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr2, got {type(arr2).__name__}")

    n1, n2 = len(arr1), len(arr2)
    if n1 != n2:
        return (False, -1)
    if n1 == 0:
        return (True, 0)

    l1 = list(arr1)
    l2 = list(arr2)

    for shift in range(n1):
        if rotate_array(l1, shift, direction="right") == l2:
            return (True, shift)

    return (False, -1)


def find_rotation_count_sorted(arr: List[int]) -> int:
    """
    Finds how many times a sorted distinct array has been rotated right (Binary Search O(log N)).

    Args:
        arr: Rotated sorted array of distinct integers.

    Returns:
        Number of right rotations (index of minimum element).

    Raises:
        TypeError: If arr is not list or elements are not ints.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError(f"Expected list or tuple for arr, got {type(arr).__name__}")
    for x in arr:
        if not isinstance(x, int):
            raise TypeError(f"All elements in arr must be integers, got {type(x).__name__}")

    n = len(arr)
    if n <= 1:
        return 0

    low, high = 0, n - 1

    while low <= high:
        if arr[low] <= arr[high]:
            return low

        mid = (low + high) // 2
        next_idx = (mid + 1) % n
        prev_idx = (mid - 1 + n) % n

        if arr[mid] <= arr[next_idx] and arr[mid] <= arr[prev_idx]:
            return mid

        if arr[mid] >= arr[low]:
            low = mid + 1
        else:
            high = mid - 1

    return 0





