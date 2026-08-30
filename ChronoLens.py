from __future__ import annotations

import argparse
import calendar
import datetime as dt
import logging
import sys
from dataclasses import dataclass
from typing import Optional


__all__ = [
    "APP_NAME",
    "VERSION",
    "DateReport",
    "build_report",
    "print_report",
    "main",
]


logger = logging.getLogger(__name__)

APP_NAME = "DayFinder Pro"
VERSION = "2.0.0"
MIN_PYTHON_VERSION = (3, 9)

PANEL_WIDTH = 64
PANEL_BORDER = "═"
PANEL_CORNER_TL = "╔"
PANEL_CORNER_TR = "╗"
PANEL_CORNER_BL = "╚"
PANEL_CORNER_BR = "╝"
PANEL_VERTICAL = "║"
PANEL_SEPARATOR = "╠"
PANEL_SEPARATOR_RIGHT = "╣"


FUN_SAYINGS = {
    "Monday": "सोमवार",
    "Tuesday": "मंगलवार",
    "Wednesday": "बुधवार",
    "Thursday": "गुरुवार",
    "Friday": "शुक्रवार",
    "Saturday": "शनिवार",
    "Sunday": "रविवार",
}


@dataclass(frozen=True)
class DateReport:
    """
    Computed information about a calendar date.

    A frozen dataclass that encapsulates all computed date-related information
    including weekday, day-of-year, ISO week, and optional age-related data.

    Attributes:
        date: The calendar date being analyzed.
        weekday: Full weekday name (e.g., "Monday").
        day_of_year: Day number within the year (1-366).
        iso_week: ISO 8601 week number (1-53).
        is_leap_year: Whether the year is a leap year.
        days_in_month: Number of days in the month.
        age: Person's age in years, or None if date is in future.
        next_birthday: Next occurrence of the birth date, or None if future.
        days_until_birthday: Days remaining until next birthday.
    """

    date: dt.date
    weekday: str
    day_of_year: int
    iso_week: int
    is_leap_year: bool
    days_in_month: int
    age: Optional[int]
    next_birthday: Optional[dt.date]
    days_until_birthday: Optional[int]


def parse_date(value: str) -> dt.date:
    """
    Parse an ISO date string and validate it.

    Parses a date in ISO format (YYYY-MM-DD) and raises a user-friendly
    error message if the format is invalid.

    Args:
        value: The date string to parse in ISO format (YYYY-MM-DD).

    Returns:
        A datetime.date object.

    Raises:
        argparse.ArgumentTypeError: If the date string is invalid.
    """
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        msg = f"invalid date '{value}'; use YYYY-MM-DD"
        logger.error(msg)
        raise argparse.ArgumentTypeError(msg) from exc


def calculate_age(birth_date: dt.date, today: dt.date) -> int:
    """
    Calculate a person's age in years.

    Computes the completed age by comparing the birth date with a reference
    date, accounting for whether the birthday has occurred this year.

    Args:
        birth_date: The person's date of birth.
        today: The reference date (typically today's date).

    Returns:
        The person's age in completed years.

    Raises:
        ValueError: If birth_date is after today.
    """
    if birth_date > today:
        raise ValueError("Birth date cannot be after the reference date")

    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def next_birthday(birth_date: dt.date, today: dt.date) -> dt.date:
    """
    Calculate the next birthday from a given date.

    Determines the next occurrence of a birthday, handling leap year dates
    (Feb 29) gracefully by substituting Feb 28 in non-leap years.

    Args:
        birth_date: The person's date of birth.
        today: The reference date for calculating the next birthday.

    Returns:
        A date representing the next birthday occurrence.

    Note:
        For Feb 29 birthdays in non-leap years, the birthday is celebrated
        on Feb 28.
    """
    try:
        birthday = birth_date.replace(year=today.year)
    except ValueError:
       
        birthday = dt.date(today.year, 2, 28)

    if birthday < today:
        try:
            birthday = birth_date.replace(year=today.year + 1)
        except ValueError:
            birthday = dt.date(today.year + 1, 2, 28)

    return birthday


def build_report(date: dt.date, today: Optional[dt.date] = None) -> DateReport:
    """
    Build a complete report for a given date.

    Computes all relevant calendar information for a date, including weekday,
    day-of-year, ISO week, leap year status, and age-related data if applicable.

    Args:
        date: The date to analyze.
        today: The reference date (defaults to today's date).

    Returns:
        A DateReport instance containing all computed information.
    """
    today = today or dt.date.today()

    age = calculate_age(date, today) if date <= today else None
    birthday = next_birthday(date, today) if date <= today else None
    days_left = (birthday - today).days if birthday else None

    return DateReport(
        date=date,
        weekday=date.strftime("%A"),
        day_of_year=date.timetuple().tm_yday,
        iso_week=date.isocalendar().week,
        is_leap_year=calendar.isleap(date.year),
        days_in_month=calendar.monthrange(date.year, date.month)[1],
        age=age,
        next_birthday=birthday,
        days_until_birthday=days_left,
    )


