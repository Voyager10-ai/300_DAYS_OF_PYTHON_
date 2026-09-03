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


