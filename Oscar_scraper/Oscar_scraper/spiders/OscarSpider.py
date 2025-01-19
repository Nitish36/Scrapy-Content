import scrapy
from scrapy_playwright.page import PageMethod


class OscarSpider(scrapy.Spider):
    name = "OscarSpider"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.scrapethissite.com/pages/ajax-javascript/#2010",
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "tr.film"),  # Wait for data to load
                    PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_timeout", 6000)  # Wait for AJAX data
                ]
            }
        )

    async def parse(self, response):
        for row in response.css("tr.film"):
            yield {
                "title": row.css("td.film-title::text").get(default="").strip(),
                "nominations": row.css("td.film-nominations::text").get(default="").strip(),
                "awards": row.css("td.film-awards::text").get(default="").strip(),
            }
