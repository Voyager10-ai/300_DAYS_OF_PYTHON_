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


# ─── 2. Business / Working Days Subtraction Engine ───────────────────────────


def subtract_business_days(
    start: Union[datetime, date],
    business_days: int,
    holidays: Optional[Set[date]] = None,
) -> Union[datetime, date]:
    """
    Subtracts N business (working) days from a starting date/datetime, skipping weekends and holidays.

    Args:
        start: Starting date or datetime object.
        business_days: Number of business days to subtract (must be >= 0).
        holidays: Optional set of holiday date objects to skip.

    Returns:
        Date or datetime object offset by -N business days.

    Raises:
        ValueError: If business_days is negative.
        TypeError: If start is invalid type.
    """
    if not isinstance(start, (datetime, date)):
        raise TypeError(f"Expected date or datetime instance, got {type(start).__name__}")
    if business_days < 0:
        raise ValueError(f"Business days to subtract cannot be negative, got {business_days}")

    is_dt = isinstance(start, datetime)
    curr_date = start.date() if is_dt else start
    remaining = business_days

    one_day = timedelta(days=1)
    
    while remaining > 0:
        curr_date -= one_day
        # Monday = 0, Sunday = 6
        if curr_date.weekday() < 5 and (holidays is None or curr_date not in holidays):
            remaining -= 1

    if is_dt:
        return datetime.combine(curr_date, start.time(), tzinfo=start.tzinfo)
    else:
        return curr_date


# ─── 3. Date Difference & Elapsed Interval Calculator ─────────────────────────


def days_between(
    date1: Union[datetime, date],
    date2: Union[datetime, date],
    absolute: bool = True,
) -> int:
    """
    Calculates the number of calendar days between two dates.

    Args:
        date1: First date or datetime.
        date2: Second date or datetime.
        absolute: If True, returns positive integer distance. Else signed difference (date2 - date1).

    Returns:
        Number of days as integer.
    """
    d1 = date1.date() if isinstance(date1, datetime) else date1
    d2 = date2.date() if isinstance(date2, datetime) else date2

    diff = (d2 - d1).days
    return abs(diff) if absolute else diff


def detailed_date_diff(
    start: Union[datetime, date],
    end: Union[datetime, date],
) -> Dict[str, Any]:
    """
    Provides a detailed breakdown of the time elapsed between start and end.

    Args:
        start: Starting date or datetime.
        end: Ending date or datetime.

    Returns:
        Dictionary containing total_days, hours, minutes, seconds, and is_past.
    """
    d1 = datetime.combine(start, dt_time.min) if not isinstance(start, datetime) else start
    d2 = datetime.combine(end, dt_time.min) if not isinstance(end, datetime) else end

    # Align timezone naive/aware if needed
    if d1.tzinfo and not d2.tzinfo:
        d2 = d2.replace(tzinfo=d1.tzinfo)
    elif not d1.tzinfo and d2.tzinfo:
        d1 = d1.replace(tzinfo=d2.tzinfo)

    delta = d2 - d1
    total_seconds = delta.total_seconds()
    is_past = total_seconds < 0

    abs_sec = abs(int(total_seconds))
    days, remainder = divmod(abs_sec, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "total_days": abs((d2.date() - d1.date()).days),
        "is_past": is_past,
    }


