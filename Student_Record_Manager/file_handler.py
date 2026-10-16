import os
import csv

FIELDNAMES = ['ID', 'Name', 'Age', 'Gender', 'Course', 'Semester', 'Phone', 'Email', 'Marks', 'Grade']

def create_csv_if_not_exists(filepath: str):
    """
    Creates the CSV file with headers if it does not already exist.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    if not os.path.exists(filepath):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()
        except Exception as e:
            print(f"Error creating storage file: {e}")

def load_students(filepath: str) -> list:
    """
    Loads students from the CSV file. Handles missing/corrupt files gracefully.
    """
    create_csv_if_not_exists(filepath)
    students = []
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                print("Warning: CSV file is empty or missing headers. Re-initializing.")
                return []
                
            # Verify if expected headers are present
            missing_headers = [field for field in FIELDNAMES if field not in reader.fieldnames]
            if missing_headers:
                print(f"Warning: Corrupt CSV header. Missing columns: {missing_headers}. Re-initializing database.")
                return []
                
            for line_no, row in enumerate(reader, start=2):
                # Ensure all fields are present and not None
                if any(row.get(field) is None for field in FIELDNAMES):
                    print(f"Warning: Skipping corrupted record on line {line_no} due to missing fields.")
                    continue
                students.append(row)
    except (csv.Error, UnicodeDecodeError, IOError) as e:
        print(f"Error reading CSV file (possibly corrupted): {e}. Starting with empty database.")
        return []
    return students

def save_students(filepath: str, students: list) -> bool:
    """
    Saves the list of student records back to the CSV.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for student in students:
                # Ensure we only write fields defined in FIELDNAMES
                clean_row = {field: student.get(field, '') for field in FIELDNAMES}
                writer.writerow(clean_row)
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False
