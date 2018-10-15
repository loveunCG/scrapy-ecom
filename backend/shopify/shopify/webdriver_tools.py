from selenium import webdriver
import socket
import os

from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from .settings import CHROME_PATH, FIREFOX_PATH, BACKEND_DEBUG_MODE as DEBUG
from .exceptions import ConfigException

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
default_timeout = 30


def _init_display(width=1920, height=1080, visible=DEBUG):
    display = Display(visible=visible, size=(width, height))
    return display


def _init_chrome():
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
    binary = FirefoxBinary(FIREFOX_PATH)
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.implicitly_wait(200)
    driver.maximize_window()

    return driver


def _wait_visibility(driver, xpath, timeout=default_timeout, ignored_exceptions=ignored_exceptions):
    WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))


def _wait_presence(driver, xpath, timeout=default_timeout, ignored_exceptions=ignored_exceptions):
    WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
