import scrapy
from screlium.items import ScreliumItem
import re
import pandas as pd
from selenium import webdriver
import time
from scrapy.selector import Selector

class MaplestorySpider(scrapy.Spider):
    name = "screlium"
    start_urls = ['https://new.reddit.com/r/wallstreetbets/search/?q=-flair%3AMeme%20-flair%3ASatire%20-flair%3AShitpost&restrict_sr=1&t=day&sort=hot']
    
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('driver')

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(15)

        for i in range(20):
            self.browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
            time.sleep(5)

        # last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        # while True:
        #     driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
        #     time.sleep(5)
        #     new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        #     if new_page_height == last_page_height:
        #         break

        #     last_page_height = new_page_height

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        base_url = 'https://new.reddit.com'
        queries = selector.css('div.y8HYJ-y_lTUHkQIc1mdCq._2INHSNB8V5eaWp4P0rY_mE a::attr(href)')
        for query in queries:
            url = base_url + query.getall()[0] 
            yield scrapy.Request(url=url, callback=self.parse_post)

    def parse_post(self, response):
        item = ScreliumItem()
        title = response.xpath('//*/div/div[3]/div[1]/div/h1/text()').get()
        item['title'] = title

        content = response.xpath('//*/div/div[5]/div/p/text()').getall()
        item['content'] = content

        yield item 
