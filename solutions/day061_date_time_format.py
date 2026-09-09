# Day 61: Date Time Format
#
# Problem:
#   Write a Python program / module to format date and time in diverse custom and standard representations.
#   Includes ordinal day suffixes (1st, 2nd, 3rd, 4th), custom token-based templates (YYYY-MM-DD, MMMM DD, YYYY),
#   international culture presets (US, EU, ISO, Apache Log, HTTP/RFC 1123), friendly relative time expressions,
#   fractional sub-second precision, format pattern validation, unit tests, and Java practice.

import re
import unittest
from datetime import datetime, date, time as dt_time, timedelta, timezone
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Formatter with Ordinal Day Suffixes ─────────────────────────────


def get_day_ordinal_suffix(day: int) -> str:
    """
    Returns the English ordinal suffix ('st', 'nd', 'rd', 'th') for a day of the month.

    Args:
        day: Day of month (1 to 31).

    Returns:
        Suffix string ('st', 'nd', 'rd', or 'th').

    Raises:
        ValueError: If day is outside range 1-31.
    """
    if not (1 <= day <= 31):
        raise ValueError(f"Day must be between 1 and 31, got {day}.")

    if 11 <= day <= 13:
        return "th"

    last_digit = day % 10
    if last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    else:
        return "th"


def format_datetime_ordinal(dt: Union[datetime, date], fmt: str = "%B {d}{suffix}, %Y") -> str:
    """
    Formats a date or datetime object including ordinal day representation (e.g. 'September 9th, 2026').

    Args:
        dt: Date or datetime object.
        fmt: Format template containing '{d}' for day and '{suffix}' for ordinal suffix.

    Returns:
        Formatted date string.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected datetime or date object, got {type(dt).__name__}")

    day = dt.day
    suffix = get_day_ordinal_suffix(day)

    # Replace placeholders
    formatted_fmt = fmt.replace("{d}", str(day)).replace("{suffix}", suffix)
    return dt.strftime(formatted_fmt)
