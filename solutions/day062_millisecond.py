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
