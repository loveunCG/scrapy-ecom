from backend.shopify.shopify.spiders import ShopifySpider
from backend.shopify.shopify.items import ShopifyItem, ShopifyPrice, ShopifyVariant, ShopifyItemLoader
from backend.shopify.shopify.utils import is_empty
#from backend.shopify.shopify.components import monitor
import re
import json
import traceback
from scrapy import Request, FormRequest, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

def failure_monitor(method):
    def wrapper(crawler, response):
        try:
            return method(crawler, response)
        except:
            crawler.log.debug(traceback.format_exc())

    return wrapper

class KithSpider(ShopifySpider):
    name = "kith"
    allowed_domains = ["https://kith.com", "kith.com"]


    @failure_monitor
    def _extract_json_info(self, response):
        info_expr = re.compile(br'(?<=var product =).+?(?=;)',
                               re.MULTILINE | re.DOTALL)
        info = re.search(info_expr, response.body)
        return json.loads(info.group())


    def _fill_from_json(self, loader):
        item = loader.context['item']
        product = loader.context['ajax']
        loader.replace_value('id', product.get('id'))
        loader.replace_value('title', product.get('title'))
        loader.replace_value('handle', product.get('handle'))
        loader.replace_value('description', product.get('description'))
        loader.replace_value('published_at', product.get('published_at'))
        loader.replace_value('created_at', product.get('created_at'))
        loader.replace_value('vendor', product.get('vendor'))
        loader.replace_value('type', product.get('type'))
        loader.replace_value('tags', product.get('tags'))
        loader.replace_value('price', product.get('price'))
        loader.replace_value('price_min', product.get('price_min'))
        loader.replace_value('price_max', product.get('price_max'))
        loader.replace_value('available', product.get('available'))
        loader.replace_value('price_varies', product.get('price_varies'))
        loader.replace_value('compare_at_price', product.get('compare_at_price'))
        loader.replace_value('compare_at_price_min', product.get('compare_at_price_min'))
        loader.replace_value('compare_at_price_max', product.get('compare_at_price_max'))
        loader.replace_value('compare_at_price_varies', product.get('compare_at_price_varies'))
        loader.replace_value('variants', product.get('variants'))
        loader.replace_value('images', product.get('images'))
        loader.replace_value('options', product.get('options'))
        # loader.add_value(None, product)

        item = loader.load_item()

        return item

    def _fill_from_response(self, loader):
        pass


    def _add_to_cart(self, response):
        pass

    def _checkout(self, response):
        pass