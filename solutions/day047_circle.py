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


# ─── 4. Arc, Sector, Segment & Chord Trigonometry ──────────────────────────────


    def arc_length(self, angle_degrees: float) -> float:
        """
        Calculates arc length for a given central angle in degrees.

        Args:
            angle_degrees: Central angle in degrees (0 to 360).

        Returns:
            Arc length string value.
        """
        rad = math.radians(angle_degrees)
        return self.radius * abs(rad)

    def sector_area(self, angle_degrees: float) -> float:
        """
        Calculates the area of a circular sector for a given angle in degrees.

        Args:
            angle_degrees: Central angle in degrees.

        Returns:
            Sector area value.
        """
        return 0.5 * (self.radius ** 2) * abs(math.radians(angle_degrees))

    def chord_length(self, angle_degrees: float) -> float:
        """
        Calculates length of a chord subtended by central angle in degrees (2 * r * sin(θ/2)).

        Args:
            angle_degrees: Central angle in degrees.

        Returns:
            Chord length.
        """
        rad = math.radians(angle_degrees)
        return 2.0 * self.radius * math.sin(abs(rad) / 2.0)

    def segment_area(self, angle_degrees: float) -> float:
        """
        Calculates the area of a circular segment (region bounded by chord and arc).

        Args:
            angle_degrees: Central angle in degrees.

        Returns:
            Segment area value.
        """
        rad = abs(math.radians(angle_degrees))
        sector = 0.5 * (self.radius ** 2) * rad
        triangle = 0.5 * (self.radius ** 2) * math.sin(rad)
        return sector - triangle


# ─── 5. Operator Overloading & Dunder Magic Methods ────────────────────────────


    def __repr__(self) -> str:
        return f"Circle(radius={self.radius}, center_x={self.center_x}, center_y={self.center_y})"

    def __str__(self) -> str:
        return f"Circle(r={self.radius:.2f}, center=({self.center_x:.2f}, {self.center_y:.2f}), area={self.area:.2f})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Circle):
            return False
        return (
            math.isclose(self.radius, other.radius, rel_tol=1e-7)
            and math.isclose(self.center_x, other.center_x, rel_tol=1e-7)
            and math.isclose(self.center_y, other.center_y, rel_tol=1e-7)
        )

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius <= other.radius

    def __add__(self, other: Any) -> "Circle":
        """Adds areas of two circles to form a new combined Circle."""
        if isinstance(other, Circle):
            new_radius = math.sqrt(self.radius**2 + other.radius**2)
            return Circle(radius=new_radius, center_x=self.center_x, center_y=self.center_y)
        elif isinstance(other, (int, float)):
            return Circle(radius=self.radius + float(other), center_x=self.center_x, center_y=self.center_y)
        return NotImplemented

    def __mul__(self, factor: float) -> "Circle":
        """Scales circle radius by a scalar factor."""
        if not isinstance(factor, (int, float)):
            return NotImplemented
        if factor < 0:
            raise ValueError(f"Scaling factor cannot be negative, got {factor}")
        return Circle(radius=self.radius * float(factor), center_x=self.center_x, center_y=self.center_y)

    def __rmul__(self, factor: float) -> "Circle":
        return self.__mul__(factor)


# ─── 6. Polygon Approximation & Point Sampling Utilities ───────────────────────


    def approximate_polygon(self, n_vertices: int = 36) -> List[Tuple[float, float]]:
        """
        Approximates circle with an inscribed regular n-gon of vertices.

        Args:
            n_vertices: Number of polygon vertices (must be >= 3).

        Returns:
            List of (x, y) vertex coordinates.
        """
        if n_vertices < 3:
            raise ValueError(f"n_vertices must be at least 3, got {n_vertices}")

        vertices: List[Tuple[float, float]] = []
        angle_step = (2.0 * math.pi) / n_vertices
        for i in range(n_vertices):
            angle = i * angle_step
            vx = self.center_x + self.radius * math.cos(angle)
            vy = self.center_y + self.radius * math.sin(angle)
            vertices.append((vx, vy))
        return vertices

    def sample_points_on_perimeter(self, n_points: int = 12) -> List[Tuple[float, float]]:
        """Samples n evenly spaced 2D points along the circle perimeter."""
        return self.approximate_polygon(n_vertices=n_points)

    def sample_random_interior_point(self, seed: Optional[int] = None) -> Tuple[float, float]:
        """
        Samples a 2D point uniformly at random within the interior of the circle.

        Args:
            seed: Optional random seed.

        Returns:
            Tuple of (x, y) coordinates inside circle.
        """
        rng = random.Random(seed)
        u = rng.random()
        v = rng.random()
        r = self.radius * math.sqrt(u)
        theta = 2.0 * math.pi * v
        return (self.center_x + r * math.cos(theta), self.center_y + r * math.sin(theta))


