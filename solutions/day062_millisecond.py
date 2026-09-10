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

