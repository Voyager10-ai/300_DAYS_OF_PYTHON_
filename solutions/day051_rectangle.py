# Day 51: Rectangle
#
# Problem:
#   Write a Python program to create a Rectangle class with attributes length and width,
#   and methods to compute area, perimeter, diagonal, and check if it is a square.
#   Includes factory constructors, collision detection, geometric transformations,
#   operator overloading, serialization, unit tests, and Java practice.

import math
import json
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Rectangle Class Definition ────────────────────────────────────────


class Rectangle:
    """
    Represents a 2D axis-aligned Rectangle defined by length (width in x-axis) and width (height in y-axis)
    and optional bottom-left corner position (x, y).
    """

    def __init__(self, length: float, width: float, x: float = 0.0, y: float = 0.0):
        """
        Initializes a Rectangle object.

        Args:
            length: Length (x-dimension / horizontal side, must be >= 0).
            width: Width (y-dimension / vertical side, must be >= 0).
            x: X-coordinate of bottom-left corner (default 0.0).
            y: Y-coordinate of bottom-left corner (default 0.0).

        Raises:
            ValueError: If length or width is negative.
        """
        if length < 0:
            raise ValueError(f"Length cannot be negative, got {length}")
        if width < 0:
            raise ValueError(f"Width cannot be negative, got {width}")

        self._length = float(length)
        self._width = float(width)
        self.x = float(x)
        self.y = float(y)

    @property
    def length(self) -> float:
        """Returns length of the rectangle."""
        return self._length

    @length.setter
    def length(self, value: float) -> None:
        """Sets length of the rectangle."""
        if value < 0:
            raise ValueError(f"Length cannot be negative, got {value}")
        self._length = float(value)

    @property
    def width(self) -> float:
        """Returns width of the rectangle."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Sets width of the rectangle."""
        if value < 0:
            raise ValueError(f"Width cannot be negative, got {value}")
        self._width = float(value)

    @property
    def area(self) -> float:
        """Computes and returns area of rectangle (length * width)."""
        return self._length * self._width

    @property
    def perimeter(self) -> float:
        """Computes and returns perimeter of rectangle (2 * (length + width))."""
        return 2.0 * (self._length + self._width)

    @property
    def diagonal(self) -> float:
        """Computes and returns diagonal length (sqrt(length^2 + width^2))."""
        return math.hypot(self._length, self._width)

    @property
    def is_square(self) -> bool:
        """Checks if rectangle is a square (length == width within tolerance)."""
        return math.isclose(self._length, self._width, rel_tol=1e-7)


# ─── 2. Factory Constructors & Creation Utilities ──────────────────────────────


    @classmethod
    def from_square(cls, side: float, x: float = 0.0, y: float = 0.0) -> "Rectangle":
        """Creates a square Rectangle with equal sides."""
        return cls(length=side, width=side, x=x, y=y)

    @classmethod
    def from_points(cls, p1: Tuple[float, float], p2: Tuple[float, float]) -> "Rectangle":
        """
        Creates a Rectangle from two opposite diagonal corner points (x1, y1) and (x2, y2).
        """
        x1, y1 = p1
        x2, y2 = p2
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        return cls(length=max_x - min_x, width=max_y - min_y, x=min_x, y=min_y)

    @classmethod
    def from_area_aspect_ratio(
        cls,
        area: float,
        aspect_ratio: float = 1.0,
        x: float = 0.0,
        y: float = 0.0,
    ) -> "Rectangle":
        """
        Creates a Rectangle given target area and aspect ratio (length / width).

        Raises:
            ValueError: If area or aspect_ratio <= 0.
        """
        if area < 0:
            raise ValueError(f"Area cannot be negative, got {area}")
        if aspect_ratio <= 0:
            raise ValueError(f"Aspect ratio must be positive, got {aspect_ratio}")

        width = math.sqrt(area / aspect_ratio)
        length = width * aspect_ratio
        return cls(length=length, width=width, x=x, y=y)

