import time
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, \
    StaleElementReferenceException, \
    WebDriverException, \
    NoSuchElementException
from shopify.components.scheduler import Scheduler
from selenium.webdriver.support.ui import Select

def get_cart_list_info(driver):
    cart_url = driver.current_url
    wait = WebDriverWait(driver, 30)
    product_cart_lists = wait.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, "table.product-table > tbody")))
    product_lists = product_cart_lists.find_elements_by_tag_name('tr')
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
    billing_info = kwargs.get('checkout', None)
    check_out_email = driver.find_element_by_id('checkout_email')
    first_name = driver.find_element_by_id('checkout_shipping_address_first_name')
    last_name = driver.find_element_by_id('checkout_shipping_address_last_name')
    address1 = driver.find_element_by_id('checkout_shipping_address_address1')
    address2 = driver.find_element_by_id('checkout_shipping_address_address2')
    city = driver.find_element_by_id('checkout_shipping_address_city')
    post_code = driver.find_element_by_id('checkout_shipping_address_zip')
    phone_number = driver.find_element_by_id('checkout_shipping_address_phone')
    continue_button = driver.find_element_by_class_name('step__footer__continue-btn')
    first_name.send_keys(billing_info.first_name)
    last_name.send_keys(billing_info.last_name)
    address1.send_keys(billing_info.address1)
    address2.send_keys(billing_info.address2)
    phone_number.send_keys(billing_info.phone)
    post_code.send_keys(billing_info.zipcode)
    city.send_keys(billing_info.city)
    check_out_email.send_keys(billing_info.email)
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
    check_out_with_paypal(driver, window_before, checkout=billing_info)
    time.sleep(20)
    return True


def check_out_with_paypal(driver, window_before, **kwargs):
    billing_info = kwargs.get('checkout', None)
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
    email.send_keys(billing_info.paypal_email)
    password = driver.find_element_by_id('password').send_keys(billing_info.paypal_pw)
    login_btn.click()
    driver.switch_to.window(window_before)
    return True


def get_search_input(driver):
    return driver.find_element_by_id("search_input")


def resolve_cookie(driver):
    try:
        appifyCookie = driver.find_element_by_id('appifyCookie')
        appifyCookie.click()
    except NoSuchElementException:
        return driver
    return driver


def search_product_by_keyword(driver, keyword):
    driver = resolve_cookie(driver)
    element = get_search_input(driver)
    element.click()
    element.send_keys(keyword)
    wait = WebDriverWait(driver, 30)
    with open('shopify/javascript/search_input.js') as f:
        contents = f.read()
    driver.execute_script(contents)
    view_product_link_button = wait.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, "li.snize-ac-odd")))
    try:
        driver.execute_script(contents)
        view_product_link_button.click()
    except Exception as e:
        task = Scheduler.__waiting_for_no_result__()
        search_product_by_keyword(driver, task.keyword)

    return True


def search_all_product_by_keyword(driver, keyword):
    driver = resolve_cookie(driver)
    element = get_search_input(driver)
    element.click()
    element.send_keys(keyword)
    wait = WebDriverWait(driver, 30)
    with open('shopify/javascript/search_input.js') as f:
        contents = f.read()
    driver.execute_script(contents)
    view_all_link_button = wait.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, "li.snize-view-all-link")))
    try:
        driver.execute_script(contents)
        view_all_link_button.click()
    except Exception as e:
        print('error:', e)
    return driver


def get_product_info(driver):
    try:
        ul = driver.find_element_by_class_name('snize-search-results-content')
        li = ul.find_element_by_class_name('snize-product')
        product_link = li.find_element_by_class_name('snize-view-link')
        url = product_link.get_attribute('href')
        product_url = {'url': url}
    except Exception as e:
        product_url = {'url': ''}
    return product_url


def get_products_info(driver):
    ul = driver.find_element_by_class_name('snize-search-results-content')
    lis = ul.find_elements_by_class_name('snize-product')
    product_urls = []
    for li in lis:
        product_link = li.find_element_by_class_name('snize-view-link')
        url = product_link.get_attribute('href')
        # productLink = ProductLink(url=url)
        product_urls.append({'url': url})
        # yield productLink
    return product_urls

def add_cart(driver, url, **kwargs):
    driver.get(url)
    size = kwargs.get('size', None)
    is_available = False
    wait = WebDriverWait(driver, 30)
    try:
        select_size = wait.until(ec.visibility_of_element_located(
            (By.ID, "dk0-productSelect-option-0")))
        select_size.click()
    except Exception as e:
        return is_available
    try:
        size_id = 'dk0-' + str(size)
        selet_dropdown = driver.find_element_by_id(size_id)
        selet_dropdown.click()
    except Exception as e:
        try:
            size_id = 'dk1-' + str(size)
            selet_dropdown = driver.find_element_by_id(size_id)
            selet_dropdown.click()
        except Exception as e:
            return is_available
    try:
        buy_now_button = wait.until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "button#AddToCart")))
        buy_now_button.click()
        is_available = True
    except Exception as e:
        print('error:', e)
    return is_available


def go_to_checkout(driver, **kwargs):
    with open('shopify/javascript/open_cart.js') as f:
        open_cart_script = f.read()
    driver.execute_script(open_cart_script)
    print(open_cart_script)
    with open('shopify/javascript/scroll_open_cart.js') as f:
        scroll_cart = f.read()
    driver.execute_script(scroll_cart)
    print(scroll_cart)
    driver.implicitly_wait(10)
    with open('shopify/javascript/click_checkout_button.js') as f:
        click_script_cart_button = f.read()
    driver.execute_script(click_script_cart_button)
    print(click_script_cart_button)
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 30)
    try:
        buy_now_button = wait.until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "button.cart-checkout")))
        buy_now_button.click()
    except Exception as e:
        print('error:', e)
