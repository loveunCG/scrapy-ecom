# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, MapCompose
4



class ShopifyPrice(Item):
    price = 0.0
    currency = 'USD'


class ShopifyVariant(Item):
    id = Field()
    title = Field()
    option1 = Field()
    option2 = Field()
    option3 = Field()
    sku = Field()
    requires_shipping = Field()
    taxable = Field()
    featured_image = Field()
    available = Field()
    name = Field()
    public_title = Field()
    options = Field()
    price = Field()
    weight = Field()
    compare_at_price = Field()
    inventory_quantity = Field()
    inventory_management = Field()
    inventory_policy = Field()
    barcode = Field()


class ShopifyItem(Item):
    # name = scrapy.Field()
    id = Field(output_processor=TakeFirst())
    title = Field(output_processor=TakeFirst())
    handle = Field(output_processor=TakeFirst())
    description = Field(output_processor=TakeFirst())
    published_at = Field(output_processor=TakeFirst())
    created_at = Field(output_processor=TakeFirst())
    vendor = Field(output_processor=TakeFirst())
    type = Field(output_processor=TakeFirst() )
    tags = Field()
    price = Field(output_processor=TakeFirst())
    price_min = Field(output_processor=TakeFirst())
    price_max = Field(output_processor=TakeFirst())
    available = Field(output_processor=TakeFirst())
    price_varies = Field(output_processor=TakeFirst())
    compare_at_price = Field(output_processor=TakeFirst())
    compare_at_price_min = Field(output_processor=TakeFirst())
    compare_at_price_max = Field(output_processor=TakeFirst())
    compare_at_price_varies = Field(output_processor=TakeFirst())
    variants = Field()
    images = Field()
    options = Field()

class ShopifyItemLoader(ItemLoader):
    default_item_class = ShopifyItem
    default_output_processor = Identity()


class KithItem(ShopifyItem):
    pass

""" processors  """
def cents_to_dollars(value):
    if isinstance(value, int):
        return float(value)/100