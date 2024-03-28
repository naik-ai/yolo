import logging
from yolo.helpers.constants import YAHOO_TRAVEL_TICKERS
from yolo.integrations.clients.yfinance import YahooFinancials as YF


def yahoo_finance_update_pipeline(tickers: list) -> None:
    """
    This function will update the yahoo finance pipeline
    INPUT -> List of tickers from constants.py
    OUTPUT -> None
        - Run the pipeline for each ticker in the list and upload to BQ
    """

    for ticker in tickers:
        logging.info(f"Starting the process {ticker}")
        tickerreport = YF(ticker)
        tickerreport.upload_2_bq()

    logging.info("Finished running the yahoo finance pipeline")


if __name__ == "__main__":
    yahoo_finance_update_pipeline(YAHOO_TRAVEL_TICKERS)
