# Day 57: Round Up
#
# Problem:
#   Write a Python program / module to round up numbers to the next integer, decimal places, or multiples.
#   Includes manual ceiling logic, step/multiple rounding, financial currency rounding & charm pricing,
#   container & batch production capacity estimators, matrix transformers, multi-mode rounding engine,
#   decimal precision class, unit tests, and Java practice.

import math
import unittest
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_UP, ROUND_DOWN
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Ceiling & Decimal Round Up Functions ──────────────────────────────


def round_up_int(val: float) -> int:
    """
    Rounds up a float/int value to the smallest integer >= val (ceiling logic).
    Implements manual ceiling without relying strictly on built-in math.ceil.

    Args:
        val: Number to round up.

    Returns:
        Integer rounded up.

    Raises:
        TypeError: If input is not numeric.
    """
    if not isinstance(val, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(val).__name__}")

    if isinstance(val, int):
        return val

    int_part = int(val)
    if val > 0 and val != int_part:
        return int_part + 1
    return int_part


def round_up_to_decimals(val: float, decimals: int = 0) -> float:
    """
    Rounds up a float value to a specified number of decimal places.
    For example: round_up_to_decimals(3.14159, 2) -> 3.15.

    Args:
        val: Floating point number.
        decimals: Target decimal places (decimals >= 0).

    Returns:
        Rounded float.

    Raises:
        ValueError: If decimals < 0.
    """
    if not isinstance(decimals, int) or isinstance(decimals, bool):
        raise TypeError(f"Expected integer decimals, got {type(decimals).__name__}")
    if decimals < 0:
        raise ValueError(f"Decimals must be >= 0, got {decimals}")

    if decimals == 0:
        return float(round_up_int(val))

    factor = 10**decimals
    return math.ceil(val * factor) / factor


# ─── 2. Step & Multiple Round Up Algorithm ─────────────────────────────────────


def round_up_to_multiple(
    val: Union[int, float], multiple: Union[int, float]
) -> Union[int, float]:
    """
    Rounds up a value to the next smallest multiple of a step size.

    Args:
        val: Input number.
        multiple: Step size / multiple (multiple > 0).

    Returns:
        Rounded up value (int if both inputs are int, float otherwise).

    Raises:
        ValueError: If multiple <= 0.
    """
    if not isinstance(val, (int, float)) or not isinstance(multiple, (int, float)):
        raise TypeError("val and multiple must be numeric")
    if multiple <= 0:
        raise ValueError(f"Multiple must be > 0, got {multiple}")

    quotient = val / multiple
    ceil_q = math.ceil(quotient)
    result = ceil_q * multiple

    if isinstance(val, int) and isinstance(multiple, int):
        return int(result)
    return result


# ─── 3. Financial Currency & Charm Pricing Rounding ────────────────────────────


def round_up_currency(val: float, currency_unit: float = 0.01) -> float:
    """
    Rounds up financial amounts to the nearest currency unit (default 0.01 for cents).

    Args:
        val: Monetary amount.
        currency_unit: Smallest currency denomination (e.g. 0.01, 0.05, 0.25).

    Returns:
        Rounded monetary amount.
    """
    if currency_unit <= 0:
        raise ValueError(f"Currency unit must be > 0, got {currency_unit}")

    res = round_up_to_multiple(val, currency_unit)
    return round(float(res), 4)


def round_up_pricing_charm(val: float, charm_offset: float = 0.01) -> float:
    """
    Rounds up a price to end in a charm pricing figure (e.g. $14.20 -> $14.99).

    Args:
        val: Base price.
        charm_offset: Offset below next dollar (default 0.01 for .99 ending).

    Returns:
        Charm price.
    """
    if val <= 0:
        return 0.0

    ceil_dollar = math.ceil(val)
    if ceil_dollar == val:
        ceil_dollar += 1

    charm_price = ceil_dollar - charm_offset
    if charm_price < val:
        charm_price += 1.0

    return round(charm_price, 2)


# ─── 4. Container Capacity & Batch Production Estimators ───────────────────────


def calculate_containers_needed(items_count: int, container_capacity: int) -> int:
    """
    Calculates minimum number of containers needed to hold items_count items.

    Args:
        items_count: Total items to store/ship (items_count >= 0).
        container_capacity: Storage capacity per container (container_capacity > 0).

    Returns:
        Number of containers required.
    """
    if items_count < 0:
        raise ValueError(f"items_count must be >= 0, got {items_count}")
    if container_capacity <= 0:
        raise ValueError(f"container_capacity must be > 0, got {container_capacity}")

    if items_count == 0:
        return 0

    return round_up_int(items_count / container_capacity)


