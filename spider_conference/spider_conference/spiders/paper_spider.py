
import os,sys,csv,time
import functools
from urllib import parse
import scrapy
from scrapy import item
from scrapy.http.request import Request
from spider_conference.items import PaperItem, HEAD

def dict_check(item:dict):
    return all([item.__contains__(x) for x in HEAD])
def get_urls(name):
    recs=[]
    path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path=os.path.dirname(os.path.dirname(path))
    csv_file=os.path.join(path,"Conference_website.csv")
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
class Meta_Spider(scrapy.Spider):
    def start_requests(self):
        recs=get_urls(self.name)
        for rec in recs:
            yield scrapy.Request(url=rec[3], callback=self.parser,
                                 meta={"conference":rec[1],"year":rec[2]})
class AAAI_Spider(scrapy.Spider):
    name="AAAI"
    
    def start_requests(self):
        recs=get_urls(self.name)
        for rec in recs:
            yield scrapy.Request(url=rec[3], callback=self.parser,
                                 meta={"conference":rec[1],"year":rec[2]})

    def parser(self,response):
        pass
class CVPR_Spider(Meta_Spider):
    name="CVPR"
    def parse_abs(self,response):
        item=response.meta['item']
        abstract=response.xpath("//div[@id='abstract']")[0].xpath("string(.)").extract_first().strip()
        item["abstract"]=abstract
        a=response.xpath("//a[contains(text(),'pdf')]/@href").extract_first()
        item["pdf_link"]=parse.urljoin(response.url,a)
        if dict_check(item):
            yield item
        else:
            raise BaseException("ERROR ITEM format{}".format(item.keys()))
    def day_parser(self,response):
        papers=response.xpath("//dt[@class='ptitle']/a")
        for paper in papers:
            time.sleep(0.05)
            item=PaperItem()
            item["title"]=paper.xpath("text()").extract_first()
            item["conference"]=response.meta["conference"]
            item["year"]=response.meta["year"]
            tail=paper.xpath("@href").extract_first()
            link=parse.urljoin(response.url,tail)
            item["abstract_link"]=link
            yield scrapy.Request(url=link,callback=self.parse_abs,meta={'item':item})
        pass
    def parser(self,response):
        days=response.xpath("//dd/a[contains(text(),'Day')]/@href").getall()
        for day in days:
            url=parse.urljoin(response.url,day)
            yield scrapy.Request(url=url, callback=self.day_parser,
                                 meta={"conference":response.meta["conference"],"year":response.meta["year"]})
            
class ECCV_Spider(Meta_Spider):
    name="ECCV"
    def parse_abs(self, response):
        item=response.meta['item']
        u=response.xpath("//a[contains(text(),'pdf')]/@href").extract_first()
        item["pdf_link"]=parse.urljoin(response.url,u)
        abstract=response.xpath("//div[@id='abstract']")[0].xpath("string(.)").extract_first().strip()
        item["abstract"]=abstract    
        yield item
    def get_item(self,response,paper,year):
        time.sleep(0.1)
        item=PaperItem()
        item["title"]=paper.xpath("string(.)").extract_first().strip()
        item["conference"]=self.name
        item["year"]=year
        tail=paper.xpath("@href").extract_first()
        link=parse.urljoin(response.url,tail)
        item["abstract_link"]=link
        return item,link
    def parser(self,response):
        eccv20=response.xpath("//dt[@class='ptitle']/a[contains(@href,'eccv_2020')]")
        eccv18=response.xpath("//dt[@class='ptitle']/a[contains(@href,'eccv_2018')]")
        for paper in eccv20:
            item,link=self.get_item(response,paper,2020)
            yield scrapy.Request(url=link,callback=self.parse_abs,meta={'item':item})
        for paper in eccv18:
            item,link=self.get_item(response,paper,2018)
            yield scrapy.Request(url=link,callback=self.parse_abs,meta={'item':item})
            
class ICCV_Spider(CVPR_Spider):
    name="ICCV"
class ICLR_Spider(scrapy.Spider):
    name="ICLR"
    
    def start_requests(self):
        recs=get_urls(self.name)
        for rec in recs:
            yield scrapy.Request(url=rec[3], callback=self.parser,
                                 meta={"conference":rec[1],"year":rec[2]})
    def parser(self,response):
        pass
class ICML_Spider(Meta_Spider):
    name="ICML"
    def parse_abs(self, response):
        item=response.meta['item']
        abstract=response.xpath("//div[@id='abstract']")[0].xpath("string(.)").extract_first().strip()
        item['abstract']=abstract
        yield item
    def parser(self, response):
        papers=response.css("div.paper")
        for paper in papers:
            item=PaperItem()
            item["title"]=paper.xpath("p[@class='title']/text()").extract_first()
            item["conference"]=response.meta["conference"]
            item["year"]=response.meta["year"]
            link=paper.xpath('p[@class="links"]/a[contains(text(),"abs")]/@href').extract_first()
            item["abstract_link"]=link
            item["pdf_link"]=paper.xpath('p[@class="links"]/a[contains(text(),"PDF")]/@href').extract_first()
            yield scrapy.Request(url=link,callback=self.parse_abs,meta={'item':item})

class IJCAI_Spider(Meta_Spider):
    name="IJCAI"
    def parse_abs(self,response):
        item=response.meta['item']
        item["abstract"]=response.xpath("//*[@id='block-system-main']/div/div/div[3]/div[1]")[0]\
            .xpath("string(.)").extract_first().strip()
        yield item
    def parser(self,response):
        papers=response.xpath("//div[@class='paper_wrapper']")
        for paper in papers:
            item=PaperItem()
            item["title"]=paper.xpath(".//div[@class='title']/text()").extract_first()
            item["conference"]=response.meta["conference"]
            item["year"]=response.meta["year"]
            tail=paper.xpath(".//div[@class='details']/a[contains(text(),'PDF')]/@href").extract_first()
            item["pdf_link"]=parse.urljoin(response.url,tail)
            tail=paper.xpath(".//div[@class='details']/a[contains(text(),'Details')]/@href").extract_first()
            item["abstract_link"]=parse.urljoin(response.url,tail)
            link=item["abstract_link"]
            yield scrapy.Request(url=link,callback=self.parse_abs,meta={'item':item})
            
class NIPS_Spider(Meta_Spider):
    name="NIPS"
    def parse_abs(self,response):
        item=response.meta['item']
        item["abstract"]=response.xpath("//div[@class='container-fluid']")\
            .xpath(".//h4[contains(text(),'Abstract')]")\
            .xpath("following-sibling::p[2]").extract_first()  
        tail=response.xpath("//a[contains(text(),'Paper')]/@href").extract_first()      
        item["pdf_link"]=parse.urljoin(response.url,tail)
        yield item
    def parser(self,response):
        papers=response.xpath("//div[@class='container-fluid']").xpath(".//li")
        for paper in papers:
            item=PaperItem()
            item["title"]=paper.xpath(".//a/text()").extract_first()
            item["conference"]=response.meta["conference"]
            item["year"]=response.meta["year"]
            tail=paper.xpath(".//a/@href").extract_first()
            item["abstract_link"]=parse.urljoin(response.url,tail)
            link=item["abstract_link"]
            yield scrapy.Request(url=link,callback=self.parse_abs,meta={'item':item})
