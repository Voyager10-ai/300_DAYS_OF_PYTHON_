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


# ─── 5. Millisecond Rate Limiter Engine ──────────────────────────────────────


class MillisecondTokenBucket:
    """
    Token bucket rate limiter algorithm operating with millisecond-level precision.
    Refills tokens smoothly based on elapsed milliseconds.
    """

    def __init__(self, capacity: float, refill_rate_per_sec: float) -> None:
        """
        Initializes the token bucket.

        Args:
            capacity: Maximum bucket capacity in tokens.
            refill_rate_per_sec: Tokens added per second.

        Raises:
            ValueError: If capacity or refill rate is non-positive.
        """
        if capacity <= 0:
            raise ValueError(f"Capacity must be > 0, got {capacity}")
        if refill_rate_per_sec <= 0:
            raise ValueError(f"Refill rate must be > 0, got {refill_rate_per_sec}")

        self._capacity: float = float(capacity)
        self._tokens: float = float(capacity)
        self._refill_rate_per_ms: float = float(refill_rate_per_sec) / 1000.0
        self._last_refill_ms: float = time.perf_counter() * 1000.0

    def _refill(self) -> None:
        """Refills tokens based on elapsed milliseconds since last check."""
        now_ms = time.perf_counter() * 1000.0
        elapsed_ms = now_ms - self._last_refill_ms
        if elapsed_ms > 0:
            added = elapsed_ms * self._refill_rate_per_ms
            self._tokens = min(self._capacity, self._tokens + added)
            self._last_refill_ms = now_ms

    def consume(self, tokens: float = 1.0) -> bool:
        """
        Attempts to consume specified tokens.

        Args:
            tokens: Number of tokens to consume.

        Returns:
            True if tokens were available and consumed, False otherwise.
        """
        if tokens <= 0:
            raise ValueError(f"Consumed tokens must be > 0, got {tokens}")

        self._refill()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    @property
    def available_tokens(self) -> float:
        """Returns current available token count."""
        self._refill()
        return self._tokens

    @property
    def capacity(self) -> float:
        """Returns total bucket capacity."""
        return self._capacity


# ─── 6. Millisecond Debouncer & Throttler Engines ────────────────────────────


class MillisecondThrottle:
    """
    Ensures an action executes at most once every N milliseconds.
    """

    def __init__(self, interval_ms: float) -> None:
        if interval_ms <= 0:
            raise ValueError(f"Interval must be > 0 ms, got {interval_ms}")
        self.interval_ms = interval_ms
        self._last_execution_ms: Optional[float] = None

    def trigger(self) -> bool:
        """
        Attempts to execute the throttled action.

        Returns:
            True if execution allowed, False if throttled out.
        """
        now_ms = time.perf_counter() * 1000.0
        if self._last_execution_ms is None or (now_ms - self._last_execution_ms) >= self.interval_ms:
            self._last_execution_ms = now_ms
            return True
        return False

    def reset(self) -> None:
        """Resets the throttle state."""
        self._last_execution_ms = None


class MillisecondDebouncer:
    """
    Evaluates whether N milliseconds of quiet time have elapsed since the last activity event.
    """

    def __init__(self, quiet_period_ms: float) -> None:
        if quiet_period_ms <= 0:
            raise ValueError(f"Quiet period must be > 0 ms, got {quiet_period_ms}")
        self.quiet_period_ms = quiet_period_ms
        self._last_activity_ms: Optional[float] = None

    def record_activity(self) -> None:
        """Records an activity occurrence."""
        self._last_activity_ms = time.perf_counter() * 1000.0

    def is_quiet(self) -> bool:
        """
        Checks if required quiet period in milliseconds has passed since last activity.

        Returns:
            True if quiet period passed (or no activity recorded), False otherwise.
        """
        if self._last_activity_ms is None:
            return True
        now_ms = time.perf_counter() * 1000.0
        return (now_ms - self._last_activity_ms) >= self.quiet_period_ms

    def reset(self) -> None:
        """Resets debouncer activity history."""
        self._last_activity_ms = None


# ─── 7. Sub-Millisecond & Universal Time Unit Converters ─────────────────────


TIME_UNIT_TO_SECONDS = {
    "ns": 1e-9,
    "nanoseconds": 1e-9,
    "us": 1e-6,
    "microseconds": 1e-6,
    "ms": 1e-3,
    "milliseconds": 1e-3,
    "s": 1.0,
    "sec": 1.0,
    "seconds": 1.0,
    "min": 60.0,
    "minutes": 60.0,
    "h": 3600.0,
    "hr": 3600.0,
    "hours": 3600.0,
    "d": 86400.0,
    "days": 86400.0,
}


