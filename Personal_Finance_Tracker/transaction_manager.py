import utils

def generate_transaction_id(transactions: list) -> str:
    """
    Generates a unique transaction ID starting with T001.
    """
    if not transactions:
        return "T001"
        
    max_num = 0
    for t in transactions:
        tid = t.get('ID', '')
        if tid.startswith('T') and tid[1:].isdigit():
            try:
                num = int(tid[1:])
                if num > max_num:
                    max_num = num
            except ValueError:
                continue
    return f"T{max_num + 1:03d}"

def prompt_input_field(prompt_text, validator_func=None, extra_args=None, error_msg="Invalid input."):
    """
    Helper to prompt for input, validate, and allow cancelling with 'q'.
    """
    while True:
        val = input(prompt_text).strip()
        if val.lower() == 'q':
            return None, True
        if validator_func:
            # Check if validator takes type arg
            if extra_args is not None:
                is_valid = validator_func(val, *extra_args)
            else:
                is_valid = validator_func(val)
                
            if is_valid:
                return val, False
            else:
                print(f"Error: {error_msg} (Type 'q' to cancel)")
        else:
            if val:
                return val, False
            else:
                print("Error: Field cannot be empty. (Type 'q' to cancel)")

def add_income(transactions: list) -> bool:
    """
    Collects inputs for a new income transaction and appends to in-memory list.
    """
    print("\n--- Add Income (Type 'q' at any prompt to cancel) ---")
    
    date, cancelled = prompt_input_field(
        "Enter Date (DD-MM-YYYY): ", 
        utils.validate_date, 
        error_msg="Date must be a valid calendar date in DD-MM-YYYY format."
    )
    if cancelled: return False
    
    source, cancelled = prompt_input_field("Enter Income Source: ")
    if cancelled: return False
    
    amount_str, cancelled = prompt_input_field(
        "Enter Amount (Positive number): ", 
        utils.validate_amount, 
        error_msg="Amount must be a positive number."
    )
    if cancelled: return False
    amount = float(amount_str)
    
    payment_mode, cancelled = prompt_input_field(
        f"Enter Payment Mode {utils.PAYMENT_MODES}: ", 
        utils.validate_payment_mode, 
        error_msg=f"Payment Mode must be one of {utils.PAYMENT_MODES}."
    )
    if cancelled: return False
    payment_mode = utils.get_matched_payment_mode(payment_mode)
    
    description, cancelled = prompt_input_field("Enter Description: ")
    if cancelled: return False
    
    tid = generate_transaction_id(transactions)
    
    new_trans = {
        'ID': tid,
        'Date': date,
        'Type': 'Income',
        'Category': source,
        'Amount': str(amount),
        'Payment Mode': payment_mode,
        'Description': description
    }
    transactions.append(new_trans)
    print(f"Success: Income transaction {tid} successfully recorded.")
    return True

def add_expense(transactions: list) -> bool:
    """
    Collects inputs for a new expense transaction and appends to in-memory list.
    """
    print("\n--- Add Expense (Type 'q' at any prompt to cancel) ---")
    
    date, cancelled = prompt_input_field(
        "Enter Date (DD-MM-YYYY): ", 
        utils.validate_date, 
        error_msg="Date must be a valid calendar date in DD-MM-YYYY format."
    )
    if cancelled: return False
    
    category, cancelled = prompt_input_field(
        f"Enter Category {utils.EXPENSE_CATEGORIES}: ", 
        utils.validate_category, 
        extra_args=('expense',),
        error_msg=f"Category must be from the expense category list: {utils.EXPENSE_CATEGORIES}."
    )
    if cancelled: return False
    category = utils.get_matched_category(category, 'expense')
    
    amount_str, cancelled = prompt_input_field(
        "Enter Amount (Positive number): ", 
        utils.validate_amount, 
        error_msg="Amount must be a positive number."
    )
    if cancelled: return False
    amount = float(amount_str)
    
    payment_mode, cancelled = prompt_input_field(
        f"Enter Payment Mode {utils.PAYMENT_MODES}: ", 
        utils.validate_payment_mode, 
        error_msg=f"Payment Mode must be one of {utils.PAYMENT_MODES}."
    )
    if cancelled: return False
    payment_mode = utils.get_matched_payment_mode(payment_mode)
    
    description, cancelled = prompt_input_field("Enter Description: ")
    if cancelled: return False
    
    tid = generate_transaction_id(transactions)
    
    new_trans = {
        'ID': tid,
        'Date': date,
        'Type': 'Expense',
        'Category': category,
        'Amount': str(amount),
        'Payment Mode': payment_mode,
        'Description': description
    }
    transactions.append(new_trans)
    print(f"Success: Expense transaction {tid} successfully recorded.")
    return True

def format_transaction_row(t):
    return [
        t['ID'],
        t['Date'],
        t['Type'],
        t['Category'],
        t['Amount'],
        t['Payment Mode'],
        t['Description']
    ]

