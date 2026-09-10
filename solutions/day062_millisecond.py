# Day 62: Millisecond
#
# Problem:
#   Write a Python program / module to get, format, convert, and benchmark millisecond time units.
#   Includes millisecond epoch timestamp fetchers, component extraction (0-999ms),
#   duration breakdown (days, hours, mins, secs, ms), high-precision sub-millisecond sleeping,
#   millisecond token-bucket rate limiter, debouncer & throttler engines, unit converters,
#   unit tests, and Java practice.

import math
import time
import unittest
from datetime import datetime, date, time as dt_time, timedelta, timezone
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Millisecond Time Fetchers & Extraction ─────────────────────────


def get_current_milliseconds() -> int:
    """
    Returns current Unix timestamp in milliseconds since epoch.

    Returns:
        Integer timestamp in milliseconds.
    """
    return int(time.time() * 1000)


def get_epoch_milliseconds(dt: Optional[datetime] = None) -> int:
    """
    Converts a datetime object (or current time if None) into epoch milliseconds.

    Args:
        dt: Optional datetime object (naive datetimes treated as UTC).

    Returns:
        Integer epoch milliseconds.
    """
    target_dt = dt if dt is not None else datetime.now(timezone.utc)
    if target_dt.tzinfo is None:
        target_dt = target_dt.replace(tzinfo=timezone.utc)
    return int(target_dt.timestamp() * 1000)


def extract_milliseconds(dt: Optional[datetime] = None) -> int:
    """
    Extracts the millisecond portion (0 to 999) from a datetime object or current time.

    Args:
        dt: Optional datetime object.

    Returns:
        Integer milliseconds in range 0-999.
    """
    target_dt = dt if dt is not None else datetime.now()
    return target_dt.microsecond // 1000


# ─── 2. Millisecond Duration & Time Component Breakdown ───────────────────────


def breakdown_milliseconds(total_ms: int) -> Dict[str, int]:
    """
    Decomposes total milliseconds into days, hours, minutes, seconds, and remaining milliseconds.

    Args:
        total_ms: Total duration in milliseconds (must be >= 0).

    Returns:
        Dictionary with keys 'days', 'hours', 'minutes', 'seconds', 'milliseconds'.

    Raises:
        ValueError: If total_ms is negative.
        TypeError: If total_ms is not an integer/float.
    """
    if not isinstance(total_ms, (int, float)) or isinstance(total_ms, bool):
        raise TypeError(f"Expected numeric input, got {type(total_ms).__name__}")
    if total_ms < 0:
        raise ValueError(f"Duration cannot be negative, got {total_ms}")

    ms = int(total_ms)
    days, remainder = divmod(ms, 86_400_000)
    hours, remainder = divmod(remainder, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1_000)

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "milliseconds": milliseconds,
    }


def format_milliseconds_duration(total_ms: int, compact: bool = False) -> str:
    """
    Formats a duration in milliseconds into a human-readable string.

    Args:
        total_ms: Total milliseconds.
        compact: If True, uses short units ('2d 3h 15m 45s 120ms'). Else full words.

    Returns:
        Formatted duration string.
    """
    bd = breakdown_milliseconds(total_ms)

    parts = []
    if compact:
        if bd["days"] > 0:
            parts.append(f"{bd['days']}d")
        if bd["hours"] > 0:
            parts.append(f"{bd['hours']}h")
        if bd["minutes"] > 0:
            parts.append(f"{bd['minutes']}m")
        if bd["seconds"] > 0:
            parts.append(f"{bd['seconds']}s")
        if bd["milliseconds"] > 0 or not parts:
            parts.append(f"{bd['milliseconds']}ms")
        return " ".join(parts)
    else:
        if bd["days"] > 0:
            parts.append(f"{bd['days']} day{'s' if bd['days'] > 1 else ''}")
        if bd["hours"] > 0:
            parts.append(f"{bd['hours']} hour{'s' if bd['hours'] > 1 else ''}")
        if bd["minutes"] > 0:
            parts.append(f"{bd['minutes']} minute{'s' if bd['minutes'] > 1 else ''}")
        if bd["seconds"] > 0:
            parts.append(f"{bd['seconds']} second{'s' if bd['seconds'] > 1 else ''}")
        if bd["milliseconds"] > 0 or not parts:
            parts.append(f"{bd['milliseconds']} ms")
        return ", ".join(parts)


