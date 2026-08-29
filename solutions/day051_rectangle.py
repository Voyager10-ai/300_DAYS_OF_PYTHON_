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


# ─── 3. Collision Detection & Spatial Geometry ─────────────────────────────────


    def bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Calculates axis-aligned bounding box tuple (min_x, min_y, max_x, max_y).
        """
        return (self.x, self.y, self.x + self.length, self.y + self.width)

    def contains_point(self, px: float, py: float, include_boundary: bool = True) -> bool:
        """
        Checks if a 2D point (px, py) lies inside or on boundary of rectangle.

        Args:
            px: X-coordinate of test point.
            py: Y-coordinate of test point.
            include_boundary: If True, points on edge are inside.

        Returns:
            True if contained, False otherwise.
        """
        min_x, min_y, max_x, max_y = self.bounding_box()
        if include_boundary:
            return min_x - 1e-9 <= px <= max_x + 1e-9 and min_y - 1e-9 <= py <= max_y + 1e-9
        return min_x + 1e-9 < px < max_x - 1e-9 and min_y + 1e-9 < py < max_y - 1e-9

    def contains_rectangle(self, other: "Rectangle") -> bool:
        """Checks if another rectangle is completely enclosed within this rectangle."""
        min_x, min_y, max_x, max_y = self.bounding_box()
        o_min_x, o_min_y, o_max_x, o_max_y = other.bounding_box()
        return (
            min_x - 1e-9 <= o_min_x
            and o_max_x <= max_x + 1e-9
            and min_y - 1e-9 <= o_min_y
            and o_max_y <= max_y + 1e-9
        )

    def intersects_rectangle(self, other: "Rectangle") -> bool:
        """Checks if this rectangle overlaps or touches another rectangle."""
        min_x, min_y, max_x, max_y = self.bounding_box()
        o_min_x, o_min_y, o_max_x, o_max_y = other.bounding_box()
        return not (max_x < o_min_x or o_max_x < min_x or max_y < o_min_y or o_max_y < min_y)

    def intersection_rectangle(self, other: "Rectangle") -> Optional["Rectangle"]:
        """
        Computes overlapping Rectangle region between this and another rectangle.

        Returns:
            Intersecting Rectangle object, or None if no overlap.
        """
        if not self.intersects_rectangle(other):
            return None

        min_x, min_y, max_x, max_y = self.bounding_box()
        o_min_x, o_min_y, o_max_x, o_max_y = other.bounding_box()

        int_min_x = max(min_x, o_min_x)
        int_max_x = min(max_x, o_max_x)
        int_min_y = max(min_y, o_min_y)
        int_max_y = min(max_y, o_max_y)

        if int_max_x < int_min_x or int_max_y < int_min_y:
            return None

        return Rectangle(
            length=int_max_x - int_min_x,
            width=int_max_y - int_min_y,
            x=int_min_x,
            y=int_min_y,
        )


# ─── 4. Geometric Transformations ──────────────────────────────────────────────


    def aspect_ratio(self) -> float:
        """Returns aspect ratio (length / width). Returns float('inf') if width == 0."""
        if self._width == 0:
            return float("inf")
        return self._length / self._width

    def scale(self, factor_x: float, factor_y: Optional[float] = None) -> "Rectangle":
        """
        Returns a new scaled Rectangle.

        Args:
            factor_x: Scaling factor for length.
            factor_y: Scaling factor for width (defaults to factor_x).

        Returns:
            New scaled Rectangle.
        """
        if factor_y is None:
            factor_y = factor_x

        if factor_x < 0 or factor_y < 0:
            raise ValueError("Scale factors cannot be negative")

        return Rectangle(
            length=self.length * factor_x,
            width=self.width * factor_y,
            x=self.x,
            y=self.y,
        )

    def rotate_90(self) -> "Rectangle":
        """
        Rotates the rectangle by 90 degrees around its origin corner (swaps length and width).
        """
        return Rectangle(length=self.width, width=self.length, x=self.x, y=self.y)

    def translate(self, dx: float, dy: float) -> "Rectangle":
        """
        Translates (shifts) the rectangle position by (dx, dy).
        """
        return Rectangle(length=self.length, width=self.width, x=self.x + dx, y=self.y + dy)


# ─── 5. Operator Overloading & Dunder Methods ──────────────────────────────────


    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Rectangle):
            return False
        return (
            math.isclose(self.length, other.length, rel_tol=1e-7)
            and math.isclose(self.width, other.width, rel_tol=1e-7)
            and math.isclose(self.x, other.x, rel_tol=1e-7)
            and math.isclose(self.y, other.y, rel_tol=1e-7)
        )

    def __lt__(self, other: "Rectangle") -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area < other.area

    def __le__(self, other: "Rectangle") -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area <= other.area or math.isclose(self.area, other.area, rel_tol=1e-7)

    def __add__(self, other: "Rectangle") -> "Rectangle":
        """
        Operator '+' computes minimum bounding box rectangle enclosing both rectangles.
        """
        if not isinstance(other, Rectangle):
            return NotImplemented
        min_x1, min_y1, max_x1, max_y1 = self.bounding_box()
        min_x2, min_y2, max_x2, max_y2 = other.bounding_box()

        union_min_x = min(min_x1, min_x2)
        union_min_y = min(min_y1, min_y2)
        union_max_x = max(max_x1, max_x2)
        union_max_y = max(max_y1, max_y2)

        return Rectangle(
            length=union_max_x - union_min_x,
            width=union_max_y - union_min_y,
            x=union_min_x,
            y=union_min_y,
        )

    def __mul__(self, scalar: float) -> "Rectangle":
        """Operator '*' scales length and width by scalar."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return self.scale(float(scalar))

    def __rmul__(self, scalar: float) -> "Rectangle":
        return self.__mul__(scalar)

    def __repr__(self) -> str:
        return f"Rectangle(length={self.length}, width={self.width}, x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"Rectangle [{self.length}x{self.width} at ({self.x}, {self.y}), Area={self.area}]"


