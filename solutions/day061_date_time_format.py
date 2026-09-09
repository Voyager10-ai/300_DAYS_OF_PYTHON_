# Day 61: Date Time Format
#
# Problem:
#   Write a Python program / module to format date and time in diverse custom and standard representations.
#   Includes ordinal day suffixes (1st, 2nd, 3rd, 4th), custom token-based templates (YYYY-MM-DD, MMMM DD, YYYY),
#   international culture presets (US, EU, ISO, Apache Log, HTTP/RFC 1123), friendly relative time expressions,
#   fractional sub-second precision, format pattern validation, unit tests, and Java practice.

import re
import unittest
from datetime import datetime, date, time as dt_time, timedelta, timezone
from typing import List, Dict, Tuple, Set, Any, Optional, Union


# ─── 1. Core Formatter with Ordinal Day Suffixes ─────────────────────────────


def get_day_ordinal_suffix(day: int) -> str:
    """
    Returns the English ordinal suffix ('st', 'nd', 'rd', 'th') for a day of the month.

    Args:
        day: Day of month (1 to 31).

    Returns:
        Suffix string ('st', 'nd', 'rd', or 'th').

    Raises:
        ValueError: If day is outside range 1-31.
    """
    if not (1 <= day <= 31):
        raise ValueError(f"Day must be between 1 and 31, got {day}.")

    if 11 <= day <= 13:
        return "th"

    last_digit = day % 10
    if last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    else:
        return "th"


def format_datetime_ordinal(dt: Union[datetime, date], fmt: str = "%B {d}{suffix}, %Y") -> str:
    """
    Formats a date or datetime object including ordinal day representation (e.g. 'September 9th, 2026').

    Args:
        dt: Date or datetime object.
        fmt: Format template containing '{d}' for day and '{suffix}' for ordinal suffix.

    Returns:
        Formatted date string.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected datetime or date object, got {type(dt).__name__}")

    day = dt.day
    suffix = get_day_ordinal_suffix(day)

    # Replace placeholders
    formatted_fmt = fmt.replace("{d}", str(day)).replace("{suffix}", suffix)
    return dt.strftime(formatted_fmt)


# ─── 2. Custom Token Template Formatter ──────────────────────────────────────


def format_token_template(dt: Union[datetime, date], template: str) -> str:
    """
    Formats a datetime using modern tokenized template syntax (e.g. 'YYYY-MM-DD HH:mm:ss SSS').

    Supported Tokens:
        YYYY: 4-digit year (2026)        YY: 2-digit year (26)
        MMMM: Full month (September)    MMM: Short month (Sep)
        MM: 2-digit month (09)           M: 1/2-digit month (9)
        DD: 2-digit day (09)             D: 1/2-digit day (9)
        dddd: Full weekday (Wednesday)  ddd: Short weekday (Wed)
        HH: 24-hour hour (14)           hh: 12-hour hour (02)
        mm: Minute (30)                 ss: Second (45)
        SSS: Milliseconds (123)         A: AM/PM (PM)       a: am/pm (pm)

    Args:
        dt: Input date or datetime object.
        template: Tokenized template string.

    Returns:
        Formatted datetime string.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected datetime or date object, got {type(dt).__name__}")

    # Microseconds / Milliseconds
    microsec = getattr(dt, "microsecond", 0)
    millisec = microsec // 1000

    # Hours / Minutes / Seconds
    hour = getattr(dt, "hour", 0)
    minute = getattr(dt, "minute", 0)
    second = getattr(dt, "second", 0)

    hour12 = hour % 12
    if hour12 == 0:
        hour12 = 12

    am_pm = "PM" if hour >= 12 else "AM"

    replacements = [
        ("YYYY", f"{dt.year:04d}"),
        ("YY", f"{dt.year % 100:02d}"),
        ("MMMM", dt.strftime("%B")),
        ("MMM", dt.strftime("%b")),
        ("MM", f"{dt.month:02d}"),
        ("M", str(dt.month)),
        ("DD", f"{dt.day:02d}"),
        ("D", str(dt.day)),
        ("dddd", dt.strftime("%A")),
        ("ddd", dt.strftime("%a")),
        ("HH", f"{hour:02d}"),
        ("hh", f"{hour12:02d}"),
        ("mm", f"{minute:02d}"),
        ("ss", f"{second:02d}"),
        ("SSS", f"{millisec:03d}"),
        ("A", am_pm),
        ("a", am_pm.lower()),
    ]

    result = template
    # Replace tokens in order of decreasing length to avoid partial token collision
    for token, value in sorted(replacements, key=lambda x: len(x[0]), reverse=True):
        result = result.replace(token, value)

    return result


# ─── 3. International Culture Presets & Log Formatters ────────────────────────


