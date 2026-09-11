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
