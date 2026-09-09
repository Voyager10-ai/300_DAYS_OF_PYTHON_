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


# ─── 3. International Culture Presets & Log Formatters ────────────────────────


CULTURE_PRESETS = {
    "US": "%m/%d/%Y",                    # US Standard Date (MM/DD/YYYY)
    "US_DATETIME": "%m/%d/%Y %I:%M:%S %p",# US Standard DateTime
    "EU": "%d/%m/%Y",                    # European Standard Date (DD/MM/YYYY)
    "EU_DATETIME": "%d/%m/%Y %H:%M:%S",   # European Standard DateTime
    "ISO": "%Y-%m-%d",                   # ISO Date (YYYY-MM-DD)
    "ISO_DATETIME": "%Y-%m-%dT%H:%M:%S",  # ISO 8601 DateTime
    "JAPAN": "%Y年%m月%d日",             # Japanese Date
    "HTTP_RFC1123": "%a, %d %b %Y %H:%M:%S GMT", # RFC 1123 HTTP Header
    "APACHE_LOG": "[%d/%b/%Y:%H:%M:%S %z]",      # Apache/Nginx Access Log Format
    "COOKIE_DATE": "%A, %d-%b-%Y %H:%M:%S GMT", # Netscape Cookie Date
    "RSS_PUB_DATE": "%a, %d %b %Y %H:%M:%S %z", # RSS pubDate
}


def format_culture_preset(dt: datetime, preset: str = "ISO_DATETIME") -> str:
    """
    Formats datetime using international culture standards or web server protocols.

    Args:
        dt: Input datetime object.
        preset: Preset identifier (e.g., 'US', 'EU', 'ISO', 'HTTP_RFC1123', 'APACHE_LOG', 'COOKIE_DATE').

    Returns:
        Formatted datetime string.

    Raises:
        ValueError: If preset is not supported.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected datetime or date object, got {type(dt).__name__}")

    clean_preset = preset.strip().upper()
    if clean_preset not in CULTURE_PRESETS:
        raise ValueError(f"Unsupported preset '{preset}'. Choose from {list(CULTURE_PRESETS.keys())}.")

    fmt = CULTURE_PRESETS[clean_preset]

    # Ensure naive datetime gets UTC offset representation for log formats if required
    if ("%z" in fmt or "GMT" in fmt) and isinstance(dt, datetime) and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.strftime(fmt)


# ─── 4. Relative Friendly Date Formatter ─────────────────────────────────────


def format_relative_friendly(
    dt: datetime, reference_dt: Optional[datetime] = None, include_time: bool = True
) -> str:
    """
    Formats a datetime relative to today ('Today at 2:30 PM', 'Yesterday at 10:15 AM', 'Tomorrow at 9:00 AM', 'Last Monday').

    Args:
        dt: Target datetime object.
        reference_dt: Reference point (defaults to current local/UTC datetime matching dt).
        include_time: Whether to append the time portion.

    Returns:
        Friendly formatted relative date string.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    if reference_dt is None:
        reference_dt = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    else:
        if dt.tzinfo and not reference_dt.tzinfo:
            reference_dt = reference_dt.replace(tzinfo=dt.tzinfo)
        elif not dt.tzinfo and reference_dt.tzinfo:
            reference_dt = reference_dt.replace(tzinfo=None)

    target_date = dt.date()
    ref_date = reference_dt.date()
    day_diff = (target_date - ref_date).days

    time_str = f" at {dt.strftime('%I:%M %p').lstrip('0')}" if include_time else ""

    if day_diff == 0:
        return f"Today{time_str}"
    elif day_diff == -1:
        return f"Yesterday{time_str}"
    elif day_diff == 1:
        return f"Tomorrow{time_str}"
    elif -7 < day_diff < 0:
        return f"Last {dt.strftime('%A')}{time_str}"
    elif 0 < day_diff < 7:
        return f"Next {dt.strftime('%A')}{time_str}"
    else:
        return dt.strftime(f"%B %d, %Y{time_str}")



