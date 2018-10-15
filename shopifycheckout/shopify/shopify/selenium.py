import time

import socket
import os
import pickle


from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException, NoSuchElementException
from pyvirtualdisplay import Display
from .items import ProductLink
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import Proxy, ProxyType
from .settings import CHROME_PATH, FIREFOX_PATH, BACKEND_DEBUG_MODE as DEBUG, PROXY, DefaultURL
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
# from .exceptions import ConfigException


"""
number of seconds used to wait the web page's loading.
"""
WAIT_TIMEOUT = 15

"""
number of seconds used to wait the web page's loading.

"""
SELENIUM_HOSTNAME = 'selenium'
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': PROXY,
    'ftpProxy': PROXY,
    'sslProxy': PROXY,
    'noProxy': ''
})
"""
number of seconds used to wait the web page's loading.
"""

SEE_ALL_PLACEHOLDER = 'See all'
IDLE_INTERVAL_IN_SECONDS = 10

def wait_invisibility_xpath(driver, xpath, wait_timeout=None):
    if wait_timeout is None:
        wait_timeout = WAIT_TIMEOUT

    WebDriverWait(driver, wait_timeout).until(ec.invisibility_of_element_located((By.XPATH, xpath)))


def _init_display(width=1920, height=1080, visible=DEBUG):
    display = Display(visible=visible, size=(width, height))
    return display


def get_by_xpath_or_none(driver, xpath, wait_timeout=None, logs=True):
    """
    Get a web element through the xpath string passed.
    If a TimeoutException is raised the else_case is called and None is returned.
    :param driver: Selenium Webdriver to use.
    :param xpath: String containing the xpath.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :param logs: optional, prints a status message to stdout if an exception occures.
    :return: The web element or None if nothing found.
    """
    try:
        return get_by_xpath(driver, xpath, wait_timeout=wait_timeout)
    except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
        if logs:
            print("Exception Occurred:")
            print(f"XPATH:{xpath}")
            print(f"Error:{e}")
        return None


def get_by_xpath(driver, xpath, wait_timeout=None):
    """
    Get a web element through the xpath passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param xpath: xpath to use.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :return: The web element.
    """
    if wait_timeout is None:
        wait_timeout = WAIT_TIMEOUT
    return WebDriverWait(driver, wait_timeout).until(
        ec.presence_of_element_located(
            (By.XPATH, xpath)
        ))


def extracts_see_all_url(driver):
    """
    Retrieve from the the Company front page the url of the page containing the list of its employees.
    :param driver: The already opened (and logged in) webdriver, already located to the company's front page.
    :return: String: The "See All" URL.
    """
    print('Searching for the "See all * employees on LinkedIn" btn')
    see_all_xpath = f'//a/strong[starts-with(text(),"{SEE_ALL_PLACEHOLDER}")]'
    see_all_elem = get_by_xpath(driver, see_all_xpath)
    see_all_ex_text = see_all_elem.text

    a_elem = driver.find_element_by_link_text(see_all_ex_text)
    see_all_url = a_elem.get_attribute('href')

    print(f'Found the following URL: {see_all_url}')
    return see_all_url


def init_chromium():
    socket.setdefaulttimeout(60)
    if not os.path.exists(CHROME_PATH):
        raise ConfigException("Wrong chromedriver path, check settings")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=CHROME_PATH,
                              chrome_options=options)
    driver.implicitly_wait(200)
    driver.maximize_window()
    return driver


def _init_firefox():
    binary = FirefoxBinary()
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.implicitly_wait(200)
    driver.maximize_window()
    return driver


def marionette_driver(**kwargs):
    proxy_port = kwargs.get('proxy_port', None)
    proxy_ip = kwargs.get('proxy_ip', None)

    options = Options()
    if kwargs.get('headless', True):
        options.add_argument('--headless')

    dir_ = os.path.dirname(__file__)
    ffProfilePath = os.path.join(dir_, "FirefoxSeleniumProfile")
    if os.path.isdir(ffProfilePath) == False:
        os.mkdir(ffProfilePath)

    profile = webdriver.FirefoxProfile(profile_directory=ffProfilePath)

    if proxy_ip and proxy_port:
        print('setting proxy')
        profile.set_preference('network.proxy.socks_port', int(proxy_port))
        profile.set_preference('network.proxy.socks', proxy_ip)
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_ip)
        profile.set_preference("network.proxy.http_port", int(proxy_port))
        profile.update_preferences()

    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    firefox_capabilities['handleAlerts'] = True
    firefox_capabilities['acceptSslCerts'] = True
    firefox_capabilities['acceptInsecureCerts'] = True
    firefox_capabilities['javascriptEnabled'] = True

    driver = webdriver.Firefox(options=options, firefox_profile=profile,
                               capabilities=firefox_capabilities)
    if 'loadsession' in kwargs:
        load_session(driver, kwargs.get('email'))

    return driver


""" load session with account email info """


def load_session(driver, email="1", openUrl=""):
    storefile = get_sesssion_file(email)
    print('reading cookie:', storefile)
    driver.get(LINKEDIN_URL)
    try:
        for cookie in pickle.load(open(storefile, "rb")):
            driver.add_cookie(cookie)
    except Exception as err:
        print('error:', err)


""" get session file with account email info """


def get_sesssion_file(email):
    dir_ = os.path.dirname(__file__)
    _COOKIE_FILE = os.path.join(dir_, "ShopifyCookies")
    if os.path.isdir(_COOKIE_FILE) == False:
        os.makedirs(_COOKIE_FILE)

    return os.path.join(_COOKIE_FILE, email)


""" store session file with account email info """


def store_session(driver, email='1'):
    storefile = get_sesssion_file(email)
    print('storing cookie:', storefile)
    pickle.dump(driver.get_cookies() , open(storefile,"wb"))


class SeleniumSpiderMixin:
    def __init__(self, selenium_hostname=None, **kwargs):
        if selenium_hostname is None:
            selenium_hostname = SELENIUM_HOSTNAME
        self.driver = marionette_driver(headless=False)
        super().__init__(**kwargs)

    def closed(self, reason):
        pass
        self.driver.close()