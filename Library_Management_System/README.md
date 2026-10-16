# 📚 Library Management System

A portfolio-quality command-line Python application demonstrating **Object-Oriented Programming** principles. The system manages books and student records, handles issuing/returning books, and generates statistical reports — with full data persistence across CSV files.

---

## Features

| # | Feature |
|---|---------|
| 1 | Add, view, search, and delete books |
| 2 | Register, view, and delete students |
| 3 | Issue books to students with auto-generated Issue IDs |
| 4 | Return books with **late-return fine calculation (₹5/day)** |
| 5 | Enforce **borrowing limit** (max 3 books per student) |
| 6 | Block deletion of issued books or students holding books |
| 7 | Four-section library reports exported to CSV |
| 8 | Graceful handling of missing / corrupted CSV files |
| 9 | Data persists across restarts via three CSV files |

---

## Project Structure

```
Library_Management_System/
├── main.py                 ← Entry point; menu loop
├── library.py              ← Main controller class
├── book.py                 ← Book class (OOP core)
├── student.py              ← Student class (OOP core)
├── transaction_manager.py  ← Issue / Return workflow
├── report_manager.py       ← Statistical reports
├── file_handler.py         ← CSV load / save helpers
├── utils.py                ← Validators, table display, input helpers
├── data/
│   ├── books.csv           ← Book records
│   ├── students.csv        ← Student records
│   └── issued_books.csv    ← Issue / return transaction log
├── reports/
│   └── library_report.csv  ← Auto-generated report export
├── README.md
└── requirements.txt
```

---

## How to Run

> **Requires Python 3.8 or later.  No third-party libraries needed.**

```bash
cd Library_Management_System
python main.py
```

That's it — no virtual environment or `pip install` required.

---

## Main Menu

```
==================================
      LIBRARY MANAGEMENT SYSTEM
==================================
  1.  Add Book
  2.  View Books
  3.  Search Book
  4.  Register Student
  5.  View Students
  6.  Issue Book
  7.  Return Book
  8.  Delete Book
  9.  Delete Student
  10. Reports
  11. Exit
==================================
```

---

## Class Design

### `Book` (`book.py`)
Represents a single library book.

| Attribute | Type | Description |
|-----------|------|-------------|
| `book_id` | str | Unique identifier (e.g., B001) |
| `title` | str | Book title |
| `author` | str | Author name |
| `category` | str | Genre / subject area |
| `year` | int | Publication year |
| `status` | str | `"Available"` or `"Issued"` |

**Methods:** `display_book()`, `update_book()`, `mark_available()`, `mark_unavailable()`, `to_dict()`, `from_dict()`

---

### `Student` (`student.py`)
Represents a library member.

| Attribute | Type | Description |
|-----------|------|-------------|
| `student_id` | str | Unique identifier (e.g., S001) |
| `name` | str | Full name |
| `course` | str | Enrolled programme |
| `semester` | int | Current semester (1–12) |
| `phone` | str | 10-digit phone number |
| `books_borrowed` | List[str] | Book IDs currently held |

**Methods:** `display_student()`, `borrow_book(book_id)`, `return_book(book_id)`, `to_dict()`, `from_dict()`

---

### `Library` (`library.py`)
Main controller — owns all in-memory data and orchestrates operations.

**Responsibilities:**
- Loads data from CSV on startup via `file_handler`
- Delegates book/student CRUD to self
- Delegates issue/return to `TransactionManager`
- Delegates report generation to `ReportManager`
- Persists after every mutating action

---

### `TransactionManager` (`transaction_manager.py`)
Handles borrowing workflow with business rule enforcement.

| Constant | Value | Description |
|----------|-------|-------------|
| `LOAN_DAYS` | 14 | Default loan period in days |
| `MAX_BOOKS` | 3 | Maximum books per student |
| `FINE_PER_DAY` | 5 | Fine in ₹ per day after due date |

---

### `ReportManager` (`report_manager.py`)
Generates four statistical reports and exports them to CSV:
1. Total / Available / Issued book counts
2. Most borrowed category (by historical records)
3. Students with most books currently borrowed
4. Recently issued books (last 10)

---

## Data Files

| File | Purpose | Recreated if missing |
|------|---------|----------------------|
| `data/books.csv` | Book catalogue | ✓ Yes (headers only) |
| `data/students.csv` | Student registry | ✓ Yes (headers only) |
| `data/issued_books.csv` | Issue/return log | ✓ Yes (headers only) |

The seed data included in each CSV provides 5 sample books and 3 sample students for immediate demo use.

---

## Business Rules (Key Assumptions)

- New books default to `Available` status
- `LOAN_DAYS = 14` — return due 14 days after issue
- `MAX_BOOKS = 3` — a student cannot hold more than 3 books at once
- `FINE_PER_DAY = ₹5` — charged per day beyond due date
- A book **cannot be deleted** while its status is `Issued`
- A student **cannot be deleted** while they hold any borrowed book
- Phone numbers must be exactly **10 digits**
- Publication year cannot exceed the **current year**
- Book IDs and Student IDs must be **unique** (case-insensitive)
- Multiple borrowed Book IDs are stored in students.csv separated by `|`

---

## Error Handling

The system handles all of the following gracefully (no raw tracebacks):

- Book not found / Student not found
- Duplicate Book ID or Student ID
- Book already issued (cannot re-issue)
- Student at borrowing limit
- Invalid menu option
- Missing or corrupted CSV file (auto-recreated with headers)

---

## Optional Extras (not yet implemented)
- Librarian login system
- Book reservation for already-issued books
- Due-date reminder dashboard
- Expanded / filtered report exports
