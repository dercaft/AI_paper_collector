
import os,sys,csv
import scrapy
from spider_conference.items import PaperItem

def get_urls(name):
    recs=[]
    path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path=os.path.dirname(os.path.dirname(path))
    csv_file=os.path.join(path,"顶会网址.csv")
    with open(csv_file,'r',encoding="utf-8") as f:
        read=csv.reader(f)
        for item in read:
            site=item[3]
            if not site.startswith('http') or site.endswith('pdf'):
                print("Not a url or Source is a pdf file")
                continue
            if item[1] == name:
                recs.append(item)
    return recs
class AAAI_Spider(scrapy.Spider):
    name="AAAI"
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        pass
class CVPR_Spider(scrapy.Spider):
    name="CVPR"
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        pass
class ECCV_Spider(scrapy.Spider):
    name="ECCV"
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        pass
class ICCV_Spider(scrapy.Spider):
    name="ICCV"
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        pass
class ICLR_Spider(scrapy.Spider):
    name="ICLR"
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        pass
class ICML_Spider(scrapy.Spider):
    name="ICML"
    start_urls=(
            "http://proceedings.mlr.press/v80/",
            "http://proceedings.mlr.press/v97/",
            "http://proceedings.mlr.press/v119/",
            "http://proceedings.mlr.press/v139/",
        )
    def start_requests(self):
        recs=get_urls(self.name)
        
    def parse_abs(self,response):
        item=response.meta['item']
        abstract=response.xpath("//div[@id='abstract']/text()").extract_first()
        item['abstract']=abstract
        yield item
    def parser(self,response):
        papers=response.css("div.paper")
        for paper in papers:
            item=PaperItem()
            item["title"]=paper.css("p.title::text")
            link=paper.xpath('p[@class="links"]/a[contains(text(),"abs")]/@href').extract_first()
            item["abstract_link"]=link
            yield scrapy.Request(url=link,callback=self.parse_abs,meta={'item':item})

class IJCAI_Spider(scrapy.Spider):
    name="IJCAI"
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        pass
class NIPS_Spider(scrapy.Spider):
    name="NIPS"
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        pass
