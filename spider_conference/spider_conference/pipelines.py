# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter
import scrapy
from spider_conference.items import PaperItem, HEAD

class SpiderConferencePipeline:
    file=None
    def open_spider(self,spider:scrapy.Spider):
        filename=str(spider.name)+".csv"
        self.file=open("../"+filename, 'w', encoding="utf-8")
        self.writer=csv.DictWriter(self.file,fieldnames=HEAD) 
        self.writer.writeheader()
    def close_spider(self,spider):
        self.file.close()
    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item
