import json
import os
import random
import re

from backend.shopify.shopify.exceptions import ConfigError

true_args_values = (1, '1', 'true', 'True', True)
false_args_values = (0, '0', 'false', 'False', False, None)

class ProxyConfig():
    def __init__(self, config):
        with open(config, 'r') as config_file:
            try:
                self.config = json.loads(config_file.readlines())
            except:
                raise ConfigError("Proxy config file is not a valid JSON")

    @property
    def get_config(self):
        return self.config

    def get_proxy(self):
        chosen_proxy = self._weighted_choice(self.get_config())
        return "http://" + chosen_proxy

    def _weighted_choice(self, choices_dict):
        choices = [(key, value) for (key, value) in choices_dict.items()]
        total = sum(w for c, w in choices)
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices:
            if upto + w >= r:
                return c
            upto += w

def get_random_positive_float_number():
    return round(random.uniform(0.01, 100.00), 2)

def is_empty(x, y=None):
    if x:
        return x[0]
    else:
        return y

def validate_url(url):
    if not re.findall(r"^http(s)?://", url):
        url = "http://" + url
    return url

def is_valid_url(url):
    return bool(re.findall(r"^http(s)?://", url))

def replace_http_with_https(url):
    return re.sub('^http://', 'https://', url)

def extract_first(selector_list, default=None):
    for x in selector_list:
        return x.extract()
    else:
        return default



def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


