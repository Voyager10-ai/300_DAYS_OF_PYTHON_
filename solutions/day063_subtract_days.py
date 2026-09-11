# Day 63: Subtract Days
#
# Problem:
#   Write a Python program / module to subtract days, weeks, months, and years from dates and datetimes.
#   Includes core days subtraction, business/working days subtraction with holiday skipping,
#   interval difference calculators, past date series/window generators, relative past string parsers ("N days ago"),
#   month/year subtraction with month-end clipping, unit tests, and Java practice.

import re
import unittest
from datetime import datetime, date, time as dt_time, timedelta, timezone
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Date & Datetime Days Subtraction ────────────────────────────────


def subtract_days(
    dt: Union[datetime, date], days: int
) -> Union[datetime, date]:
    """
    Subtracts N days from a date or datetime object.

    Args:
        dt: Input date or datetime object.
        days: Number of days to subtract (must be >= 0).

    Returns:
        New date or datetime object offset by -N days.

    Raises:
        ValueError: If days is negative.
        TypeError: If dt is not a date or datetime instance.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected date or datetime instance, got {type(dt).__name__}")
    if not isinstance(days, (int, float)) or isinstance(days, bool):
        raise TypeError(f"Expected integer for days, got {type(days).__name__}")
    if days < 0:
        raise ValueError(f"Days to subtract cannot be negative, got {days}")

    return dt - timedelta(days=days)


def n_days_ago(days: int, from_date: Optional[Union[datetime, date]] = None) -> Union[datetime, date]:
    """
    Returns the date/datetime exactly N days prior to a starting point (defaults to current time/date).

    Args:
        days: Number of days to look back.
        from_date: Optional reference point (defaults to current local date/datetime).

    Returns:
        Date or datetime object N days ago.
    """
    ref = from_date if from_date is not None else datetime.now()
    return subtract_days(ref, days)