def view_transactions(transactions: list):
    """
    Displays transactions in a tabular format.
    """
    print("\n==================== TRANSACTION HISTORY ====================")
    if not transactions:
        print("No transactions found.")
        print("=============================================================")
        return
        
    headers = ['ID', 'Date', 'Type', 'Category', 'Amount', 'Payment Mode', 'Description']
    # Show most recent first.
    # Assumption: Transactions list can be reversed to show most recent.
    # Sorting by Date is also an option, but reversing is standard if they are appended in chronological order.
    # Let's reverse the view list
    reversed_list = list(reversed(transactions))
    
    # Optional Extra: Display last 10 transactions or all
    print(f"Displaying all {len(transactions)} transaction(s) (newest first):")
    rows = [format_transaction_row(t) for t in reversed_list]
    utils.display_table(headers, rows)

def search_transaction(transactions: list):
    """
    Searches for transaction by ID, Date, Category, or Type.
    """
    if not transactions:
        print("\nNo transactions found in database to search.")
        return

    print("\n--- Search Transaction ---")
    print("1. Search by ID")
    print("2. Search by Date (DD-MM-YYYY)")
    print("3. Search by Category")
    print("4. Search by Type (Income/Expense)")
    
    choice = input("Enter choice (1-4): ").strip()
    results = []
    
    if choice == '1':
        tid = input("Enter Transaction ID (e.g. T001): ").strip().lower()
        results = [t for t in transactions if t['ID'].lower() == tid]
    elif choice == '2':
        date_q = input("Enter Date (DD-MM-YYYY): ").strip()
        results = [t for t in transactions if t['Date'] == date_q]
    elif choice == '3':
        cat_q = input("Enter Category Name: ").strip().lower()
        results = [t for t in transactions if cat_q in t['Category'].lower()]
    elif choice == '4':
        type_q = input("Enter Type (Income/Expense): ").strip().lower()
        results = [t for t in transactions if t['Type'].lower() == type_q]
    else:
        print("Invalid search option.")
        return

    print(f"\nSearch Results ({len(results)} matches found):")
    if results:
        headers = ['ID', 'Date', 'Type', 'Category', 'Amount', 'Payment Mode', 'Description']
        rows = [format_transaction_row(t) for t in results]
        utils.display_table(headers, rows)
    else:
        print("No matching transactions found.")

def update_transaction(transactions: list) -> bool:
    """
    Updates transaction details by matching ID.
    """
    if not transactions:
        print("\nNo transactions to update.")
        return False
        
    tid = input("\nEnter Transaction ID to update: ").strip()
    trans = None
    for t in transactions:
        if t['ID'] == tid:
            trans = t
            break
            
    if not trans:
        print(f"Error: Transaction with ID {tid} not found.")
        return False
        
    print("\n--- Existing Transaction Details ---")
    headers = ['ID', 'Date', 'Type', 'Category', 'Amount', 'Payment Mode', 'Description']
    utils.display_table(headers, [format_transaction_row(trans)])
    
    print("Enter new values. Press Enter to leave a field unchanged.")
    print("Type 'q' at any prompt to abort editing this field.")
    
    modified = False
    
    # Update Date
    while True:
        date = input(f"New Date [{trans['Date']}]: ").strip()
        if date.lower() == 'q': return False
        if not date: break
        if utils.validate_date(date):
            trans['Date'] = date
            modified = True
            break
        else:
            print("Error: Date must be in DD-MM-YYYY format.")
            
    # Update Category / Source
    while True:
        category = input(f"New Category/Source [{trans['Category']}]: ").strip()
        if category.lower() == 'q': return False
        if not category: break
        
        # Validations depend on the type of transaction
        if utils.validate_category(category, trans['Type']):
            trans['Category'] = utils.get_matched_category(category, trans['Type'])
            modified = True
            break
        else:
            if trans['Type'] == 'Expense':
                print(f"Error: Expense Category must be one of: {utils.EXPENSE_CATEGORIES}")
            else:
                print("Error: Income source cannot be empty.")

    # Update Amount
    while True:
        amount_str = input(f"New Amount [{trans['Amount']}]: ").strip()
        if amount_str.lower() == 'q': return False
        if not amount_str: break
        if utils.validate_amount(amount_str):
            trans['Amount'] = str(float(amount_str))
            modified = True
            break
        else:
            print("Error: Amount must be a positive number.")

    # Update Description
    desc = input(f"New Description [{trans['Description']}]: ").strip()
    if desc.lower() == 'q': return False
    if desc:
        trans['Description'] = desc
        modified = True
        
    if modified:
        print(f"Success: Transaction {tid} successfully updated.")
        return True
    else:
        print("No modifications were performed.")
        return False

def delete_transaction(transactions: list) -> bool:
    """
    Deletes transaction details by matching ID.
    """
    if not transactions:
        print("\nNo transactions in database to delete.")
        return False
        
    tid = input("\nEnter Transaction ID to delete: ").strip()
    trans = None
    for t in transactions:
        if t['ID'] == tid:
            trans = t
            break
            
    if not trans:
        print(f"Error: Transaction with ID {tid} not found.")
        return False
        
    print("\n--- Transaction Details ---")
    headers = ['ID', 'Date', 'Type', 'Category', 'Amount', 'Payment Mode', 'Description']
    utils.display_table(headers, [format_transaction_row(trans)])
    
    confirm = input("Are you sure you want to permanently delete this transaction? (y/n): ").strip().lower()
    if confirm == 'y':
        transactions.remove(trans)
        print(f"Success: Transaction {tid} has been deleted.")
        return True
    else:
        print("Delete operation cancelled.")
        return False
