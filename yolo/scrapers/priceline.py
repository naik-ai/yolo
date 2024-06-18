import scrapy
import os
from PyPDF2 import PdfFileReader
import io
from yolo.helpers.constants import earnings_reports_links

# Last 8 Quater's Priceline Data


class PDFSpider(scrapy.Spider):
    name = "pdf_spider"
    start_urls = [
        # Specify the correct URL to scrape for PDF links
        earnings_reports_links["bookingholdings"]
    ]

    # Custom settings to manage robot rules and download delays
    custom_settings = {
        "DOWNLOAD_DELAY": 2,  # To avoid overloading the server
        "ROBOTSTXT_OBEY": False,  # Ignore robots.txt rules
    }

    def parse(self, response):
        pdf_links = response.xpath('//a[contains(@href, ".pdf")]/@href').getall()

        # Debug information to ensure PDFs are found
        self.log(f"Found PDF links: {pdf_links}")

        # Request download for each PDF found
        for link in pdf_links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(absolute_url, callback=self.parse_pdf)

    def parse_pdf(self, response):
        pdf_file = io.BytesIO(response.body)
        pdf_reader = PdfFileReader(pdf_file)

        # Extract text from each page and accumulate it
        pdf_text = []
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_text.append(page.extractText())

        # Join the text from all pages
        extracted_text = "\n".join(pdf_text)

        # Save the extracted text to a file in 'extracted_texts' folder
        folder_path = os.path.join("..", "extracted_texts")
        os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

        # Log a message when the text is saved
        self.log(f"Extracted text from PDF: {file_path}")