def _center_text(text: str, width: int = PANEL_WIDTH) -> str:
    """
    Center text within a fixed width.

    Args:
        text: The text to center.
        width: The target width (default: PANEL_WIDTH).

    Returns:
        The centered text string.
    """
    return text.center(width - 2)  


def _format_panel_line(content: str, width: int = PANEL_WIDTH) -> str:
    """
    Format a single line of the panel with borders.

    Args:
        content: The content to display.
        width: The total panel width.

    Returns:
        A formatted panel line.
    """
    padding = width - 4  
    return f"{PANEL_VERTICAL}  {content:<{padding}}{PANEL_VERTICAL}"


def _print_panel_header() -> None:
    """Print the top border of the panel."""
    border = PANEL_BORDER * (PANEL_WIDTH - 2)
    print(f"{PANEL_CORNER_TL}{border}{PANEL_CORNER_TR}")


def _print_panel_separator() -> None:
    """Print a horizontal separator line within the panel."""
    border = PANEL_BORDER * (PANEL_WIDTH - 2)
    print(f"{PANEL_SEPARATOR}{border}{PANEL_SEPARATOR_RIGHT}")


def _print_panel_footer() -> None:
    """Print the bottom border of the panel."""
    border = PANEL_BORDER * (PANEL_WIDTH - 2)
    print(f"{PANEL_CORNER_BL}{border}{PANEL_CORNER_BR}")


def print_report(report: DateReport) -> None:
    """
    Render a formatted terminal report of date information.

    Displays a visually formatted panel containing all date information
    from the provided DateReport.

    Args:
        report: The DateReport instance to display.
    """
    d = report.date

    print()
    _print_panel_header()
    print(_format_panel_line(_center_text("✦ DAYFINDER PRO ✦")))
    _print_panel_separator()

    
    print(_format_panel_line(f"Date            : {d.strftime('%A, %d %B %Y')}"))
    print(_format_panel_line(f"Weekday         : {report.weekday}"))
    print(_format_panel_line(f"Day of year     : {report.day_of_year}"))
    print(_format_panel_line(f"ISO week        : {report.iso_week}"))
    print(_format_panel_line(f"Days in month   : {report.days_in_month}"))
    leap_status = "Yes" if report.is_leap_year else "No"
    print(_format_panel_line(f"Leap year       : {leap_status}"))

    
    if report.age is not None:
        print(_format_panel_line(f"Age             : {report.age} years"))
        birthday_text = report.next_birthday.strftime("%A, %d %B %Y")
        print(_format_panel_line(f"Next birthday   : {birthday_text}"))
        print(_format_panel_line(
            f"Birthday in     : {report.days_until_birthday} day(s)"
        ))
    else:
        print(_format_panel_line("Age             : Date is in the future"))

    _print_panel_separator()
    print(_format_panel_line(f"Fun fact        : {FUN_SAYINGS[report.weekday]}"))
    _print_panel_footer()
    print()


def interactive_mode() -> dt.date:
    """
    Collect a date from the user interactively.

    Displays a prompt and validates user input, repeatedly asking until
    a valid ISO date (YYYY-MM-DD) is provided.

    Returns:
        A validated datetime.date object.

    Raises:
        KeyboardInterrupt: If the user cancels the input (Ctrl+C).
    """
    print("\n" + "=" * 64)
    print("                 ✦ DAYFINDER PRO ✦")
    print("=" * 64)
    print("Enter a date to discover its calendar details.")
    print("Format: YYYY-MM-DD  (example: 2000-01-01)\n")

    while True:
        raw = input("Date > ").strip()
        try:
            return dt.date.fromisoformat(raw)
        except ValueError:
            print("  ✗ Invalid date. Please use YYYY-MM-DD.\n")


def build_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line interface.

    Builds an argument parser with support for optional date input and
    version display.

    Returns:
        A configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="dayfinder",
        description="Explore useful information about any calendar date.",
        epilog="For more information, visit: https://example.com/dayfinder",
    )
    parser.add_argument(
        "date",
        nargs="?",
        type=parse_date,
        help="date in YYYY-MM-DD format; if omitted, interactive mode is used",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    return parser


def main() -> int:
    """
    Application entry point.

    Orchestrates argument parsing, date report generation, and output display.
    Handles user interrupts and errors gracefully.

    Returns:
        Exit code: 0 for success, 1 for errors, 130 for interrupts.
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        selected_date = args.date or interactive_mode()
        report = build_report(selected_date)
        print_report(report)
        logger.info(f"Successfully analyzed date: {selected_date}")
        return 0
    except (KeyboardInterrupt, EOFError):
        print("\n\nGoodbye! 👋")
        logger.info("User interrupted the application")
        return 130
    except BrokenPipeError:
        
        logger.debug("Broken pipe error encountered")
        return 0
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        logger.error(f"ValueError: {exc}")
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        logger.exception(f"Unexpected error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
