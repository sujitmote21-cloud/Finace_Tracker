import os
import csv

TRANS_HEADERS = ['ID', 'Date', 'Type', 'Category', 'Amount', 'Payment Mode', 'Description']
BUDGET_HEADERS = ['Month', 'Category', 'Limit']

def create_file_if_not_exists(filepath: str, headers: list):
    """
    Ensures containing directory and CSV files exist with headers.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    if not os.path.exists(filepath):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        except Exception as e:
            print(f"Error creating file {filepath}: {e}")

def load_transactions(filepath: str) -> list:
    """
    Loads transactions.csv safely. Handles missing or corrupted files.
    """
    create_file_if_not_exists(filepath, TRANS_HEADERS)
    transactions = []
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                print("Warning: transactions.csv is empty or missing headers. Re-initializing.")
                return []
                
            missing = [h for h in TRANS_HEADERS if h not in reader.fieldnames]
            if missing:
                print(f"Warning: Corrupted transactions header. Missing fields: {missing}. Re-initializing database.")
                return []
                
            for line, row in enumerate(reader, start=2):
                if any(row.get(h) is None for h in TRANS_HEADERS):
                    print(f"Warning: Skipping corrupted transaction on line {line} due to missing fields.")
                    continue
                transactions.append(row)
    except (csv.Error, UnicodeDecodeError, IOError) as e:
        print(f"Error loading transactions (possibly corrupted): {e}. Starting with empty database.")
        return []
    return transactions

def save_transactions(filepath: str, transactions: list) -> bool:
    """
    Persists transactions to CSV.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=TRANS_HEADERS)
            writer.writeheader()
            for t in transactions:
                # Clean row to write only defined headers
                clean_row = {h: t.get(h, '') for h in TRANS_HEADERS}
                writer.writerow(clean_row)
        return True
    except Exception as e:
        print(f"Error saving transactions: {e}")
        return False

def load_budget(filepath: str) -> list:
    """
    Loads budget.csv safely. Handles missing or corrupted files.
    """
    create_file_if_not_exists(filepath, BUDGET_HEADERS)
    budgets = []
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                print("Warning: budget.csv is empty or missing headers. Re-initializing.")
                return []
                
            missing = [h for h in BUDGET_HEADERS if h not in reader.fieldnames]
            if missing:
                print(f"Warning: Corrupted budget header. Missing fields: {missing}. Re-initializing budget database.")
                return []
                
            for line, row in enumerate(reader, start=2):
                if any(row.get(h) is None for h in BUDGET_HEADERS):
                    print(f"Warning: Skipping corrupted budget entry on line {line}.")
                    continue
                budgets.append(row)
    except (csv.Error, UnicodeDecodeError, IOError) as e:
        print(f"Error loading budgets (possibly corrupted): {e}. Starting with empty budgets.")
        return []
    return budgets

def save_budget(filepath: str, budgets: list) -> bool:
    """
    Persists budgets to CSV.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=BUDGET_HEADERS)
            writer.writeheader()
            for b in budgets:
                clean_row = {h: b.get(h, '') for h in BUDGET_HEADERS}
                writer.writerow(clean_row)
        return True
    except Exception as e:
        print(f"Error saving budgets: {e}")
        return False
