import dlt
import logging
import asyncio
import pandas as pd

from dlt.common.libs.pydantic import pydantic_to_table_schema_columns
from dlt.common.typing import TDataItems
from dlt.extract.source import DltResource
from typing import Iterator, Sequence

from yolo.helpers.bq_utility import get_raw_from_bq
from yolo.helpers.constants import (
    YAHOO_TRAVEL_TICKERS,
)


def generate_url_by_parameters(
    base_url: str, function: str, api_key: str, symbols: list, **kwargs
) -> list:
    urls = []
    for symbol in symbols:
        payload = {
            "function": function,
            "keywords": symbol,
            "apikey": api_key,
            **kwargs,
        }
        query_string = "&".join([f"{key}={value}" for key, value in payload.items()])
        url = f"{base_url}?{query_string}"
        urls.append(url)
    return urls


# TODO: Daily stock data for all symbols
# TODO: News for all symbols
# TODO: Search for symbol that didnt match
# TODO: Fundamental data for all symbols
# TODO: INCOME_STATEMENT
# TODO: BALANCE_SHEET
# TODO: CASH_FLOW
# TODO: Economic Indicators
# TODO: Sector performance for all symbols
# TODO: Stock data for all symbols


if __name__ == "__main__":
    urls = generate_url_by_parameters(
        YAHOO_TRAVEL_TICKERS, "SYMBOL_SEARCH", "EN9CPB8SBC9MKIPI"
    )
    print(urls)