# ─── 6. Vertex Generator & Point Sampling ──────────────────────────────────────


    def vertices(self) -> List[Tuple[float, float]]:
        """
        Returns four corner vertices of rectangle in counter-clockwise order:
        [Bottom-Left, Bottom-Right, Top-Right, Top-Left].
        """
        min_x, min_y, max_x, max_y = self.bounding_box()
        return [
            (min_x, min_y),
            (max_x, min_y),
            (max_x, max_y),
            (min_x, max_y),
        ]

    def sample_grid_points(self, rows: int = 5, cols: int = 5) -> List[Tuple[float, float]]:
        """
        Generates a grid of evenly spaced (x, y) coordinates inside and on boundary.

        Args:
            rows: Number of grid divisions along y-axis.
            cols: Number of grid divisions along x-axis.

        Returns:
            List of 2D coordinate tuples.
        """
        if rows < 1 or cols < 1:
            raise ValueError("Rows and cols must be >= 1")

        min_x, min_y, max_x, max_y = self.bounding_box()
        x_step = self.length / cols if cols > 1 else 0
        y_step = self.width / rows if rows > 1 else 0

        points: List[Tuple[float, float]] = []
        for r in range(rows + 1):
            py = min_y + r * y_step
            for c in range(cols + 1):
                px = min_x + c * x_step
                points.append((round(px, 6), round(py, 6)))

        return points

    def sample_random_interior_point(self, seed: Optional[int] = None) -> Tuple[float, float]:
        """Samples a uniformly distributed random point strictly inside rectangle."""
        if seed is not None:
            random.seed(seed)

        rx = self.x + random.uniform(0, self.length)
        ry = self.y + random.uniform(0, self.width)
        return (rx, ry)


