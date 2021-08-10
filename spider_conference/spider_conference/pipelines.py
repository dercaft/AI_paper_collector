# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter
import scrapy
from spider_conference.items import PaperItem
HEAD=[
    "title",
    "conference",
    "year",
    "abstract",
    "abstract_link",
    "pdf_link",
]
class SpiderConferencePipeline:
    file=None
    def open_spider(self,spider):
        self.file=open("./test.csv", 'w')
        self.writer=csv.DictWriter(self.file,fieldnames=HEAD) 
        self.writer.writeheader()
    def close_spider(self,spider):
        self.file.close()
    def process_item(self, item, spider):
        print("ITEM is: ",type(item))
        self.writer.writerow(item)
        return item
