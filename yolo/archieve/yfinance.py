import pandas as pd
import numpy as np
import pandas_gbq as pbq
import logging
from yolo.clients.yfinance import YahooFinancials
from yolo.helpers.constants import PROJECT_ID, YAHOO_FINANCE_STATEMENT_TYPES
from yolo.helpers.bq_utility import read_sql_from_file_add_template


def upload_2_bq(self, project_id: str = PROJECT_ID):
    """
    upload_2_bq:
        Upload data from Yahoo Finance to BQ

    Args:
        df (pd.DataFrame): The dataframe to be uploaded to BQ
        project_id (str): The project id to upload to. Defaults to PROJECT_ID.

    Returns:
        None - Logging for pipeline completion
    """

    for statement in YAHOO_FINANCE_STATEMENT_TYPES:

        logging.info(f"Starting the process {statement}")
        method_name = f"fetch_{statement}"
        if hasattr(self, method_name):
            df = getattr(self, method_name)()

        latest_date_date = self.get_latest_date_from_bq_table_by_col(
            statement_type=statement, col="date"
        )

        if latest_date_date:
            # if new data is greater, upload the new data only relevant to the new dates
            logging.info(
                f"Latest End of Quarter Date: {latest_date_date}, pull reports after this date"
            )
            df = df[df["date"] > latest_date_date].reset_index(drop=True)

        # if none -> upload all of data else upload filtered data
        if not df.empty:
            pbq.to_gbq(
                df,
                destination_table=f"raw.source_yfinance_{statement}",
                if_exists="append",
                project_id=project_id,
            )

        else:
            logging.info(f"No new data to upload for {statement}")


def get_latest_date_from_bq_table_by_ticker(
    self,
    statement_type: str,
    col: int,
) -> pd.Timestamp | None:
    """
    The sql used is same as routes Helper module: get_latest_by_bq_table_and_date_col
    """
    try:

        sql = read_sql_from_file_add_template(
            sql_file_name="source_yfinance_latest_report_date_by_ticker",
            template_data={
                "project_id": PROJECT_ID,
                "statement_type": statement_type,
                "ticker": self.ticker,
                "col": col,
            },
        )
        logging.info(f"SQL, Latest Date from {statement_type} for {self.ticker}: {sql}")
        df = pbq.read_gbq(sql)
        final_start_date = np.array(df[col])[0]

        # if NaN, return None
        if pd.isna(final_start_date):
            return None
        return pd.to_datetime(final_start_date, utc=True)

    except pbq.exceptions.GenericGBQException as e:
        if "Reason: 404" in str(e):
            logging.info(
                f"The table raw.source_yfinance_{statement_type} was not found."
            )
            return None
        if "Unrecognized name: date" in str(e):
            logging.info("The column date was not found.")
            return None
        else:
            raise


if __name__ == "__main__":
    ticker = "TCOM"
    logging.info(f"Starting the process {ticker}")
    tickerreport = YahooFinancials(ticker)
    # tickerreport.upload_2_bq()

    df = tickerreport.fetch_history(start="2024-01-01", end="2024-03-01")

    print(df["date"].min())
    print(df["date"].max())
