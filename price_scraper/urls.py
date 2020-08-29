from price_scraper.views import PriceListView
from django.urls import path

urlpatterns = [
    path('price', PriceListView.as_view(), name='price-list'),
]
