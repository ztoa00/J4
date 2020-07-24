# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from datetime import datetime

from .items import ScrapeNewsDataItem, ScrapeNewsNonDataItem

class ScrapeNewsPipeline:

    def open_spider(self, spider):
        now = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        self.filename1 = spider.allowed_domains[0] + str(now) + ".txt"
        self.file1 = open(self.filename1, 'w')
        self.filename2 = spider.allowed_domains[0] + "non_data_urls" + str(now) + ".txt"
        self.file2 = open(self.filename2, 'w')

    def close_spider(self, spider):
        self.file1.close()
        self.file2.close()

    def process_item(self, item, spider):

        if isinstance(item, ScrapeNewsDataItem):
            self.file1.write("URL : " + str(item['URL']) + "\n")
            self.file1.write("Title : " + str(item['Title']) + "\n")
            self.file1.write("Content : " + str(item['Content']) + "\n")
            self.file1.write("\n")

        if isinstance(item, ScrapeNewsNonDataItem):
            self.file2.write("URL : " + str(item['URL']) + "\n")
            self.file2.write("\n")

        return item
