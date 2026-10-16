import os

def validate_email(email: str) -> bool:
    """
    Validates email. Must contain '@' and '.com'.
    """
    # Assumption: Email should be of valid structure (e.g. user@domain.com)
    if not email or not isinstance(email, str):
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
        
    user, domain = parts
    return len(user) > 0 and len(domain) > 0 and '.com' in domain and domain.index('.com') > 0

def validate_phone(phone: str) -> bool:
    """
    Validates phone number. Must be exactly 10 digits.
    """
    if not phone or not isinstance(phone, str):
        return False
    return phone.isdigit() and len(phone) == 10

def validate_marks(marks_val) -> bool:
    """
    Validates marks. Must be between 0 and 100.
    """
    try:
        val = float(marks_val)
        return 0 <= val <= 100
    except (ValueError, TypeError):
        return False

def validate_age(age_val) -> bool:
    """
    Validates age. Must be between 16 and 35.
    """
    try:
        val = int(age_val)
        return 16 <= val <= 35
    except (ValueError, TypeError):
        return False

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def display_table(headers, rows):
    """
    Displays data in a neat terminal table.
    """
    if not headers:
        return
        
    # Convert all cell values to string
    str_rows = [[str(cell) for cell in row] for row in rows]
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for idx, cell in enumerate(row):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(cell))
                
    # Build header/row separator line
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    # Print the table
    print(separator)
    header_row = "| " + " | ".join(h.ljust(col_widths[idx]) for idx, h in enumerate(headers)) + " |"
    print(header_row)
    print(separator)
    
    for row in str_rows:
        # Pad row if it has fewer elements than headers
        if len(row) < len(headers):
            row = row + [""] * (len(headers) - len(row))
        row = row[:len(headers)]
        
        data_row = "| " + " | ".join(cell.ljust(col_widths[idx]) for idx, cell in enumerate(row)) + " |"
        print(data_row)
    print(separator)
