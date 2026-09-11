# Day 63: Subtract Days
#
# Problem:
#   Write a Python program / module to subtract days, weeks, months, and years from dates and datetimes.
#   Includes core days subtraction, business/working days subtraction with holiday skipping,
#   interval difference calculators, past date series/window generators, relative past string parsers ("N days ago"),
#   month/year subtraction with month-end clipping, unit tests, and Java practice.

import re
import unittest
from datetime import datetime, date, time as dt_time, timedelta, timezone
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Date & Datetime Days Subtraction ────────────────────────────────


def subtract_days(
    dt: Union[datetime, date], days: int
) -> Union[datetime, date]:
    """
    Subtracts N days from a date or datetime object.

    Args:
        dt: Input date or datetime object.
        days: Number of days to subtract (must be >= 0).

    Returns:
        New date or datetime object offset by -N days.

    Raises:
        ValueError: If days is negative.
        TypeError: If dt is not a date or datetime instance.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected date or datetime instance, got {type(dt).__name__}")
    if not isinstance(days, (int, float)) or isinstance(days, bool):
        raise TypeError(f"Expected integer for days, got {type(days).__name__}")
    if days < 0:
        raise ValueError(f"Days to subtract cannot be negative, got {days}")

    return dt - timedelta(days=days)


def n_days_ago(days: int, from_date: Optional[Union[datetime, date]] = None) -> Union[datetime, date]:
    """
    Returns the date/datetime exactly N days prior to a starting point (defaults to current time/date).

    Args:
        days: Number of days to look back.
        from_date: Optional reference point (defaults to current local date/datetime).

    Returns:
        Date or datetime object N days ago.
    """
    ref = from_date if from_date is not None else datetime.now()
    return subtract_days(ref, days)


# ─── 2. Business / Working Days Subtraction Engine ───────────────────────────


def subtract_business_days(
    start: Union[datetime, date],
    business_days: int,
    holidays: Optional[Set[date]] = None,
) -> Union[datetime, date]:
    """
    Subtracts N business (working) days from a starting date/datetime, skipping weekends and holidays.

    Args:
        start: Starting date or datetime object.
        business_days: Number of business days to subtract (must be >= 0).
        holidays: Optional set of holiday date objects to skip.

    Returns:
        Date or datetime object offset by -N business days.

    Raises:
        ValueError: If business_days is negative.
        TypeError: If start is invalid type.
    """
    if not isinstance(start, (datetime, date)):
        raise TypeError(f"Expected date or datetime instance, got {type(start).__name__}")
    if business_days < 0:
        raise ValueError(f"Business days to subtract cannot be negative, got {business_days}")

    is_dt = isinstance(start, datetime)
    curr_date = start.date() if is_dt else start
    remaining = business_days

    one_day = timedelta(days=1)
    
    while remaining > 0:
        curr_date -= one_day
        # Monday = 0, Sunday = 6
        if curr_date.weekday() < 5 and (holidays is None or curr_date not in holidays):
            remaining -= 1

    if is_dt:
        return datetime.combine(curr_date, start.time(), tzinfo=start.tzinfo)
    else:
        return curr_date


# ─── 3. Date Difference & Elapsed Interval Calculator ─────────────────────────


def days_between(
    date1: Union[datetime, date],
    date2: Union[datetime, date],
    absolute: bool = True,
) -> int:
    """
    Calculates the number of calendar days between two dates.

    Args:
        date1: First date or datetime.
        date2: Second date or datetime.
        absolute: If True, returns positive integer distance. Else signed difference (date2 - date1).

    Returns:
        Number of days as integer.
    """
    d1 = date1.date() if isinstance(date1, datetime) else date1
    d2 = date2.date() if isinstance(date2, datetime) else date2

    diff = (d2 - d1).days
    return abs(diff) if absolute else diff


def detailed_date_diff(
    start: Union[datetime, date],
    end: Union[datetime, date],
) -> Dict[str, Any]:
    """
    Provides a detailed breakdown of the time elapsed between start and end.

    Args:
        start: Starting date or datetime.
        end: Ending date or datetime.

    Returns:
        Dictionary containing total_days, hours, minutes, seconds, and is_past.
    """
    d1 = datetime.combine(start, dt_time.min) if not isinstance(start, datetime) else start
    d2 = datetime.combine(end, dt_time.min) if not isinstance(end, datetime) else end

    # Align timezone naive/aware if needed
    if d1.tzinfo and not d2.tzinfo:
        d2 = d2.replace(tzinfo=d1.tzinfo)
    elif not d1.tzinfo and d2.tzinfo:
        d1 = d1.replace(tzinfo=d2.tzinfo)

    delta = d2 - d1
    total_seconds = delta.total_seconds()
    is_past = total_seconds < 0

    abs_sec = abs(int(total_seconds))
    days, remainder = divmod(abs_sec, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "total_days": abs((d2.date() - d1.date()).days),
        "is_past": is_past,
    }


# ─── 4. Past Date Series & Window Generator ──────────────────────────────────


def get_past_dates_list(
    num_days: int,
    start_from: Optional[Union[datetime, date]] = None,
    reverse: bool = False,
) -> List[Union[datetime, date]]:
    """
    Generates a list of N consecutive past dates starting from a reference date.

    Args:
        num_days: Number of past days to generate (must be >= 1).
        start_from: Starting reference date (defaults to current date/datetime).
        reverse: If True, orders list chronologically (oldest to newest).

    Returns:
        List of date or datetime objects.

    Raises:
        ValueError: If num_days < 1.
    """
    if num_days < 1:
        raise ValueError(f"num_days must be at least 1, got {num_days}")

    ref = start_from if start_from is not None else datetime.now()
    dates_list = [subtract_days(ref, i) for i in range(num_days)]

    if reverse:
        dates_list.reverse()

    return dates_list


def get_past_date_range(
    num_days: int,
    start_from: Optional[Union[datetime, date]] = None,
) -> Tuple[Union[datetime, date], Union[datetime, date]]:
    """
    Returns a tuple of (past_start_date, reference_end_date) representing a lookback window.

    Args:
        num_days: Size of lookback window in days.
        start_from: End reference date (defaults to current date/datetime).

    Returns:
        Tuple of (past_start_date, reference_end_date).
    """
    ref = start_from if start_from is not None else datetime.now()
    past_start = subtract_days(ref, num_days)
    return past_start, ref


# ─── 5. Relative Past Time String Parser ──────────────────────────────────────


def parse_past_relative_string(
    text: str, reference_dt: Optional[datetime] = None
) -> datetime:
    """
    Parses human-readable relative past expressions like '5 days ago', '2 weeks ago',
    '3 hours ago', 'yesterday' into a datetime object.

    Args:
        text: Input relative expression (case-insensitive).
        reference_dt: Reference datetime (defaults to current time).

    Returns:
        Calculated datetime object.

    Raises:
        ValueError: If expression string cannot be parsed.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string text, got {type(text).__name__}")

    clean = text.strip().lower()
    ref = reference_dt if reference_dt is not None else datetime.now()

    if clean == "today":
        return ref
    elif clean == "yesterday":
        return ref - timedelta(days=1)

    # Match patterns like "5 days ago", "1 day ago", "3 weeks ago", "12 hours ago", "45 minutes ago"
    match = re.match(r"^(\d+)\s+(day|days|week|weeks|hour|hours|minute|minutes)\s+ago$", clean)
    if not match:
        raise ValueError(f"Unable to parse relative past string '{text}'.")

    amount = int(match.group(1))
    unit = match.group(2)

    if "day" in unit:
        return ref - timedelta(days=amount)
    elif "week" in unit:
        return ref - timedelta(weeks=amount)
    elif "hour" in unit:
        return ref - timedelta(hours=amount)
    elif "minute" in unit:
        return ref - timedelta(minutes=amount)
    else:
        raise ValueError(f"Unsupported unit in string '{text}'.")


