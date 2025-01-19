import scrapy
from ebook_scraper.items import EbookScraperItem
from scrapy.loader import ItemLoader


class EbookSpider(scrapy.Spider):
    name = "ebook"
    start_urls = ["https://books.toscrape.com/catalogue/category/books_1/"]
    cols = ["title", "price"]

    def __init__(self):
        super().__init__()
        self.page_count = 0

    def parse(self, response):
        self.page_count += 1
        ebooks = response.css("article.product_pod")

        for ebook in ebooks:
            loader = ItemLoader(item=EbookScraperItem())
            loader.add_value('title', ebook.css("h3 a[title]::text").get())
            loader.add_value('price', ebook.css("p.price_color::text").get())

            # Extract book URL
            book_url = ebook.css("h3 a").attrib['href'].replace('../..', 'https://books.toscrape.com/catalogue/')
            loader.add_value('url', book_url)

            # Yield request to the book's detail page
            yield scrapy.Request(url=book_url, callback=self.parse_details, meta={'loader': loader})

        # Handle pagination
        next_btn = response.css("li.next a")
        if next_btn:
            next_page = f"{self.start_urls[0]}/{next_btn.attrib['href']}"
            yield scrapy.Request(url=next_page, callback=self.parse)

        print("[PAGE COUNT]", self.page_count)

    def parse_details(self, response):
        """ Extract additional details from the book's page """
        loader = response.meta['loader']

        # Extract additional data (Example: description)
        description = response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        loader.add_value('description', description)
        product_details = {}
        table = response.css("table")
        for row in table.css("tr"):
            heading = row.css("th::text").get()
            data = row.css("td::text").get()
            product_details[heading] = data
            loader.add_value('details', product_details[heading])
        
        yield loader.load_item()


"""
    def parse(self, response):
        print("Our Response")
        # print(response.css("h3 a::text").get())
        ebooks = response.css("article")
        for ebook in ebooks:
            # title = ebook.css("h3 a::text").get()
            title = ebook.css("h3 a[title]::text").get()
            price = ebook.css("p.price_color::text").get()
            title2 = ebook.xpath('//h3/a[@title]/@title').get()
            title3 = ebook.css('h3 a::attr(title)').get()
            title4 = ebook.css('h3 a').attrib['title']
            yield {
                "title": title,
                "price": price,
                "title2": title2
            }
"""
