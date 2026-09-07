# Day 59: Convert DateTime
#
# Problem:
#   Write a Python program / module to parse, format, and convert date & time objects.
#   Includes flexible string-to-datetime parsing across multiple ISO/RFC formats,
#   custom datetime formatting, Unix epoch timestamp conversions (sec/ms/us),
#   timezone conversions using zoneinfo/UTC, relative humanized time differences ("time ago"),
#   business days calculation, period bounds (day/week/month/year), unit tests, and Java practice.

import unittest
from datetime import datetime, date, time as dt_time, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. String to Datetime Parsing Engine ────────────────────────────────────


DEFAULT_DATETIME_FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%f%z",  # ISO 8601 with ms and timezone (e.g. 2026-09-07T14:30:00.123456+00:00)
    "%Y-%m-%dT%H:%M:%S%z",     # ISO 8601 with timezone
    "%Y-%m-%dT%H:%M:%S.%f",    # ISO 8601 with ms
    "%Y-%m-%dT%H:%M:%S",       # ISO 8601 basic
    "%Y-%m-%d %H:%M:%S.%f",    # Standard SQL with ms
    "%Y-%m-%d %H:%M:%S",       # Standard SQL
    "%Y/%m/%d %H:%M:%S",       # Slash delimiter datetime
    "%d-%m-%Y %H:%M:%S",       # European datetime with dash
    "%d/%m/%Y %H:%M:%S",       # European datetime with slash
    "%m/%d/%Y %H:%M:%S",       # US datetime
    "%Y-%m-%d",                # ISO Date only
    "%d-%m-%Y",                # European Date with dash
    "%d/%m/%Y",                # European Date with slash
    "%m/%d/%Y",                # US Date
    "%a, %d %b %Y %H:%M:%S GMT", # RFC 2822
]


def parse_datetime_string(
    date_str: str,
    custom_format: Optional[str] = None,
    default_tz: Optional[timezone] = None,
) -> datetime:
    """
    Parses a date/time string into a datetime object.

    Args:
        date_str: Input string representing date and time.
        custom_format: Optional specific strptime format to attempt first.
        default_tz: Optional timezone to attach if the parsed datetime is naive.

    Returns:
        datetime object.

    Raises:
        ValueError: If input string cannot be parsed by any known format.
        TypeError: If input date_str is not a string.
    """
    if not isinstance(date_str, str):
        raise TypeError(f"Expected string input, got {type(date_str).__name__}")

    clean_str = date_str.strip()
    if not clean_str:
        raise ValueError("Cannot parse empty string.")

    # Try ISO fromisoformat first (Python 3.7+)
    if "T" in clean_str or " " in clean_str:
        try:
            dt = datetime.fromisoformat(clean_str)
            if dt.tzinfo is None and default_tz is not None:
                dt = dt.replace(tzinfo=default_tz)
            return dt
        except ValueError:
            pass

    formats = [custom_format] if custom_format else DEFAULT_DATETIME_FORMATS
    for fmt in formats:
        if fmt is None:
            continue
        try:
            dt = datetime.strptime(clean_str, fmt)
            if dt.tzinfo is None and default_tz is not None:
                dt = dt.replace(tzinfo=default_tz)
            return dt
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date string '{date_str}' with available formats.")
