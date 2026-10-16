# Personal Finance Tracker

A command-line interface (CLI) data-analysis application in Python to record incomes and expenses, manage budgets, track savings goals, analyze spending using `pandas`, and generate interactive visual graphs using `matplotlib`.

## Features

- **Core Transaction Management**:
  - Add Income (stores date, source/category, amount, payment mode, description).
  - Add Expense (stores date, category, amount, payment mode, description).
  - View full history sorted with newest entries first.
  - Search transactions by ID, Date, Category, or Type.
  - Update or Delete records with instant data consistency checks.
- **Robust Validators**: Validates inputs for positive values, proper Date format (`DD-MM-YYYY`), payment modes, and expense categories.
- **Advanced Data Analysis (pandas)**:
  - Monthly Summary computes total income, total expenses, savings, and savings percentage.
  - Generates descending category-wise expense breakdowns.
  - Tracks high and low expenses for any month.
  - Computes Average Daily Spending (Total Expense ÷ distinct active spending days).
- **Budget Goal Monitoring**:
  - Compares monthly spending per category against limits inside `budget.csv`.
  - Marks categories as "Budget Remaining" or "Budget Exceeded" with precise overages/remainders.
- **Visual Chart Export (matplotlib)**:
  - Pie chart representing expense distribution: saved to `graphs/category_chart.png`.
  - Grouped bar chart comparing monthly Income vs Expense: saved to `graphs/expense_chart.png`.
  - Line chart tracing net monthly savings trends over time: saved to `graphs/savings_chart.png`.
- **Flexible Data Store**: CSV databases survive system restarts and recover cleanly from missing directories or file corruption.

## Libraries Used

- **`pandas`**: Used for statistical analysis, calculations, sorting, and reporting.
- **`matplotlib`**: Headless backend renderer (Agg) used to generate and save charts.

## Folder Structure

```
Personal_Finance_Tracker/
├── main.py                # App entry point & interactive menu loop
├── transaction_manager.py # Add, edit, delete, view, search transactions
├── report_manager.py      # Pandas reporting, summaries, and budget checkers
├── graph_manager.py       # Matplotlib pie/bar/line graph generators
├── file_handler.py        # Safe CSV loading and saving
├── utils.py               # Validation rules, clear screen, and custom tables
├── data/
│   ├── transactions.csv   # Transactions ledger (auto-generated)
│   └── budget.csv         # Category budget targets (auto-generated)
├── reports/
│   └── monthly_report.csv # Compiled monthly summaries (auto-generated)
├── graphs/
│   ├── expense_chart.png  # Income vs Expense comparison (auto-generated)
│   ├── category_chart.png # Expense category breakdown pie (auto-generated)
│   └── savings_chart.png  # Savings path line graph (auto-generated)
├── README.md              # System documentation
└── requirements.txt       # Project dependencies
```

## Running the Application

### 1. Install Dependencies
Make sure you have `pandas` and `matplotlib` installed:
```bash
pip install -r requirements.txt
```

### 2. Execute
Navigate to the project directory and run the main entry point:
```bash
cd Personal_Finance_Tracker
python main.py
```
Use the numeric menu choices to manage transactions, set budgets, and generate reports/graphs. All modifications persist immediately.

## Verification
You can execute automated logic checks and graph generation validations using:
```bash
python scratch/test_tracker_logic.py
```