# ─── 7. Serialization & Report Formatting ──────────────────────────────────────


    def to_dict(self) -> Dict[str, Any]:
        """Converts circle parameters and computed geometric properties into a dictionary."""
        return {
            "radius": self.radius,
            "diameter": self.diameter,
            "center": {"x": self.center_x, "y": self.center_y},
            "area": round(self.area, 6),
            "perimeter": round(self.perimeter, 6),
            "bounding_box": self.bounding_box(),
        }

    def to_json(self, indent: int = 2) -> str:
        """Serializes circle representation into a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Circle":
        """Instantiates a Circle from a dictionary payload."""
        radius = data["radius"]
        center = data.get("center", {"x": 0.0, "y": 0.0})
        return cls(radius=radius, center_x=center.get("x", 0.0), center_y=center.get("y", 0.0))

    @classmethod
    def from_json(cls, json_str: str) -> "Circle":
        """Instantiates a Circle from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def format_report(self) -> str:
        """Formats a clean summary report string for the Circle object."""
        min_x, min_y, max_x, max_y = self.bounding_box()
        lines = [
            f"=== 🔴 Circle Geometry Summary Report ===",
            f"  Center Coordinates : ({self.center_x:.4f}, {self.center_y:.4f})",
            f"  Radius (r)         : {self.radius:.4f}",
            f"  Diameter (d)       : {self.diameter:.4f}",
            f"  Area (A)           : {self.area:.4f} sq units",
            f"  Perimeter (C)      : {self.perimeter:.4f} units",
            f"  Bounding Box AABB  : X:[{min_x:.2f}, {max_x:.2f}], Y:[{min_y:.2f}, {max_y:.2f}]",
            f"========================================",
        ]
        return "\n".join(lines)


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestCircleOperations(unittest.TestCase):
    def setUp(self):
        self.c1 = Circle(radius=5.0, center_x=0.0, center_y=0.0)
        self.c2 = Circle(radius=3.0, center_x=4.0, center_y=0.0)

    def test_circle_basic_properties(self):
        c = Circle(5.0)
        self.assertEqual(c.radius, 5.0)
        self.assertEqual(c.diameter, 10.0)
        self.assertAlmostEqual(c.area, math.pi * 25.0)
        self.assertAlmostEqual(c.perimeter, 2.0 * math.pi * 5.0)

        c.diameter = 12.0
        self.assertEqual(c.radius, 6.0)

    def test_negative_radius_raises_error(self):
        with self.assertRaises(ValueError):
            Circle(-1.0)
        with self.assertRaises(ValueError):
            Circle.from_area(-10.0)

    def test_factory_constructors(self):
        c_dia = Circle.from_diameter(10.0)
        self.assertEqual(c_dia.radius, 5.0)

        c_area = Circle.from_area(math.pi * 16.0)
        self.assertAlmostEqual(c_area.radius, 4.0)

        c_perim = Circle.from_perimeter(2.0 * math.pi * 7.0)
        self.assertAlmostEqual(c_perim.radius, 7.0)

        c_3pts = Circle.from_three_points((0, 1), (1, 0), (0, -1))
        self.assertAlmostEqual(c_3pts.radius, 1.0)
        self.assertAlmostEqual(c_3pts.center_x, 0.0)
        self.assertAlmostEqual(c_3pts.center_y, 0.0)

    def test_collision_and_spatial_methods(self):
        self.assertTrue(self.c1.contains_point(3.0, 4.0))
        self.assertFalse(self.c1.contains_point(6.0, 0.0))

        # Intersection test
        self.assertTrue(self.c1.intersects_circle(self.c2))

        # Bounding box
        bbox = self.c1.bounding_box()
        self.assertEqual(bbox, (-5.0, -5.0, 5.0, 5.0))

    def test_sector_and_segment_trigonometry(self):
        c = Circle(10.0)
        self.assertAlmostEqual(c.arc_length(180), math.pi * 10.0)
        self.assertAlmostEqual(c.sector_area(180), 0.5 * math.pi * 100.0)

    def test_operator_overloading(self):
        c_sum = self.c1 + self.c2  # r1=5 (area 25pi), r2=3 (area 9pi) -> combined area 34pi -> r = sqrt(34)
        self.assertAlmostEqual(c_sum.radius, math.sqrt(34))

        c_scaled = self.c1 * 2.0
        self.assertEqual(c_scaled.radius, 10.0)

        self.assertTrue(self.c2 < self.c1)

    def test_polygon_and_sampling(self):
        vertices = self.c1.approximate_polygon(n_vertices=4)
        self.assertEqual(len(vertices), 4)

        pt = self.c1.sample_random_interior_point(seed=42)
        self.assertTrue(self.c1.contains_point(pt[0], pt[1]))

    def test_serialization(self):
        json_str = self.c1.to_json()
        restored = Circle.from_json(json_str)
        self.assertEqual(self.c1, restored)

        report = self.c1.format_report()
        self.assertIn("Circle Geometry Summary Report", report)


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" 🔴 Day 47: Circle Geometry & Area/Perimeter Calculator - Demo")
    print("=" * 60)

    # 1. Circle Properties
    c = Circle(radius=7.5, center_x=2.0, center_y=3.0)
    print("\n1. Circle Properties & Computations:")
    print(f"   Radius       : {c.radius}")
    print(f"   Diameter     : {c.diameter}")
    print(f"   Area         : {c.area:.4f} sq units")
    print(f"   Perimeter    : {c.perimeter:.4f} units")
    print(f"   Bounding Box : {c.bounding_box()}")

    # 2. Sector & Trigonometry
    angle = 60.0
    print(f"\n2. Sector & Trigonometric Computations (Angle = {angle}°):")
    print(f"   Arc Length   : {c.arc_length(angle):.4f}")
    print(f"   Sector Area  : {c.sector_area(angle):.4f}")
    print(f"   Chord Length : {c.chord_length(angle):.4f}")
    print(f"   Segment Area : {c.segment_area(angle):.4f}")

    # 3. Factory Constructors
    c3 = Circle.from_three_points((0, 3), (3, 0), (0, -3))
    print(f"\n3. Circumcircle from 3 Points (0,3), (3,0), (0,-3):")
    print(f"   Radius : {c3.radius:.4f}, Center: ({c3.center_x}, {c3.center_y})")

    # 4. Summary Report Output
    print("\n4. Formatted Summary Report:")
    print(c.format_report())

    # 5. Unit Test Suite Execution
    print("\n5. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCircleOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








