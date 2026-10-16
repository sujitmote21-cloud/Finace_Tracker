"""
transaction_manager.py
----------------------
Handles the Issue Book and Return Book workflows.

Key business rules implemented here:
  - Verify student and book exist before any action.
  - A book must be 'Available' to be issued.
  - A student cannot borrow more than MAX_BOOKS at once.
  - Issue IDs are auto-generated (I001, I002 …).
  - Loan period is LOAN_DAYS days; fine of FINE_PER_DAY rupees/day for late returns.
"""

import datetime
from typing import List, Dict, Optional

from book import Book
from student import Student
import file_handler as fh

# ----------------------------------------------------------------------
# Constants  (document assumptions with comments)
# ----------------------------------------------------------------------

# Assumption: Default loan period is 14 days.
LOAN_DAYS: int = 14

# Assumption: Maximum books a student may borrow at one time.
MAX_BOOKS: int = 3

# Assumption: Fine is ₹5 per day for each day past the due date.
FINE_PER_DAY: int = 5


class TransactionManager:
    """
    Manages the borrowing and returning of books.

    This class is stateless between calls — it works with the
    books, students, and issued_records lists passed by Library.
    """

    # ------------------------------------------------------------------
    # Issue Book
    # ------------------------------------------------------------------

    def issue_book(
        self,
        books: List[Book],
        students: List[Student],
        issued_records: List[Dict],
    ) -> bool:
        """
        Interactive workflow to issue a book to a student.

        Steps:
          1. Collect Student ID and Book ID from the user.
          2. Verify student exists.
          3. Check borrowing limit.
          4. Verify book exists and is Available.
          5. Check book is not already in an open issue.
          6. Create issue record and update all data structures.

        Returns True if the issue succeeded, False otherwise.
        """
        print("\n  -- Issue Book --")
        student_id = input("  Enter Student ID : ").strip().upper()
        book_id = input("  Enter Book ID    : ").strip().upper()

        # -- Step 2: Find student --------------------------------------
        student = self._find_student(students, student_id)
        if student is None:
            print(f"\n  [X]  Student '{student_id}' not found.")
            return False

        # -- Step 3: Borrowing limit -----------------------------------
        if len(student.books_borrowed) >= MAX_BOOKS:
            print(
                f"\n  [X]  '{student.name}' has already borrowed {MAX_BOOKS} book(s) "
                f"(limit: {MAX_BOOKS}). Cannot issue more."
            )
            return False

        # -- Step 4: Find book -----------------------------------------
        book = self._find_book(books, book_id)
        if book is None:
            print(f"\n  [X]  Book '{book_id}' not found.")
            return False

        if book.status != "Available":
            print(f"\n  [X]  Book '{book.title}' is currently Issued. Cannot re-issue.")
            return False

        # -- Step 5: Guard against duplicate open issues ---------------
        # (Extra safety — should not happen if status is correct, but be defensive)
        if self._find_open_issue(issued_records, student_id, book_id):
            print(
                f"\n  [X]  An open issue record already exists for "
                f"student '{student_id}' and book '{book_id}'."
            )
            return False

        # -- Step 6: Create transaction --------------------------------
        issue_id = self._generate_issue_id(issued_records)
        issue_date = datetime.date.today()
        # Assumption: Return date is LOAN_DAYS days after issue date.
        return_date = issue_date + datetime.timedelta(days=LOAN_DAYS)

        record: Dict = {
            "Issue ID": issue_id,
            "Student ID": student_id,
            "Book ID": book_id,
            "Issue Date": issue_date.isoformat(),
            "Return Date": return_date.isoformat(),
            "Status": "Issued",
        }
        issued_records.append(record)

        # Update book and student in-memory
        book.mark_unavailable()
        student.borrow_book(book_id)

        print(f"\n  [OK]  Book '{book.title}' issued to '{student.name}'.")
        print(f"     Issue ID    : {issue_id}")
        print(f"     Issue Date  : {issue_date}")
        print(f"     Due Date    : {return_date}  (loan period: {LOAN_DAYS} days)")
        return True

    # ------------------------------------------------------------------
    # Return Book
    # ------------------------------------------------------------------

    def return_book(
        self,
        books: List[Book],
        students: List[Student],
        issued_records: List[Dict],
    ) -> bool:
        """
        Interactive workflow to return a borrowed book.

        Steps:
          1. Collect Student ID and Book ID from user.
          2. Find the open issue record.
          3. Calculate any late fine.
          4. Mark record as Returned; mark book Available; update student.

        Returns True if return succeeded, False otherwise.
        """
        print("\n  -- Return Book --")
        student_id = input("  Enter Student ID : ").strip().upper()
        book_id = input("  Enter Book ID    : ").strip().upper()

        # -- Step 2: Find the open issue -------------------------------
        record = self._find_open_issue(issued_records, student_id, book_id)
        if record is None:
            print(
                f"\n  [X]  No open issue found for student '{student_id}' "
                f"and book '{book_id}'."
            )
            return False

        # -- Step 3: Fine calculation ----------------------------------
        today = datetime.date.today()
        due_date = datetime.date.fromisoformat(record["Return Date"])
        fine = 0
        if today > due_date:
            late_days = (today - due_date).days
            # Assumption: Fine applies only after the due date, ₹5 per day.
            fine = late_days * FINE_PER_DAY
            print(f"\n  [!]  Book returned {late_days} day(s) late.")
            print(f"     Fine due: ₹{fine}  (₹{FINE_PER_DAY}/day × {late_days} day(s))")
        else:
            print("\n  [OK]  Book returned on time. No fine.")

        # -- Step 4: Update all data structures ------------------------
        record["Return Date"] = today.isoformat()
        record["Status"] = "Returned"

        book = self._find_book(books, book_id)
        if book:
            book.mark_available()

        student = self._find_student(students, student_id)
        if student:
            student.return_book(book_id)

        title = book.title if book else book_id
        name = student.name if student else student_id
        print(f"\n  [OK]  '{title}' returned by '{name}' on {today}.")
        return True

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _find_book(books: List[Book], book_id: str) -> Optional[Book]:
        """Return the Book with the matching ID, or None."""
        return next((b for b in books if b.book_id == book_id), None)

    @staticmethod
    def _find_student(students: List[Student], student_id: str) -> Optional[Student]:
        """Return the Student with the matching ID, or None."""
        return next((s for s in students if s.student_id == student_id), None)

    @staticmethod
    def _find_open_issue(
        issued_records: List[Dict], student_id: str, book_id: str
    ) -> Optional[Dict]:
        """Return the first open issue record matching student + book, or None."""
        for rec in issued_records:
            if (
                rec.get("Student ID", "").upper() == student_id
                and rec.get("Book ID", "").upper() == book_id
                and rec.get("Status", "").lower() == "issued"
            ):
                return rec
        return None

    @staticmethod
    def _generate_issue_id(issued_records: List[Dict]) -> str:
        """
        Generate the next sequential Issue ID in the format 'I001'.
        Finds the maximum existing numeric suffix and increments by 1.
        """
        max_num = 0
        for rec in issued_records:
            issue_id = rec.get("Issue ID", "")
            if issue_id.startswith("I") and issue_id[1:].isdigit():
                max_num = max(max_num, int(issue_id[1:]))
        return f"I{(max_num + 1):03d}"
