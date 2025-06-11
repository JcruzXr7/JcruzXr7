# Budgeting Tool

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    gspread = None  # gspread is optional
    ServiceAccountCredentials = None


def read_excel(path: str) -> pd.DataFrame:
    """Load budget data from an Excel file."""
    return pd.read_excel(path)


def read_google_sheet(spreadsheet_id: str, sheet_name: str, credentials_json: str) -> pd.DataFrame:
    """Load data from a Google Sheet using gspread."""
    if gspread is None:
        raise ImportError("gspread is required for Google Sheets access")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)


def summarize_cashflow(df: pd.DataFrame, amount_col: str = "Amount", type_col: str = "Type") -> pd.DataFrame:
    """Return a summary of income and expenses."""
    summary = df.groupby(type_col)[amount_col].sum().reset_index()
    return summary


def plot_cashflow(summary_df: pd.DataFrame, amount_col: str = "Amount", type_col: str = "Type") -> None:
    """Plot income vs expenses as a bar chart."""
    summary_df.plot(kind="bar", x=type_col, y=amount_col, legend=False)
    plt.ylabel("Amount")
    plt.title("Cash Flow")
    plt.tight_layout()
    plt.show()


def main(excel_path: Optional[str] = None,
         spreadsheet_id: Optional[str] = None,
         sheet_name: str = "Sheet1",
         credentials_json: Optional[str] = None) -> None:
    """Load data and display a cash flow chart."""
    if excel_path:
        df = read_excel(excel_path)
    elif spreadsheet_id and credentials_json:
        df = read_google_sheet(spreadsheet_id, sheet_name, credentials_json)
    else:
        raise ValueError("Provide either an Excel path or Google Sheet details")

    summary = summarize_cashflow(df)
    print(summary)
    plot_cashflow(summary)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Visualize budget from Excel or Google Sheets")
    parser.add_argument("--excel", help="Path to Excel file", dest="excel_path")
    parser.add_argument("--spreadsheet", help="Google Spreadsheet ID", dest="spreadsheet_id")
    parser.add_argument("--sheet", help="Worksheet name", default="Sheet1", dest="sheet_name")
    parser.add_argument("--creds", help="Path to Google service account JSON", dest="credentials_json")

    args = parser.parse_args()
    main(excel_path=args.excel_path,
         spreadsheet_id=args.spreadsheet_id,
         sheet_name=args.sheet_name,
         credentials_json=args.credentials_json)
