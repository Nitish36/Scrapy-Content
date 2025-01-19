# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst


def get_price(txt):
    return float(txt.replace('£', ''))


def get_quantity(txt):
    return int(
        txt.replace('(', '').split()[0]
    )


class EbookScraperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field(output_processor=TakeFirst())
    price = Field(
        input_processor=MapCompose(get_price),
        output_processor=TakeFirst()
    )
    url = Field(output_processor=TakeFirst())
    quantity = Field(
        input_processor=MapCompose(get_quantity),
        output_processor=TakeFirst()
    )
    description = Field(output_processor=TakeFirst())
    details = Field(output_processor=TakeFirst())
    pass
