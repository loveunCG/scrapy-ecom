import logging
from scrapy import Request, FormRequest, Spider
import re
import json
import os
from urllib.parse import urljoin
import time
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException, NoSuchElementException

from abc import ABC, ABCMeta, abstractmethod
from shopify.components import CrawlerComponent, monitor
from shopify.settings import DEFAULT_REQUEST_HEADERS
from shopify.items import ShopifyItem, ShopifyVariant, ShopifyPrice, ShopifyItemLoader
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class ShopifySpider(CrawlerComponent, Spider):
    name = None

    # allowed_domains = [""]
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__()
        super(CrawlerComponent, self).__init__(*args, **kwargs)
        self.product_link = kwargs.get('product_link')
        self.headers = DEFAULT_REQUEST_HEADERS

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
    def _checkout(self, response):
        pass
