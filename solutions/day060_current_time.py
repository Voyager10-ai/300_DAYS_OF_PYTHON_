# Day 60: Current Time
#
# Problem:
#   Write a Python program / module to get, format, and analyze the current time.
#   Includes local and UTC current time providers, high-precision monotonic & nanosecond timers,
#   multi-timezone world clocks, 12h/24h digital & analog clock angle calculators,
#   UTC offset & DST analyzers, NTP clock drift simulator, stopwatch & lap timers,
#   unit tests, and Java practice.

import math
import time
import unittest
from datetime import datetime, date, time as dt_time, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Current Time Provider ───────────────────────────────────────────


def get_current_datetime(tz: Optional[Union[str, timezone, ZoneInfo]] = None) -> datetime:
    """
    Returns the current datetime in the specified timezone (defaults to system local time).

    Args:
        tz: Optional timezone specifier ('UTC', 'America/New_York', ZoneInfo, or timezone instance).

    Returns:
        Timezone-aware or local datetime object.

    Raises:
        ValueError: If timezone specifier is invalid.
    """
    if tz is None:
        return datetime.now()

    if isinstance(tz, str):
        clean_tz = tz.strip()
        if clean_tz.upper() == "UTC":
            return datetime.now(timezone.utc)
        try:
            tz_obj = ZoneInfo(clean_tz)
        except Exception as e:
            raise ValueError(f"Invalid timezone name '{tz}': {e}")
        return datetime.now(tz_obj)

    if isinstance(tz, (timezone, ZoneInfo)):
        return datetime.now(tz)

    raise TypeError(f"Expected timezone as str, timezone, or ZoneInfo; got {type(tz).__name__}")


def get_current_time_str(
    fmt: str = "%H:%M:%S",
    tz: Optional[Union[str, timezone, ZoneInfo]] = None,
) -> str:
    """
    Formats the current time into a string.

    Args:
        fmt: strftime format pattern (default is 'HH:MM:SS').
        tz: Optional timezone specifier.

    Returns:
        Formatted current time string.
    """
    dt = get_current_datetime(tz=tz)
    return dt.strftime(fmt)


def get_current_utc() -> datetime:
    """
    Returns the current datetime in UTC timezone.

    Returns:
        UTC timezone-aware datetime object.
    """
    return datetime.now(timezone.utc)


