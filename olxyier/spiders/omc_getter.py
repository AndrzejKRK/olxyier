import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field #произвольные поля
import sys
from scrapy import Selector

class OmcGetterSpider(scrapy.Spider):
    name = "omc_getter"
    allowed_domains = ['otomoto.pl']

    def start_requests(self):
        page_numbers = 516
        for item_id in range(page_numbers):
            print(f"ID: {item_id}")
            url = f"https://www.otomoto.pl/osobowe/ford?search%5Border%5D=created_at_first%3Adesc&page={item_id}"
            print(url)
            request = scrapy.Request(url, callback=self.parse)
            yield request
                
    def parse(self, response):
        print(f"URL: {response.url}")
        selector = Selector(response)
        table = selector.xpath('//section[@class="ooa-1rnjex3 ev7e6t817"]')

        for card_id, card in enumerate(table):
            item = Selector(text=card.extract())
            
            short = item.xpath('//p[@class="ev7e6t88 ooa-17thc3y er34gjf0"]/text()')[0].getall()[0]
            url = item.xpath('//h1[@class="ev7e6t89 ooa-1xvnx1e er34gjf0"]')[0].css('a::attr(href)')[0].get()
            thumnail = item.css('img')[0].css('img::attr(src)')[0].get()
            title = item.xpath('//h1[@class="ev7e6t89 ooa-1xvnx1e er34gjf0"]')[0].xpath('//a/text()')[0].get()
            price = item.xpath('//h3[@class="ev7e6t82 ooa-bz4efo er34gjf0"]/text()')[0].get()
        
            data = {
                'link': url,
                'title': title,
                'short': short,
                'thumnail': thumnail,
                'price': price
            }
            yield data