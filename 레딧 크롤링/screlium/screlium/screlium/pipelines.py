# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

class ScreliumPipeline:
    def __init__(self):
        #open("이름", "wb") 에서 이름을 수정하여 저장하고자 하는 파일 이름 변경
        self.file = open("reddit.csv", "wb")
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
