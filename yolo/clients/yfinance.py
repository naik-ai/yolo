import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


class YahooFinancials:
    """
    YahooFinancials:
      A class to fetch financials from Yahoo Finance

        - Input: ticker (str)
        - Output: Data pipleline, that is state aware on quarter_end_date basis.

    Methods for this pipeline:
        - fetch_income_statement: Fetch income statement
        - fetch_balance_sheet: Fetch balance sheet
        - fetch_cashflow: Fetch cashflow
        - fetch_info: Fetch info
        - clean_report: Clean report
        - clean_q_report: Clean quarterly report
    """

    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def fetch_income_statement(self) -> pd.DataFrame:
        return self.clean_q_report(self.stock.quarterly_income_stmt)

    def fetch_balance_sheet(self) -> pd.DataFrame:
        return self.clean_q_report(self.stock.quarterly_balance_sheet)

    def fetch_cashflow(self) -> pd.DataFrame:
        return self.clean_q_report(self.stock.quarterly_cashflow)

    def fetch_info(self) -> pd.DataFrame:

        info = self.stock.info
        info.pop("companyOfficers", None)
        df = self.clean_report(pd.DataFrame([info]))
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(" ", "_")
        return df

    def fetch_history(
        self, start: str = None, end: str = None, period=None
    ) -> pd.DataFrame:
        df = self.clean_report(
            self.stock.history(start=start, end=end, period=period).reset_index()
        )
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(" ", "_")
        df["date"] = pd.to_datetime(df["date"], utc=True)
        return df

    def clean_report(self, df: pd.DataFrame):
        df["ticker"] = self.ticker
        df["upload_date"] = pd.to_datetime("today", utc=True)
        return df

    def clean_q_report(self, df: pd.DataFrame) -> pd.DataFrame:
        clean_df = self.clean_report(df)
        clean_df = clean_df.reset_index().rename(columns={"index": "kpi"})
        clean_df = clean_df.melt(
            id_vars=["ticker", "upload_date", "kpi"], var_name="date"
        )
        clean_df["date"] = pd.to_datetime(clean_df["date"], utc=True)
        clean_df["value"] = clean_df["value"].astype(str)
        clean_df.columns = clean_df.columns.str.lower()
        clean_df.columns = clean_df.columns.str.replace(" ", "_")
        return clean_df
