import dlt
import logging
from yolo.integrations.yfinance import yahoo_finance_pipeline


def pipeline_integrations_yfinance():
    """

    Steps
        - Runs the yahoo_finance_pipeline using DLT pipeline: yolo_yfinance
            - pulls the data for below methods
            - Loads the data into BigQuery to resp tables in raw dataset
    Source Methods:
        - yahoo_finance_pipeline
        - yahoo_finance_info,
        - yahoo_finance_income_statement,
        - yahoo_finance_balance_sheet,
        - yahoo_finance_cash_flow,
        - yahoo_finance_history,
    Awareness:
        - Data replaces in BQ for all methods when called
        - No Time aware

    """

    logging.info("Running DLT yolo_yfinance pipeline")
    p = dlt.pipeline(
        pipeline_name="yolo_yfinance",
        destination="bigquery",
        dataset_name="raw",
    )
    p.run(yahoo_finance_pipeline(), loader_file_format="jsonl")
    logging.info("Finished DLT yolo_yfinance pipeline")


if __name__ == "__main__":

    # TODO: Add Prefect flow and subflow to all pipelines

    pipeline_integrations_yfinance()