CULTURE_PRESETS = {
    "US": "%m/%d/%Y",                    # US Standard Date (MM/DD/YYYY)
    "US_DATETIME": "%m/%d/%Y %I:%M:%S %p",# US Standard DateTime
    "EU": "%d/%m/%Y",                    # European Standard Date (DD/MM/YYYY)
    "EU_DATETIME": "%d/%m/%Y %H:%M:%S",   # European Standard DateTime
    "ISO": "%Y-%m-%d",                   # ISO Date (YYYY-MM-DD)
    "ISO_DATETIME": "%Y-%m-%dT%H:%M:%S",  # ISO 8601 DateTime
    "JAPAN": "%Y年%m月%d日",             # Japanese Date
    "HTTP_RFC1123": "%a, %d %b %Y %H:%M:%S GMT", # RFC 1123 HTTP Header
    "APACHE_LOG": "[%d/%b/%Y:%H:%M:%S %z]",      # Apache/Nginx Access Log Format
    "COOKIE_DATE": "%A, %d-%b-%Y %H:%M:%S GMT", # Netscape Cookie Date
    "RSS_PUB_DATE": "%a, %d %b %Y %H:%M:%S %z", # RSS pubDate
}


def format_culture_preset(dt: datetime, preset: str = "ISO_DATETIME") -> str:
    """
    Formats datetime using international culture standards or web server protocols.

    Args:
        dt: Input datetime object.
        preset: Preset identifier (e.g., 'US', 'EU', 'ISO', 'HTTP_RFC1123', 'APACHE_LOG', 'COOKIE_DATE').

    Returns:
        Formatted datetime string.

    Raises:
        ValueError: If preset is not supported.
    """
    if not isinstance(dt, (datetime, date)):
        raise TypeError(f"Expected datetime or date object, got {type(dt).__name__}")

    clean_preset = preset.strip().upper()
    if clean_preset not in CULTURE_PRESETS:
        raise ValueError(f"Unsupported preset '{preset}'. Choose from {list(CULTURE_PRESETS.keys())}.")

    fmt = CULTURE_PRESETS[clean_preset]

    # Ensure naive datetime gets UTC offset representation for log formats if required
    if ("%z" in fmt or "GMT" in fmt) and isinstance(dt, datetime) and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.strftime(fmt)


# ─── 4. Relative Friendly Date Formatter ─────────────────────────────────────


