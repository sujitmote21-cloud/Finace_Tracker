import os
import pandas as pd
import utils

def get_dataframe(transactions: list) -> pd.DataFrame:
    """
    Converts list of transactions to pandas DataFrame with proper data types.
    """
    if not transactions:
        return pd.DataFrame(columns=['ID', 'Date', 'Type', 'Category', 'Amount', 'Payment Mode', 'Description'])
        
    df = pd.DataFrame(transactions)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
    return df

def generate_monthly_report(transactions: list, month_year: str, budgets: list, reports_dir: str):
    """
    Generates and displays comprehensive financial reports for the specified MM-YYYY month.
    Also exports the summary to reports/monthly_report.csv.
    """
    # 1. Convert to DataFrame and filter
    df = get_dataframe(transactions)
    if df.empty:
        print("\nNo transaction data available to generate reports.")
        return
        
    try:
        month, year = map(int, month_year.split('-'))
    except ValueError:
        print("Error: Month-Year format must be MM-YYYY.")
        return
        
    month_df = df[(df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    
    if month_df.empty:
        print(f"\nNo transaction records found for the month: {month_year}")
        return
        
    # Group into income and expenses
    income_df = month_df[month_df['Type'] == 'Income']
    expense_df = month_df[month_df['Type'] == 'Expense']
    
    total_income = income_df['Amount'].sum()
    total_expense = expense_df['Amount'].sum()
    total_savings = total_income - total_expense
    savings_pct = (total_savings / total_income * 100) if total_income > 0 else 0.0
    
    # Category-wise Expense breakdown
    cat_breakdown = []
    if not expense_df.empty:
        cat_grp = expense_df.groupby('Category')['Amount'].sum().reset_index()
        # Sort descending by Amount
        cat_grp = cat_grp.sort_values(by='Amount', ascending=False)
        cat_breakdown = cat_grp.values.tolist()
        
    # High / Low Expense
    highest_exp = "N/A"
    lowest_exp = "N/A"
    if not expense_df.empty:
        idx_max = expense_df['Amount'].idxmax()
        idx_min = expense_df['Amount'].idxmin()
        h_row = expense_df.loc[idx_max]
        l_row = expense_df.loc[idx_min]
        highest_exp = f"₹{h_row['Amount']:.2f} on {h_row['Date'].strftime('%d-%m-%Y')} (Category: {h_row['Category']}, ID: {h_row['ID']})"
        lowest_exp = f"₹{l_row['Amount']:.2f} on {l_row['Date'].strftime('%d-%m-%Y')} (Category: {l_row['Category']}, ID: {l_row['ID']})"
        
    # Average Daily Spending
    avg_daily_spend = 0.0
    if not expense_df.empty:
        # Number of unique days that have expenses
        distinct_days = expense_df['Date'].dt.date.nunique()
        avg_daily_spend = total_expense / distinct_days if distinct_days > 0 else 0.0
        
    # Counts
    income_count = len(income_df)
    expense_count = len(expense_df)
    total_count = len(month_df)

    # Print summary layout
    print("\n==============================================")
    print(f"       FINANCIAL SUMMARY FOR {month_year}       ")
    print("==============================================")
    print(f"Total Income        : ₹{total_income:.2f}")
    print(f"Total Expense       : ₹{total_expense:.2f}")
    print(f"Net Savings         : ₹{total_savings:.2f}")
    print(f"Savings Percentage  : {savings_pct:.2f}%")
    print("----------------------------------------------")
    print(f"Transaction Counts  : {total_count} (Income: {income_count}, Expense: {expense_count})")
    print(f"Average Daily Spend : ₹{avg_daily_spend:.2f} / day")
    print(f"Highest Expense     : {highest_exp}")
    print(f"Lowest Expense      : {lowest_exp}")
    print("==============================================")

    # Print Category Breakdown Table
    if cat_breakdown:
        print("\nCategory-wise Expense Breakdown:")
        utils.display_table(["Category", "Amount Spent (₹)"], [[cat, f"₹{amt:.2f}"] for cat, amt in cat_breakdown])
    else:
        print("\nNo expense records for this month to display breakdown.")
        
    # Export report to CSV
    export_summary_report(month_year, total_income, total_expense, total_savings, savings_pct, avg_daily_spend, reports_dir)

def export_summary_report(month_year, income, expense, savings, savings_pct, avg_daily, reports_dir):
    """
    Exports summary metrics to reports/monthly_report.csv
    """
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir, exist_ok=True)
        
    filepath = os.path.join(reports_dir, 'monthly_report.csv')
    try:
        report_data = {
            'Month': [month_year],
            'Total Income': [f"{income:.2f}"],
            'Total Expense': [f"{expense:.2f}"],
            'Net Savings': [f"{savings:.2f}"],
            'Savings Percentage': [f"{savings_pct:.2f}%"],
            'Average Daily Spend': [f"{avg_daily:.2f}"]
        }
        report_df = pd.DataFrame(report_data)
        report_df.to_csv(filepath, index=False)
        print(f"Success: Summary report exported to {filepath}")
    except Exception as e:
        print(f"Error exporting monthly report: {e}")

def display_budget_status(transactions: list, budgets: list, month_year: str):
    """
    Compares category spending against budget targets inside budget.csv.
    """
    # 1. Group expenses for this month
    df = get_dataframe(transactions)
    if df.empty:
        print("\nNo transactions found to compute budget status.")
        return
        
    try:
        month, year = map(int, month_year.split('-'))
    except ValueError:
        print("Error: Month-Year format must be MM-YYYY.")
        return
        
    month_df = df[(df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    expense_df = month_df[month_df['Type'] == 'Expense']
    
    # Calculate actual spending per category
    actual_spent = {}
    if not expense_df.empty:
        actual_spent = expense_df.groupby('Category')['Amount'].sum().to_dict()
        
    # 2. Get budgets for this month
    if not budgets:
        print(f"\nNo budget limits have been configured in budget.csv.")
        # If we have actual spending, we show them as without budget limit
        if actual_spent:
            print("Category-wise Spending (No Budgets Set):")
            rows = [[cat, "N/A", f"₹{amt:.2f}", "No Budget Set", "N/A"] for cat, amt in actual_spent.items()]
            utils.display_table(["Category", "Budget Limit", "Actual Spend", "Status", "Difference"], rows)
        return
        
    # Read budgets into pandas
    b_df = pd.DataFrame(budgets)
    b_df['Limit'] = pd.to_numeric(b_df['Limit'], errors='coerce').fillna(0.0)
    month_budgets = b_df[b_df['Month'] == month_year]
    
    if month_budgets.empty:
        print(f"\nNo budget limits configured for the month: {month_year}")
        if actual_spent:
            print("Category-wise Spending (No Budgets Set for this month):")
            rows = [[cat, "N/A", f"₹{amt:.2f}", "No Budget Set", "N/A"] for cat, amt in actual_spent.items()]
            utils.display_table(["Category", "Budget Limit", "Actual Spend", "Status", "Difference"], rows)
        return

    # Compare
    print(f"\n==========================================================")
    print(f"               BUDGET STATUS FOR {month_year}             ")
    print(f"==========================================================")
    
    rows = []
    # Merge budget limits and actual spending
    for _, row in month_budgets.iterrows():
        cat = row['Category']
        limit = float(row['Limit'])
        actual = actual_spent.get(cat, 0.0)
        diff = limit - actual
        
        if diff >= 0:
            status = "Budget Remaining"
            diff_str = f"₹{diff:.2f}"
        else:
            status = "Budget Exceeded"
            diff_str = f"₹{abs(diff):.2f}"
            
        rows.append([
            cat,
            f"₹{limit:.2f}",
            f"₹{actual:.2f}",
            status,
            diff_str
        ])
        
    # Also show categories spent on but with no budget set
    for cat, actual in actual_spent.items():
        if cat not in month_budgets['Category'].values:
            rows.append([
                cat,
                "No Limit",
                f"₹{actual:.2f}",
                "No Budget Set",
                "N/A"
            ])
            
    utils.display_table(
        ["Category", "Budget Limit", "Actual Spend", "Status", "Difference"],
        rows
    )

def set_budget_limit(budgets: list, month_year: str) -> bool:
    """
    Prompt and set budget limit inside budgets memory list.
    """
    print(f"\n--- Set Budget Limit for {month_year} ---")
    
    category, cancelled = transaction_manager_prompt_input_field(
        f"Enter Expense Category {utils.EXPENSE_CATEGORIES}: ",
        utils.validate_category,
        extra_args=('expense',),
        error_msg=f"Category must be from the expense category list: {utils.EXPENSE_CATEGORIES}."
    )
    if cancelled: return False
    category = utils.get_matched_category(category, 'expense')
    
    limit_str, cancelled = transaction_manager_prompt_input_field(
        "Enter Budget Limit Amount: ",
        utils.validate_amount,
        error_msg="Limit must be a positive number."
    )
    if cancelled: return False
    limit = float(limit_str)
    
    # Check if budget already exists for this category/month
    existing = None
    for b in budgets:
        if b['Month'] == month_year and b['Category'] == category:
            existing = b
            break
            
    if existing:
        existing['Limit'] = str(limit)
        print(f"Success: Budget limit for {category} in {month_year} updated to ₹{limit:.2f}.")
    else:
        new_budget = {
            'Month': month_year,
            'Category': category,
            'Limit': str(limit)
        }
        budgets.append(new_budget)
        print(f"Success: Budget limit for {category} in {month_year} set to ₹{limit:.2f}.")
        
    return True

# Helper import proxy since we cannot circular import easily
def transaction_manager_prompt_input_field(prompt, validator, extra_args=None, error_msg=""):
    # Duplicate logic to avoid circular import with transaction_manager.py
    while True:
        val = input(prompt).strip()
        if val.lower() == 'q':
            return None, True
        if validator:
            is_valid = validator(val, *extra_args) if extra_args is not None else validator(val)
            if is_valid:
                return val, False
            else:
                print(f"Error: {error_msg} (Type 'q' to cancel)")
        else:
            if val:
                return val, False
            else:
                print("Error: Field cannot be empty. (Type 'q' to cancel)")
