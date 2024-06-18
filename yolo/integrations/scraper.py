import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class BookingIrSpider(scrapy.Spider):
    name = "booking_ir"
    allowed_domains = ["ir.bookingholdings.com"]
    start_urls = [
        "https://ir.bookingholdings.com/financials/quarterly-results/default.aspx"
    ]

    def parse(self, response):
        # Assuming PDF links are contained within <a> tags with a specific class or ID
        # You might need to adjust the selector based on the actual page structure
        pdf_links = response.css("a.pdf-link::attr(href)").getall()
        for link in pdf_links:
            # Assuming the date and quarter information can be extracted from the link text or an adjacent element
            # Adjust the selector accordingly
            date_and_quarter = response.css("a.pdf-link::text").get()
            yield {
                "file_urls": [response.urljoin(link)],
                "date_and_quarter": date_and_quarter,
            }


# Enable the built-in Files Pipeline
ITEM_PIPELINES = {
    "scrapy.pipelines.files.FilesPipeline": 1,
}

# Specify the folder where downloaded files will be stored
FILES_STORE = "/path/to/your/desired/folder"


# Get project settings
settings = get_project_settings()

# Specify the output format and destination
settings.set(
    "FEEDS",
    {
        "reports.json": {
            "format": "json",
            "encoding": "utf8",
            "store_empty": False,
            "fields": None,
            "indent": 4,
        },
    },
)
# Update the settings if necessary, for example:
# settings.set('ITEM_PIPELINES', {
#     'scrapy.pipelines.files.FilesPipeline': 1,
# })
# settings.set('FILES_STORE', '/path/to/your/desired/folder')

# Create a CrawlerProcess with the project settings
process = CrawlerProcess(settings)

# Add the spider to the process
process.crawl(BookingIrSpider)

# Start the crawling process
process.start()