# ─── 7. Serialization & Formatted Reports ──────────────────────────────────────


    def to_dict(self) -> Dict[str, Any]:
        """Serializes rectangle state into a dictionary."""
        return {
            "length": self.length,
            "width": self.width,
            "x": self.x,
            "y": self.y,
            "area": self.area,
            "perimeter": self.perimeter,
            "diagonal": self.diagonal,
            "is_square": self.is_square,
        }

    def to_json(self, indent: Optional[int] = 2) -> str:
        """Serializes rectangle state into JSON format."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rectangle":
        """Deserializes a Rectangle object from a dictionary."""
        return cls(
            length=data["length"],
            width=data["width"],
            x=data.get("x", 0.0),
            y=data.get("y", 0.0),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Rectangle":
        """Deserializes a Rectangle object from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def format_report(self) -> str:
        """Generates a detailed multi-line text summary report of rectangle properties."""
        lines = [
            f"📐 Rectangle Geometry Report",
            f"   Position (x, y)  : ({self.x:.2f}, {self.y:.2f})",
            f"   Length (x-axis)  : {self.length:.2f}",
            f"   Width (y-axis)   : {self.width:.2f}",
            f"   Area             : {self.area:.2f}",
            f"   Perimeter        : {self.perimeter:.2f}",
            f"   Diagonal Length  : {self.diagonal:.2f}",
            f"   Aspect Ratio     : {self.aspect_ratio():.2f}",
            f"   Is Square?       : {'Yes' if self.is_square else 'No'}",
        ]
        return "\n".join(lines)


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestRectangleOperations(unittest.TestCase):
    def test_rectangle_initialization_and_properties(self):
        r = Rectangle(10, 5, 1, 2)
        self.assertEqual(r.length, 10.0)
        self.assertEqual(r.width, 5.0)
        self.assertEqual(r.area, 50.0)
        self.assertEqual(r.perimeter, 30.0)
        self.assertAlmostEqual(r.diagonal, math.sqrt(125))
        self.assertFalse(r.is_square)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            Rectangle(-5, 10)
        with self.assertRaises(ValueError):
            Rectangle(10, -5)

    def test_factory_constructors(self):
        sq = Rectangle.from_square(6)
        self.assertTrue(sq.is_square)
        self.assertEqual(sq.area, 36.0)

        pts = Rectangle.from_points((1, 2), (5, 8))
        self.assertEqual(pts.length, 4.0)
        self.assertEqual(pts.width, 6.0)

        ratio = Rectangle.from_area_aspect_ratio(200, aspect_ratio=2.0)
        self.assertAlmostEqual(ratio.length, 20.0)
        self.assertAlmostEqual(ratio.width, 10.0)

    def test_spatial_geometry(self):
        r1 = Rectangle(10, 10, 0, 0)
        self.assertTrue(r1.contains_point(5, 5))
        self.assertFalse(r1.contains_point(15, 5))

        r2 = Rectangle(4, 4, 2, 2)
        self.assertTrue(r1.contains_rectangle(r2))

        r3 = Rectangle(5, 5, 8, 8)
        self.assertTrue(r1.intersects_rectangle(r3))

        inter = r1.intersection_rectangle(r3)
        self.assertIsNotNone(inter)
        self.assertEqual(inter.length, 2.0)
        self.assertEqual(inter.width, 2.0)

    def test_geometric_transformations(self):
        r = Rectangle(10, 5, 0, 0)
        scaled = r.scale(2)
        self.assertEqual(scaled.length, 20.0)
        self.assertEqual(scaled.width, 10.0)

        rot = r.rotate_90()
        self.assertEqual(rot.length, 5.0)
        self.assertEqual(rot.width, 10.0)

        trans = r.translate(5, -5)
        self.assertEqual(trans.x, 5.0)
        self.assertEqual(trans.y, -5.0)

    def test_operators(self):
        r1 = Rectangle(10, 5, 0, 0)
        r2 = Rectangle(10, 5, 0, 0)
        self.assertEqual(r1, r2)

        r3 = Rectangle(2, 2, 0, 0)
        self.assertTrue(r3 < r1)

        union = r1 + Rectangle(10, 5, 10, 10)
        self.assertEqual(union.length, 20.0)
        self.assertEqual(union.width, 15.0)

        scaled_mul = r1 * 3
        self.assertEqual(scaled_mul.length, 30.0)

    def test_vertex_and_grid_sampling(self):
        r = Rectangle(4, 4, 0, 0)
        verts = r.vertices()
        self.assertEqual(len(verts), 4)
        self.assertEqual(verts[0], (0.0, 0.0))
        self.assertEqual(verts[2], (4.0, 4.0))

        grid = r.sample_grid_points(rows=2, cols=2)
        self.assertEqual(len(grid), 9)

        rx, ry = r.sample_random_interior_point(seed=42)
        self.assertTrue(r.contains_point(rx, ry))

    def test_serialization_and_reports(self):
        r = Rectangle(12, 6, 3, 4)
        r_json = r.to_json()
        reconstructed = Rectangle.from_json(r_json)
        self.assertEqual(r, reconstructed)

        report = r.format_report()
        self.assertIn("Area             : 72.00", report)


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" 📐 Day 51: 2D Rectangle Geometry - Interactive Demo")
    print("=" * 60)

    # 1. Instantiate Core Rectangle
    rect = Rectangle(length=12.0, width=8.0, x=2.0, y=3.0)
    print(f"\n1. Rectangle Initialized:\n{rect.format_report()}")

    # 2. Collision & Intersection
    r2 = Rectangle(length=10.0, width=10.0, x=8.0, y=5.0)
    inter = rect.intersection_rectangle(r2)
    print(f"\n2. Rectangle Collision & Overlap:")
    print(f"   Rect 1: {rect}")
    print(f"   Rect 2: {r2}")
    print(f"   Intersects? {rect.intersects_rectangle(r2)}")
    print(f"   Overlap Box: {inter}")

    # 3. Geometric Transformations
    scaled = rect.scale(1.5)
    rotated = rect.rotate_90()
    print(f"\n3. Transformations:")
    print(f"   Scaled (1.5x) : {scaled}")
    print(f"   Rotated 90°   : {rotated}")

    # 4. JSON Representation
    print(f"\n4. JSON Representation:\n{rect.to_json()}")

    # 5. Unit Test Suite Execution
    print("\n5. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRectangleOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