def get_current_utc_str(fmt: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
    """
    Formats current UTC datetime as a string.

    Args:
        fmt: Format pattern.

    Returns:
        Formatted current UTC string.
    """
    return get_current_utc().strftime(fmt)


# ─── 2. High-Precision Monotonic & Performance Timers ────────────────────────


def get_current_nanos() -> int:
    """
    Returns high-resolution current system time in nanoseconds since epoch.

    Returns:
        Nanoseconds as integer.
    """
    return time.time_ns()


def get_monotonic_time() -> float:
    """
    Returns monotonic clock time in seconds (cannot go backwards, unaffected by system clock updates).

    Returns:
        Monotonic time as float.
    """
    return time.monotonic()


class HighPrecisionTimer:
    """
    High-precision benchmark timer using monotonic performance counter.
    Can be used as a context manager or manually via start()/stop().
    """

    def __init__(self) -> None:
        self._start_ns: Optional[int] = None
        self._elapsed_ns: Optional[int] = None

    def start(self) -> "HighPrecisionTimer":
        """Starts timing."""
        self._start_ns = time.perf_counter_ns()
        self._elapsed_ns = None
        return self

    def stop(self) -> float:
        """
        Stops timing and returns elapsed time in seconds.

        Returns:
            Elapsed seconds as float.

        Raises:
            RuntimeError: If timer was not started.
        """
        if self._start_ns is None:
            raise RuntimeError("Timer was not started.")
        self._elapsed_ns = time.perf_counter_ns() - self._start_ns
        return self.elapsed_seconds

    @property
    def elapsed_nanoseconds(self) -> int:
        """Returns elapsed nanoseconds."""
        if self._elapsed_ns is not None:
            return self._elapsed_ns
        if self._start_ns is not None:
            return time.perf_counter_ns() - self._start_ns
        raise RuntimeError("Timer was not started.")

    @property
    def elapsed_milliseconds(self) -> float:
        """Returns elapsed milliseconds."""
        return self.elapsed_nanoseconds / 1_000_000.0

    @property
    def elapsed_seconds(self) -> float:
        """Returns elapsed seconds."""
        return self.elapsed_nanoseconds / 1_000_000_000.0

    def __enter__(self) -> "HighPrecisionTimer":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


# ─── 3. World Clock & Multi-Timezone Fetcher ─────────────────────────────────


DEFAULT_WORLD_CITIES = [
    "UTC",
    "America/New_York",
    "Europe/London",
    "Europe/Paris",
    "Asia/Kolkata",
    "Asia/Tokyo",
    "Australia/Sydney",
]


def get_multi_timezone_datetimes(
    timezones: Optional[List[str]] = None,
) -> Dict[str, datetime]:
    """
    Fetches current datetime for a list of timezone names simultaneously.

    Args:
        timezones: List of timezone strings (defaults to major world cities).

    Returns:
        Dictionary mapping timezone name -> timezone-aware datetime object.

    Raises:
        ValueError: If a timezone string is invalid.
    """
    tz_list = timezones if timezones is not None else DEFAULT_WORLD_CITIES
    results = {}
    now_utc = datetime.now(timezone.utc)

    for tz_name in tz_list:
        clean_tz = tz_name.strip()
        if clean_tz.upper() == "UTC":
            results[clean_tz] = now_utc
        else:
            try:
                tz_obj = ZoneInfo(clean_tz)
                results[clean_tz] = now_utc.astimezone(tz_obj)
            except Exception as e:
                raise ValueError(f"Failed to resolve timezone '{tz_name}': {e}")

    return results


def get_world_clock(
    timezones: Optional[List[str]] = None,
    fmt: str = "%Y-%m-%d %H:%M:%S %Z",
) -> Dict[str, str]:
    """
    Returns a formatted world clock dictionary mapping timezone names to current time strings.

    Args:
        timezones: List of timezone names.
        fmt: strftime format specifier.

    Returns:
        Dictionary mapping timezone name -> formatted time string.
    """
    dt_map = get_multi_timezone_datetimes(timezones)
    return {tz_name: dt.strftime(fmt) for tz_name, dt in dt_map.items()}


# ─── 4. Analog & Digital Clock Representations ───────────────────────────────


def get_analog_clock_angles(dt: Optional[datetime] = None) -> Dict[str, float]:
    """
    Calculates clock hand rotation angles (0 to 360 degrees, 12 o'clock = 0 deg) for a given datetime.

    Args:
        dt: Input datetime (defaults to current system time).

    Returns:
        Dictionary with 'hour_angle', 'minute_angle', and 'second_angle' in degrees.
    """
    target_dt = dt if dt is not None else datetime.now()
    hour = target_dt.hour % 12
    minute = target_dt.minute
    second = target_dt.second + (target_dt.microsecond / 1_000_000.0)

    # 360 deg / 60 sec = 6 deg/sec
    second_angle = (second * 6.0) % 360.0

    # 360 deg / 60 min = 6 deg/min + continuous movement from seconds
    minute_angle = ((minute + second / 60.0) * 6.0) % 360.0

    # 360 deg / 12 hrs = 30 deg/hr + continuous movement from minutes
    hour_angle = ((hour + (minute + second / 60.0) / 60.0) * 30.0) % 360.0

    return {
        "hour_angle": round(hour_angle, 4),
        "minute_angle": round(minute_angle, 4),
        "second_angle": round(second_angle, 4),
    }


def format_12h_24h(dt: Optional[datetime] = None) -> Dict[str, str]:
    """
    Returns 12-hour and 24-hour time strings for a datetime object.

    Args:
        dt: Input datetime (defaults to current time).

    Returns:
        Dictionary containing 'time_12h', 'time_24h', 'period' ('AM'/'PM').
    """
    target_dt = dt if dt is not None else datetime.now()
    return {
        "time_12h": target_dt.strftime("%I:%M:%S %p"),
        "time_24h": target_dt.strftime("%H:%M:%S"),
        "period": target_dt.strftime("%p"),
    }


def format_digital_clock(
    dt: Optional[datetime] = None, show_seconds: bool = True, use_12h: bool = False
) -> str:
    """
    Formats datetime as a digital clock display string.

    Args:
        dt: Input datetime (defaults to current time).
        show_seconds: Whether to include seconds.
        use_12h: Whether to use 12-hour format with AM/PM.

    Returns:
        Digital clock string e.g. '[14:30:45]' or '[02:30:45 PM]'.
    """
    target_dt = dt if dt is not None else datetime.now()
    if use_12h:
        fmt = "%I:%M:%S %p" if show_seconds else "%I:%M %p"
    else:
        fmt = "%H:%M:%S" if show_seconds else "%H:%M"

    return f"[{target_dt.strftime(fmt)}]"



