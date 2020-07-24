# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeNewsDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    URL = scrapy.Field()
    Title = scrapy.Field()
    Content = scrapy.Field()


class ScrapeNewsNonDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    URL = scrapy.Field()

