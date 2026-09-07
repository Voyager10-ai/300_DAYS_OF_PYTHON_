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


# ─── 2. Datetime to String Formatter ─────────────────────────────────────────


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formats a datetime object using strftime pattern.

    Args:
        dt: Input datetime object.
        fmt: Format specifier pattern.

    Returns:
        Formatted datetime string.

    Raises:
        TypeError: If dt is not a datetime object.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")
    return dt.strftime(fmt)


def to_iso8601(dt: datetime, include_microseconds: bool = False) -> str:
    """
    Converts datetime to ISO 8601 standard string.

    Args:
        dt: Input datetime object.
        include_microseconds: Whether to include fractional seconds.

    Returns:
        ISO 8601 formatted string.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")
    
    if not include_microseconds:
        dt = dt.replace(microsecond=0)
    return dt.isoformat()


def to_rfc2822(dt: datetime) -> str:
    """
    Converts datetime to RFC 2822 compliant format (commonly used in HTTP/Email headers).

    Args:
        dt: Input datetime object.

    Returns:
        RFC 2822 formatted string.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")
    # Default to GMT if naive
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


# ─── 3. Unix Epoch Timestamp Converters ──────────────────────────────────────


def datetime_to_epoch(dt: datetime, unit: str = "seconds") -> Union[int, float]:
    """
    Converts a datetime object into a Unix epoch timestamp.

    Args:
        dt: Input datetime object (naive datetimes are treated as UTC).
        unit: Output unit ('seconds', 'milliseconds', 'microseconds', 'float_seconds').

    Returns:
        Integer or float timestamp value.

    Raises:
        ValueError: If unsupported unit is specified.
        TypeError: If dt is not a datetime object.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    # Treat naive datetimes as UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    ts_float = dt.timestamp()

    if unit == "seconds":
        return int(ts_float)
    elif unit == "float_seconds":
        return ts_float
    elif unit == "milliseconds":
        return int(ts_float * 1000)
    elif unit == "microseconds":
        return int(ts_float * 1_000_000)
    else:
        raise ValueError(f"Invalid unit '{unit}'. Supported units: 'seconds', 'float_seconds', 'milliseconds', 'microseconds'.")


def epoch_to_datetime(
    timestamp: Union[int, float],
    unit: str = "seconds",
    tz: Optional[Union[timezone, ZoneInfo]] = timezone.utc,
) -> datetime:
    """
    Converts a Unix epoch timestamp into a timezone-aware datetime object.

    Args:
        timestamp: Integer or float epoch timestamp.
        unit: Input unit ('seconds', 'milliseconds', 'microseconds').
        tz: Target timezone for output datetime (defaults to UTC).

    Returns:
        Timezone-aware datetime object.

    Raises:
        ValueError: If unsupported unit is specified.
        TypeError: If timestamp is non-numeric.
    """
    if not isinstance(timestamp, (int, float)) or isinstance(timestamp, bool):
        raise TypeError(f"Expected numeric timestamp, got {type(timestamp).__name__}")

    if unit == "seconds":
        seconds = float(timestamp)
    elif unit == "milliseconds":
        seconds = float(timestamp) / 1000.0
    elif unit == "microseconds":
        seconds = float(timestamp) / 1_000_000.0
    else:
        raise ValueError(f"Invalid unit '{unit}'. Supported units: 'seconds', 'milliseconds', 'microseconds'.")

    return datetime.fromtimestamp(seconds, tz=tz)


# ─── 4. Timezone Conversion Engine ───────────────────────────────────────────


def _resolve_tz(tz_input: Union[str, timezone, ZoneInfo]) -> Union[timezone, ZoneInfo]:
    """Helper to convert string timezone names (e.g., 'America/New_York', 'UTC', 'Asia/Kolkata') to tzinfo."""
    if isinstance(tz_input, (timezone, ZoneInfo)):
        return tz_input
    if isinstance(tz_input, str):
        clean_tz = tz_input.strip()
        if clean_tz.upper() == "UTC":
            return timezone.utc
        try:
            return ZoneInfo(clean_tz)
        except Exception as e:
            raise ValueError(f"Unknown or invalid timezone name '{tz_input}': {e}")
    raise TypeError(f"Expected timezone as string, timezone, or ZoneInfo; got {type(tz_input).__name__}")


def convert_timezone(
    dt: datetime,
    target_tz: Union[str, timezone, ZoneInfo],
    source_tz: Optional[Union[str, timezone, ZoneInfo]] = None,
) -> datetime:
    """
    Converts a datetime from its source timezone to a target timezone.

    Args:
        dt: Input datetime.
        target_tz: Target timezone (e.g. 'Asia/Kolkata', 'America/New_York', 'UTC').
        source_tz: Source timezone if dt is naive.

    Returns:
        New timezone-aware datetime object.

    Raises:
        ValueError: If dt is naive and source_tz is not provided.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    tgt_tz = _resolve_tz(target_tz)

    if dt.tzinfo is None:
        if source_tz is None:
            raise ValueError("Naive datetime provided without source_tz specification.")
        src_tz = _resolve_tz(source_tz)
        dt = dt.replace(tzinfo=src_tz)

    return dt.astimezone(tgt_tz)


def to_utc(
    dt: datetime,
    source_tz: Optional[Union[str, timezone, ZoneInfo]] = None,
) -> datetime:
    """
    Converts a datetime object to UTC timezone.

    Args:
        dt: Input datetime object.
        source_tz: Source timezone if dt is naive.

    Returns:
        UTC timezone-aware datetime object.
    """
    return convert_timezone(dt, target_tz=timezone.utc, source_tz=source_tz)


# ─── 5. Relative Time Difference & Humanizer ("Time Ago") ────────────────────


def humanize_timedelta(td: timedelta) -> str:
    """
    Converts a timedelta object into a human-readable duration string.
    (e.g., '2 days, 3 hours', '45 seconds', 'just now').

    Args:
        td: Input timedelta object.

    Returns:
        Human-readable duration string.
    """
    total_seconds = int(td.total_seconds())

    if abs(total_seconds) < 5:
        return "just now"

    is_negative = total_seconds < 0
    seconds = abs(total_seconds)

    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0 and days == 0:  # Include minutes if under a day
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if secs > 0 and days == 0 and hours == 0:  # Include seconds if under an hour
        parts.append(f"{secs} second{'s' if secs > 1 else ''}")

    result = ", ".join(parts)
    return f"{result} ago" if is_negative else result


def time_ago(dt: datetime, reference_dt: Optional[datetime] = None) -> str:
    """
    Calculates the relative time difference between a datetime and a reference point (default current time).

    Args:
        dt: Target datetime.
        reference_dt: Reference datetime (defaults to current UTC/local time matching dt's timezone status).

    Returns:
        String such as '5 minutes ago', 'in 2 hours', or 'just now'.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    if reference_dt is None:
        reference_dt = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    else:
        # Align timezones if one is naive and the other is aware
        if dt.tzinfo and not reference_dt.tzinfo:
            reference_dt = reference_dt.replace(tzinfo=dt.tzinfo)
        elif not dt.tzinfo and reference_dt.tzinfo:
            reference_dt = reference_dt.replace(tzinfo=None)

    diff = reference_dt - dt
    total_seconds = int(diff.total_seconds())

    if abs(total_seconds) < 5:
        return "just now"

    if total_seconds > 0:
        # Past event
        duration_str = humanize_timedelta(diff)
        return f"{duration_str} ago"
    else:
        # Future event
        duration_str = humanize_timedelta(-diff)
        return f"in {duration_str}"




