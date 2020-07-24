import scrapy
import logging

from ..items import ScrapeNewsItem


class NewsSpider(scrapy.Spider):

    name = 'news'
    custom_settings = {
        'DEPTH_LIMIT': 1
    }
    total_link_count = 1
    count = 1

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
            self.logger.error("\tscrapy crawl news -a domain='thehindu.com' -a start_url='https://www.thehindu.com' ")
            self.logger.error("\tscrapy crawl news -a domain='oneindia.com' -a start_url='https://www.oneindia.com' \n")

        super(NewsSpider, self).__init__(*args, **kwargs)

    def clean_text(self, cleaning_content):
        cleaned_text = ''
        for line in cleaning_content:
            striped_line = line.strip()
            if striped_line:
                cleaned_text = cleaned_text + " " + striped_line
        return cleaned_text.strip()

    def clean_scraped_urls(self, scraped_urls):
        scraped_urls_set = set()
        for url in scraped_urls:
            if url[0] == '/':
                url = self.start_urls[0] + url
                scraped_urls_set.add(url)
            elif url.startswith(self.start_urls[0]):
                scraped_urls_set.add(url)
        return scraped_urls_set

    def parse(self, response):

        scraped_urls = response.css('a::attr(href)').extract()
        scraped_urls_set = self.clean_scraped_urls(scraped_urls)

        url = response.request.url
        title = response.css('h1::text').extract()
        content = response.css('p::text').extract()

        if title and content:
            item = ScrapeNewsItem()
            item['URL'] = url
            item['Title'] = self.clean_text(title)
            item['Content'] = self.clean_text(content)
            yield item
        else:
            self.logger.info("Topic and Content not found in : {}".format(url))

        self.logger.info("Scraping on {}/{} : {}".format(self.count, str(self.total_link_count), url))
        self.logger.info("Links Found in this site :" + str(len(scraped_urls_set)))

        self.total_link_count += len(scraped_urls_set)
        self.count += 1

        yield from response.follow_all(scraped_urls_set, callback=self.parse)
