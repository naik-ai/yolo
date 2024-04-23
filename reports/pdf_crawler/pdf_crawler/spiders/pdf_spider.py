# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# import pdfminer.high_level
# import re
# from io import BytesIO

# # Regular expression to identify PDF links
# PDF_PATTERN = re.compile(r'\.pdf$', re.IGNORECASE)

# class PdfSpider(CrawlSpider):
#     name = "pdf_spider"
#     allowed_domains = ["priceline.com"]  # Update as needed
#     start_urls = ["https://www.priceline.com/"]

#     # Follow all links and extract PDFs
#     rules = (
#         Rule(
#             LinkExtractor(allow=PDF_PATTERN),
#             callback='parse_pdf',
#             follow=True,
#         ),
#     )

#     def parse_pdf(self, response):
#         if PDF_PATTERN.search(response.url):
#             pdf_text = self.extract_text_from_pdf(response.body)
#             yield {
#                 'url': response.url,
#                 'text': pdf_text,
#             }
#         else:
#             # Check if HTML class or other identifier leads to PDFs
#             self.log(f"Non-PDF URL found: {response.url}")

#     def extract_text_from_pdf(self, pdf_data):
#         try:
#             text = pdfminer.high_level.extract_text(BytesIO(pdf_data))
#             return text
#         except Exception as e:
#             self.log(f"Error extracting text from PDF: {e}")
#             return "Error extracting text"






import scrapy
import os
from PyPDF2 import PdfFileReader
import io

class PDFSpider(scrapy.Spider):
    name = "pdf_spider"
    start_urls = [
        # Specify the correct URL to scrape for PDF links
        "https://www.priceline.com/",
    ]

    # Custom settings to manage robot rules and download delays
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # To avoid overloading the server
        'ROBOTSTXT_OBEY': False,  # Ignore robots.txt rules
    }

    def parse(self, response):
        # Find all links to PDF files using XPath
        pdf_links = response.xpath('//a[contains(@href, ".pdf")]/@href').getall()

        # Debug information to ensure PDFs are found
        self.log(f"Found PDF links: {pdf_links}")

        # Request download for each PDF found
        for link in pdf_links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(absolute_url, callback=self.parse_pdf)

    def parse_pdf(self, response):
        # Read PDF from response body and process its text
        pdf_file = io.BytesIO(response.body)
        pdf_reader = PdfFileReader(pdf_file)

        # Extract text from each page and accumulate it
        pdf_text = []
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_text.append(page.extractText())  # Extract text from the page

        # Join the text from all pages
        extracted_text = "\n".join(pdf_text)

        # Save the extracted text to a file in 'extracted_texts' folder
        folder_path = os.path.join("..", "extracted_texts")
        os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

        # Save extracted text as a .txt file
        filename = response.url.split("/")[-1] + ".txt"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'w') as f:
            f.write(extracted_text)

        # Log a message when the text is saved
        self.log(f"Extracted text from PDF: {file_path}")
