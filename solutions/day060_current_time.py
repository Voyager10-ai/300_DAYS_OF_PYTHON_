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


# ─── 5. UTC Offset & Daylight Saving Time (DST) Analyzer ────────────────────


def get_current_utc_offset(tz_name: Optional[str] = None) -> Tuple[float, str]:
    """
    Calculates current UTC offset hours and formatted string (e.g. +05:30, -04:00) for a timezone.

    Args:
        tz_name: Optional timezone name (defaults to local system time).

    Returns:
        Tuple of (offset_hours as float, formatted_offset_str as str).
    """
    if tz_name is None:
        dt = datetime.now().astimezone()
    elif tz_name.upper() == "UTC":
        dt = datetime.now(timezone.utc)
    else:
        dt = datetime.now(ZoneInfo(tz_name))

    offset = dt.utcoffset()
    if offset is None:
        return 0.0, "+00:00"

    total_seconds = int(offset.total_seconds())
    offset_hours = total_seconds / 3600.0

    sign = "+" if total_seconds >= 0 else "-"
    abs_seconds = abs(total_seconds)
    hours, remainder = divmod(abs_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    formatted_str = f"{sign}{hours:02d}:{minutes:02d}"
    return offset_hours, formatted_str


def is_dst_active(tz_name: Optional[str] = None, dt: Optional[datetime] = None) -> bool:
    """
    Determines if Daylight Saving Time (DST) is active for a given timezone and datetime.

    Args:
        tz_name: Optional timezone name (defaults to local timezone).
        dt: Optional datetime (defaults to current time).

    Returns:
        True if DST is active, False otherwise.
    """
    target_dt = dt if dt is not None else datetime.now()
    if tz_name is not None and tz_name.upper() != "UTC":
        target_dt = target_dt.astimezone(ZoneInfo(tz_name))
    elif tz_name is None:
        target_dt = target_dt.astimezone()

    dst_delta = target_dt.dst()
    return dst_delta is not None and dst_delta.total_seconds() != 0


def get_timezone_info(tz_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns comprehensive metadata about a timezone.

    Args:
        tz_name: Timezone string name.

    Returns:
        Dictionary containing tz_name, current_time, offset_hours, offset_string, and dst_active.
    """
    dt = get_current_datetime(tz=tz_name)
    offset_hours, offset_str = get_current_utc_offset(tz_name)
    dst_status = is_dst_active(tz_name, dt)

    return {
        "timezone_name": tz_name or "Local",
        "current_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone_abbrev": dt.strftime("%Z"),
        "offset_hours": offset_hours,
        "offset_string": offset_str,
        "dst_active": dst_status,
    }


# ─── 6. NTP Clock Drift & Synchronization Analyzer ───────────────────────────


class NTPSyncChecker:
    """
    Simulates Network Time Protocol (NTP) synchronization and evaluates clock drift against an authoritative reference server.
    """

    def __init__(self, server_name: str = "pool.ntp.org", max_allowed_drift_ms: float = 500.0) -> None:
        self.server_name = server_name
        self.max_allowed_drift_ms = max_allowed_drift_ms

    def evaluate_drift(
        self,
        local_time: datetime,
        reference_time: datetime,
        round_trip_delay_ms: float = 20.0,
    ) -> Dict[str, Any]:
        """
        Evaluates clock drift between local system time and reference server time.

        Args:
            local_time: Local system timestamp.
            reference_time: Authoritative NTP reference server timestamp.
            round_trip_delay_ms: Network round trip latency in ms.

        Returns:
            Dictionary containing drift_ms, within_tolerance, and synchronized status.
        """
        # Ensure both are timezone aware or both naive
        if local_time.tzinfo and not reference_time.tzinfo:
            reference_time = reference_time.replace(tzinfo=local_time.tzinfo)
        elif not local_time.tzinfo and reference_time.tzinfo:
            local_time = local_time.replace(tzinfo=reference_time.tzinfo)

        # Account for network delay (half-trip latency offset)
        adjusted_reference = reference_time + timedelta(milliseconds=round_trip_delay_ms / 2.0)
        drift_delta = local_time - adjusted_reference
        drift_ms = drift_delta.total_seconds() * 1000.0

        within_tolerance = abs(drift_ms) <= self.max_allowed_drift_ms

        return {
            "ntp_server": self.server_name,
            "local_time": local_time.isoformat(),
            "reference_time": reference_time.isoformat(),
            "round_trip_delay_ms": round_trip_delay_ms,
            "drift_ms": round(drift_ms, 3),
            "within_tolerance": within_tolerance,
            "sync_status": "SYNCHRONIZED" if within_tolerance else "DRIFT_DETECTED",
        }


def check_clock_drift(
    simulated_reference_time: datetime,
    max_allowed_drift_ms: float = 500.0,
) -> Dict[str, Any]:
    """
    Convenience wrapper to check local system clock drift against a reference time.

    Args:
        simulated_reference_time: Authoritative reference time.
        max_allowed_drift_ms: Max drift threshold in ms.

    Returns:
        Drift report dictionary.
    """
    checker = NTPSyncChecker(max_allowed_drift_ms=max_allowed_drift_ms)
    local_now = datetime.now(simulated_reference_time.tzinfo)
    return checker.evaluate_drift(local_now, simulated_reference_time)


# ─── 7. Stopwatch & Lap Timer Engine ─────────────────────────────────────────


class Stopwatch:
    """
    Multi-lap stopwatch supporting start, pause, resume, reset, and lap split timing.
    """

    def __init__(self) -> None:
        self._is_running: bool = False
        self._accumulated_ns: int = 0
        self._last_start_ns: Optional[int] = None
        self._laps: List[Tuple[int, float, float]] = []  # (lap_index, lap_time_sec, total_time_sec)
        self._last_lap_total_sec: float = 0.0

    def start(self) -> None:
        """Starts or resumes the stopwatch."""
        if not self._is_running:
            self._is_running = True
            self._last_start_ns = time.perf_counter_ns()

    def pause(self) -> float:
        """
        Pauses the stopwatch.

        Returns:
            Current total elapsed seconds.
        """
        if self._is_running and self._last_start_ns is not None:
            self._accumulated_ns += time.perf_counter_ns() - self._last_start_ns
            self._is_running = False
            self._last_start_ns = None
        return self.elapsed_seconds

    def reset(self) -> None:
        """Resets the stopwatch to zero and clears laps."""
        self._is_running = False
        self._accumulated_ns = 0
        self._last_start_ns = None
        self._laps.clear()
        self._last_lap_total_sec = 0.0

    def lap(self) -> Tuple[int, float, float]:
        """
        Records a lap split.

        Returns:
            Tuple of (lap_number, lap_duration_seconds, total_duration_seconds).

        Raises:
            RuntimeError: If stopwatch is not running.
        """
        if not self._is_running:
            raise RuntimeError("Cannot record lap while stopwatch is paused or reset.")

        total_sec = self.elapsed_seconds
        lap_sec = total_sec - self._last_lap_total_sec
        self._last_lap_total_sec = total_sec

        lap_number = len(self._laps) + 1
        lap_data = (lap_number, round(lap_sec, 6), round(total_sec, 6))
        self._laps.append(lap_data)
        return lap_data

    @property
    def is_running(self) -> bool:
        """Returns True if stopwatch is currently running."""
        return self._is_running

    @property
    def elapsed_seconds(self) -> float:
        """Returns total elapsed seconds."""
        total_ns = self._accumulated_ns
        if self._is_running and self._last_start_ns is not None:
            total_ns += time.perf_counter_ns() - self._last_start_ns
        return total_ns / 1_000_000_000.0

    @property
    def laps(self) -> List[Tuple[int, float, float]]:
        """Returns recorded laps."""
        return list(self._laps)


# ─── 8. Unit Test Suite ──────────────────────────────────────────────────────


class TestCurrentTimeOperations(unittest.TestCase):
    """Comprehensive unit test suite for current time and clock utilities."""

    def test_get_current_datetime_and_strings(self) -> None:
        now_local = get_current_datetime()
        self.assertIsInstance(now_local, datetime)

        now_utc = get_current_utc()
        self.assertEqual(now_utc.tzinfo, timezone.utc)

        time_str = get_current_time_str(fmt="%H:%M:%S")
        self.assertEqual(len(time_str.split(":")), 3)

        utc_str = get_current_utc_str()
        self.assertIn("UTC", utc_str)

    def test_high_precision_timers(self) -> None:
        nanos = get_current_nanos()
        self.assertTrue(nanos > 0)

        mono = get_monotonic_time()
        self.assertTrue(mono > 0)

        with HighPrecisionTimer() as timer:
            time.sleep(0.01)

        self.assertGreaterEqual(timer.elapsed_milliseconds, 5.0)
        self.assertGreaterEqual(timer.elapsed_seconds, 0.005)

    def test_world_clock(self) -> None:
        wc = get_world_clock(["UTC", "Asia/Kolkata", "America/New_York"])
        self.assertIn("UTC", wc)
        self.assertIn("Asia/Kolkata", wc)
        self.assertIn("America/New_York", wc)

        multi_dt = get_multi_timezone_datetimes(["UTC", "Asia/Tokyo"])
        self.assertEqual(multi_dt["UTC"].tzinfo, timezone.utc)

    def test_analog_and_digital_clock(self) -> None:
        fixed_dt = datetime(2026, 9, 8, 3, 30, 0)
        angles = get_analog_clock_angles(fixed_dt)
        # At 3:30:00 -> minute hand at 30 min = 180 deg. Hour hand at 3.5 hrs = 105 deg.
        self.assertAlmostEqual(angles["minute_angle"], 180.0, places=1)
        self.assertAlmostEqual(angles["hour_angle"], 105.0, places=1)
        self.assertAlmostEqual(angles["second_angle"], 0.0, places=1)

        fmt_res = format_12h_24h(fixed_dt)
        self.assertEqual(fmt_res["time_12h"], "03:30:00 AM")
        self.assertEqual(fmt_res["time_24h"], "03:30:00")

        dig = format_digital_clock(fixed_dt, show_seconds=True, use_12h=False)
        self.assertEqual(dig, "[03:30:00]")

    def test_utc_offset_and_dst(self) -> None:
        offset_hours, offset_str = get_current_utc_offset("UTC")
        self.assertEqual(offset_hours, 0.0)
        self.assertEqual(offset_str, "+00:00")

        tz_info = get_timezone_info("Asia/Kolkata")
        self.assertEqual(tz_info["offset_hours"], 5.5)
        self.assertEqual(tz_info["offset_string"], "+05:30")

    def test_ntp_sync_checker(self) -> None:
        ref_time = datetime(2026, 9, 8, 12, 0, 0, tzinfo=timezone.utc)
        local_time = datetime(2026, 9, 8, 12, 0, 0, 100000, tzinfo=timezone.utc)  # 100ms drift

        checker = NTPSyncChecker(max_allowed_drift_ms=500.0)
        res = checker.evaluate_drift(local_time, ref_time, round_trip_delay_ms=20.0)
        self.assertEqual(res["sync_status"], "SYNCHRONIZED")
        self.assertTrue(res["within_tolerance"])

    def test_stopwatch(self) -> None:
        sw = Stopwatch()
        self.assertFalse(sw.is_running)

        sw.start()
        self.assertTrue(sw.is_running)
        time.sleep(0.01)

        lap1 = sw.lap()
        self.assertEqual(lap1[0], 1)
        self.assertGreater(lap1[1], 0.0)

        elapsed = sw.pause()
        self.assertFalse(sw.is_running)
        self.assertGreater(elapsed, 0.0)

        sw.reset()
        self.assertEqual(sw.elapsed_seconds, 0.0)
        self.assertEqual(len(sw.laps), 0)

    def test_exceptions_and_edge_cases(self) -> None:
        with self.assertRaises(ValueError):
            get_current_datetime(tz="NonExistent/Timezone")
        with self.assertRaises(RuntimeError):
            timer = HighPrecisionTimer()
            _ = timer.elapsed_seconds
        with self.assertRaises(RuntimeError):
            sw = Stopwatch()
            sw.lap()







