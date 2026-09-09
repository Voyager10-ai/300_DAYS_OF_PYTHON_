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


# ─── 2. Custom Token Template Formatter ──────────────────────────────────────


def format_token_template(dt: Union[datetime, date], template: str) -> str:
    """
    Formats a datetime using modern tokenized template syntax (e.g. 'YYYY-MM-DD HH:mm:ss SSS').

    Supported Tokens:
        YYYY: 4-digit year (2026)        YY: 2-digit year (26)
        MMMM: Full month (September)    MMM: Short month (Sep)
        MM: 2-digit month (09)           M: 1/2-digit month (9)
        DD: 2-digit day (09)             D: 1/2-digit day (9)
        dddd: Full weekday (Wednesday)  ddd: Short weekday (Wed)
        HH: 24-hour hour (14)           hh: 12-hour hour (02)
        mm: Minute (30)                 ss: Second (45)
        SSS: Milliseconds (123)         A: AM/PM (PM)       a: am/pm (pm)

    Args:
        dt: Input date or datetime object.
        template: Tokenized template string.

    Returns:
        Formatted datetime string.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected datetime or date object, got {type(dt).__name__}")

    # Microseconds / Milliseconds
    microsec = getattr(dt, "microsecond", 0)
    millisec = microsec // 1000

    # Hours / Minutes / Seconds
    hour = getattr(dt, "hour", 0)
    minute = getattr(dt, "minute", 0)
    second = getattr(dt, "second", 0)

    hour12 = hour % 12
    if hour12 == 0:
        hour12 = 12

    am_pm = "PM" if hour >= 12 else "AM"

    replacements = [
        ("YYYY", f"{dt.year:04d}"),
        ("YY", f"{dt.year % 100:02d}"),
        ("MMMM", dt.strftime("%B")),
        ("MMM", dt.strftime("%b")),
        ("MM", f"{dt.month:02d}"),
        ("M", str(dt.month)),
        ("DD", f"{dt.day:02d}"),
        ("D", str(dt.day)),
        ("dddd", dt.strftime("%A")),
        ("ddd", dt.strftime("%a")),
        ("HH", f"{hour:02d}"),
        ("hh", f"{hour12:02d}"),
        ("mm", f"{minute:02d}"),
        ("ss", f"{second:02d}"),
        ("SSS", f"{millisec:03d}"),
        ("A", am_pm),
        ("a", am_pm.lower()),
    ]

    result = template
    # Replace tokens in order of decreasing length to avoid partial token collision
    for token, value in sorted(replacements, key=lambda x: len(x[0]), reverse=True):
        result = result.replace(token, value)

    return result