def convert_time_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Converts a time quantity between arbitrary time units (nanoseconds to days).

    Args:
        value: Numerical value to convert.
        from_unit: Source time unit ('ns', 'us', 'ms', 'sec', 'min', 'hr', 'day').
        to_unit: Target time unit.

    Returns:
        Converted float value.

    Raises:
        ValueError: If an unsupported unit is specified.
        TypeError: If value is non-numeric.
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"Expected numeric value, got {type(value).__name__}")

    src_unit = from_unit.strip().lower()
    tgt_unit = to_unit.strip().lower()

    if src_unit not in TIME_UNIT_TO_SECONDS:
        raise ValueError(f"Unsupported source unit '{from_unit}'. Choose from {list(TIME_UNIT_TO_SECONDS.keys())}.")
    if tgt_unit not in TIME_UNIT_TO_SECONDS:
        raise ValueError(f"Unsupported target unit '{to_unit}'. Choose from {list(TIME_UNIT_TO_SECONDS.keys())}.")

    # Convert source unit to base seconds, then to target unit
    seconds = float(value) * TIME_UNIT_TO_SECONDS[src_unit]
    result = seconds / TIME_UNIT_TO_SECONDS[tgt_unit]
    return result


# ─── 8. Unit Test Suite ──────────────────────────────────────────────────────


class TestMillisecondOperations(unittest.TestCase):
    """Comprehensive unit test suite for millisecond-level utilities."""

    def test_fetchers_and_extraction(self) -> None:
        ms = get_current_milliseconds()
        self.assertTrue(ms > 1_700_000_000_000)

        dt = datetime(2026, 9, 10, 14, 30, 45, 123456, tzinfo=timezone.utc)
        self.assertEqual(extract_milliseconds(dt), 123)
        self.assertEqual(get_epoch_milliseconds(dt), int(dt.timestamp() * 1000))

    def test_duration_breakdown_and_formatter(self) -> None:
        # 2 days, 3 hours, 15 minutes, 45 seconds, 120 ms
        total_ms = (2 * 86400 + 3 * 3600 + 15 * 60 + 45) * 1000 + 120
        bd = breakdown_milliseconds(total_ms)
        self.assertEqual((bd["days"], bd["hours"], bd["minutes"], bd["seconds"], bd["milliseconds"]), (2, 3, 15, 45, 120))

        formatted_full = format_milliseconds_duration(total_ms, compact=False)
        self.assertIn("2 days, 3 hours, 15 minutes, 45 seconds, 120 ms", formatted_full)

        formatted_compact = format_milliseconds_duration(total_ms, compact=True)
        self.assertEqual(formatted_compact, "2d 3h 15m 45s 120ms")

    def test_timestamp_parsing_and_formatting(self) -> None:
        ts_ms = 1788964245123
        dt = parse_millisecond_timestamp(ts_ms)
        self.assertEqual(dt.year, 2026)

        formatted = format_datetime_with_ms(dt)
        self.assertTrue(formatted.endswith(".123"))

    def test_precise_sleep_and_timer(self) -> None:
        elapsed_sleep = precise_sleep_ms(15)
        self.assertGreaterEqual(elapsed_sleep, 14.0)

        with MillisecondTimer() as timer:
            time.sleep(0.01)

        self.assertGreaterEqual(timer.elapsed_milliseconds, 5.0)

    def test_rate_limiter_token_bucket(self) -> None:
        bucket = MillisecondTokenBucket(capacity=5, refill_rate_per_sec=10)
        self.assertTrue(bucket.consume(3))
        self.assertTrue(bucket.consume(2))
        self.assertFalse(bucket.consume(1))  # Empty

        time.sleep(0.15)  # Refills ~1.5 tokens
        self.assertTrue(bucket.consume(1))

    def test_debouncer_and_throttler(self) -> None:
        throttle = MillisecondThrottle(interval_ms=50)
        self.assertTrue(throttle.trigger())
        self.assertFalse(throttle.trigger())  # Throttled

        debouncer = MillisecondDebouncer(quiet_period_ms=50)
        debouncer.record_activity()
        self.assertFalse(debouncer.is_quiet())
        time.sleep(0.06)
        self.assertTrue(debouncer.is_quiet())

    def test_convert_time_units(self) -> None:
        self.assertEqual(convert_time_units(1000, "ms", "s"), 1.0)
        self.assertEqual(convert_time_units(1, "sec", "ms"), 1000.0)
        self.assertEqual(convert_time_units(1000000, "us", "s"), 1.0)
        self.assertEqual(convert_time_units(1, "hr", "min"), 60.0)

    def test_exceptions_and_edge_cases(self) -> None:
        with self.assertRaises(ValueError):
            breakdown_milliseconds(-100)
        with self.assertRaises(TypeError):
            parse_millisecond_timestamp("invalid")  # type: ignore
        with self.assertRaises(ValueError):
            MillisecondTokenBucket(capacity=-5, refill_rate_per_sec=10)
        with self.assertRaises(ValueError):
            convert_time_units(10, "invalid_unit", "ms")







