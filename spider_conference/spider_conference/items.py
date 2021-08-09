# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderConferenceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class PaperItem(scrapy.Item):
    name=scrapy.Field()
    pdf_link=scrapy.Field()
    abstract_link=scrapy.Field()
    abstract=scrapy.Field()
    infos=scrapy.Field()
