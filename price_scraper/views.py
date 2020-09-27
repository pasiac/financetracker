from django.views.generic.list import ListView

from price_scraper.models import Price


class PriceListView(ListView):
    model = Price
    paginate_by = 20
