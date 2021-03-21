import logging

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def soup(url, file: bool = False) -> (BeautifulSoup, bool):
    success = True
    if file:  # for loading a file
        page_data = url.read()
    else:
        logging.basicConfig(level=logging.DEBUG)
        s = requests.Session()
        status_forcelist = tuple(x for x in requests.status_codes._codes if x != 200)
        retries = Retry(total=5, backoff_factor=1, status_forcelist=status_forcelist, raise_on_status=True)
        s.mount('http://', HTTPAdapter(max_retries=retries))

        get = s.get(url)
        if get.status_code != 200:
            success = False

        get.encoding = get.apparent_encoding
        page_data = get.text

    return BeautifulSoup(page_data, "html.parser"), success


def recipe_content(url, file: bool) -> BeautifulSoup:
    recipe = soup(url, file)[0].find('div', {'itemtype': "http://schema.org/Recipe"})
    assert recipe is not None
    return recipe
