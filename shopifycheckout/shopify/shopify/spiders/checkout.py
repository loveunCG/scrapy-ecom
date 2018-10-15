# -*- coding: utf-8 -*-
from shopify.spiders import ShopifySpider
from shopify.items import ShopifyItem, ShopifyPrice, ShopifyVariant, ShopifyItemLoader
from selenium.webdriver.common.by import By
from shopify.utils import is_empty, _strip
from shopify.components.gateway import get_profile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from shopify.components.logic import search_product_by_keyword, get_product_info, add_cart, go_to_checkout
from shopify.selenium import SeleniumSpiderMixin

IDLE_INTERVAL_IN_SECONDS = 5


class CheckoutSpider(SeleniumSpiderMixin, ShopifySpider):
    name = 'checkout'
    allowed_domains = ['kith.com']
    start_urls = ['https://kith.com/']

    def parse(self, response):
        self.driver.get('https://kith.com/')
        # for search by keyboard
        # search_product_by_keyword(self.driver, 'sport')
        # time.sleep(IDLE_INTERVAL_IN_SECONDS)
        # product_urls = get_product_info(self.driver)
        # product_info = []
        # if product_urls is not None:
        #     for product_url in product_urls:
        #         print('-------', product_url, '-----------')
        #         product_info.append(Request(url=product_url['url'],  callback=self.get_product_detail_info, dont_filter=True,))
        #         add_cart(self.driver, product_url['url'])
        url = 'https://sq-develop.tech/DigitalHealthFellow.html'

        isavailable = add_cart(self.driver, url)
        go_to_checkout(self.driver)

        cart_info = get_cart_list_info(self.driver)
        is_checkout = set_checkout_info(self.driver)
        return cart_info
        # return Request(url='https://kith.com/products
        # /greg-lauren-50-50-sky-cowboy-flannel-studio-shirt-navy-light-blue',
        #
        #         callback=self.get_product_detail_info, dont_filter=True,)

    def closed(self):
        self.driver.close()
        pass

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
        item = loader.load_item()
        return item

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

    def _fill_from_response(self, loader):
        pass

    def _add_to_cart(self, response):
        pass

    def _checkout(self, response):
        pass

    def _extract_json_info(self, response):
        pass

    def _fill_from_json(self, response):
        pass


def get_cart_list_info(driver):
        cart_url = driver.current_url
        wait = WebDriverWait(driver, 30)
        product_cart_lists = wait.until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "table.product-table > tbody")))
        product_lists =product_cart_lists.find_elements_by_tag_name('tr')
        cart_lists = []
        for _list in product_lists:
            try:
                product__description = _list.find_element_by_class_name('product__description').text
                product__price = _list.find_element_by_class_name('product__price').text
                product__quantity = _list.find_element_by_class_name('product__quantity').text
                cart_lists.append({"description": product__description,
                                   "price": product__price,
                                   "quantity": product__quantity})
            except NoSuchElementException as e:
                print(e)
                pass
        total_price = driver.find_element_by_xpath('//span[@class="payment-due__price"]').text
        return {"total_price": total_price, "cart_list": cart_lists, "cart_url": cart_url}


def set_checkout_info(driver, url=None, **kwargs):
    check_out_email = driver.find_element_by_id('checkout_email')
    first_name = driver.find_element_by_id('checkout_shipping_address_first_name')
    last_name = driver.find_element_by_id('checkout_shipping_address_last_name')
    address1 = driver.find_element_by_id('checkout_shipping_address_address1')
    address2 = driver.find_element_by_id('checkout_shipping_address_address2')
    city = driver.find_element_by_id('checkout_shipping_address_city')
    post_code = driver.find_element_by_id('checkout_shipping_address_zip')
    phone_number = driver.find_element_by_id('checkout_shipping_address_phone')
    continue_button = driver.find_element_by_class_name('step__footer__continue-btn')
    first_name.send_keys('loveuncg')
    last_name.send_keys('loveuncg')
    address1.send_keys('loveuncg')
    address2.send_keys('loveuncg')
    phone_number.send_keys('1564324658')
    post_code.send_keys('110000')
    city.send_keys('liao ning')
    city.send_keys('liao ning')

    check_out_email.send_keys('loveun1988@outlook.com')
    continue_button.click()
    print('-------loading-------')
    wait = WebDriverWait(driver, 30)
    next_button = wait.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, "button.step__footer__continue-btn")))
    shipping_price = driver.find_element_by_class_name('radio__label__accessory').text
    shipping_method = driver.find_element_by_class_name('radio__label__primary').text
    next_button.click()
    wait = WebDriverWait(driver, 30)
    window_before = None
    while not window_before:
        window_before = driver.current_window_handle
    next_button = wait.until(ec.visibility_of_element_located(
         (By.CSS_SELECTOR, "button.step__footer__continue-btn")))
    next_button.click()
    check_out_with_paypal(driver, window_before)
    time.sleep(20)
    return True


def check_out_with_paypal(driver, window_before):
    paypal_window_handle = None
    while not paypal_window_handle:
        for handle in driver.window_handles:
            if handle != window_before:
                paypal_window_handle = handle
                break

    driver.switch_to.window(paypal_window_handle)
    wait = WebDriverWait(driver, 30)
    login_btn = wait.until(ec.visibility_of_element_located(
        (By.ID, "btnLogin")))
    email = driver.find_element_by_id('email')
    email.clear()
    email.send_keys('chrlmoonstar@gmail.com')
    password = driver.find_element_by_id('password').send_keys('shddkshdvkr113')
    login_btn.click()
    driver.switch_to.window(window_before)

    return True