# ─── 6. Month & Year Subtraction Engine ──────────────────────────────────────


def subtract_months(
    dt: Union[datetime, date], months: int
) -> Union[datetime, date]:
    """
    Subtracts N months from a date or datetime object with month-end clipping.
    (e.g., March 31 - 1 month = February 28/29).

    Args:
        dt: Input date or datetime object.
        months: Number of months to subtract (must be >= 0).

    Returns:
        Date or datetime object offset by -N months.

    Raises:
        ValueError: If months is negative.
        TypeError: If dt is invalid type.
    """
    import calendar

    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected date or datetime instance, got {type(dt).__name__}")
    if months < 0:
        raise ValueError(f"Months to subtract cannot be negative, got {months}")

    total_months = dt.year * 12 + (dt.month - 1) - months
    target_year, target_month_idx = divmod(total_months, 12)
    target_month = target_month_idx + 1

    _, max_days_in_month = calendar.monthrange(target_year, target_month)
    target_day = min(dt.day, max_days_in_month)

    if isinstance(dt, datetime):
        return dt.replace(year=target_year, month=target_month, day=target_day)
    else:
        return date(target_year, target_month, target_day)


def subtract_years(
    dt: Union[datetime, date], years: int
) -> Union[datetime, date]:
    """
    Subtracts N years from a date or datetime object, handling Feb 29 leap day clipping.

    Args:
        dt: Input date or datetime object.
        years: Number of years to subtract (must be >= 0).

    Returns:
        Date or datetime object offset by -N years.

    Raises:
        ValueError: If years is negative.
    """
    import calendar

    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected date or datetime instance, got {type(dt).__name__}")
    if years < 0:
        raise ValueError(f"Years to subtract cannot be negative, got {years}")

    target_year = dt.year - years
    _, max_days_in_month = calendar.monthrange(target_year, dt.month)
    target_day = min(dt.day, max_days_in_month)

    if isinstance(dt, datetime):
        return dt.replace(year=target_year, day=target_day)
    else:
        return date(target_year, dt.month, target_day)


