# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MkCrawlerItem(scrapy.Item):
    # 저장하고자 하는 카테고리 추가시 => 이름 = scrapy.Field()
    url= scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    pass