def format_relative_friendly(
    dt: datetime, reference_dt: Optional[datetime] = None, include_time: bool = True
) -> str:
    """
    Formats a datetime relative to today ('Today at 2:30 PM', 'Yesterday at 10:15 AM', 'Tomorrow at 9:00 AM', 'Last Monday').

    Args:
        dt: Target datetime object.
        reference_dt: Reference point (defaults to current local/UTC datetime matching dt).
        include_time: Whether to append the time portion.

    Returns:
        Friendly formatted relative date string.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    if reference_dt is None:
        reference_dt = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    else:
        if dt.tzinfo and not reference_dt.tzinfo:
            reference_dt = reference_dt.replace(tzinfo=dt.tzinfo)
        elif not dt.tzinfo and reference_dt.tzinfo:
            reference_dt = reference_dt.replace(tzinfo=None)

    target_date = dt.date()
    ref_date = reference_dt.date()
    day_diff = (target_date - ref_date).days

    time_str = f" at {dt.strftime('%I:%M %p').lstrip('0')}" if include_time else ""

    if day_diff == 0:
        return f"Today{time_str}"
    elif day_diff == -1:
        return f"Yesterday{time_str}"
    elif day_diff == 1:
        return f"Tomorrow{time_str}"
    elif -7 < day_diff < 0:
        return f"Last {dt.strftime('%A')}{time_str}"
    elif 0 < day_diff < 7:
        return f"Next {dt.strftime('%A')}{time_str}"
    else:
        return dt.strftime(f"%B %d, %Y{time_str}")


# ─── 5. Fractional & Sub-Second Precision Formatter ──────────────────────────


def format_subsecond_precision(
    dt: datetime, precision: str = "ms", base_fmt: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Formats a datetime object with explicitly formatted sub-second precision (milliseconds, microseconds, nanoseconds).

    Args:
        dt: Input datetime object.
        precision: Sub-second precision ('ms' for 3 digits, 'us' for 6 digits, 'ns' for 9 digits).
        base_fmt: Base strftime pattern for year, month, day, time.

    Returns:
        Formatted datetime string with sub-second fraction appended.

    Raises:
        ValueError: If precision specifier is unsupported.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    clean_prec = precision.strip().lower()
    base_str = dt.strftime(base_fmt)
    microsec = dt.microsecond

    if clean_prec == "ms":
        millisec = microsec // 1000
        return f"{base_str}.{millisec:03d}"
    elif clean_prec == "us":
        return f"{base_str}.{microsec:06d}"
    elif clean_prec == "ns":
        # Python datetime microsecond extended with 3 zero digits for nanoseconds representation
        nanosec = microsec * 1000
        return f"{base_str}.{nanosec:09d}"
    else:
        raise ValueError(f"Invalid precision '{precision}'. Choose from 'ms' (milliseconds), 'us' (microseconds), 'ns' (nanoseconds).")


# ─── 6. Format Pattern Validator & Inspector ─────────────────────────────────


KNOWN_STRFTIME_DIRECTIVES = {
    "%a", "%A", "%b", "%B", "%c", "%d", "%f", "%H", "%I", "%j", "%m", "%M",
    "%p", "%S", "%U", "%w", "%W", "%x", "%X", "%y", "%Y", "%z", "%Z", "%%"
}


def validate_strftime_pattern(pattern: str) -> Dict[str, Any]:
    """
    Validates a strftime format pattern string for correctness and extracts recognized directives.

    Args:
        pattern: The strftime format pattern to inspect.

    Returns:
        Dictionary containing is_valid, directives_found, unrecognized_percent, and test_output.
    """
    if not isinstance(pattern, str):
        raise TypeError(f"Expected string pattern, got {type(pattern).__name__}")

    sample_dt = datetime(2026, 9, 9, 14, 30, 45, 123456, tzinfo=timezone.utc)
    directives_found = re.findall(r"%[a-zA-Z%]", pattern)
    
    unrecognized = [d for d in directives_found if d not in KNOWN_STRFTIME_DIRECTIVES]

    try:
        test_out = sample_dt.strftime(pattern)
        is_valid = len(unrecognized) == 0
        err_msg = None
    except Exception as e:
        test_out = None
        is_valid = False
        err_msg = str(e)

    return {
        "pattern": pattern,
        "is_valid": is_valid,
        "directives_found": list(dict.fromkeys(directives_found)),  # deduplicated preserving order
        "unrecognized_directives": unrecognized,
        "sample_output": test_out,
        "error_message": err_msg,
    }


def inspect_format_tokens(template: str) -> List[str]:
    """
    Extracts all supported custom token identifiers (e.g. YYYY, MMMM, DD, HH, SSS) present in a template string.

    Args:
        template: Tokenized template string.

    Returns:
        List of recognized tokens present in the template.
    """
    known_tokens = [
        "YYYY", "YY", "MMMM", "MMM", "MM", "M", "DD", "D", "dddd", "ddd",
        "HH", "hh", "mm", "ss", "SSS", "A", "a"
    ]
    found = []
    for token in known_tokens:
        if token in template:
            found.append(token)
    return found


# ─── 7. Flexible Mask & Padding Formatter ────────────────────────────────────


def format_masked_datetime(dt: datetime, mask: str = "####-##-## ##:##:##") -> str:
    """
    Fills digits of datetime into a numerical mask string containing '#' characters.
    Order of digits: YYYYMMDDHHMMSS.

    Args:
        dt: Input datetime.
        mask: Mask string e.g. '####-##-## ##:##:##' or '##/##/####'.

    Returns:
        Masked datetime string.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")

    digits = dt.strftime("%Y%m%d%H%M%S")
    digit_idx = 0
    result_chars = []

    for char in mask:
        if char == "#":
            if digit_idx < len(digits):
                result_chars.append(digits[digit_idx])
                digit_idx += 1
            else:
                result_chars.append("0")
        else:
            result_chars.append(char)

    return "".join(result_chars)


def pad_time_string(time_str: str, target_length: int = 8, pad_char: str = "0") -> str:
    """
    Pads single digit time components in a formatted time string (e.g. '9:5:3' -> '09:05:03').

    Args:
        time_str: Raw unpadded time string (e.g. '9:5:3' or '1:30 PM').
        target_length: Desired minimum length.
        pad_char: Character to pad with.

    Returns:
        Padded time string.
    """
    if not isinstance(time_str, str):
        raise TypeError(f"Expected string time_str, got {type(time_str).__name__}")

    # Split time components by colon
    parts = time_str.strip().split(":")
    padded_parts = []

    for idx, part in enumerate(parts):
        sub_parts = part.strip().split(" ")
        num_part = sub_parts[0]
        if num_part.isdigit() and len(num_part) == 1:
            num_part = f"{pad_char}{num_part}"
        
        if len(sub_parts) > 1:
            padded_parts.append(f"{num_part} {' '.join(sub_parts[1:])}")
        else:
            padded_parts.append(num_part)

    return ":".join(padded_parts)


# ─── 8. Unit Test Suite ──────────────────────────────────────────────────────


