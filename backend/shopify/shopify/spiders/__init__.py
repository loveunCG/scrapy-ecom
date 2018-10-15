import logging
from scrapy import Request, FormRequest, Spider
import re
import json
import os
from urllib.parse import urljoin

from abc import ABC, ABCMeta, abstractmethod
from backend.shopify.shopify.components import CrawlerComponent, monitor
from backend.shopify.shopify.settings import DEFAULT_REQUEST_HEADERS
from backend.shopify.shopify.items import ShopifyItem, ShopifyVariant, ShopifyPrice, ShopifyItemLoader
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class ShopifySpider(CrawlerComponent, Spider):
    name = "shopify"

    # allowed_domains = [""]
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__()
        super(CrawlerComponent, self).__init__(*args, **kwargs)
        self.product_link = kwargs.get('product_link')

        self.headers = DEFAULT_REQUEST_HEADERS

    def start_requests(self):
        headers = self.headers.copy()
        yield Request(self.product_link, callback=self._parse_product_page,
                      headers=headers)

    @abstractmethod
    def _extract_json_info(self, response):
        pass

    def _fill_item(self, loader):
        if loader.context.get('ajax'):
            return self._fill_from_json(loader)
        return self._fill_from_response(loader)

    @abstractmethod
    def _fill_from_json(self, loader):
        pass

    @abstractmethod
    def _fill_from_response(self, loader):
        pass

    def _parse_product_page(self, response):
        loader = ShopifyItemLoader(
            response=response,
            ajax=self._extract_json_info(response),
            )
        item = self._fill_item(loader)
        yield item

        return self._add_to_cart(response)

    @abstractmethod
    def _add_to_cart(self, response):
        pass

    @abstractmethod
    def _checkout(self, response):
        pass
