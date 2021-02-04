import scrapy
from reddit.items import RedditItem
import re
import pandas as pd
from selenium import webdriver
import time
from scrapy.selector import Selector
from datetime import datetime, timedelta

class RedditSpider(scrapy.Spider):
    name = "reddit"
    start_urls = ['https://new.reddit.com/r/wallstreetbets/top/']
    
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome(driver) #드라이버 위치

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(15)
        '''
        꼭 전체 스크롤을 내리고 난 뒤에 정보를 불러와야 할까?
        '''

        #스크롤
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
            time.sleep(5)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            if new_page_height == last_page_height:
                break

            last_page_height = new_page_height

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)

        #포스팅 시간을 기점으로 크롤링 할 게시물 분류 - 24시간 이내의 게시글만
        posts = selector.css('div._1poyrkZ7g36PawDueRza-J._11R7M_VOgKO1RJyRSRErT3')
        for post in posts:
            posting_time = post.css('div._3AStxql1mQsrZuUIFP9xSg.nU4Je7n-eSXStTBAPMYt8 a::text').getall()[1]
            if 'hours' in posting_time:
                base_url = 'https://new.reddit.com'
                query = post.css('div.y8HYJ-y_lTUHkQIc1mdCq._2INHSNB8V5eaWp4P0rY_mE a::attr(href)').get()
                url = base_url + query 
                yield scrapy.Request(url=url, callback=self.parse_post)
            else:
                pass

    def parse_post(self, response):
        item = RedditItem()
        title = response.xpath('//*/div/div[3]/div[1]/div/h1/text()').get()
        item['title'] = title

        content = response.xpath('//*/div/div[5]/div/p/text()').getall()
        item['content'] = content

        #크롤링 시점으로부터 시간 차이를 통해 포스팅 날짜 파싱 
        scrap_time = datetime.now()
        time_gap = response.css('div._3AStxql1mQsrZuUIFP9xSg.nU4Je7n-eSXStTBAPMYt8 a::text').get()
        time_gap = int(time_gap.split()[0])
        posting_time = scrap_time - timedelta(hours=time_gap)
        item['posting_time'] = posting_time.strftime('%Y%m%d')
        yield item 