# ─── 7. Calendar Window & Age Calculator ─────────────────────────────────────


def calculate_age_and_days(
    start_date: Union[datetime, date],
    target_date: Optional[Union[datetime, date]] = None,
) -> Dict[str, int]:
    """
    Calculates exact age/elapsed calendar duration in years, months, days, and total days.

    Args:
        start_date: Birth date or past reference date.
        target_date: End reference date (defaults to current date).

    Returns:
        Dictionary containing 'years', 'months', 'days', and 'total_days'.

    Raises:
        ValueError: If start_date is in the future relative to target_date.
    """
    import calendar

    d1 = start_date.date() if isinstance(start_date, datetime) else start_date
    d2 = (
        target_date.date()
        if isinstance(target_date, datetime)
        else (target_date if target_date is not None else date.today())
    )

    if d1 > d2:
        raise ValueError(f"start_date ({d1}) cannot be after target_date ({d2})")

    years = d2.year - d1.year
    months = d2.month - d1.month
    days = d2.day - d1.day

    if days < 0:
        months -= 1
        prev_month = d2.month - 1 if d2.month > 1 else 12
        prev_year = d2.year if d2.month > 1 else d2.year - 1
        _, days_in_prev_month = calendar.monthrange(prev_year, prev_month)
        days += days_in_prev_month

    if months < 0:
        years -= 1
        months += 12

    total_days = (d2 - d1).days

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_days": total_days,
    }


# ─── 8. Unit Test Suite ───────────────────────────────────────────────────────


class TestSubtractDaysOperations(unittest.TestCase):
    """Comprehensive test suite for date subtraction utilities."""

    def test_subtract_days_date_and_datetime(self):
        d = date(2026, 9, 11)
        dt = datetime(2026, 9, 11, 14, 30)

        self.assertEqual(subtract_days(d, 5), date(2026, 9, 6))
        self.assertEqual(subtract_days(dt, 10), datetime(2026, 9, 1, 14, 30))

        with self.assertRaises(ValueError):
            subtract_days(d, -1)

        with self.assertRaises(TypeError):
            subtract_days("2026-09-11", 5)

    def test_n_days_ago(self):
        ref = date(2026, 9, 11)
        self.assertEqual(n_days_ago(7, from_date=ref), date(2026, 9, 4))

    def test_subtract_business_days(self):
        friday = date(2026, 9, 11)
        self.assertEqual(subtract_business_days(friday, 1), date(2026, 9, 10))

        monday = date(2026, 9, 14)
        self.assertEqual(subtract_business_days(monday, 1), date(2026, 9, 11))

        holidays = {date(2026, 9, 10)}
        self.assertEqual(subtract_business_days(friday, 1, holidays=holidays), date(2026, 9, 9))

    def test_days_between_and_detailed_diff(self):
        d1 = date(2026, 9, 1)
        d2 = date(2026, 9, 11)

        self.assertEqual(days_between(d1, d2), 10)
        self.assertEqual(days_between(d2, d1, absolute=False), -10)

        dt1 = datetime(2026, 9, 10, 10, 0)
        dt2 = datetime(2026, 9, 11, 12, 30)
        diff = detailed_date_diff(dt1, dt2)

        self.assertEqual(diff["days"], 1)
        self.assertEqual(diff["hours"], 2)
        self.assertEqual(diff["minutes"], 30)

    def test_past_dates_generators(self):
        ref = date(2026, 9, 11)
        past_list = get_past_dates_list(3, start_from=ref, reverse=True)
        self.assertEqual(past_list, [date(2026, 9, 9), date(2026, 9, 10), date(2026, 9, 11)])

        p_start, p_end = get_past_date_range(5, start_from=ref)
        self.assertEqual(p_start, date(2026, 9, 6))
        self.assertEqual(p_end, date(2026, 9, 11))

    def test_parse_past_relative_string(self):
        ref = datetime(2026, 9, 11, 12, 0)
        self.assertEqual(parse_past_relative_string("yesterday", reference_dt=ref), datetime(2026, 9, 10, 12, 0))
        self.assertEqual(parse_past_relative_string("3 days ago", reference_dt=ref), datetime(2026, 9, 8, 12, 0))
        self.assertEqual(parse_past_relative_string("2 weeks ago", reference_dt=ref), datetime(2026, 8, 28, 12, 0))
        self.assertEqual(parse_past_relative_string("4 hours ago", reference_dt=ref), datetime(2026, 9, 11, 8, 0))

        with self.assertRaises(ValueError):
            parse_past_relative_string("invalid string", reference_dt=ref)

    def test_subtract_months_and_years(self):
        d_march = date(2025, 3, 31)
        self.assertEqual(subtract_months(d_march, 1), date(2025, 2, 28))

        leap = date(2024, 2, 29)
        self.assertEqual(subtract_years(leap, 1), date(2023, 2, 28))

    def test_calculate_age_and_days(self):
        birth = date(2000, 5, 15)
        target = date(2026, 9, 11)
        res = calculate_age_and_days(birth, target)

        self.assertEqual(res["years"], 26)
        self.assertEqual(res["months"], 3)
        self.assertEqual(res["days"], 27)

        with self.assertRaises(ValueError):
            calculate_age_and_days(target, birth)


