import dlt
from dlt.common.libs.pydantic import pydantic_to_table_schema_columns
from dlt.common.typing import TDataItems
from dlt.extract.source import DltResource
from typing import Iterator, Sequence
import pandas as pd
import logging
from yolo.clients.yfinance import YahooFinancials
from yolo.helpers.constants import (
    YAHOO_TRAVEL_TICKERS,
)
from yolo.helpers.bq_utility import get_raw_from_bq
from yolo.models.yfinance import (
    YahooFinancialsInfo,
    YahooFinancialsIncomeStatement,
    YahooFinancialsBalanceSheet,
    YahooFinancialsCashFlow,
    YahooFinancialsHistory,
)


# ---
# INFO: source_yfinance__info
# ---


@dlt.resource(
    table_name="source_yfinance__info",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(YahooFinancialsInfo),
)
def yahoo_finance_info() -> Iterator[TDataItems]:
    all_info_df = pd.DataFrame()
    for ticker in YAHOO_TRAVEL_TICKERS:
        yf = YahooFinancials(ticker)
        info_df = yf.fetch_info()
        all_info_df = pd.concat([all_info_df, info_df], ignore_index=True)

    all_info_df = all_info_df.astype(str)
    data = all_info_df.to_dict(orient="records")

    for item in data:
        yield YahooFinancialsInfo(**item)


# ---
# Income Statement: source_yfinance__income_statement
# ---


@dlt.resource(
    table_name="source_yfinance__income_statement",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(YahooFinancialsIncomeStatement),
)
def yahoo_finance_income_statement() -> Iterator[TDataItems]:
    tickers = get_raw_from_bq("source_yfinance_tickers_mkt_cap_grt_zero")[
        "ticker"
    ].to_list()
    all_income_statement_df = pd.DataFrame()
    for ticker in tickers:
        yf = YahooFinancials(ticker)
        income_statement_df = yf.fetch_income_statement()
        if not income_statement_df.empty:
            all_income_statement_df = pd.concat(
                [all_income_statement_df, income_statement_df], ignore_index=True
            )
        else:
            logging.info(f"No income statement data for {ticker}")
    data = all_income_statement_df.to_dict(orient="records")
    for item in data:
        yield YahooFinancialsIncomeStatement(**item)


# ---
# Balance Sheet: source_yfinance__balance_sheet
# ---


@dlt.resource(
    table_name="source_yfinance__balance_sheet",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(YahooFinancialsBalanceSheet),
)
def yahoo_finance_balance_sheet() -> Iterator[TDataItems]:
    tickers = get_raw_from_bq("source_yfinance_tickers_mkt_cap_grt_zero")[
        "ticker"
    ].to_list()
    all_balance_sheet_df = pd.DataFrame()
    for ticker in tickers:
        yf = YahooFinancials(ticker)
        balance_sheet_df = yf.fetch_balance_sheet()
        if not balance_sheet_df.empty:
            all_balance_sheet_df = pd.concat(
                [all_balance_sheet_df, balance_sheet_df], ignore_index=True
            )
        else:
            logging.info(f"No balance sheet data for {ticker}")
    data = all_balance_sheet_df.to_dict(orient="records")
    for item in data:
        yield YahooFinancialsBalanceSheet(**item)


# ---
# Cash Flow: source_yfinance__cash_flow
# ---
@dlt.resource(
    table_name="source_yfinance__cash_flow",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(YahooFinancialsCashFlow),
)
def yahoo_finance_cash_flow() -> Iterator[TDataItems]:
    tickers = get_raw_from_bq("source_yfinance_tickers_mkt_cap_grt_zero")[
        "ticker"
    ].to_list()
    all_cash_flow_df = pd.DataFrame()
    for ticker in tickers:
        yf = YahooFinancials(ticker)
        cash_flow_df = yf.fetch_cashflow()
        if not cash_flow_df.empty:
            all_cash_flow_df = pd.concat(
                [all_cash_flow_df, cash_flow_df], ignore_index=True
            )
        else:
            logging.info(f"No cash flow data for {ticker}")
    data = all_cash_flow_df.to_dict(orient="records")
    for item in data:
        yield YahooFinancialsCashFlow(**item)


# ---
# History: source_yfinance__history
# ---
@dlt.resource(
    table_name="source_yfinance__history",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(YahooFinancialsHistory),
)
def yahoo_finance_history() -> Iterator[TDataItems]:
    tickers = get_raw_from_bq("source_yfinance_tickers_mkt_cap_grt_zero")[
        "ticker"
    ].to_list()
    all_history_df = pd.DataFrame()
    for ticker in tickers:
        yf = YahooFinancials(ticker)
        history_df = yf.fetch_history()
        if not history_df.empty:
            all_history_df = pd.concat([all_history_df, history_df], ignore_index=True)
        else:
            logging.info(f"No history data for {ticker}")
    data = all_history_df.to_dict(orient="records")
    for item in data:
        yield YahooFinancialsHistory(**item)


# Sources
@dlt.source(
    max_table_nesting=0,
)
def yahoo_finance_pipeline() -> Sequence[DltResource]:
    return [
        yahoo_finance_info,
        yahoo_finance_income_statement,
        yahoo_finance_balance_sheet,
        yahoo_finance_cash_flow,
        yahoo_finance_history,
    ]
