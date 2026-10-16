import os
import csv
import utils

FIELDNAMES = ['ID', 'Name', 'Age', 'Gender', 'Course', 'Semester', 'Phone', 'Email', 'Marks', 'Grade']

def calculate_grade(marks: float) -> str:
    """
    Calculates student Grade based on Marks:
       90–100 -> A+
       80–89 -> A
       70–79 -> B
       60–69 -> C
       50–59 -> D
       Below 50 -> F
    """
    # Assumption: Grade boundaries are inclusive of lower bound
    if marks >= 90:
        return 'A+'
    elif marks >= 80:
        return 'A'
    elif marks >= 70:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 50:
        return 'D'
    else:
        return 'F'

def prompt_validated_input(prompt_text, validator_func=None, error_msg="Invalid input."):
    """
    Helper to get clean, validated input from user. Returns (value, cancelled).
    """
    while True:
        val = input(prompt_text).strip()
        if val.lower() == 'q':
            return None, True
        if not val:
            print("Error: Field cannot be empty. (Type 'q' to cancel)")
            continue
        if validator_func:
            if validator_func(val):
                return val, False
            else:
                print(f"Error: {error_msg} (Type 'q' to cancel)")
        else:
            return val, False

def add_student(students: list) -> bool:
    """
    Collects inputs for a new student, validates, calculates grade, and appends to in-memory list.
    Returns True if added successfully, False otherwise.
    """
    print("\n--- Add Student Record (Type 'q' at any prompt to cancel) ---")
    
    # ID check
    def id_validator(s_id):
        # Reject duplicate Student IDs
        return not any(s['ID'] == s_id for s in students)

    student_id, cancelled = prompt_validated_input(
        "Enter Student ID: ", 
        id_validator, 
        "Duplicate Student ID. Each student must have a unique ID."
    )
    if cancelled:
        print("Add Student operation cancelled.")
        return False
        
    name, cancelled = prompt_validated_input("Enter Student Name: ")
    if cancelled:
        print("Add Student operation cancelled.")
        return False

    age_str, cancelled = prompt_validated_input(
        "Enter Age (16-35): ", 
        utils.validate_age, 
        "Age must be an integer between 16 and 35."
    )
    if cancelled:
        print("Add Student operation cancelled.")
        return False
    age = int(age_str)

    gender, cancelled = prompt_validated_input("Enter Gender: ")
    if cancelled:
        print("Add Student operation cancelled.")
        return False

    course, cancelled = prompt_validated_input("Enter Course: ")
    if cancelled:
        print("Add Student operation cancelled.")
        return False

    semester, cancelled = prompt_validated_input("Enter Semester: ")
    if cancelled:
        print("Add Student operation cancelled.")
        return False

    phone, cancelled = prompt_validated_input(
        "Enter Phone (10 digits): ", 
        utils.validate_phone, 
        "Phone number must be exactly 10 digits."
    )
    if cancelled:
        print("Add Student operation cancelled.")
        return False

    email, cancelled = prompt_validated_input(
        "Enter Email (must contain '@' and '.com'): ", 
        utils.validate_email, 
        "Email must contain '@' and '.com'."
    )
    if cancelled:
        print("Add Student operation cancelled.")
        return False

    marks_str, cancelled = prompt_validated_input(
        "Enter Marks (0-100): ", 
        utils.validate_marks, 
        "Marks must be a number between 0 and 100."
    )
    if cancelled:
        print("Add Student operation cancelled.")
        return False
    marks = float(marks_str)
    
    # Auto-derive Grade
    grade = calculate_grade(marks)
    
    new_student = {
        'ID': student_id,
        'Name': name,
        'Age': str(age),
        'Gender': gender,
        'Course': course,
        'Semester': semester,
        'Phone': phone,
        'Email': email,
        'Marks': str(marks),
        'Grade': grade
    }
    
    students.append(new_student)
    print(f"Success: Student {name} (ID: {student_id}) has been added.")
    return True

def format_student_for_table(s):
    return [
        s['ID'],
        s['Name'],
        s['Age'],
        s['Gender'],
        s['Course'],
        s['Semester'],
        s['Phone'],
        s['Email'],
        s['Marks'],
        s['Grade']
    ]

