"""
main.py
-------
Entry point for the Library Management System.

Displays the main menu in a loop, routes choices to the Library class,
and handles invalid input without crashing.
"""

from library import Library
from utils import clear_screen, press_enter_to_continue


# ----------------------------------------------------------------------
# Menu definition
# ----------------------------------------------------------------------

MENU = """
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
"""

VALID_CHOICES = set(range(1, 12))


def display_menu() -> None:
    print(MENU)


def get_choice() -> int:
    """
    Read a menu choice from stdin.
    Returns -1 for any non-integer or out-of-range input so the
    main loop can print a friendly message without crashing.
    """
    raw = input("  Enter your choice (1-11): ").strip()
    if raw.isdigit() and int(raw) in VALID_CHOICES:
        return int(raw)
    return -1


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

def main() -> None:
    clear_screen()
    print("\n  Loading Library Management System …")
    library = Library()   # Loads all data from CSVs on startup
    print("  Data loaded successfully.\n")

    while True:
        display_menu()
        choice = get_choice()

        if choice == -1:
            print("\n  [X]  Invalid choice. Please enter a number between 1 and 11.")
            press_enter_to_continue()
            clear_screen()
            continue

        clear_screen()

        if choice == 1:
            library.add_book()
        elif choice == 2:
            library.view_books()
        elif choice == 3:
            library.search_book()
        elif choice == 4:
            library.register_student()
        elif choice == 5:
            library.view_students()
        elif choice == 6:
            library.issue_book()
        elif choice == 7:
            library.return_book()
        elif choice == 8:
            library.delete_book()
        elif choice == 9:
            library.delete_student()
        elif choice == 10:
            library.generate_reports()
        elif choice == 11:
            print("\n  Goodbye! All data has been saved.\n")
            break

        press_enter_to_continue()
        clear_screen()


if __name__ == "__main__":
    main()
