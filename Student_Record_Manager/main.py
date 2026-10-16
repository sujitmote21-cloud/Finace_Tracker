import os
import sys
import utils
import file_handler
import student_manager
import gui

# Set up paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'students.csv')

def run_cli(students):
    # Wait briefly or continue
    input("\nPress Enter to proceed to the main menu...")
    
    while True:
        utils.clear_screen()
        print("============================")
        print(" STUDENT RECORD MANAGEMENT  ")
        print("============================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Statistics")
        print("7. Exit")
        print("============================")
        
        choice = input("Enter Choice: ").strip()
        
        if choice == '1':
            modified = student_manager.add_student(students)
            if modified:
                file_handler.save_students(DB_PATH, students)
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            student_manager.view_students(students)
            
        elif choice == '3':
            student_manager.search_student(students)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            modified = student_manager.update_student(students)
            if modified:
                file_handler.save_students(DB_PATH, students)
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            modified = student_manager.delete_student(students)
            if modified:
                file_handler.save_students(DB_PATH, students)
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            student_manager.show_statistics(students)
            input("\nPress Enter to continue...")
            
        elif choice == '7':
            print("\nExiting Student Record Management System. Goodbye!")
            sys.exit(0)
            
        else:
            print("\nError: Invalid menu choice. Please select a number between 1 and 7.")
            input("\nPress Enter to try again...")

def main():
    # Load database on startup
    print("Loading student database...")
    students = file_handler.load_students(DB_PATH)
    print(f"Loaded {len(students)} records.")
    
    if '--cli' in sys.argv:
        run_cli(students)
    else:
        # Launch beautiful GUI
        print("Launching Graphical User Interface...")
        app = gui.StudentRecordApp(students, DB_PATH)
        app.mainloop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting gracefully...")
        sys.exit(0)
