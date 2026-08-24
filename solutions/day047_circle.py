# Day 47: Circle
#
# Problem:
#   Write a Python program to create a Circle class that computes area and perimeter (circumference).
#   Includes factory constructors, collision detection, sector/segment calculations,
#   operator overloading, polygon approximation, serialization, unit tests, and Java practice.

import math
import json
import random
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Circle Class Definition ──────────────────────────────────────────


class Circle:
    """
    Represents a 2D geometric Circle defined by a radius and optional center coordinates (x, y).
    """

    def __init__(self, radius: float, center_x: float = 0.0, center_y: float = 0.0):
        """
        Initializes a Circle object.

        Args:
            radius: Radius of the circle (must be >= 0).
            center_x: X-coordinate of the circle center (default 0.0).
            center_y: Y-coordinate of the circle center (default 0.0).

        Raises:
            ValueError: If radius is negative.
        """
        if radius < 0:
            raise ValueError(f"Radius cannot be negative, got {radius}")
        self._radius = float(radius)
        self.center_x = float(center_x)
        self.center_y = float(center_y)

    @property
    def radius(self) -> float:
        """Returns the radius of the circle."""
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        """Sets the radius of the circle."""
        if value < 0:
            raise ValueError(f"Radius cannot be negative, got {value}")
        self._radius = float(value)

    @property
    def diameter(self) -> float:
        """Returns the diameter of the circle."""
        return 2.0 * self._radius

    @diameter.setter
    def diameter(self, value: float) -> None:
        """Sets the diameter of the circle."""
        if value < 0:
            raise ValueError(f"Diameter cannot be negative, got {value}")
        self._radius = float(value) / 2.0

    @property
    def area(self) -> float:
        """Computes and returns the area of the circle (π * r^2)."""
        return math.pi * (self._radius ** 2)

    @property
    def perimeter(self) -> float:
        """Computes and returns the perimeter (circumference) of the circle (2 * π * r)."""
        return 2.0 * math.pi * self._radius

    @property
    def circumference(self) -> float:
        """Alias for perimeter."""
        return self.perimeter
