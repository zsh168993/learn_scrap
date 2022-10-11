# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class WebAttributesItem(scrapy.Item):
    # define the fields for your item here like:
    web_attributes_response = scrapy.Field()
    web_item_cas = scrapy.Field()
class WebPricesItem(scrapy.Item):
    # define the fields for your item here like:
    web_prices_response = scrapy.Field()
    web_item_cas_page = scrapy.Field()
    web_item_cas = scrapy.Field()

class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    image_name = scrapy.Field()
    image_source = scrapy.Field()


class PriceItem(scrapy.Item):
    # define the fields for your item here like:
    price_item = scrapy.Field()


class ProductInformationItem(scrapy.Item):
    # define the fields for your item here like:
    product_information = scrapy.Field()
