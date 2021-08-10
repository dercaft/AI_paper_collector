# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

HEAD=[
    "title",
    "conference",
    "year",
    "abstract",
    "abstract_link",
    "pdf_link",
]
class SpiderConferenceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class PaperItem(scrapy.Item):
    title=scrapy.Field()
    conference=scrapy.Field()
    year=scrapy.Field()
    abstract=scrapy.Field()
    pdf_link=scrapy.Field()
    abstract_link=scrapy.Field()
