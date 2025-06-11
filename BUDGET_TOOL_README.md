# Budget Tool

This project provides a simple command line utility for visualizing a budget stored in an Excel file or Google Sheet.

## Features

- Load data from an Excel spreadsheet using `pandas`.
- Optionally connect to Google Sheets via `gspread` and a service account.
- Summarize income and expenses by type.
- Display a bar chart of cash flow using `matplotlib`.

## Usage

1. Install the required Python packages (for example, with `pip`):
   ```bash
   pip install pandas matplotlib gspread oauth2client
   ```
2. Prepare your data with at least three columns: `Type` (e.g., Income or Expense), `Category`, and `Amount`.
3. Run the tool with an Excel file:
   ```bash
   python budget_tool.py --excel path/to/budget.xlsx
   ```
4. Or use a Google Sheet by providing the spreadsheet ID, worksheet name, and service account credentials:
   ```bash
   python budget_tool.py --spreadsheet SPREADSHEET_ID --sheet Sheet1 --creds service_account.json
   ```

The script prints a summary table and displays a bar chart of income versus expenses.
