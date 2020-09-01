from __future__ import absolute_import, unicode_literals

from datetime import date
from decimal import Decimal
from typing import List

from celery import task
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from price_scraper.models import Price, Product
from tracker.models import Expense

WEBDRIVER_PATH = "/home/dawid/financestracker/chromedriver"
NOT_FOUND_MESSAGE = "Nie znaleziono produktów spełniających kryteria wyszukiwania."
STOKROTKA_PATH = "https://sklep.stokrotka.pl/szukaj/?search=product&string="
STOKROTKA_ITEM_XPATH = "/html/body/div[3]/div/div[2]/div[2]/div[1]"


@task()
def get_prices():
    # Scrapes web to find prices of today added expense
    items_name = Expense.objects.filter(date__date=date.today()).values_list(
        "title", flat=True
    )
    for item in items_name:
        response = fetch_data(item)
        # Clear data
        if NOT_FOUND_MESSAGE in response:
            continue
        else:
            add_or_update_product(clear_data(response))


def fetch_data(item_name, path=STOKROTKA_PATH, xpath=STOKROTKA_ITEM_XPATH):
    # Configure
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    # Fetch data
    driver = webdriver.Chrome(options=options, executable_path=WEBDRIVER_PATH)
    driver.get(f"{path}{item_name}")
    response = driver.find_elements_by_xpath(xpath)[0].text
    driver.close()
    return response


def clear_data(response):
    response = (
        response.replace("\n▾", "")
        .replace("\n▴", "")
        .replace(",", ".")
        .replace("zł", "")
        .split("\n")
    )
    response_iterator = iter(response)
    return list(zip(response_iterator, response_iterator))


def add_or_update_product(items: List):
    for item in items:
        # If there are 2 prices (old, new) grab only current
        value = item[1].split(" ")[0]
        value = Decimal(value)
        product = Product.objects.filter(title=item[0])
        product = Price.objects.filter(product__title=item[0], value=value)
        if not product:
            product = Product.objects.create(title=item[0], category="spozywcze")
            product.save()
            price = Price.objects.create(
                shop_name="Stokrotka", value=value, product=product
            )
            price.save()
            print(f"Save product {product} with {price}")
        else:
            print("This item already exist")
            continue
