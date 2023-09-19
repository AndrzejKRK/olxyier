import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field #произвольные поля
import sys
from scrapy import Selector

from tqdm import tqdm
import json

def read_manifest(path):
    manifest = []
    with open(path, 'r') as f:
        for line in tqdm(f, desc="Reading manifest data"):
            line = line.replace("\n", "")
            if line[len(line)-1] == ",":
                line = line[:len(line)-1]
            print(line)
            try:
                data = json.loads(line)
                manifest.append(data)
            except:
                pass
    return manifest

class OtomotoGetterSpider(scrapy.Spider):
    name = "otomoto_getter"
    allowed_domains = ['otomoto.pl']

    def __init__(self):
        path = 'otomoto.json'
        #path_created = r'ford_desc.json'
        self.data = read_manifest(path)
        #self.already_processed = [i['link'] for i in read_manifest(path_created)]

        print(f"LENGHT OF LINKS: {len(self.data)}")


    def start_requests(self):
        for item_id, item in enumerate(self.data):
            if 'otomoto.pl' in item['link']:
                # if item['link'] in self.already_processed:
                #     print(20 * "&$")
                #     continue
                print(f"ACTUALU is {item_id}" )
                request = scrapy.Request(item['link'], callback=self.parse)
                request.meta['item'] = item
                yield request


    def parse(self, response):
        print(10*"**")

        selector = Selector(response)

        table = selector.xpath('//*[@id="parameters"]/ul/li')

        ad_id_inst = selector.xpath('//*[@id="ad_id"]/text()')
        ad_id = ad_id_inst[0].get() if len(ad_id_inst) > 0 else "not_found"

        date = selector.xpath('//*[@id="siteWrap"]/main/div[1]/div[1]/div[1]/div/div[6]/div/span[1]/span/text()').get()

        features = selector.xpath('//*[@id="siteWrap"]/main/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/div/ul/li/text()')
        list_of_equipments = []
        for item in features:

            text = item.get()
            if text != None:
                text.replace("\n", " ")
                text = ' '.join(text.split())

            if text != None and text != '':
                list_of_equipments.append(text)
                
        description = selector.xpath('//*[@id="description"]/div/text()')[0].get()
        if description != None:
            description.replace("\n", " ")
            description = ' '.join(description.split())

        parameters = {}
        
        for record_id, record in enumerate(table):
            param_name = record.css('span::text').get()

            text = record.css('div.offer-params__value::text').get()

            if text != None:
                text.replace("\n", " ")
                text = ' '.join(text.split())

            if text == '' or  text == None:
                text = record.css('a.offer-params__link::text').get()

            if text != None:
                text.replace("\n", " ")
                text = ' '.join(text.split())

            parameters.update({
                param_name: text
            })

        
        data = {
            'main_url': response.url,
            'parameters': parameters,
            'equipments':list_of_equipments,
            'description': description,
            'date': date,
            'id': ad_id

        }
        print(data)
        yield data

        # next_page = selector.xpath('//*[@data-cy="pagination-forward"]/@href').extract()
        # print("Next page: {}".format(next_page))

        # if len(next_page) > 0 :
        #     yield response.follow(next_page[-1], self.parse)
        # print("Finish")