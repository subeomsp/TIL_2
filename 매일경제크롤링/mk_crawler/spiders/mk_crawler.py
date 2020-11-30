import scrapy
from mk_crawler.items import MkCrawlerItem
import re


class MkSpider(scrapy.Spider):
    name = "mk_crawler"
    
    def start_requests(self):
       item = MkCrawlerItem()
       #카테고리 = 경제 / 기업 / 사회 / 국제 / 부동산 / 증권 / 정치 / IT·과학 / 문화 
       category_list = ['economy','business', 'society', 'world', 'realestate', 'stock', 'politics', 'it', 'culture']
       for category in category_list:
           #pages 를 조정해 크롤링할 페이지 지정
            for page in range(10):
                urls = [
                        "https://www.mk.co.kr/news/{}/?page={}".format(category, page)
                    ]
                for url in urls:
                    yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        current_url = response.url
        #기업 카테고리에서 url이 담긴 tag가 다른 문제 해결
        if 'business' in current_url: 
            article_urls =  response.xpath('//*[@id="container_left"]/div[3]/dl/dt/a/@href').extract()
        else:
            article_urls =  response.xpath('//*[@id="container_left"]/div[1]/dl/dt/a/@href').extract()    
        
        for url in article_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = MkCrawlerItem()
        #url 
        item['url'] = response.url 
        
        #기사 
        item['content'] = response.xpath(
            '//*[@id="article_body"]/div').getall()

        #제목
        item['title'] = response.xpath(
            '//*[@id="top_header"]/div/div/h1/text()').extract()
        
        #기사 작성일
        item['date'] = response.xpath(
            '//*[@id="top_header"]/div/div/div[1]/ul/li[2]/text()').get()
            
        yield item
