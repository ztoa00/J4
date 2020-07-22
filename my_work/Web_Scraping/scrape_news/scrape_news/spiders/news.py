import scrapy
# from bs4 import BeautifulSoup

from ..items import ScrapeNewsItem


class NewsSpider(scrapy.Spider):

    name = 'news'
    custom_settings = {
        'DEPTH_LIMIT': 2
    }
    total_link_count = 1
    count = 1

    def __init__(self, *args, **kwargs):

        start_url = kwargs.pop('start_url', '')
        domain = kwargs.pop('domain', '')
        if domain and start_url:
            self.allowed_domains = [domain]
            self.start_urls = [start_url]
        else:
            print("Usage")
            print("======")
            print("\tRequired Arguments : 2 ")
            print("\tMissing Arguments : domain, start_url.")
            print("\tUsage is like : ")
            print()
            print("\t\tscrapy crawl news -a domain='thehindu.com' -a start_url='https://www.thehindu.com' ")
            print("\t\tscrapy crawl news -a domain='oneindia.com' -a start_url='https://www.oneindia.com' ")
            print()

        super(NewsSpider, self).__init__(*args, **kwargs)

    def clean_text(self, text):
        cleaned_text = ''
        for line in text:
            line = line.strip()
            if line:
                cleaned_text = cleaned_text + " " + line
        return cleaned_text.strip()

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

        url = response.request.url
        title = response.css('h1::text').extract()
        content = response.css('p::text').extract()

        if title and content:
            item = ScrapeNewsItem()
            item['URL'] = url
            item['Title'] = self.clean_text(title)
            item['Content'] = self.clean_text(content)
            yield item

        print("Scraping on {}/{} : {}".format(self.count, str(self.total_link_count), url))
        print("Links Found in this site :" + str(len(scraped_urls_set)))

        self.total_link_count += len(scraped_urls_set)
        self.count += 1

        yield from response.follow_all(scraped_urls_set, callback=self.parse)
