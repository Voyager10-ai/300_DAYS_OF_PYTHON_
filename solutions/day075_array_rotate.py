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