# ─── 3. Millisecond Timestamp Parsing & Formatting ───────────────────────────


def parse_millisecond_timestamp(
    ms_timestamp: Union[int, float], tz: timezone = timezone.utc
) -> datetime:
    """
    Converts epoch milliseconds into a timezone-aware datetime object.

    Args:
        ms_timestamp: Epoch timestamp in milliseconds.
        tz: Target timezone (defaults to UTC).

    Returns:
        Timezone-aware datetime object.

    Raises:
        TypeError: If ms_timestamp is not numeric.
    """
    if not isinstance(ms_timestamp, (int, float)) or isinstance(ms_timestamp, bool):
        raise TypeError(f"Expected numeric timestamp, got {type(ms_timestamp).__name__}")

    seconds = float(ms_timestamp) / 1000.0
    return datetime.fromtimestamp(seconds, tz=tz)


def format_datetime_with_ms(
    dt: Optional[datetime] = None, base_fmt: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Formats a datetime object with 3-digit millisecond resolution appended (e.g. '2026-09-10 14:30:00.123').

    Args:
        dt: Optional datetime object (defaults to current time).
        base_fmt: Base strftime format string.

    Returns:
        Formatted datetime string with '.fff' milliseconds.
    """
    target_dt = dt if dt is not None else datetime.now()
    ms = target_dt.microsecond // 1000
    base_str = target_dt.strftime(base_fmt)
    return f"{base_str}.{ms:03d}"



# ─── 4. High-Precision Delay & Millisecond Timer ──────────────────────────────


def precise_sleep_ms(ms: float) -> float:
    """
    Suspends execution for a specified duration in milliseconds using hybrid sleep + spin wait
    to achieve high timing precision.

    Args:
        ms: Target sleep duration in milliseconds.

    Returns:
        Actual elapsed duration in milliseconds.

    Raises:
        ValueError: If ms is negative.
    """
    if ms < 0:
        raise ValueError(f"Sleep duration cannot be negative, got {ms}")

    target_sec = ms / 1000.0
    start_time = time.perf_counter()
    end_time = start_time + target_sec

    # Sleep coarse duration if > 3ms to avoid CPU spinning
    remaining = end_time - time.perf_counter()
    if remaining > 0.003:
        time.sleep(remaining - 0.002)

    # Spin-wait remainder for high precision
    while time.perf_counter() < end_time:
        pass

    actual_elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return round(actual_elapsed_ms, 4)


class MillisecondTimer:
    """
    Precision timer class for benchmarking operations in milliseconds.
    """

    def __init__(self) -> None:
        self._start_perf: Optional[float] = None
        self._elapsed_ms: Optional[float] = None

    def start(self) -> "MillisecondTimer":
        """Starts timing."""
        self._start_perf = time.perf_counter()
        self._elapsed_ms = None
        return self

    def stop(self) -> float:
        """
        Stops timing and returns elapsed milliseconds.

        Returns:
            Elapsed time in milliseconds.
        """
        if self._start_perf is None:
            raise RuntimeError("Timer was not started.")
        self._elapsed_ms = (time.perf_counter() - self._start_perf) * 1000.0
        return self._elapsed_ms

    @property
    def elapsed_milliseconds(self) -> float:
        """Returns elapsed milliseconds."""
        if self._elapsed_ms is not None:
            return self._elapsed_ms
        if self._start_perf is not None:
            return (time.perf_counter() - self._start_perf) * 1000.0
        raise RuntimeError("Timer was not started.")

    @property
    def elapsed_seconds(self) -> float:
        """Returns elapsed seconds."""
        return self.elapsed_milliseconds / 1000.0

    def __enter__(self) -> "MillisecondTimer":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()



