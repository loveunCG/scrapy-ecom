# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ShopifycheckoutSpider(CrawlSpider):
    name = 'shopifycheckout'

    # allowed_domains = ['https://google.com']
    # start_urls = ['http://https://google.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def __init__(self,*args,**kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        ShopifycheckoutSpider.rules = [
            Rule(LinkExtractor(unique=True),callback='parse_item'),
        ]
        super(ShopifycheckoutSpider,self).__init__(*args,**kwargs)

    


    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        i = {}
        i['url'] = response.url
        return i
