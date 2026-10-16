"""
library.py
----------
Library — the main controller class.

Holds collections of Book and Student objects and orchestrates all
user-facing operations.  Delegates I/O to file_handler, transaction
logic to TransactionManager, and reporting to ReportManager.
"""

from typing import List, Optional

from book import Book
from student import Student
from transaction_manager import TransactionManager
from report_manager import ReportManager
import file_handler as fh
from utils import (
    display_table,
    get_non_empty_input,
    get_valid_phone,
    get_valid_year,
    get_valid_semester,
    validate_book_id_unique,
    validate_student_id_unique,
    press_enter_to_continue,
)


class Library:
    """
    Main controller: owns the in-memory book/student collections and
    all mutating operations.  Persists after every mutation.
    """

    def __init__(self):
        # Load all data on startup
        self.books: List[Book] = fh.load_books()
        self.students: List[Student] = fh.load_students()
        self.issued_records: List[dict] = fh.load_issued_books()

        self._transaction_mgr = TransactionManager()
        self._report_mgr = ReportManager()

    # ------------------------------------------------------------------
    # Book operations
    # ------------------------------------------------------------------

    def add_book(self) -> None:
        """Collect book details from user, validate, and persist."""
        print("\n  -- Add New Book --")

        book_id = get_non_empty_input("  Book ID   : ").upper()
        if not validate_book_id_unique(book_id, [b.book_id for b in self.books]):
            print(f"\n  [X]  Book ID '{book_id}' already exists. Duplicate IDs are not allowed.")
            return

        title = get_non_empty_input("  Title     : ")
        author = get_non_empty_input("  Author    : ")

        # Show category options
        print("  Categories: " + ", ".join(Book.VALID_CATEGORIES))
        category = get_non_empty_input("  Category  : ")

        year = get_valid_year()

        book = Book(
            book_id=book_id,
            title=title,
            author=author,
            category=category,
            year=int(year),
            status="Available",  # Assumption: new books default to Available
        )
        self.books.append(book)
        fh.save_books(self.books)

        print(f"\n  [OK]  Book '{title}' (ID: {book_id}) added successfully.")

    def view_books(self) -> None:
        """Display all books in a formatted table."""
        if not self.books:
            print("\n  (No books in the library yet.)")
            return

        headers = ["Book ID", "Title", "Author", "Category", "Year", "Status"]
        rows = [
            [b.book_id, b.title, b.author, b.category, b.year, b.status]
            for b in self.books
        ]
        display_table(headers, rows, title="ALL BOOKS")

    def search_book(self) -> None:
        """Search books by Book ID, Title, Author, or Category (case-insensitive)."""
        print("\n  -- Search Book --")
        print("  Search by: 1) Book ID  2) Title  3) Author  4) Category")
        choice = input("  Enter choice (1-4): ").strip()

        field_map = {"1": "Book ID", "2": "Title", "3": "Author", "4": "Category"}
        if choice not in field_map:
            print("  [X]  Invalid search option.")
            return

        field = field_map[choice]
        query = get_non_empty_input(f"  Enter {field}: ").lower()

        results = []
        for b in self.books:
            target = {
                "Book ID": b.book_id,
                "Title": b.title,
                "Author": b.author,
                "Category": b.category,
            }[field].lower()
            if query in target:
                results.append([b.book_id, b.title, b.author, b.category, b.year, b.status])

        if not results:
            print(f"\n  No books found matching '{query}' in {field}.")
        else:
            headers = ["Book ID", "Title", "Author", "Category", "Year", "Status"]
            display_table(headers, results, title=f"SEARCH RESULTS — {field}: '{query.upper()}'")

    def delete_book(self) -> None:
        """
        Remove a book from the library.
        Refuses if the book is currently Issued.
        """
        print("\n  -- Delete Book --")
        book_id = input("  Enter Book ID to delete: ").strip().upper()

        book = self._find_book(book_id)
        if book is None:
            print(f"\n  [X]  Book '{book_id}' not found.")
            return

        if book.status == "Issued":
            print(
                f"\n  [X]  Cannot delete '{book.title}' — it is currently Issued. "
                f"Please wait until it is returned."
            )
            return

        confirm = input(
            f"  Are you sure you want to delete '{book.title}'? (yes/no): "
        ).strip().lower()
        if confirm != "yes":
            print("  Delete operation cancelled.")
            return

        self.books.remove(book)
        fh.save_books(self.books)
        print(f"\n  [OK]  Book '{book.title}' (ID: {book_id}) deleted successfully.")

    # ------------------------------------------------------------------
    # Student operations
    # ------------------------------------------------------------------

    def register_student(self) -> None:
        """Collect student details from user, validate, and persist."""
        print("\n  -- Register Student --")

        student_id = get_non_empty_input("  Student ID : ").upper()
        if not validate_student_id_unique(student_id, [s.student_id for s in self.students]):
            print(
                f"\n  [X]  Student ID '{student_id}' already exists. Duplicate IDs not allowed."
            )
            return

        name = get_non_empty_input("  Name       : ")
        course = get_non_empty_input("  Course     : ")
        semester = get_valid_semester()
        phone = get_valid_phone()

        student = Student(
            student_id=student_id,
            name=name,
            course=course,
            semester=int(semester),
            phone=phone,
        )
        self.students.append(student)
        fh.save_students(self.students)

        print(f"\n  [OK]  Student '{name}' (ID: {student_id}) registered successfully.")

    def view_students(self) -> None:
        """Display all students in a formatted table."""
        if not self.students:
            print("\n  (No students registered yet.)")
            return

        headers = ["Student ID", "Name", "Course", "Semester", "Phone", "Books Borrowed"]
        rows = [
            [
                s.student_id,
                s.name,
                s.course,
                s.semester,
                s.phone,
                len(s.books_borrowed),
            ]
            for s in self.students
        ]
        display_table(headers, rows, title="ALL STUDENTS")

    def delete_student(self) -> None:
        """
        Remove a student from the registry.
        Refuses if the student currently has any book issued.
        """
        print("\n  -- Delete Student --")
        student_id = input("  Enter Student ID to delete: ").strip().upper()

        student = self._find_student(student_id)
        if student is None:
            print(f"\n  [X]  Student '{student_id}' not found.")
            return

        if student.books_borrowed:
            print(
                f"\n  [X]  Cannot delete '{student.name}' — they currently hold "
                f"{len(student.books_borrowed)} book(s): {', '.join(student.books_borrowed)}. "
                f"Please wait until all books are returned."
            )
            return

        confirm = input(
            f"  Are you sure you want to delete '{student.name}'? (yes/no): "
        ).strip().lower()
        if confirm != "yes":
            print("  Delete operation cancelled.")
            return

        self.students.remove(student)
        fh.save_students(self.students)
        print(f"\n  [OK]  Student '{student.name}' (ID: {student_id}) deleted successfully.")

    # ------------------------------------------------------------------
    # Issue / Return (delegate to TransactionManager)
    # ------------------------------------------------------------------

    def issue_book(self) -> None:
        """Issue a book to a student."""
        success = self._transaction_mgr.issue_book(
            self.books, self.students, self.issued_records
        )
        if success:
            # Persist all three data stores
            fh.save_books(self.books)
            fh.save_students(self.students)
            fh.save_issued_books(self.issued_records)

    def return_book(self) -> None:
        """Process a book return."""
        success = self._transaction_mgr.return_book(
            self.books, self.students, self.issued_records
        )
        if success:
            fh.save_books(self.books)
            fh.save_students(self.students)
            fh.save_issued_books(self.issued_records)

    # ------------------------------------------------------------------
    # Reports (delegate to ReportManager)
    # ------------------------------------------------------------------

    def generate_reports(self) -> None:
        """Generate and display all library reports."""
        self._report_mgr.generate_all_reports(
            self.books, self.students, self.issued_records
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _find_book(self, book_id: str) -> Optional[Book]:
        return next((b for b in self.books if b.book_id == book_id), None)

    def _find_student(self, student_id: str) -> Optional[Student]:
        return next((s for s in self.students if s.student_id == student_id), None)
