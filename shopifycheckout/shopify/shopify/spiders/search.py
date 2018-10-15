# -*- coding: utf-8 -*-
import time
from shopify.spiders import ShopifySpider
from shopify.items import ShopifyItem, ShopifyPrice, ShopifyVariant, ShopifyItemLoader
from selenium.webdriver.common.by import By
from shopify.utils import is_empty, _strip, validate_url, TaskStatus
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from shopify.selenium import SeleniumSpiderMixin
from shopify.components.logic import search_product_by_keyword, \
    get_product_info, \
    add_cart, \
    go_to_checkout, \
    set_checkout_info,\
    check_out_with_paypal
from shopify.components.gateway import update_task_status
from shopify.components.scheduler import Scheduler
from scrapy import Request

class SearchSpider(SeleniumSpiderMixin, ShopifySpider):
    name = 'search'
    allowed_domains = ['kith.com']
    start_urls = ['http://kith.com/']


    def parse(self, response):
        task = Scheduler.__waiting_for_active_task__()
        url = validate_url(task.site)
        keyword = task.keyword
        self.driver.get(url)
        search_product_by_keyword(self.driver, keyword)
        product_url = get_product_info(self.driver)
        print('----', product_url)
        product_info = Request(url=product_url['url'],  callback=self.get_product_detail_info, dont_filter=True)
        isAvailable = add_cart(self.driver, product_url['url'], size=task.size)
        if isAvailable is False:
            update_task_status(task, TaskStatus.NOTAVAILABLE)
            return False
        else:
            update_task_status(task, TaskStatus.CHECKOUTING)
        go_to_checkout(self.driver)
        set_checkout_info(self.driver, checkout=task.checkout)
        time.sleep(10)

    def _fill_from_response(self, loader):
        pass

    def _checkout(self, response):
        pass

    def _extract_json_info(self, response):
        pass

    def _fill_from_json(self, response):
        pass

    def get_product_detail_info(self, response):
        product_name = response.css('div.product-single-header-upper').xpath('//h1/text()').extract()
        product_variant = response.css('div.product-single-header-upper > span.-variant::text').extract()
        product_currency = response.css('#priceCurrency::text')
        product_price = response.css('#ProductPrice::text').extract()
        product_cart_action = response.css('#AddToCartForm').extract()
        available = response.css('#AddToCartText::text').extract()
        product_details = response.css('div.product-single-details-rte::text').extract()
        product_img_urls = response.css('div.super-slider-slide').xpath('//img/@src').extract()
        shop_item = ShopifyItem(title=_strip(product_name[0]),
                                description=_strip(product_details[0]),
                                price=_strip(product_price[0]),
                                images=product_img_urls,
                                available=_strip(available[0]),
                                variants=_strip(product_variant[0]),
                                handle=_strip(product_cart_action[0]))
        print(product_img_urls)
        return shop_item
