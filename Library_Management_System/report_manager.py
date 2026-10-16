"""
report_manager.py
-----------------
Generates statistical reports from the in-memory data and exports
them to reports/library_report.csv.

Reports produced:
  1. Total / Available / Issued book counts
  2. Most Borrowed Category (by historical issued_books records)
  3. Student with maximum books currently borrowed
  4. Recently Issued Books (last 10 by Issue Date)
"""

import datetime
from collections import Counter
from typing import List, Dict, Optional

from book import Book
from student import Student
import file_handler as fh
from utils import display_table


class ReportManager:
    """
    Generates and exports library reports.
    All methods are read-only — no mutations to data.
    """

    def generate_all_reports(
        self,
        books: List[Book],
        students: List[Student],
        issued_records: List[Dict],
    ) -> None:
        """Run all reports, display them, and export to CSV."""
        print("\n" + "=" * 60)
        print("                  LIBRARY REPORTS")
        print("=" * 60)

        self._report_book_counts(books)
        self._report_most_borrowed_category(books, issued_records)
        self._report_top_borrower(students)
        self._report_recent_issues(issued_records)
        self._export_report(books, students, issued_records)

    # ------------------------------------------------------------------
    # Report 1: Book counts
    # ------------------------------------------------------------------

    def _report_book_counts(self, books: List[Book]) -> None:
        total = len(books)
        available = sum(1 for b in books if b.status == "Available")
        issued = total - available

        print("\n  [BOOKS]  Book Statistics")
        headers = ["Metric", "Count"]
        rows = [
            ["Total Books", total],
            ["Available Books", available],
            ["Issued Books", issued],
        ]
        display_table(headers, rows)

    # ------------------------------------------------------------------
    # Report 2: Most borrowed category
    # ------------------------------------------------------------------

    def _report_most_borrowed_category(
        self, books: List[Book], issued_records: List[Dict]
    ) -> None:
        print("  [TOP]  Most Borrowed Category")

        if not issued_records:
            print("     No issue records found.\n")
            return

        # Build a map from Book ID → Category
        book_category = {b.book_id: b.category for b in books}

        category_counts: Counter = Counter()
        for rec in issued_records:
            bid = rec.get("Book ID", "").upper()
            cat = book_category.get(bid, "Unknown")
            category_counts[cat] += 1

        headers = ["Category", "Times Borrowed"]
        rows = [[cat, count] for cat, count in category_counts.most_common()]
        display_table(headers, rows)

    # ------------------------------------------------------------------
    # Report 3: Top borrower (currently)
    # ------------------------------------------------------------------

    def _report_top_borrower(self, students: List[Student]) -> None:
        print("  [STUDENT]  Students with Most Books Currently Borrowed")

        if not students:
            print("     No student records found.\n")
            return

        sorted_students = sorted(
            students, key=lambda s: len(s.books_borrowed), reverse=True
        )
        headers = ["Student ID", "Name", "Books Currently Borrowed"]
        rows = [
            [s.student_id, s.name, len(s.books_borrowed)]
            for s in sorted_students
            if len(s.books_borrowed) > 0
        ]
        if not rows:
            print("     No student currently holds a book.\n")
        else:
            display_table(headers, rows)

    # ------------------------------------------------------------------
    # Report 4: Recently issued books (last 10)
    # ------------------------------------------------------------------

    def _report_recent_issues(self, issued_records: List[Dict]) -> None:
        print("  [TIME]  Recently Issued Books (Last 10)")

        if not issued_records:
            print("     No issue records found.\n")
            return

        # Sort by Issue Date descending; take top 10
        sorted_records = sorted(
            issued_records,
            key=lambda r: r.get("Issue Date", ""),
            reverse=True,
        )[:10]

        headers = ["Issue ID", "Student ID", "Book ID", "Issue Date", "Due Date", "Status"]
        rows = [
            [
                r.get("Issue ID", ""),
                r.get("Student ID", ""),
                r.get("Book ID", ""),
                r.get("Issue Date", ""),
                r.get("Return Date", ""),
                r.get("Status", ""),
            ]
            for r in sorted_records
        ]
        display_table(headers, rows)

    # ------------------------------------------------------------------
    # Export to CSV
    # ------------------------------------------------------------------

    def _export_report(
        self,
        books: List[Book],
        students: List[Student],
        issued_records: List[Dict],
    ) -> None:
        """
        Build a single flat CSV with all report data, grouped by section.
        Each section starts with a blank row and a section-header row.
        """
        export_rows: List[Dict] = []
        headers = ["Section", "Label", "Value"]

        # -- Section 1: Book counts ------------------------------------
        total = len(books)
        available = sum(1 for b in books if b.status == "Available")
        issued_count = total - available
        export_rows += [
            {"Section": "Book Statistics", "Label": "Total Books", "Value": total},
            {"Section": "", "Label": "Available Books", "Value": available},
            {"Section": "", "Label": "Issued Books", "Value": issued_count},
            {"Section": "", "Label": "", "Value": ""},  # blank separator
        ]

        # -- Section 2: Category counts --------------------------------
        book_category = {b.book_id: b.category for b in books}
        category_counts: Counter = Counter()
        for rec in issued_records:
            bid = rec.get("Book ID", "").upper()
            cat = book_category.get(bid, "Unknown")
            category_counts[cat] += 1

        export_rows.append(
            {"Section": "Most Borrowed Category", "Label": "Category", "Value": "Times Borrowed"}
        )
        for cat, cnt in category_counts.most_common():
            export_rows.append({"Section": "", "Label": cat, "Value": cnt})
        export_rows.append({"Section": "", "Label": "", "Value": ""})

        # -- Section 3: Top borrowers ----------------------------------
        export_rows.append(
            {"Section": "Current Borrowers", "Label": "Student Name", "Value": "Books Borrowed"}
        )
        for s in sorted(students, key=lambda x: len(x.books_borrowed), reverse=True):
            if s.books_borrowed:
                export_rows.append(
                    {"Section": "", "Label": s.name, "Value": len(s.books_borrowed)}
                )
        export_rows.append({"Section": "", "Label": "", "Value": ""})

        # -- Section 4: Recent issues ----------------------------------
        export_rows.append(
            {
                "Section": "Recent Issues (last 10)",
                "Label": "Issue ID | Student | Book",
                "Value": "Issue Date | Status",
            }
        )
        sorted_records = sorted(
            issued_records,
            key=lambda r: r.get("Issue Date", ""),
            reverse=True,
        )[:10]
        for r in sorted_records:
            label = f"{r.get('Issue ID','')} | {r.get('Student ID','')} | {r.get('Book ID','')}"
            value = f"{r.get('Issue Date','')} | {r.get('Status','')}"
            export_rows.append({"Section": "", "Label": label, "Value": value})

        fh.save_report_csv(export_rows, headers)
        print("  [OK]  Report exported to reports/library_report.csv\n")
