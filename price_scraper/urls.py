from django.urls import path

from price_scraper.views import PriceListView

urlpatterns = [
    path("price", PriceListView.as_view(), name="price-list"),
]
