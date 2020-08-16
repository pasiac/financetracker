from __future__ import absolute_import, unicode_literals

import requests
from bs4 import BeautifulSoup
from celery import task
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tracker.models import IncomeOutcome

WEBDRIVER_PATH = "/home/dawid/financestracker/chromedriver"
NOT_FOUND_MESSAGE = "Nie znaleziono produktów spełniających kryteria wyszukiwania."


@task()
def get_prices():
    items_name = IncomeOutcome.objects.values_list("title", flat=True)
    stokrotka_items = []

    for item in items_name:
        response = fetch_stokrotka_data(item)
        # Clear data
        if NOT_FOUND_MESSAGE in response:
            continue
        else:
            stokrotka_items.append(clear_data(response))

    print(stokrotka_items)

def fetch_stokrotka_data(item_name):
    # Configure
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    # Fetch data
    driver = webdriver.Chrome(options=options, executable_path=WEBDRIVER_PATH)
    driver.get(f"https://sklep.stokrotka.pl/szukaj/?search=product&string={item_name}")
    response = driver.find_elements_by_xpath(
        "/html/body/div[3]/div/div[2]/div[2]/div[1]"
    )[0].text
    driver.close()
    return response

def clear_data(response):
    response = response.replace("\n▾", "").replace("\n▴", "").split("\n")
    response_iterator = iter(response)
    return list(zip(response_iterator, response_iterator))
