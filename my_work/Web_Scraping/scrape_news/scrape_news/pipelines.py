# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import xlsxwriter


class ScrapeNewsPipeline:

    def open_spider(self, spider):
        self.filename = "domain" + ".txt"
        self.file = open(self.filename, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        self.file.write("URL : " + str(item['URL']) + "\n")
        self.file.write("Title : " + str(item['Title']) + "\n")
        self.file.write("Content : " + str(item['Content']) + "\n")
        self.file.write("\n")

        """
        self.file.write(str(item)+"\n")
        self.file.write("\n")
        """

        return item


"""
fname = "scraped_urls.xlsx"
workbook = xlsxwriter.Workbook(fname)
worksheet = workbook.add_worksheet()
for row,url in enumerate(scraped_urls):
    worksheet.write(row, 0, url)
workbook.close()    
"""
