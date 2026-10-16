"""
book.py
-------
Defines the Book class representing a single library book.
Demonstrates OOP encapsulation with clear attributes and methods.
"""


class Book:
    """
    Represents a single book in the library.

    Attributes:
        book_id     (str)  : Unique identifier for the book (e.g., B001)
        title       (str)  : Title of the book
        author      (str)  : Author of the book
        category    (str)  : Category/genre (e.g., Programming, History)
        year        (int)  : Publication year
        status      (str)  : 'Available' or 'Issued'
    """

    # Assumption: Predefined categories to keep data consistent.
    VALID_CATEGORIES = [
        "Programming",
        "Economics",
        "Mathematics",
        "Statistics",
        "Literature",
        "History",
        "Science",
        "Other",
    ]

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        category: str,
        year: int,
        status: str = "Available",
    ):
        self.book_id = book_id.strip().upper()
        self.title = title.strip()
        self.author = author.strip()
        self.category = category.strip()
        self.year = int(year)
        # Assumption: Default status is 'Available' when a new book is added.
        self.status = status.strip() if status else "Available"

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display_book(self) -> None:
        """Print a formatted summary of this book's details."""
        print("\n" + "-" * 40)
        print(f"  Book ID   : {self.book_id}")
        print(f"  Title     : {self.title}")
        print(f"  Author    : {self.author}")
        print(f"  Category  : {self.category}")
        print(f"  Year      : {self.year}")
        print(f"  Status    : {self.status}")
        print("-" * 40)

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def update_book(
        self,
        title: str = None,
        author: str = None,
        category: str = None,
        year: int = None,
    ) -> None:
        """
        Update one or more fields of the book.
        Only non-None arguments are applied.
        """
        if title is not None:
            self.title = title.strip()
        if author is not None:
            self.author = author.strip()
        if category is not None:
            self.category = category.strip()
        if year is not None:
            self.year = int(year)

    def mark_available(self) -> None:
        """Set the book's status to 'Available'."""
        self.status = "Available"

    def mark_unavailable(self) -> None:
        """Set the book's status to 'Issued' (makes the book unavailable)."""
        self.status = "Issued"

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a plain dict suitable for CSV serialisation."""
        return {
            "Book ID": self.book_id,
            "Title": self.title,
            "Author": self.author,
            "Category": self.category,
            "Year": self.year,
            "Status": self.status,
        }

    @classmethod
    def from_dict(cls, row: dict) -> "Book":
        """
        Construct a Book instance from a CSV row dict.
        Raises ValueError if required keys are missing.
        """
        required = ["Book ID", "Title", "Author", "Category", "Year", "Status"]
        for key in required:
            if key not in row:
                raise ValueError(f"Missing column '{key}' in books.csv row: {row}")
        return cls(
            book_id=row["Book ID"],
            title=row["Title"],
            author=row["Author"],
            category=row["Category"],
            year=row["Year"],
            status=row["Status"],
        )

    def __repr__(self) -> str:
        return (
            f"Book(id={self.book_id!r}, title={self.title!r}, "
            f"status={self.status!r})"
        )