def view_students(students: list):
    """
    Displays list of student records.
    Provides options to sort, filter, or display top 5.
    """
    if not students:
        print("\nNo student records found in the database.")
        return

    while True:
        print("\n--- View Options ---")
        print("1. View All (Unsorted)")
        print("2. Sort by Marks (High to Low)")
        print("3. Sort by Name (A-Z)")
        print("4. Sort by ID (A-Z)")
        print("5. Filter by Course")
        print("6. Filter by Semester")
        print("7. View Top 5 Students")
        print("8. Return to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            display_list(students, "All Student Records")
        elif choice == '2':
            sorted_students = sorted(students, key=lambda x: float(x['Marks']), reverse=True)
            display_list(sorted_students, "Students Sorted by Marks (Highest First)")
        elif choice == '3':
            sorted_students = sorted(students, key=lambda x: x['Name'].lower())
            display_list(sorted_students, "Students Sorted by Name (A-Z)")
        elif choice == '4':
            sorted_students = sorted(students, key=lambda x: x['ID'].lower())
            display_list(sorted_students, "Students Sorted by ID (A-Z)")
        elif choice == '5':
            course_q = input("Enter Course to filter by: ").strip().lower()
            filtered = [s for s in students if course_q in s['Course'].lower()]
            display_list(filtered, f"Students in Course matching '{course_q}'")
        elif choice == '6':
            sem_q = input("Enter Semester to filter by: ").strip().lower()
            filtered = [s for s in students if sem_q in s['Semester'].lower()]
            display_list(filtered, f"Students in Semester matching '{sem_q}'")
        elif choice == '7':
            # Sort descending and take top 5
            sorted_students = sorted(students, key=lambda x: float(x['Marks']), reverse=True)
            display_list(sorted_students[:5], "Top 5 Students (by Marks)")
        elif choice == '8':
            break
        else:
            print("Invalid option. Please choose between 1 and 8.")

def display_list(student_list: list, title: str):
    """
    Prints a list of students in a table format with a title.
    """
    print(f"\n=== {title} ===")
    if not student_list:
        print("No student records to display.")
        return
        
    headers = ['ID', 'Name', 'Age', 'Gender', 'Course', 'Semester', 'Phone', 'Email', 'Marks', 'Grade']
    rows = [format_student_for_table(s) for s in student_list]
    utils.display_table(headers, rows)

def search_student(students: list):
    """
    Performs lookup by ID, Name, or Course.
    """
    if not students:
        print("\nNo student records in the database to search.")
        return

    print("\n--- Search Student ---")
    print("1. Search by ID")
    print("2. Search by Name")
    print("3. Search by Course")
    
    choice = input("Enter Choice: ").strip()
    results = []
    
    if choice == '1':
        student_id = input("Enter Student ID: ").strip().lower()
        results = [s for s in students if s['ID'].lower() == student_id]
    elif choice == '2':
        name_q = input("Enter Student Name: ").strip().lower()
        results = [s for s in students if name_q in s['Name'].lower()]
    elif choice == '3':
        course_q = input("Enter Course Name: ").strip().lower()
        results = [s for s in students if course_q in s['Course'].lower()]
    else:
        print("Invalid search choice.")
        return

    display_list(results, f"Search Results ({len(results)} found)")

def update_student(students: list) -> bool:
    """
    Finds student by ID and allows updating chosen fields.
    Returns True if database was modified, False otherwise.
    """
    if not students:
        print("\nNo student records in database to update.")
        return False

    student_id = input("\nEnter Student ID to update: ").strip()
    student = None
    for s in students:
        if s['ID'] == student_id:
            student = s
            break
            
    if not student:
        print(f"Error: Student with ID {student_id} not found.")
        return False
        
    print("\n--- Existing Record ---")
    display_list([student], "Current Student Info")
    print("Enter new details below. Leave blank and press Enter to keep current values.")
    print("Type 'q' at any prompt to abort updating this field.")
    
    modified = False

    # Name Update
    name = input(f"New Name [{student['Name']}]: ").strip()
    if name.lower() == 'q':
        print("Update cancelled.")
        return False
    if name:
        student['Name'] = name
        modified = True

    # Phone Update
    while True:
        phone = input(f"New Phone [{student['Phone']}]: ").strip()
        if phone.lower() == 'q':
            print("Update cancelled.")
            return False
        if not phone:
            break
        if utils.validate_phone(phone):
            student['Phone'] = phone
            modified = True
            break
        else:
            print("Error: Phone number must be exactly 10 digits.")

    # Email Update
    while True:
        email = input(f"New Email [{student['Email']}]: ").strip()
        if email.lower() == 'q':
            print("Update cancelled.")
            return False
        if not email:
            break
        if utils.validate_email(email):
            student['Email'] = email
            modified = True
            break
        else:
            print("Error: Email must contain '@' and '.com'.")

    # Semester Update
    semester = input(f"New Semester [{student['Semester']}]: ").strip()
    if semester.lower() == 'q':
        print("Update cancelled.")
        return False
    if semester:
        student['Semester'] = semester
        modified = True

    # Marks Update (triggers grade recalculation)
    while True:
        marks_str = input(f"New Marks [{student['Marks']}]: ").strip()
        if marks_str.lower() == 'q':
            print("Update cancelled.")
            return False
        if not marks_str:
            break
        if utils.validate_marks(marks_str):
            new_marks = float(marks_str)
            student['Marks'] = str(new_marks)
            # Auto-calculate and update grade
            student['Grade'] = calculate_grade(new_marks)
            modified = True
            break
        else:
            print("Error: Marks must be a number between 0 and 100.")

    if modified:
        print(f"Success: Student record for ID {student_id} updated successfully.")
        return True
    else:
        print("No changes were made to the student record.")
        return False

def delete_student(students: list) -> bool:
    """
    Finds a student by ID, asks for confirmation, and deletes if confirmed.
    Returns True if record was deleted, False otherwise.
    """
    if not students:
        print("\nNo student records in database to delete.")
        return False

    student_id = input("\nEnter Student ID to delete: ").strip()
    student = None
    for s in students:
        if s['ID'] == student_id:
            student = s
            break
            
    if not student:
        print(f"Error: Student with ID {student_id} not found.")
        return False
        
    print("\n--- Record to Delete ---")
    display_list([student], "Record Details")
    
    confirm = input(f"Are you sure you want to permanently delete this student record? (y/n): ").strip().lower()
    if confirm == 'y':
        students.remove(student)
        print(f"Success: Student with ID {student_id} has been deleted.")
        return True
    else:
        print("Delete operation cancelled.")
        return False

def show_statistics(students: list):
    """
    Computes and displays statistics:
    - Total Students
    - Average Marks
    - Highest Marks
    - Lowest Marks
    - Pass Percentage (Marks >= 50)
    - Topper(s) (name & marks)
    Optionally exports stats to CSV.
    """
    if not students:
        print("\nNo student records to generate statistics.")
        return

    # Gather numeric values
    total_students = len(students)
    marks_list = [float(s['Marks']) for s in students]
    avg_marks = sum(marks_list) / total_students
    highest_marks = max(marks_list)
    lowest_marks = min(marks_list)
    
    pass_count = sum(1 for m in marks_list if m >= 50)
    pass_percentage = (pass_count / total_students) * 100
    
    # Identify topper(s)
    toppers = [s for s in students if float(s['Marks']) == highest_marks]
    topper_names = ", ".join(f"{t['Name']} (ID: {t['ID']})" for t in toppers)
    
    print("\n==================================")
    print("       STUDENT STATISTICS         ")
    print("==================================")
    print(f"Total Students   : {total_students}")
    print(f"Average Marks    : {avg_marks:.2f}")
    print(f"Highest Marks    : {highest_marks:.2f}")
    print(f"Lowest Marks     : {lowest_marks:.2f}")
    print(f"Pass Percentage  : {pass_percentage:.2f}%")
    print(f"Topper(s)        : {topper_names} [{highest_marks:.2f}]")
    print("==================================")
    
    # Optional Extra: Export stats to CSV
    export_choice = input("Would you like to export these statistics to a CSV file? (y/n): ").strip().lower()
    if export_choice == 'y':
        export_statistics(total_students, avg_marks, highest_marks, lowest_marks, pass_percentage, topper_names)

def export_statistics(total, avg, high, low, pass_pct, topper_names):
    """
    Exports computed statistics to a separate stats CSV file.
    """
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'statistics.csv')
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Total Students', total])
            writer.writerow(['Average Marks', f"{avg:.2f}"])
            writer.writerow(['Highest Marks', f"{high:.2f}"])
            writer.writerow(['Lowest Marks', f"{low:.2f}"])
            writer.writerow(['Pass Percentage', f"{pass_pct:.2f}%"])
            writer.writerow(['Topper(s)', topper_names])
        print(f"Success: Statistics exported to {filepath}")
    except Exception as e:
        print(f"Error exporting statistics: {e}")
