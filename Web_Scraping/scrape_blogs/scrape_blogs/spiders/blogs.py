import scrapy
import logging

from ..items import ScrapeBlogsItem


class BlogsSpider(scrapy.Spider):

    name = 'blogs'
    allowed_domains = ['']
    start_urls = ['']

    page_number = 1
    logger = logging.getLogger()

    def __init__(self, *args, **kwargs):

        start_url = kwargs.pop('start_url', '')
        domain = kwargs.pop('domain', '')
        if domain and start_url:
            self.allowed_domains = [domain]
            self.start_urls = [start_url]
        else:
            self.logger.error("Usage")
            self.logger.error("======")
            self.logger.error("Required Arguments : 2 ")
            self.logger.error("Missing Arguments : domain, start_url.")
            self.logger.error("Usage is like : ")
            self.logger.error("\tscrapy crawl blogs -a domain='moneyexcel.com' -a start_url='https://moneyexcel.com' ")
            self.logger.error("\tscrapy crawl blogs -a domain='marketcalls.com' -a start_url='https://www.marketcalls.in' \n")

        super(BlogsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        articles = response.css('article').css('header')
        if len(articles) > 1:
            for article in articles:
                h1 = article.css('h1')
                h2 = article.css('h2')
                if h1:
                    url = h1.css('a::attr(href)').extract()
                    title = h1.css('h2').css('a::text').extract()
                else:
                    url = h2.css('a::attr(href)').extract()
                    title = h2.css('h2').css('a::text').extract()
                update_date = article.css('.updated::text').extract()
                upload_date = article.css('time').css('::text').extract()

                item = ScrapeBlogsItem()
                item['url'] = url
                item['title'] = title
                item['upload_date'] = upload_date
                item['update_date'] = update_date
                yield item

            self.logger.info("Scraping on : {}/page/{}".format(self.start_urls[0], self.page_number))

            self.page_number += 1
            if self.start_urls[0].endswith('/'):
                next_url = self.start_urls[0] + "page/{}".format(self.page_number)
            else:
                next_url = self.start_urls[0] + "/page/{}".format(self.page_number)

            yield response.follow(next_url, callback=self.parse)
