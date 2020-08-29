from django.shortcuts import render
from django.views.generic.list import ListView
from price_scraper.models import Price

# Create your views here.
class PriceListView(ListView):
    model = Price
    paginate_by = 20