# ─── 9. Interactive CLI Demonstration ─────────────────────────────────────────


def main() -> None:
    """Demonstrates all Day 63 subtract days utilities."""
    print("=" * 65)
    print(" DAY 63: SUBTRACT DAYS & DATE OFFSETS DEMONSTRATION")
    print("=" * 65)

    today = date.today()
    now = datetime.now()

    print(f"\n1. Core Days Subtraction:")
    print(f"   Today's Date           : {today}")
    print(f"   10 Days Ago            : {subtract_days(today, 10)}")
    print(f"   30 Days Ago (n_days_ago): {n_days_ago(30, from_date=today)}")

    print(f"\n2. Business Days Subtraction:")
    print(f"   5 Business Days Ago    : {subtract_business_days(today, 5)}")
    holidays = {today - timedelta(days=2)}
    print(f"   5 Business Days (w/ Hol): {subtract_business_days(today, 5, holidays=holidays)}")

    print(f"\n3. Interval & Difference Calculation:")
    start_date = date(2026, 1, 1)
    print(f"   Days between 2026-01-01 and today ({today}): {days_between(start_date, today)} days")
    detailed = detailed_date_diff(start_date, today)
    print(f"   Detailed Difference    : {detailed['days']}d {detailed['hours']}h {detailed['minutes']}m {detailed['seconds']}s")

    print(f"\n4. Past Date Series Generator:")
    past_5 = get_past_dates_list(5, start_from=today, reverse=True)
    print(f"   Past 5 Days (Chronological): {[str(d) for d in past_5]}")
    p_start, p_end = get_past_date_range(7, start_from=today)
    print(f"   7-Day Lookback Window     : {p_start} -> {p_end}")

    print(f"\n5. Relative Past String Parser:")
    expressions = ["yesterday", "3 days ago", "2 weeks ago", "5 hours ago"]
    for expr in expressions:
        parsed = parse_past_relative_string(expr, reference_dt=now)
        print(f"   '{expr:<15}' -> {parsed.strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n6. Month & Year Subtraction Engine:")
    d_march = date(2026, 3, 31)
    print(f"   {d_march} - 1 Month  : {subtract_months(d_march, 1)}")
    print(f"   {today} - 5 Years    : {subtract_years(today, 5)}")

    print(f"\n7. Age & Calendar Calculator:")
    birth = date(1998, 4, 20)
    age_info = calculate_age_and_days(birth, today)
    print(f"   Birth Date: {birth} -> Age: {age_info['years']}y {age_info['months']}m {age_info['days']}d (Total: {age_info['total_days']} days)")

    print("\n" + "=" * 65)
    print(" Running Unit Test Suite...")
    print("=" * 65)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)


if __name__ == "__main__":
    main()
