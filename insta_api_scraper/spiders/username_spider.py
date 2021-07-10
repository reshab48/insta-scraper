import scrapy
from scrapy.selector import Selector

from insta_api_scraper.items import UsernameItem

class UsernameSpider(scrapy.Spider):
    name = 'username'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'insta_api_scraper.middlewares.InstaApiScraperDownloaderMiddleware': 400
        }
    }

    def start_requests(self):
        countries = ['united-states']

        for country in countries:
            for i in range(10):
                yield scrapy.Request(
                    f'https://starngage.com/app/global/influencer/ranking/{country}?page={i+1}',
                    callback=self.parse_handle
                )

    def parse_handle(self, response, **kwargs):
        for row in response.css('table tbody tr').getall():
            handle = Selector(text=Selector(text=row).css('td').getall()[2]).css('a::text').get()
            influencer_handle = handle.replace('@', '')
            yield UsernameItem({'username': influencer_handle})