def calculate_batch_production(order_quantity: int, batch_size: int) -> Dict[str, int]:
    """
    Calculates batch production requirements given minimum order quantity and fixed batch size.

    Args:
        order_quantity: Required units (>= 0).
        batch_size: Fixed units per production run (> 0).

    Returns:
        Dictionary with batches_needed, total_produced, and excess_units.
    """
    if order_quantity < 0 or batch_size <= 0:
        raise ValueError("Invalid order quantity or batch size")

    batches = calculate_containers_needed(order_quantity, batch_size)
    total_produced = batches * batch_size
    excess = total_produced - order_quantity

    return {
        "order_quantity": order_quantity,
        "batch_size": batch_size,
        "batches_needed": batches,
        "total_produced": total_produced,
        "excess_units": excess,
    }


# ─── 5. List & Matrix Rounding Transformers ───────────────────────────────────


def round_up_list(numbers: List[float], decimals: int = 0) -> List[float]:
    """
    Rounds up every numeric element in a list to specified decimals.

    Args:
        numbers: List of floats/ints.
        decimals: Decimal places (decimals >= 0).

    Returns:
        New list with rounded values.
    """
    if not isinstance(numbers, list):
        raise TypeError(f"Expected list, got {type(numbers).__name__}")

    return [round_up_to_decimals(num, decimals) for num in numbers]


def round_up_matrix(matrix: List[List[float]], decimals: int = 0) -> List[List[float]]:
    """
    Rounds up every numeric element in a 2D matrix to specified decimals.

    Args:
        matrix: List of lists of numbers.
        decimals: Decimal places.

    Returns:
        New 2D matrix with rounded values.
    """
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise TypeError("Matrix must be a list of lists")

    return [round_up_list(row, decimals) for row in matrix]


# ─── 6. Multi-Mode Custom Rounding Dispatcher ──────────────────────────────────


def custom_rounding(val: float, decimals: int = 0, mode: str = "up") -> float:
    """
    Rounds a float using different configurable rounding modes:
    - 'up' / 'ceil': Always rounds towards positive infinity.
    - 'down' / 'floor': Always rounds towards negative infinity.
    - 'half_up': Standard arithmetic rounding (.5 rounds away from zero).
    - 'half_even': Banker's rounding (.5 rounds to nearest even integer).
    - 'truncate': Truncates fractional digits towards zero.

    Args:
        val: Input number.
        decimals: Target decimal places.
        mode: Rounding mode string.

    Returns:
        Rounded float value.

    Raises:
        ValueError: If mode is unknown.
    """
    mode_clean = mode.strip().lower()
    factor = 10**decimals

    if mode_clean in ("up", "ceil"):
        return math.ceil(val * factor) / factor
    elif mode_clean in ("down", "floor"):
        return math.floor(val * factor) / factor
    elif mode_clean == "half_up":
        # Shift, add 0.5, floor for positive (or subtract for negative)
        scaled = val * factor
        if scaled >= 0:
            return math.floor(scaled + 0.5) / factor
        else:
            return math.ceil(scaled - 0.5) / factor
    elif mode_clean == "half_even":
        return round(val, decimals)
    elif mode_clean in ("truncate", "trunc"):
        scaled = val * factor
        return math.trunc(scaled) / factor
    else:
        raise ValueError(f"Unknown rounding mode '{mode}'. Options: 'up', 'down', 'half_up', 'half_even', 'truncate'")


# ─── 7. PrecisionRounder Class Using Decimal Module ───────────────────────────


