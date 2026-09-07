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


# ─── 6. Business Days & Holiday Calculator ───────────────────────────────────


def is_business_day(
    d: Union[date, datetime],
    custom_holidays: Optional[Set[date]] = None,
) -> bool:
    """
    Checks whether a given date or datetime is a business day (Monday - Friday and not a holiday).

    Args:
        d: Date or datetime object.
        custom_holidays: Optional set of date objects representing holidays.

    Returns:
        True if business day, False otherwise.
    """
    check_date = d.date() if isinstance(d, datetime) else d
    # Monday=0, Sunday=6
    if check_date.weekday() >= 5:
        return False
    if custom_holidays and check_date in custom_holidays:
        return False
    return True


def add_business_days(
    start_date: Union[date, datetime],
    num_days: int,
    custom_holidays: Optional[Set[date]] = None,
) -> date:
    """
    Adds (or subtracts) N business days to/from a starting date.

    Args:
        start_date: Initial date or datetime.
        num_days: Number of business days to add (positive) or subtract (negative).
        custom_holidays: Optional set of holiday dates to skip.

    Returns:
        Resulting date object after adding N business days.
    """
    curr = start_date.date() if isinstance(start_date, datetime) else start_date
    step = 1 if num_days >= 0 else -1
    remaining = abs(num_days)

    while remaining > 0:
        curr += timedelta(days=step)
        if is_business_day(curr, custom_holidays=custom_holidays):
            remaining -= 1

    return curr


def count_business_days(
    start_date: Union[date, datetime],
    end_date: Union[date, datetime],
    custom_holidays: Optional[Set[date]] = None,
) -> int:
    """
    Counts the number of business days between start_date and end_date (inclusive of start, exclusive of end).

    Args:
        start_date: Starting date/datetime.
        end_date: Ending date/datetime.
        custom_holidays: Optional set of holiday dates.

    Returns:
        Count of business days.
    """
    d1 = start_date.date() if isinstance(start_date, datetime) else start_date
    d2 = end_date.date() if isinstance(end_date, datetime) else end_date

    if d1 > d2:
        return -count_business_days(d2, d1, custom_holidays=custom_holidays)

    count = 0
    curr = d1
    while curr < d2:
        if is_business_day(curr, custom_holidays=custom_holidays):
            count += 1
        curr += timedelta(days=1)

    return count


# ─── 7. Calendar & Period Bound Calculators ──────────────────────────────────


