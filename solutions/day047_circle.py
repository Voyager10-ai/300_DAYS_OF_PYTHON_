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


# ─── 2. Factory Constructors & Special Creation Methods ────────────────────────


    @classmethod
    def from_diameter(cls, diameter: float, center_x: float = 0.0, center_y: float = 0.0) -> "Circle":
        """Creates a Circle from a given diameter."""
        return cls(radius=diameter / 2.0, center_x=center_x, center_y=center_y)

    @classmethod
    def from_area(cls, area: float, center_x: float = 0.0, center_y: float = 0.0) -> "Circle":
        """Creates a Circle from a given target area."""
        if area < 0:
            raise ValueError(f"Area cannot be negative, got {area}")
        radius = math.sqrt(area / math.pi)
        return cls(radius=radius, center_x=center_x, center_y=center_y)

    @classmethod
    def from_perimeter(cls, perimeter: float, center_x: float = 0.0, center_y: float = 0.0) -> "Circle":
        """Creates a Circle from a given target perimeter (circumference)."""
        if perimeter < 0:
            raise ValueError(f"Perimeter cannot be negative, got {perimeter}")
        radius = perimeter / (2.0 * math.pi)
        return cls(radius=radius, center_x=center_x, center_y=center_y)

    @classmethod
    def from_three_points(
        cls,
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        p3: Tuple[float, float],
    ) -> "Circle":
        """
        Creates a circumcircle passing through three 2D points (x1, y1), (x2, y2), (x3, y3).

        Raises:
            ValueError: If the points are collinear and do not form a unique circle.
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(d) < 1e-9:
            raise ValueError("The three points are collinear; no unique circle exists.")

        ux = (
            (x1**2 + y1**2) * (y2 - y3)
            + (x2**2 + y2**2) * (y3 - y1)
            + (x3**2 + y3**2) * (y1 - y2)
        ) / d
        uy = (
            (x1**2 + y1**2) * (x3 - x2)
            + (x2**2 + y2**2) * (x1 - x3)
            + (x3**2 + y3**2) * (x2 - x1)
        ) / d

        radius = math.hypot(x1 - ux, y1 - uy)
        return cls(radius=radius, center_x=ux, center_y=uy)


# ─── 3. Collision Detection & Spatial Geometry ─────────────────────────────────


    def distance_to_center(self, x: float, y: float) -> float:
        """Calculates Euclidean distance from circle center to point (x, y)."""
        return math.hypot(x - self.center_x, y - self.center_y)

    def distance_between_centers(self, other: "Circle") -> float:
        """Calculates Euclidean distance between centers of two circles."""
        return self.distance_to_center(other.center_x, other.center_y)

    def contains_point(self, x: float, y: float, include_boundary: bool = True) -> bool:
        """
        Checks if a 2D point (x, y) lies inside (or on the boundary of) the circle.

        Args:
            x: X-coordinate of test point.
            y: Y-coordinate of test point.
            include_boundary: If True, points on boundary are considered inside.

        Returns:
            True if point is contained, False otherwise.
        """
        dist = self.distance_to_center(x, y)
        if include_boundary:
            return dist <= self._radius + 1e-9
        return dist < self._radius - 1e-9

    def contains_circle(self, other: "Circle") -> bool:
        """Checks if another circle is completely contained within this circle."""
        dist = self.distance_between_centers(other)
        return dist + other.radius <= self._radius + 1e-9

    def intersects_circle(self, other: "Circle") -> bool:
        """
        Checks if this circle intersects or touches another circle.

        Returns:
            True if circles overlap or touch, False otherwise.
        """
        dist = self.distance_between_centers(other)
        return (abs(self.radius - other.radius) - 1e-9 <= dist <= self.radius + other.radius + 1e-9)

    def concentric_with(self, other: "Circle", tolerance: float = 1e-7) -> bool:
        """Checks if two circles share the same center coordinates within tolerance."""
        return self.distance_between_centers(other) <= tolerance

    def bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Calculates the axis-aligned bounding box (AABB) of the circle.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        return (
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
        )