class PrecisionRounder:
    """
    High-precision financial rounding wrapper using Python's decimal.Decimal module
    to eliminate floating-point representation errors.
    """

    @staticmethod
    def _to_decimal(val: Union[str, float, Decimal]) -> Decimal:
        if isinstance(val, Decimal):
            return val
        return Decimal(str(val))

    @classmethod
    def ceil(cls, val: Union[str, float, Decimal], decimals: int = 0) -> Decimal:
        """Rounds up towards positive infinity using Decimal ROUND_CEILING."""
        d = cls._to_decimal(val)
        exp = Decimal("1") if decimals == 0 else Decimal(f"1e-{decimals}")
        return d.quantize(exp, rounding=ROUND_CEILING)

    @classmethod
    def floor(cls, val: Union[str, float, Decimal], decimals: int = 0) -> Decimal:
        """Rounds down towards negative infinity using Decimal ROUND_FLOOR."""
        d = cls._to_decimal(val)
        exp = Decimal("1") if decimals == 0 else Decimal(f"1e-{decimals}")
        return d.quantize(exp, rounding=ROUND_FLOOR)

    @classmethod
    def half_up(cls, val: Union[str, float, Decimal], decimals: int = 0) -> Decimal:
        """Standard half-up arithmetic rounding using Decimal ROUND_HALF_UP."""
        d = cls._to_decimal(val)
        exp = Decimal("1") if decimals == 0 else Decimal(f"1e-{decimals}")
        return d.quantize(exp, rounding=ROUND_HALF_UP)

    @classmethod
    def round_currency(cls, val: Union[str, float, Decimal]) -> Decimal:
        """Rounds up to 2 decimal currency places (Cents)."""
        return cls.ceil(val, decimals=2)


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestRoundUpOperations(unittest.TestCase):
    def test_round_up_int(self):
        self.assertEqual(round_up_int(4.1), 5)
        self.assertEqual(round_up_int(4.0), 4)
        self.assertEqual(round_up_int(-4.1), -4)
        self.assertEqual(round_up_int(0.0), 0)

    def test_round_up_decimals(self):
        self.assertEqual(round_up_to_decimals(3.14159, 2), 3.15)
        self.assertEqual(round_up_to_decimals(3.100, 2), 3.10)

    def test_round_up_multiple(self):
        self.assertEqual(round_up_to_multiple(17, 5), 20)
        self.assertEqual(round_up_to_multiple(12.1, 0.5), 12.5)
        with self.assertRaises(ValueError):
            round_up_to_multiple(10, 0)

    def test_currency_and_charm(self):
        self.assertEqual(round_up_currency(14.213, 0.05), 14.25)
        self.assertEqual(round_up_pricing_charm(14.20), 14.99)

    def test_container_capacity(self):
        self.assertEqual(calculate_containers_needed(105, 20), 6)
        prod = calculate_batch_production(105, 20)
        self.assertEqual(prod["batches_needed"], 6)
        self.assertEqual(prod["total_produced"], 120)
        self.assertEqual(prod["excess_units"], 15)

    def test_list_and_matrix(self):
        self.assertEqual(round_up_list([1.1, 2.2, 3.3]), [2.0, 3.0, 4.0])
        mat = [[1.12, 2.23], [3.34, 4.45]]
        self.assertEqual(round_up_matrix(mat, 1), [[1.2, 2.3], [3.4, 4.5]])

    def test_custom_rounding_modes(self):
        self.assertEqual(custom_rounding(3.14, 1, mode="up"), 3.2)
        self.assertEqual(custom_rounding(3.14, 1, mode="down"), 3.1)
        self.assertEqual(custom_rounding(3.15, 1, mode="half_up"), 3.2)
        self.assertEqual(custom_rounding(3.14, 1, mode="truncate"), 3.1)

    def test_precision_rounder(self):
        self.assertEqual(PrecisionRounder.ceil("3.14159", 2), Decimal("3.15"))
        self.assertEqual(PrecisionRounder.floor("3.14159", 2), Decimal("3.14"))
        self.assertEqual(PrecisionRounder.round_currency("14.201"), Decimal("14.21"))


# ─── 9. Interactive CLI Demo Runner ───────────────────────────────────────────


def main():
    print("=" * 60)
    print(" ⬆️ Day 57: Round Up Calculator & Engine - Interactive Demo")
    print("=" * 60)

    # 1. Core Round Up
    print("\n1. Core Integer & Decimal Round Up:")
    print(f"   round_up_int(4.1)          : {round_up_int(4.1)}")
    print(f"   round_up_to_decimals(3.14159, 2) : {round_up_to_decimals(3.14159, 2)}")

    # 2. Step & Multiple Rounding
    print("\n2. Step & Multiple Rounding:")
    print(f"   round_up_to_multiple(17, 5)   : {round_up_to_multiple(17, 5)}")
    print(f"   round_up_to_multiple(12.1, 0.5): {round_up_to_multiple(12.1, 0.5)}")

    # 3. Currency & Charm Pricing
    print("\n3. Currency & Charm Pricing:")
    print(f"   round_up_currency(14.213, 0.05): ${round_up_currency(14.213, 0.05)}")
    print(f"   round_up_pricing_charm(14.20) : ${round_up_pricing_charm(14.20)}")

    # 4. Container Capacity Estimator
    print("\n4. Container & Batch Production Estimator:")
    prod = calculate_batch_production(order_quantity=105, batch_size=20)
    print(f"   Order 105 units @ Batch 20 -> {prod['batches_needed']} batches ({prod['total_produced']} units, excess {prod['excess_units']})")

    # 5. Multi-Mode Custom Rounding
    print("\n5. Multi-Mode Rounding Modes (Val = 3.14159, Decimals = 2):")
    for mode in ["up", "down", "half_up", "half_even", "truncate"]:
        print(f"   Mode '{mode:<9}': {custom_rounding(3.14159, 2, mode=mode)}")

    # 6. Unit Test Suite Execution
    print("\n6. Executing Unit Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoundUpOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nDemo execution complete!")


if __name__ == "__main__":
    main()








