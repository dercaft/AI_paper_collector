
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
class AAAI_Spider(Meta_Spider):
    name="AAAI"
    
    def old_paper(self,response):
        item=response.meta['item']
        # abstract=response.xpath("//*[@id='abstract']/div/text()").extract_first().strip("\"")
        abstract=" ".join(response.xpath('//*[@id="abstract"]/div/text()').getall())
        item["abstract"]=abstract
        a=response.xpath("//*[@id='paper']/a/@href").extract_first()
        item["pdf_link"]=parse.urljoin(response.url,a)
        if dict_check(item):
            yield item
        else:
            raise BaseException("ERROR ITEM format{}".format(item.keys()))
        
    def new_paper(self,response):
        item=response.meta['item']
        abstract=response.xpath("//section[@class=contains(@class,'abstract')]/text()").getall()
        for i in range(len(abstract)):
            abstract[i]=abstract[i].strip("\"")
        abstract=" ".join(abstract)
        abstract=abstract.replace("Abstract", "").strip()
        item["abstract"]=abstract
        if dict_check(item):
            yield item
        else:
            raise BaseException("ERROR ITEM format{}".format(item.keys()))        
        pass
    def parse_page(self,response):
        papers=response.xpath("//*[@id='box6']/div/p[@class='left']")
        
        for paper in papers:
            time.sleep(0.05)
            item=PaperItem()
            link=paper.xpath("a/@href").extract_first()
            item["title"]=paper.xpath("a/text()").extract_first().strip()
            item["conference"]=response.meta["conference"]
            item["year"]=response.meta["year"]
            item["pdf_link"]=paper.xpath("a[text()='PDF']/@href").get()
            item["abstract_link"]=link
            yield scrapy.Request(url=link,callback=self.new_paper,meta={'item':item})
        pass
    def parser(self,response):
        year=response.meta["year"]
        if int(year) <2020:
            papers=response.xpath("//*[@id='box6']/div/p[@class='left']")
            for paper in papers:
                time.sleep(0.05)
                item=PaperItem()
                link=paper.xpath("a/@href").get()
                item["title"]=paper.xpath("a/text()").get()
                item["conference"]=response.meta["conference"]
                item["year"]=response.meta["year"]
                item["abstract_link"]=link
                pdf_link=paper.xpath("a[text()='PDF']/@href").get()
                # print("PDFIS: ",pdf_link)
                if int(year)!=2018 and pdf_link: item["pdf_link"]=pdf_link
                if int(year)==2018:
                    link=link.replace("view", "viewPaper")
                    yield scrapy.Request(url=link,callback=self.old_paper,meta={'item':item})
                else:
                    yield scrapy.Request(url=link,callback=self.new_paper,meta={'item':item})
                pass
        else:
            pages=response.xpath("//*[@id='box6']/div/ul/li")
            for page in pages:
                u=page.xpath("a/@href").get()
                link=parse.urljoin(response.url,u)
                yield scrapy.Request(url=link,callback=self.parse_page,meta=response.meta)
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
    '''
    SAME WITH CVPR
    '''
    name="ICCV"
class ICLR_Spider(Meta_Spider):
    name="ICLR"
    INCLUDE_TAB={
        "2018":["accepted-oral-papers","accepted-poster-papers","workshop-papers"],
        "2019":["accepted-oral-papers","accepted-poster-papers"],
        "2020":["accept-poster","accept-spotlight","accept-talk"],
        "2021":["oral-presentations","spotlight-presentations","poster-presentations"],
    }
    def parser(self,response):
        import time
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.wait import WebDriverWait
        from urllib import parse
        ROOT=response.url
        # INCLUDE=["oral-presentations","spotlight-presentations","poster-presentations"]
        INCLUDE=self.INCLUDE_TAB[response.meta["year"]]
        # ROOT='https://openreview.net/group?id=ICLR.cc/2021/Conference'
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})

        # driver = webdriver.Edge(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedgedriver.exe') # ,options=options)
        driver = webdriver.Chrome(executable_path=r'C:/Program Files/Google/Chrome/Application/chromedriver.exe',options=options)
        driver.get(ROOT)
        driver.maximize_window()
        # cond = EC.presence_of_element_located((By.XPATH, '//*[@id="oral-presentations"]'))
        # cond = EC.presence_of_element_located((By.XPATH, '//*[@class="tabs-container"]'))
        cond = EC.presence_of_element_located((By.XPATH, '//*[@id="notes"]'))
        WebDriverWait(driver, 60).until(cond)
        # page = driver.page_source
        # print(page)
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//ul[@role="tablist"]/li/a')))
        tabs = driver.find_elements_by_xpath('//ul[@role="tablist"]/li/a')
        # print("TABS: ",len(tabs))
        for i,tab in enumerate(tabs):
            # old=tab
            # tab=tab.find_element_by_xpath('./a')
            # print("TAB: ",tab)
            link=tab.get_attribute("href")
            name=link.split("#")[-1]
            print("*"*20)
            print(i,type(tab))
            print(link)
            print(name)
            if not name in INCLUDE: continue
            driver.execute_script("var q=document.documentElement.scrollTop=0")
            if tab.is_enabled() and tab.is_displayed(): 
                tab.click()
            paper_path='//*[@id="{}"]/ul/li'.format(name)
            # 这里需要额外的加载时间来等列表全部加载完毕，直接提取会出现没有这个列表的问题。
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, paper_path)))
            time.sleep(0.2)
            papers=driver.find_elements_by_xpath(paper_path)
            print("LENGTH: ",len(papers))
            print("*"*20)
            for i,paper in enumerate(papers):
                # if i>2: break
                title=paper.find_element_by_xpath("./h4/a[1]").text.strip()
                abs=paper.find_element_by_xpath("./h4/a[1]").get_attribute("href")
                abstract_link=parse.urljoin(ROOT,abs)
                pdf=paper.find_element_by_xpath("./h4/a[2]").get_attribute("href")
                pdf_link=parse.urljoin(ROOT,pdf)
                target=paper.find_element_by_xpath("./a")
                driver.execute_script("arguments[0].scrollIntoView();", target)
                driver.execute_script("arguments[0].click();", target)
                # target.click()
                time.sleep(0.5)
                items = paper.find_elements_by_xpath('.//li')
                keyword = ''.join([x.text for x in items if 'Keywords' in x.text])
                abstract = ''.join([x.text for x in items if 'Abstract' in x.text])
                keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ').replace('Keywords: ', '')
                abstract = abstract.strip().replace('\t', ' ').replace('\n', ' ').replace('Abstract: ', '')
                
                item=PaperItem()
                item["title"]=title
                item["conference"]=self.name
                item["year"]=response.meta["year"]
                item["abstract"]=abstract
                item["abstract_link"]=abstract_link
                item["pdf_link"]=pdf_link
                yield item
                pass
        driver.close()        
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
        # item["abstract"]=response.xpath("//div[@class='container-fluid']")\
        #     .xpath(".//h4[contains(text(),'Abstract')]")\
        #     .xpath("following-sibling::p[2]").extract_first()  
        # item["abstract"]=response.xpath("/html/body/div[2]/div/p[4]/text()")
        ps=response.xpath("//div[@class='col']/p/text()").getall()
        ave=sum([len(i) for i in ps])/len(ps)
        abss=[i for i in ps if len(i)>ave]
        item["abstract"]=" ".join(abss)
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
