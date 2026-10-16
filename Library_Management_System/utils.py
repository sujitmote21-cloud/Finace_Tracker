"""
utils.py
--------
Utility / helper functions shared across the system.
Covers input validation, screen helpers, and table display.
"""

import os
import datetime
from typing import List, Dict, Any


# ----------------------------------------------------------------------
# Screen helpers
# ----------------------------------------------------------------------

def clear_screen() -> None:
    """Clear the terminal screen (works on Windows, macOS, and Linux)."""
    os.system("cls" if os.name == "nt" else "clear")


def display_table(headers: List[str], rows: List[List[Any]], title: str = "") -> None:
    """
    Print a formatted ASCII table from a list of headers and row values.

    Parameters:
        headers : Column header strings
        rows    : Each inner list must have len == len(headers)
        title   : Optional title printed above the table
    """
    if not rows and not headers:
        print("  (no data to display)")
        return

    # Compute column widths (max of header length and each row value length)
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    header_row = "|" + "|".join(
        f" {str(h).ljust(col_widths[i])} " for i, h in enumerate(headers)
    ) + "|"

    if title:
        total_width = sum(col_widths) + 3 * len(col_widths) + 1
        print("\n" + "=" * total_width)
        print(f"  {title}")
        print("=" * total_width)

    print(separator)
    print(header_row)
    print(separator)
    if not rows:
        inner_width = len(separator) - 2
        print("|" + " No records found. ".center(inner_width) + "|")
    else:
        for row in rows:
            data_row = "|" + "|".join(
                f" {str(cell).ljust(col_widths[i])} " for i, cell in enumerate(row)
            ) + "|"
            print(data_row)
    print(separator)
    print()


# ----------------------------------------------------------------------
# Validators
# ----------------------------------------------------------------------

def validate_phone(phone: str) -> bool:
    """
    Return True if phone is exactly 10 digits, False otherwise.

    Valid   : '9876543210'  → True
    Invalid : '12345'       → False  (too short)
    Invalid : 'abcd123456'  → False  (non-numeric)
    """
    return phone.isdigit() and len(phone) == 10


def validate_year(year: str) -> bool:
    """
    Return True if year is a 4-digit integer not exceeding the current year.

    Valid   : '2023'  → True  (past year)
    Invalid : '2999'  → False (future year beyond current)
    Invalid : 'abcd'  → False (non-numeric)
    """
    current_year = datetime.date.today().year
    if not year.isdigit():
        return False
    return 1000 <= int(year) <= current_year


def validate_book_id_unique(book_id: str, existing_ids: List[str]) -> bool:
    """
    Return True if book_id is NOT already in existing_ids (i.e., unique).

    Valid   : 'B005' not in ['B001','B002'] → True
    Invalid : 'B001' in ['B001','B002']     → False
    """
    return book_id.strip().upper() not in [bid.upper() for bid in existing_ids]


def validate_student_id_unique(student_id: str, existing_ids: List[str]) -> bool:
    """
    Return True if student_id is NOT already in existing_ids (i.e., unique).

    Valid   : 'S005' not in ['S001','S002'] → True
    Invalid : 'S001' in ['S001','S002']     → False
    """
    return student_id.strip().upper() not in [sid.upper() for sid in existing_ids]


def validate_semester(semester: str) -> bool:
    """
    Return True if semester is a positive integer (1–12 is a reasonable range).
    Assumption: Semesters run from 1 to 12.
    """
    if not semester.isdigit():
        return False
    return 1 <= int(semester) <= 12


# ----------------------------------------------------------------------
# Input helpers
# ----------------------------------------------------------------------

def get_non_empty_input(prompt: str) -> str:
    """Prompt the user until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!]  This field cannot be empty. Please try again.")


def get_valid_phone(prompt: str = "  Phone (10 digits): ") -> str:
    """Prompt until a valid 10-digit phone number is entered."""
    while True:
        phone = input(prompt).strip()
        if validate_phone(phone):
            return phone
        print("  [!]  Phone must be exactly 10 digits. Please try again.")


def get_valid_year(prompt: str = "  Publication Year : ") -> str:
    """Prompt until a valid publication year is entered."""
    while True:
        year = input(prompt).strip()
        if validate_year(year):
            return year
        current = datetime.date.today().year
        print(f"  [!]  Year must be a number between 1000 and {current}. Please try again.")


def get_valid_semester(prompt: str = "  Semester (1-12) : ") -> str:
    """Prompt until a valid semester number is entered."""
    while True:
        sem = input(prompt).strip()
        if validate_semester(sem):
            return sem
        print("  [!]  Semester must be a number between 1 and 12. Please try again.")


def get_valid_menu_choice(prompt: str, valid_range: range) -> int:
    """Prompt until an integer within valid_range is entered."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and int(raw) in valid_range:
            return int(raw)
        print(f"  [!]  Please enter a number between {valid_range.start} and {valid_range.stop - 1}.")


def press_enter_to_continue() -> None:
    """Pause execution until the user presses Enter."""
    input("\n  Press Enter to continue...")
