import os
from datetime import datetime

EXPENSE_CATEGORIES = ['Food', 'Rent', 'Travel', 'Shopping', 'Education', 'Bills', 'Entertainment', 'Medical', 'Others']
PAYMENT_MODES = ['Cash', 'UPI', 'Debit Card', 'Credit Card', 'Bank Transfer']

def validate_amount(amount_val) -> bool:
    """
    Validates that the amount is a positive number.
    """
    try:
        val = float(amount_val)
        return val > 0
    except (ValueError, TypeError):
        return False

def validate_date(date_str: str) -> bool:
    """
    Validates that date is in DD-MM-YYYY format.
    """
    if not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(date_str.strip(), "%d-%m-%Y")
        return True
    except ValueError:
        return False

def validate_category(category: str, trans_type: str) -> bool:
    """
    Validates Category. Expense category must be from fixed list.
    Income source (stored as category) must be non-empty.
    """
    if not category or not isinstance(category, str):
        return False
        
    category_stripped = category.strip()
    if not category_stripped:
        return False
        
    if trans_type.lower() == 'expense':
        # Case insensitive compare to list
        return any(c.lower() == category_stripped.lower() for c in EXPENSE_CATEGORIES)
    elif trans_type.lower() == 'income':
        return len(category_stripped) > 0
    return False

def get_matched_category(category: str, trans_type: str) -> str:
    """
    Helper to return case-corrected expense category name from list.
    """
    if trans_type.lower() == 'income':
        return category.strip()
        
    category_stripped = category.strip().lower()
    for c in EXPENSE_CATEGORIES:
        if c.lower() == category_stripped:
            return c
    return category.strip()

def validate_payment_mode(mode: str) -> bool:
    """
    Validates that Payment Mode is from fixed list.
    """
    if not mode or not isinstance(mode, str):
        return False
    mode_stripped = mode.strip().lower()
    return any(m.lower() == mode_stripped for m in PAYMENT_MODES)

def get_matched_payment_mode(mode: str) -> str:
    """
    Helper to return case-corrected payment mode name from list.
    """
    mode_stripped = mode.strip().lower()
    for m in PAYMENT_MODES:
        if m.lower() == mode_stripped:
            return m
    return mode.strip()

def clear_screen():
    """
    Clears the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def display_table(headers, rows):
    """
    Displays grid in a custom dynamic column widths layout.
    """
    if not headers:
        return
        
    str_rows = [[str(cell) for cell in row] for row in rows]
    
    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for idx, cell in enumerate(row):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(cell))
                
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    print(separator)
    header_row = "| " + " | ".join(h.ljust(col_widths[idx]) for idx, h in enumerate(headers)) + " |"
    print(header_row)
    print(separator)
    
    for row in str_rows:
        if len(row) < len(headers):
            row = row + [""] * (len(headers) - len(row))
        row = row[:len(headers)]
        
        data_row = "| " + " | ".join(cell.ljust(col_widths[idx]) for idx, cell in enumerate(row)) + " |"
        print(data_row)
    print(separator)
