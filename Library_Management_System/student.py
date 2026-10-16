"""
student.py
----------
Defines the Student class representing a library member.
Demonstrates OOP encapsulation with clear attributes and methods.
"""

from typing import List


class Student:
    """
    Represents a student (library member).

    Attributes:
        student_id    (str)       : Unique identifier (e.g., S001)
        name          (str)       : Full name of the student
        course        (str)       : Enrolled course / programme
        semester      (int)       : Current semester number
        phone         (str)       : 10-digit phone number
        books_borrowed (List[str]): List of Book IDs currently borrowed
    """

    def __init__(
        self,
        student_id: str,
        name: str,
        course: str,
        semester: int,
        phone: str,
        books_borrowed: List[str] = None,
    ):
        self.student_id = student_id.strip().upper()
        self.name = name.strip()
        self.course = course.strip()
        self.semester = int(semester)
        self.phone = phone.strip()
        # Assumption: books_borrowed is a list of Book IDs (strings).
        # An empty list means the student has no books currently issued.
        self.books_borrowed: List[str] = books_borrowed if books_borrowed is not None else []

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display_student(self) -> None:
        """Print a formatted summary of this student's details."""
        borrowed = ", ".join(self.books_borrowed) if self.books_borrowed else "None"
        print("\n" + "-" * 44)
        print(f"  Student ID     : {self.student_id}")
        print(f"  Name           : {self.name}")
        print(f"  Course         : {self.course}")
        print(f"  Semester       : {self.semester}")
        print(f"  Phone          : {self.phone}")
        print(f"  Books Borrowed : {borrowed}")
        print("-" * 44)

    # ------------------------------------------------------------------
    # Borrow / Return helpers (business logic lives in TransactionManager)
    # ------------------------------------------------------------------

    def borrow_book(self, book_id: str) -> None:
        """
        Record a book as borrowed by adding its ID to books_borrowed.
        Note: Limit enforcement is done in TransactionManager, not here.
        """
        book_id = book_id.strip().upper()
        if book_id not in self.books_borrowed:
            self.books_borrowed.append(book_id)

    def return_book(self, book_id: str) -> bool:
        """
        Remove a book from books_borrowed when it is returned.
        Returns True if the book was found and removed, False otherwise.
        """
        book_id = book_id.strip().upper()
        if book_id in self.books_borrowed:
            self.books_borrowed.remove(book_id)
            return True
        return False

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a plain dict suitable for CSV serialisation."""
        return {
            "Student ID": self.student_id,
            "Name": self.name,
            "Course": self.course,
            "Semester": self.semester,
            "Phone": self.phone,
            # Assumption: Multiple borrowed book IDs are joined with '|' in CSV.
            "Books Borrowed": "|".join(self.books_borrowed),
        }

    @classmethod
    def from_dict(cls, row: dict) -> "Student":
        """
        Construct a Student instance from a CSV row dict.
        Raises ValueError if required keys are missing.
        """
        required = ["Student ID", "Name", "Course", "Semester", "Phone"]
        for key in required:
            if key not in row:
                raise ValueError(f"Missing column '{key}' in students.csv row: {row}")
        # Parse the pipe-separated borrowed list; handle empty gracefully.
        raw_borrowed = row.get("Books Borrowed", "").strip()
        books_borrowed = [b for b in raw_borrowed.split("|") if b.strip()] if raw_borrowed else []
        return cls(
            student_id=row["Student ID"],
            name=row["Name"],
            course=row["Course"],
            semester=row["Semester"],
            phone=row["Phone"],
            books_borrowed=books_borrowed,
        )

    def __repr__(self) -> str:
        return (
            f"Student(id={self.student_id!r}, name={self.name!r}, "
            f"borrowed={self.books_borrowed})"
        )
