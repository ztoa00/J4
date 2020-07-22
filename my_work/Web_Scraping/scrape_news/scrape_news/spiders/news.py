import scrapy
# from bs4 import BeautifulSoup

from ..items import ScrapeNewsItem


class NewsSpider(scrapy.Spider):

    name = 'news'

    def __init__(self, *args, **kwargs):
        start_url = kwargs.pop('start_url', '')
        domain = kwargs.pop('domain', '')
        if domain and start_url:
            self.allowed_domains = [domain]
            self.start_urls = [start_url]
        else:
            print("Required 2 User Arguments.\nMissing Arguments : domain, start_url.\n"
                  "Usage is like : scrapy crawl news -a domain='thehindu.com' -a start_url='https://www.thehindu.com'")
        super(NewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        # For bs4 selector
        # soup = BeautifulSoup(response.text, 'html.parser')
        # scraped_urls = soup.find_all('a', href=True)

        # For Scrapy CSS Selector
        scraped_urls = response.css('a::attr(href)').extract()

        scraped_urls_set = set()
        for url in scraped_urls:
            if url[0] == '/':
                url = self.start_urls[0] + url
                scraped_urls_set.add(url)
            elif url.startswith(self.start_urls[0]):
                scraped_urls_set.add(url)
        yield from response.follow_all(scraped_urls_set, callback=self.parse_scraped_url)

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
        title = response.css('h1::text').extract()
        content = response.css('p::text').extract()
        if title and content:
            item['URL'] = url
            item['Title'] = self.clean_text(title)
            item['Content'] = self.clean_text(content)
            yield item
