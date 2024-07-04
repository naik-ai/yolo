import requests as req
import fitz
import tabula
import logging
import camelot
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO)


pdf_links = [
    "https://investors.mmtcdn.com/MMYT_Earnings_Release_Q4_FY_24_2a409c106d.pdf"
]


def extract_text_before_table(pdf_path, page_number):
    response = req.get(pdf_path)
    filename = pdf_path.split("/")[-1]
    with open(f"data/{filename}", "wb") as f:
        f.write(response.content)

    doc = fitz.open(f"data/{filename}")
    page = doc.load_page(page_number)

    # Find tables on the page
    tables = page.find_tables()
    if not tables:
        print("No tables found on the page.")

    if tables:  # at least one table found?
        df = pd.DataFrame(tables[0].extract())
        logging.info(df)


# Example usage


def extract_tables_from_pdf(
    pdf_link: str, pages: str | int = "all", implementation: str = "camelot"
) -> list:
    logging.info(f"Extracting tables from {pdf_link}")

    if implementation == "tabula":
        logging.info("Using tabula implementation")
        options = {"pages": pages, "multiple_tables": True}

        tables = tabula.read_pdf(
            pdf_link,
            **options,
        )

        return tables

    elif implementation == "camelot":
        logging.info("Using camelot implementation")

        pages_str = str(pages) if isinstance(pages, int) else pages

        tables = camelot.read_pdf(
            pdf_link,
            pages=pages_str,
            flavor="stream",
            # flavor="lattice",
        )

        dataframes = [table.df for table in tables]
        return dataframes

    else:
        raise ValueError(f"Invalid implementation: {implementation}")


def save_df_to_csv(
    df: pd.DataFrame, filename: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
):
    file = f"data/{filename}.csv"
    df.to_csv(file, index=False)
    logging.info(f"Saved {file}")


def main(implementation: str = "camelot", pages: str | int = "all"):
    try:
        for link in pdf_links:
            tables = extract_tables_from_pdf(
                link, pages=pages, implementation=implementation
            )
            logging.info(f"Extracted {len(tables)} tables")
            for i, table in enumerate(tables):

                if not table.empty and len(table) > 1:
                    table.columns = table.iloc[0]
                    table = table[1:]
                logging.info(f"Table {i+1}:")
                logging.info(table)
                save_df_to_csv(table, filename=f"1st_page_table_{i}")
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    # main(
    #     implementation="tabula",
    #     pages=10,
    # )

    page_number = 9
    extract_text_before_table(pdf_links[0], page_number)
