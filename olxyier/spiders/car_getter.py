import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field #произвольные поля
import sys
from scrapy import Selector

class CarGetterSpider(scrapy.Spider):
    name = "car_getter"
    allowed_domains = ['olx.pl', 'otomoto.pl']
    start_urls = ['https://www.olx.pl/motoryzacja/samochody/ford']

    # This method must be in the spider, 
    # and will be automatically called by the crawl command.
    # def start_requests(self):
    #     self.index = 0
    #     urls = ['https://www.olx.pl/motoryzacja/samochody',]
    #     for url in urls:
    #         # We make a request to each url and call the parse function on the http response.
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(10*"**")

        selector = Selector(response)
        table = selector.xpath('//*[@data-cy="l-card"]')

        for record_id, record in enumerate(table):
            link = record.css('a.css-rc5s2u::attr(href)').get()
            title = record.css('div.css-u2ayx9').css('h6::text').get()
            price = record.css('div.css-u2ayx9').css('p::text').get()

            data = {
                'main_url': response.url,
                'link': link,
                'title': title,
                'price': price
            }
            print(data)
            yield data

        next_page = selector.xpath('//*[@data-cy="pagination-forward"]/@href').extract()
        print("Next page: {}".format(next_page))

        if len(next_page) > 0 :
            yield response.follow(next_page[-1], self.parse)
        print("Finish")