def get_period_bounds(dt: datetime, period: str = "day") -> Tuple[datetime, datetime]:
    """
    Computes the start (00:00:00.000000) and end (23:59:59.999999) datetimes for a given period.

    Args:
        dt: Input datetime.
        period: One of 'day', 'week', 'month', 'quarter', 'year'.

    Returns:
        Tuple of (start_datetime, end_datetime).

    Raises:
        ValueError: If period is not supported.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    clean_period = period.strip().lower()

    if clean_period == "day":
        start_dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start_dt, end_dt

    elif clean_period == "week":
        # Week starts on Monday (weekday=0)
        start_date = dt.date() - timedelta(days=dt.weekday())
        start_dt = datetime.combine(start_date, dt_time.min, tzinfo=dt.tzinfo)
        end_date = start_date + timedelta(days=6)
        end_dt = datetime.combine(end_date, dt_time.max, tzinfo=dt.tzinfo)
        return start_dt, end_dt

    elif clean_period == "month":
        start_dt = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Find next month 1st day minus 1 microsecond
        if dt.month == 12:
            next_month = dt.replace(year=dt.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            next_month = dt.replace(month=dt.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dt = next_month - timedelta(microseconds=1)
        return start_dt, end_dt

    elif clean_period == "quarter":
        quarter_start_month = 3 * ((dt.month - 1) // 3) + 1
        start_dt = dt.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        if quarter_start_month + 3 > 12:
            next_q = dt.replace(year=dt.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            next_q = dt.replace(month=quarter_start_month + 3, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dt = next_q - timedelta(microseconds=1)
        return start_dt, end_dt

    elif clean_period == "year":
        start_dt = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dt = dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        return start_dt, end_dt

    else:
        raise ValueError(f"Invalid period '{period}'. Choose from 'day', 'week', 'month', 'quarter', 'year'.")


# ─── 8. Unit Test Suite ──────────────────────────────────────────────────────


class TestDateTimeConverters(unittest.TestCase):
    """Comprehensive unit test suite for all datetime conversion utilities."""

    def test_parse_datetime_string(self) -> None:
        # ISO format
        dt1 = parse_datetime_string("2026-09-07T14:30:00")
        self.assertEqual((dt1.year, dt1.month, dt1.day, dt1.hour, dt1.minute), (2026, 9, 7, 14, 30))

        # Standard SQL
        dt2 = parse_datetime_string("2026-09-07 14:30:00")
        self.assertEqual(dt2.year, 2026)

        # Date only
        dt3 = parse_datetime_string("2026-09-07")
        self.assertEqual((dt3.year, dt3.month, dt3.day), (2026, 9, 7))

        # Custom format
        dt4 = parse_datetime_string("07/09/2026 14-30", custom_format="%d/%m/%Y %H-%M")
        self.assertEqual((dt4.day, dt4.month, dt4.year, dt4.hour), (7, 9, 2026, 14))

    def test_format_datetime_and_standards(self) -> None:
        dt = datetime(2026, 9, 7, 14, 30, 0, tzinfo=timezone.utc)
        self.assertEqual(format_datetime(dt, "%Y/%m/%d"), "2026/09/07")
        self.assertEqual(to_iso8601(dt), "2026-09-07T14:30:00+00:00")
        self.assertIn("Mon, 07 Sep 2026 14:30:00", to_rfc2822(dt))

    def test_epoch_conversions(self) -> None:
        dt = datetime(2026, 9, 7, 12, 0, 0, tzinfo=timezone.utc)
        sec = datetime_to_epoch(dt, unit="seconds")
        ms = datetime_to_epoch(dt, unit="milliseconds")
        self.assertEqual(ms, sec * 1000)

        dt_reconstructed = epoch_to_datetime(sec, unit="seconds", tz=timezone.utc)
        self.assertEqual(dt, dt_reconstructed)

        dt_ms_reconstructed = epoch_to_datetime(ms, unit="milliseconds", tz=timezone.utc)
        self.assertEqual(dt, dt_ms_reconstructed)

    def test_timezone_conversions(self) -> None:
        dt_utc = datetime(2026, 9, 7, 12, 0, 0, tzinfo=timezone.utc)
        dt_ny = convert_timezone(dt_utc, target_tz="America/New_York")
        # NY is UTC-4 in September (EDT)
        self.assertEqual(dt_ny.hour, 8)

        # Convert back to UTC
        dt_back = to_utc(dt_ny)
        self.assertEqual(dt_back.hour, 12)

    def test_humanize_and_time_ago(self) -> None:
        ref = datetime(2026, 9, 7, 12, 0, 0)
        past_dt = datetime(2026, 9, 7, 10, 0, 0)
        future_dt = datetime(2026, 9, 7, 15, 0, 0)

        self.assertEqual(time_ago(past_dt, reference_dt=ref), "2 hours ago")
        self.assertEqual(time_ago(future_dt, reference_dt=ref), "in 3 hours")

        td = timedelta(days=2, hours=5)
        self.assertEqual(humanize_timedelta(td), "2 days, 5 hours")

    def test_business_days(self) -> None:
        # Monday Sept 7, 2026
        mon = date(2026, 9, 7)
        fri = date(2026, 9, 11)
        sat = date(2026, 9, 12)

        self.assertTrue(is_business_day(mon))
        self.assertFalse(is_business_day(sat))

        # Add 5 business days from Monday Sept 7 -> should land on Monday Sept 14
        next_mon = add_business_days(mon, 5)
        self.assertEqual(next_mon, date(2026, 9, 14))

        # Count business days mon to fri (5 days: Mon, Tue, Wed, Thu, Fri)
        self.assertEqual(count_business_days(mon, date(2026, 9, 12)), 5)

        # Custom holiday test
        holidays = {date(2026, 9, 8)}  # Tuesday is a holiday
        self.assertFalse(is_business_day(date(2026, 9, 8), custom_holidays=holidays))
        self.assertEqual(count_business_days(mon, date(2026, 9, 12), custom_holidays=holidays), 4)

    def test_period_bounds(self) -> None:
        dt = datetime(2026, 9, 7, 14, 30, 45)
        
        # Day bounds
        d_start, d_end = get_period_bounds(dt, "day")
        self.assertEqual((d_start.hour, d_start.minute, d_start.second), (0, 0, 0))
        self.assertEqual((d_end.hour, d_end.minute, d_end.second), (23, 59, 59))

        # Month bounds (Sept has 30 days)
        m_start, m_end = get_period_bounds(dt, "month")
        self.assertEqual(m_start.day, 1)
        self.assertEqual(m_end.day, 30)

        # Quarter bounds (Sept is Q3: July 1 - Sept 30)
        q_start, q_end = get_period_bounds(dt, "quarter")
        self.assertEqual((q_start.month, q_start.day), (7, 1))
        self.assertEqual((q_end.month, q_end.day), (9, 30))

        # Year bounds
        y_start, y_end = get_period_bounds(dt, "year")
        self.assertEqual((y_start.month, y_start.day), (1, 1))
        self.assertEqual((y_end.month, y_end.day), (12, 31))

    def test_exceptions_and_edge_cases(self) -> None:
        with self.assertRaises(ValueError):
            parse_datetime_string("invalid-date-string-12345")
        with self.assertRaises(TypeError):
            format_datetime("not-a-datetime")  # type: ignore
        with self.assertRaises(ValueError):
            get_period_bounds(datetime.now(), "decade")
        with self.assertRaises(ValueError):
            convert_timezone(datetime.now(), "NonExistent/Timezone")


# ─── 9. Interactive CLI Runner ───────────────────────────────────────────────


def main() -> None:
    """Demonstrates all datetime parsing, formatting, and conversion capabilities."""
    print("=" * 70)
    print(" DAY 59: DATETIME CONVERSION & TIMEZONE TOOLKIT")
    print("=" * 70)

    raw_str = "2026-09-07T15:45:30.123456+00:00"
    parsed_dt = parse_datetime_string(raw_str)
    print(f"\n1. String Parsing:")
    print(f"   • Raw Input String: '{raw_str}'")
    print(f"   • Parsed Datetime:  {parsed_dt} (tzinfo={parsed_dt.tzinfo})")

    print("\n2. Formatting & Standards:")
    print(f"   • ISO 8601:  {to_iso8601(parsed_dt)}")
    print(f"   • RFC 2822:  {to_rfc2822(parsed_dt)}")
    print(f"   • Custom:    {format_datetime(parsed_dt, '%A, %B %d, %Y at %I:%M %p')}")

    print("\n3. Unix Epoch Timestamps:")
    sec = datetime_to_epoch(parsed_dt, unit="seconds")
    ms = datetime_to_epoch(parsed_dt, unit="milliseconds")
    print(f"   • Epoch Seconds:      {sec}")
    print(f"   • Epoch Milliseconds: {ms}")
    print(f"   • Reconstructed DT:   {epoch_to_datetime(ms, unit='milliseconds')}")

    print("\n4. Timezone Conversions:")
    ny_dt = convert_timezone(parsed_dt, target_tz="America/New_York")
    tokyo_dt = convert_timezone(parsed_dt, target_tz="Asia/Tokyo")
    kolkata_dt = convert_timezone(parsed_dt, target_tz="Asia/Kolkata")
    print(f"   • New York (EDT):    {ny_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"   • Tokyo (JST):       {tokyo_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"   • Kolkata (IST):     {kolkata_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    print("\n5. Relative Time & Humanizer:")
    past_event = parsed_dt - timedelta(hours=3, minutes=15)
    future_event = parsed_dt + timedelta(days=5, hours=2)
    print(f"   • Past Event:   {time_ago(past_event, reference_dt=parsed_dt)}")
    print(f"   • Future Event: {time_ago(future_event, reference_dt=parsed_dt)}")

    print("\n6. Business Days Calculation:")
    start_date = parsed_dt.date()
    holidays = {start_date + timedelta(days=1)}  # Tomorrow is a holiday
    added_date = add_business_days(start_date, 5, custom_holidays=holidays)
    print(f"   • Start Date:       {start_date} ({start_date.strftime('%A')})")
    print(f"   • Custom Holiday:   {list(holidays)[0]}")
    print(f"   • +5 Business Days: {added_date} ({added_date.strftime('%A')})")

    print("\n7. Period Bounds (Month & Quarter):")
    m_start, m_end = get_period_bounds(parsed_dt, "month")
    q_start, q_end = get_period_bounds(parsed_dt, "quarter")
    print(f"   • Month Range:   [{m_start}] -> [{m_end}]")
    print(f"   • Quarter Range: [{q_start}] -> [{q_end}]")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    unittest.main(exit=False)
    print()
    main()








