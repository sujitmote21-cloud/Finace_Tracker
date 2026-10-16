import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Forces matplotlib to run headlessly without GUI windows
import matplotlib.pyplot as plt
import report_manager

def check_dir(filepath):
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def generate_category_pie_chart(transactions: list, month_year: str, save_path: str) -> bool:
    """
    Renders and saves a pie chart of expenses by category for a specific month.
    """
    check_dir(save_path)
    df = report_manager.get_dataframe(transactions)
    if df.empty:
        print("No transactions available to generate pie chart.")
        return False
        
    try:
        month, year = map(int, month_year.split('-'))
    except ValueError:
        print("Error: Month-Year format must be MM-YYYY.")
        return False
        
    month_df = df[(df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    expense_df = month_df[month_df['Type'] == 'Expense']
    
    if expense_df.empty:
        print(f"No expense transactions found for {month_year} to generate pie chart.")
        return False
        
    # Group by category
    cat_data = expense_df.groupby('Category')['Amount'].sum()
    
    # Custom Styling
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Generate pie chart
    wedges, texts, autotexts = ax.pie(
        cat_data, 
        labels=cat_data.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        textprops=dict(color="black"),
        shadow=False
    )
    
    # Clean design
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=11)
    
    ax.set_title(f"Expense Breakdown by Category ({month_year})", fontsize=14, weight="bold", pad=20)
    plt.tight_layout()
    
    try:
        fig.savefig(save_path, dpi=120)
        plt.close(fig)
        print(f"Success: Expense pie chart saved to {save_path}")
        return True
    except Exception as e:
        print(f"Error saving expense pie chart: {e}")
        plt.close(fig)
        return False

def generate_income_expense_bar_chart(transactions: list, save_path: str) -> bool:
    """
    Renders and saves a bar chart of monthly Income vs Expense comparison.
    """
    check_dir(save_path)
    df = report_manager.get_dataframe(transactions)
    if df.empty:
        print("No transactions available to generate comparison bar chart.")
        return False
        
    # Extract Month Year Period for grouping
    df['Period'] = df['Date'].dt.to_period('M')
    
    # Sum by Period and Type
    summary = df.groupby(['Period', 'Type'])['Amount'].sum().unstack(fill_value=0.0)
    
    # Check if we have both columns
    if 'Income' not in summary.columns:
        summary['Income'] = 0.0
    if 'Expense' not in summary.columns:
        summary['Expense'] = 0.0
        
    summary = summary.sort_index()
    # Limit to last 12 active periods to keep plot neat
    summary = summary.tail(12)
    
    if summary.empty:
        print("No summary data available to plot bar chart.")
        return False
        
    # Convert index back to string for clean plotting labels
    periods_str = [str(p) for p in summary.index]
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_indexes = range(len(periods_str))
    width = 0.35
    
    rects1 = ax.bar([x - width/2 for x in x_indexes], summary['Income'], width, label='Income', color='#26a69a')
    rects2 = ax.bar([x + width/2 for x in x_indexes], summary['Expense'], width, label='Expense', color='#ef5350')
    
    ax.set_ylabel('Amount (₹)', fontsize=11, labelpad=10)
    ax.set_xlabel('Month', fontsize=11, labelpad=10)
    ax.set_title('Monthly Income vs Expense Comparison', fontsize=14, weight='bold', pad=15)
    ax.set_xticks(x_indexes)
    ax.set_xticklabels(periods_str, rotation=30)
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    
    try:
        fig.savefig(save_path, dpi=120)
        plt.close(fig)
        print(f"Success: Income vs Expense bar chart saved to {save_path}")
        return True
    except Exception as e:
        print(f"Error saving bar chart: {e}")
        plt.close(fig)
        return False

def generate_savings_trend_line(transactions: list, save_path: str) -> bool:
    """
    Renders and saves a line chart of monthly Savings trend over time.
    """
    check_dir(save_path)
    df = report_manager.get_dataframe(transactions)
    if df.empty:
        print("No transactions available to generate savings trend chart.")
        return False
        
    df['Period'] = df['Date'].dt.to_period('M')
    
    summary = df.groupby(['Period', 'Type'])['Amount'].sum().unstack(fill_value=0.0)
    if 'Income' not in summary.columns:
        summary['Income'] = 0.0
    if 'Expense' not in summary.columns:
        summary['Expense'] = 0.0
        
    summary = summary.sort_index()
    summary['Savings'] = summary['Income'] - summary['Expense']
    
    summary = summary.tail(12) # last 12 months
    
    if summary.empty:
        print("No data available to plot line chart.")
        return False
        
    periods_str = [str(p) for p in summary.index]
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot line
    ax.plot(periods_str, summary['Savings'], marker='o', linewidth=2.5, color='#5c6bc0', label='Savings (Income - Expense)')
    
    # Draw helper horizontal line at zero
    ax.axhline(0, color='grey', linestyle='--', linewidth=1, alpha=0.7)
    
    ax.set_ylabel('Net Savings (₹)', fontsize=11, labelpad=10)
    ax.set_xlabel('Month', fontsize=11, labelpad=10)
    ax.set_title('Monthly Savings Trend Over Time', fontsize=14, weight='bold', pad=15)
    ax.set_xticks(range(len(periods_str)))
    ax.set_xticklabels(periods_str, rotation=30)
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    
    try:
        fig.savefig(save_path, dpi=120)
        plt.close(fig)
        print(f"Success: Savings trend line chart saved to {save_path}")
        return True
    except Exception as e:
        print(f"Error saving savings trend line: {e}")
        plt.close(fig)
        return False
