from __future__ import absolute_import, unicode_literals

from celery import task
from .models import IncomeOutcome
import requests
from bs4 import BeautifulSoup


@task()
def get_prices():
    items_names = IncomeOutcome.objects.values_list("title", flat=True)
    items_response_list = [requests.get(f'https://zakupy.auchan.pl/shop/search/{name}') for name in items_names]
    
    print("I have to use silenium to complete this task")