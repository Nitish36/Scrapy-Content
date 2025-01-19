import scrapy
from scrapy_playwright.page import PageMethod

class QuoteSpider(scrapy.Spider):
    name = "quote"

    def start_requests(self):
        yield scrapy.Request(
            "https://quotes.toscrape.com/js",
            meta=dict(
				playwright=True,
				playwright_include_page=True,
				playwright_page_methods=[
                PageMethod("wait_for_selector", "div.quote"),
                PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod("wait_for_selector", "div.quote:nth-child(12)"),  # 10 per page
            ],
			))

    async def parse(self, response):
            page = response.meta["playwright_page"]
            await page.screenshot(path="example.png", full_page=True)  #page.pdf to store as pdf
            await page.pdf(path="example.pdf", format="A4")
            # screenshot contains the image's bytes
            await page.close()
            
            """ 
            2nd Method
            lst = []
            for quote in response.css("span.text::text").getall():
                lst.append(quote)

            print("[Quotes Count]: ", len(lst))
            print("[Quotes Count]: ", lst)"""

            """page = response.meta["playwright_page"]
            title = await page.title()
            for quote in response.css("div.quote span.text::text").getall():
                yield {
                    "quote": quote,
                    "title": title
                }
            await page.close()"""
