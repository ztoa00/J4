# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from itemadapter import ItemAdapter

from .items import ScrapeBlogsItem


class ScrapeBlogsPipeline:
    def open_spider(self, spider):
        now = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        self.filename = spider.allowed_domains[0] + str(now) + ".txt"
        self.file = open(self.filename, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        if isinstance(item, ScrapeBlogsItem):
            self.file.write("URL : " + str(item['url']) + "\n")
            self.file.write("Title : " + str(item['title']) + "\n")
            self.file.write("Upload Date : " + str(item['upload_date']) + "\n")
            self.file.write("Update Date : " + str(item['update_date']) + "\n")
            self.file.write("\n")

        return item
