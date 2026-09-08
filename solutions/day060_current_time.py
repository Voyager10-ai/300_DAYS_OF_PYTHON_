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