class TestDateTimeFormatOperations(unittest.TestCase):
    """Comprehensive unit test suite for date-time formatting utilities."""

    def test_ordinal_day_suffixes(self) -> None:
        self.assertEqual(get_day_ordinal_suffix(1), "st")
        self.assertEqual(get_day_ordinal_suffix(2), "nd")
        self.assertEqual(get_day_ordinal_suffix(3), "rd")
        self.assertEqual(get_day_ordinal_suffix(4), "th")
        self.assertEqual(get_day_ordinal_suffix(11), "th")
        self.assertEqual(get_day_ordinal_suffix(12), "th")
        self.assertEqual(get_day_ordinal_suffix(13), "th")
        self.assertEqual(get_day_ordinal_suffix(21), "st")
        self.assertEqual(get_day_ordinal_suffix(22), "nd")
        self.assertEqual(get_day_ordinal_suffix(23), "rd")
        self.assertEqual(get_day_ordinal_suffix(31), "st")

        dt = date(2026, 9, 9)
        self.assertEqual(format_datetime_ordinal(dt), "September 9th, 2026")

    def test_format_token_template(self) -> None:
        dt = datetime(2026, 9, 9, 14, 30, 45, 123456)
        formatted = format_token_template(dt, "YYYY-MM-DD HH:mm:ss SSS A")
        self.assertEqual(formatted, "2026-09-09 14:30:45 123 PM")

        formatted_12h = format_token_template(dt, "hh:mm A")
        self.assertEqual(formatted_12h, "02:30 PM")

    def test_culture_presets(self) -> None:
        dt = datetime(2026, 9, 9, 12, 30, 0, tzinfo=timezone.utc)
        self.assertEqual(format_culture_preset(dt, "US"), "09/09/2026")
        self.assertEqual(format_culture_preset(dt, "EU"), "09/09/2026")
        self.assertEqual(format_culture_preset(dt, "ISO"), "2026-09-09")
        self.assertIn("Wed, 09 Sep 2026 12:30:00 GMT", format_culture_preset(dt, "HTTP_RFC1123"))

    def test_relative_friendly_format(self) -> None:
        ref_dt = datetime(2026, 9, 9, 12, 0, 0)
        today_dt = datetime(2026, 9, 9, 14, 30, 0)
        yesterday_dt = datetime(2026, 9, 8, 10, 15, 0)
        tomorrow_dt = datetime(2026, 9, 10, 9, 0, 0)

        self.assertEqual(format_relative_friendly(today_dt, reference_dt=ref_dt), "Today at 2:30 PM")
        self.assertEqual(format_relative_friendly(yesterday_dt, reference_dt=ref_dt), "Yesterday at 10:15 AM")
        self.assertEqual(format_relative_friendly(tomorrow_dt, reference_dt=ref_dt), "Tomorrow at 9:00 AM")

    def test_subsecond_precision(self) -> None:
        dt = datetime(2026, 9, 9, 14, 30, 45, 123456)
        self.assertEqual(format_subsecond_precision(dt, "ms"), "2026-09-09 14:30:45.123")
        self.assertEqual(format_subsecond_precision(dt, "us"), "2026-09-09 14:30:45.123456")
        self.assertEqual(format_subsecond_precision(dt, "ns"), "2026-09-09 14:30:45.123456000")

    def test_validate_strftime_pattern_and_inspector(self) -> None:
        val = validate_strftime_pattern("%Y-%m-%d %H:%M:%S")
        self.assertTrue(val["is_valid"])
        self.assertEqual(len(val["unrecognized_directives"]), 0)

        val_invalid = validate_strftime_pattern("%Y-%m-%d %Q")
        self.assertFalse(val_invalid["is_valid"])

        tokens = inspect_format_tokens("YYYY-MM-DD HH:mm:ss SSS")
        self.assertIn("YYYY", tokens)
        self.assertIn("MM", tokens)
        self.assertIn("DD", tokens)
        self.assertIn("SSS", tokens)

    def test_masked_datetime_and_padding(self) -> None:
        dt = datetime(2026, 9, 9, 14, 30, 45)
        masked = format_masked_datetime(dt, "####/##/## ##:##:##")
        self.assertEqual(masked, "2026/09/09 14:30:45")

        padded = pad_time_string("9:5:3 PM")
        self.assertEqual(padded, "09:05:03 PM")

    def test_exceptions_and_edge_cases(self) -> None:
        with self.assertRaises(ValueError):
            get_day_ordinal_suffix(35)
        with self.assertRaises(ValueError):
            format_culture_preset(datetime.now(), "UNSUPPORTED_PRESET")
        with self.assertRaises(TypeError):
            format_relative_friendly("not-a-datetime")  # type: ignore
        with self.assertRaises(ValueError):
            format_subsecond_precision(datetime.now(), precision="invalid")







