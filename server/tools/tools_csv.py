
import pandas as pd
from datetime import datetime
from langchain_core.tools import tool

class TransactionCSVTool:

    def __init__(self):

        self.df = None


    @tool
    def load_csv(file_path: str) -> str:
        """Load a CSV file containing banking transactions. Required columns:
        Transaction Date, Post Date, Description, Category, Type, Amount, Memo"""

        try:
            df = pd.read_csv(file_path, parse_dates=["Transaction Date", "Post Date"])
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            TransactionCSVTool.df = df
            return f"CSV loaded with {len(df)} transactions."
        except Exception as e:
            return f"Error loading CSV: {str(e)}"


    @tool
    def spending_summary_last_month() -> str:
        """Calculate total spending for the last calendar month."""

        if TransactionCSVTool.df is None:
            return "No CSV loaded. Use the load_csv tool first."

        df = TransactionCSVTool.df
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        last_year = now.year if now.month > 1 else now.year - 1

        filtered = df[
            (df["Amount"] < 0) &  # negative amounts = spending
            (df["Transaction Date"].dt.month == last_month) &
            (df["Transaction Date"].dt.year == last_year)
        ]

        total = filtered["Amount"].sum()
        return f"Total spending in {last_month}/{last_year}: ${abs(total):.2f}"
