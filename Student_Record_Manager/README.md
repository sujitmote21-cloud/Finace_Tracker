# Student Record Management System

A portfolio-quality command-line interface (CLI) application developed in Python. It supports adding, viewing, searching, updating, deleting, and analyzing student records. All records are persisted locally in a CSV file, ensuring that the student database survives system restarts.

## Features

- **Robust Validators**: Real-time validation for email structure, 10-digit phone numbers, age limits (16–35), and marks (0–100).
- **Auto-Grade Calculation**: Grades are derived automatically from students' marks:
  - 90–100 &rarr; `A+`
  - 80–89 &rarr; `A`
  - 70–79 &rarr; `B`
  - 60–69 &rarr; `C`
  - 50–59 &rarr; `D`
  - Below 50 &rarr; `F`
- **Dynamic Text Tables**: A custom-built table formatter displaying record listings neatly inside a dynamically calculated grid.
- **Enhanced Search and View Operations**:
  - Perform lookups by ID, Name, or Course.
  - Sort record listings by Marks, Name, or ID.
  - Filter record listings by Course or Semester.
  - Display the top 5 performing students.
- **Statistics Dashboards**:
  - Generates metrics: total student count, average marks, highest/lowest mark, pass percentage, and identity of the topper(s).
  - Ability to export compiled statistics to a `statistics.csv` file.
- **Resilient File Handling**: Checks for DB directory structure and auto-generates database columns. Gracefully catches corrupted headers, formatting differences, or parsing errors without crashing.

## Folder Structure

```
Student_Record_Manager/
├── main.py             # Application Entry Point & Menu UI loop
├── student_manager.py  # Core operational logic (Add, Edit, Delete, Stats, etc.)
├── file_handler.py     # CSV Persistence (Loading, Saving, Re-initialization)
├── utils.py            # Input validators, CLI helpers, & custom table formatter
├── data/
│   └── students.csv    # Saved student records database (created dynamically)
├── README.md           # Documentation
└── requirements.txt    # Project dependencies list (Standard Library only)
```

## Getting Started

### Prerequisites
- Python 3.x

### Run Instructions
1. Navigate to the project directory:
   ```bash
   cd Student_Record_Manager
   ```
2. Start the program:
   - **Launch GUI (Default):**
     ```bash
     python main.py
     ```
   - **Launch CLI (Interactive Command-Line):**
     ```bash
     python main.py --cli
     ```
3. Data is automatically loaded and saved back to `data/students.csv`.

## Verification & Testing
To ensure database operations and validators remain fully compliant, there are unit and manual verification scripts in the conversation's scratch space.
- Run validator checks:
  ```bash
  python scratch/test_validators.py
  ```
- Run flow verification checks:
  ```bash
  python scratch/verify_cli.py
  ```
