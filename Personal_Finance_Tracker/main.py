import os
import sys
from datetime import datetime
import utils
import file_handler
import transaction_manager
import report_manager
import graph_manager

# Set up paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'transactions.csv')
BUDGET_PATH = os.path.join(BASE_DIR, 'data', 'budget.csv')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
GRAPHS_DIR = os.path.join(BASE_DIR, 'graphs')

def prompt_month_year(prompt_msg="Enter Month and Year (MM-YYYY, e.g. 07-2026, leave blank for current month): ") -> str:
    """
    Helper to get validated MM-YYYY month and year from the user.
    """
    while True:
        val = input(prompt_msg).strip()
        if not val:
            # Default to current month-year
            return datetime.now().strftime("%m-%Y")
        
        # Verify format
        parts = val.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            m, y = int(parts[0]), int(parts[1])
            if 1 <= m <= 12 and 1900 <= y <= 2100:
                # Format to pad single digit month (e.g. 7-2026 -> 07-2026)
                return f"{m:02d}-{y}"
        print("Error: Invalid format. Please enter as MM-YYYY (e.g., 07-2026).")

def main():
    # Load persistence files on startup
    print("Loading databases...")
    transactions = file_handler.load_transactions(DB_PATH)
    budgets = file_handler.load_budget(BUDGET_PATH)
    print(f"Loaded {len(transactions)} transaction record(s).")
    print(f"Loaded {len(budgets)} budget limit(s).")
    
    input("\nPress Enter to proceed to the main menu...")
    
    while True:
        utils.clear_screen()
        print("====================================")
        print("      PERSONAL FINANCE TRACKER      ")
        print("====================================")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Search Transaction")
        print("5. Update Transaction")
        print("6. Delete Transaction")
        print("7. Monthly Summary")
        print("8. Budget Status")
        print("9. Financial Reports")
        print("10. Expense Charts")
        print("11. Exit")
        print("====================================")
        
        choice = input("Enter Choice (1-11): ").strip()
        
        if choice == '1':
            modified = transaction_manager.add_income(transactions)
            if modified:
                file_handler.save_transactions(DB_PATH, transactions)
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            modified = transaction_manager.add_expense(transactions)
            if modified:
                file_handler.save_transactions(DB_PATH, transactions)
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            transaction_manager.view_transactions(transactions)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            transaction_manager.search_transaction(transactions)
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            modified = transaction_manager.update_transaction(transactions)
            if modified:
                file_handler.save_transactions(DB_PATH, transactions)
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            modified = transaction_manager.delete_transaction(transactions)
            if modified:
                file_handler.save_transactions(DB_PATH, transactions)
            input("\nPress Enter to continue...")
            
        elif choice == '7':
            month_year = prompt_month_year()
            # Show summary only
            df = report_manager.get_dataframe(transactions)
            if df.empty:
                print("\nNo transaction data available.")
            else:
                try:
                    month, year = map(int, month_year.split('-'))
                    month_df = df[(df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
                    if month_df.empty:
                        print(f"\nNo transactions found for {month_year}.")
                    else:
                        inc = month_df[month_df['Type'] == 'Income']['Amount'].sum()
                        exp = month_df[month_df['Type'] == 'Expense']['Amount'].sum()
                        sav = inc - exp
                        sav_pct = (sav / inc * 100) if inc > 0 else 0.0
                        
                        print("\n==================================")
                        print(f"    MONTHLY SUMMARY ({month_year})   ")
                        print("==================================")
                        print(f"Total Income : ₹{inc:.2f}")
                        print(f"Total Expense: ₹{exp:.2f}")
                        print(f"Net Savings  : ₹{sav:.2f}")
                        print(f"Savings %    : {sav_pct:.2f}%")
                        print("==================================")
                except ValueError:
                    print("Error: Could not parse Month-Year.")
            input("\nPress Enter to continue...")
            
        elif choice == '8':
            month_year = prompt_month_year()
            report_manager.display_budget_status(transactions, budgets, month_year)
            
            # Offer configuration
            print("\nConfigure Budgets:")
            print("1. Set or Update a Category Budget Limit")
            print("2. Return to Main Menu")
            budget_opt = input("Enter choice (1-2): ").strip()
            if budget_opt == '1':
                modified = report_manager.set_budget_limit(budgets, month_year)
                if modified:
                    file_handler.save_budget(BUDGET_PATH, budgets)
            input("\nPress Enter to continue...")
            
        elif choice == '9':
            month_year = prompt_month_year()
            report_manager.generate_monthly_report(transactions, month_year, budgets, REPORTS_DIR)
            input("\nPress Enter to continue...")
            
        elif choice == '10':
            month_year = prompt_month_year()
            print("\nGenerating charts...")
            
            pie_path = os.path.join(GRAPHS_DIR, 'category_chart.png')
            bar_path = os.path.join(GRAPHS_DIR, 'expense_chart.png')
            line_path = os.path.join(GRAPHS_DIR, 'savings_chart.png')
            
            p_ok = graph_manager.generate_category_pie_chart(transactions, month_year, pie_path)
            b_ok = graph_manager.generate_income_expense_bar_chart(transactions, bar_path)
            l_ok = graph_manager.generate_savings_trend_line(transactions, line_path)
            
            if p_ok or b_ok or l_ok:
                print(f"\nSaved charts to: {GRAPHS_DIR}")
            else:
                print("\nFailed to generate charts. Ensure sufficient transaction records exist.")
            input("\nPress Enter to continue...")
            
        elif choice == '11':
            print("\nExiting Personal Finance Tracker. Goodbye!")
            sys.exit(0)
            
        else:
            print("\nError: Invalid choice. Select a number between 1 and 11.")
            input("\nPress Enter to try again...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting gracefully...")
        sys.exit(0)
