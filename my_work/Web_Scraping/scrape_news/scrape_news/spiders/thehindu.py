import scrapy

from ..items import ScrapeNewsItem


class TheHinduSpider(scrapy.Spider):
    name = 'thehindu'
    allowed_domains = ['thehindu.com']
    start_urls = ['https://www.thehindu.com/news/']

    def parse(self, response):

        scraped_urls = set()

        a_tag_urls = response.css('a[href*=www\.thehindu\.com]::attr(href)').extract()
        for url in a_tag_urls:
            if url not in scraped_urls:
                scraped_urls.add(url)

        yield from response.follow_all(scraped_urls, callback=self.parse_scraped_url)

    def clean_text(self, text):

        cleaned_text = ''
        for line in text:
            line = line.strip()
            if line:
                cleaned_text = cleaned_text + " " + line

        return cleaned_text.strip()

    def parse_scraped_url(self, response):

        item = ScrapeNewsItem()

        url = response.request.url
        title = response.css('.title::text').extract()
        content = response.css('.intro+ div p').css('::text').extract()

        if title and content:

            item['URL'] = url
            item['Title'] = self.clean_text(title)
            item['Content'] = self.clean_text(content)

            yield item
