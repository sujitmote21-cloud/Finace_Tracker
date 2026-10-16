"""
file_handler.py
---------------
Handles all CSV I/O: loading and saving Books, Students, and
issued-book records.  Converts between CSV rows and domain objects.

Design principle: this module knows about files; the Library class
knows about business logic.  Keep them separate.
"""

import csv
import os
from typing import List, Dict

from book import Book
from student import Student


# ----------------------------------------------------------------------
# File paths  (relative to the project root)
# ----------------------------------------------------------------------

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")

BOOKS_FILE = os.path.join(DATA_DIR, "books.csv")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.csv")
ISSUED_FILE = os.path.join(DATA_DIR, "issued_books.csv")
REPORT_FILE = os.path.join(REPORTS_DIR, "library_report.csv")

# CSV column headers
BOOKS_HEADERS = ["Book ID", "Title", "Author", "Category", "Year", "Status"]
STUDENTS_HEADERS = [
    "Student ID", "Name", "Course", "Semester", "Phone", "Books Borrowed"
]
ISSUED_HEADERS = [
    "Issue ID", "Student ID", "Book ID", "Issue Date", "Return Date", "Status"
]


# ----------------------------------------------------------------------
# Internal helpers
# ----------------------------------------------------------------------

def _ensure_dir(path: str) -> None:
    """Create directory (and parents) if it does not exist."""
    os.makedirs(path, exist_ok=True)


def _ensure_csv(filepath: str, headers: List[str]) -> None:
    """
    Create a CSV file with the given headers if it does not already exist.
    If the file exists but is empty, write the headers so the rest of the
    code can always assume a well-formed file.
    """
    _ensure_dir(os.path.dirname(filepath))
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
        return
    # File exists — check whether it has at least a header row
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
    except Exception:
        # Corrupted file: recreate with headers only
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def _read_csv(filepath: str, headers: List[str]) -> List[Dict]:
    """
    Safely read a CSV file.  Returns a list of row dicts.
    Never raises an exception — returns [] on any error.
    Missing columns in a row are silently ignored (row will lack that key).
    """
    _ensure_csv(filepath, headers)
    rows = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip completely blank rows
                if any(v.strip() for v in row.values() if v):
                    rows.append(dict(row))
    except Exception as e:
        print(f"  [!]  Warning: Could not fully read '{os.path.basename(filepath)}': {e}")
    return rows


def _write_csv(filepath: str, headers: List[str], rows: List[Dict]) -> None:
    """
    Overwrite a CSV file with the given list of row dicts.
    Creates parent directories if they don't exist.
    """
    _ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


# ----------------------------------------------------------------------
# Books
# ----------------------------------------------------------------------

def load_books() -> List[Book]:
    """
    Load all books from books.csv and return a list of Book objects.
    Rows that cannot be parsed (missing/corrupt columns) are skipped
    with a warning so the program never crashes.
    """
    rows = _read_csv(BOOKS_FILE, BOOKS_HEADERS)
    books = []
    for row in rows:
        try:
            books.append(Book.from_dict(row))
        except (ValueError, KeyError) as e:
            print(f"  [!]  Skipping malformed book row: {e}")
    return books


def save_books(books: List[Book]) -> None:
    """Persist the current list of Book objects to books.csv."""
    rows = [b.to_dict() for b in books]
    _write_csv(BOOKS_FILE, BOOKS_HEADERS, rows)


# ----------------------------------------------------------------------
# Students
# ----------------------------------------------------------------------

def load_students() -> List[Student]:
    """
    Load all students from students.csv and return a list of Student objects.
    Malformed rows are skipped with a warning.
    """
    rows = _read_csv(STUDENTS_FILE, STUDENTS_HEADERS)
    students = []
    for row in rows:
        try:
            students.append(Student.from_dict(row))
        except (ValueError, KeyError) as e:
            print(f"  [!]  Skipping malformed student row: {e}")
    return students


def save_students(students: List[Student]) -> None:
    """Persist the current list of Student objects to students.csv."""
    rows = [s.to_dict() for s in students]
    _write_csv(STUDENTS_FILE, STUDENTS_HEADERS, rows)


# ----------------------------------------------------------------------
# Issued Books
# ----------------------------------------------------------------------

def load_issued_books() -> List[Dict]:
    """
    Load all issued-book records from issued_books.csv.
    Returns a list of plain dicts (no domain object — kept simple).
    """
    return _read_csv(ISSUED_FILE, ISSUED_HEADERS)


def save_issued_books(records: List[Dict]) -> None:
    """Persist the issued-books list to issued_books.csv."""
    _write_csv(ISSUED_FILE, ISSUED_HEADERS, records)


# ----------------------------------------------------------------------
# Reports directory bootstrap
# ----------------------------------------------------------------------

def ensure_reports_dir() -> None:
    """Create the reports/ directory if it does not exist."""
    _ensure_dir(REPORTS_DIR)


def save_report_csv(rows: List[Dict], headers: List[str]) -> None:
    """Write report data to reports/library_report.csv."""
    ensure_reports_dir()
    _write_csv(REPORT_FILE, headers, rows)
