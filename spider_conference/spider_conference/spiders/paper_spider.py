import scrapy

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
    
    def start_requests(self):
        urls=[
        ]
        pass
    def parser(self,response):
        papers=response.css("div.paper")
        for paper in papers:
            title=paper.css("p.title::text")
            
        pass
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
