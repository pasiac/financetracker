from django.urls import path

from tracker.views import *
# MainPageTemplateView, ExpenseListView, ExpenseDetailView


urlpatterns = [
    path("", MainPageTemplateView.as_view(), name="index"),
    # path("wydatki/<order>", expense_list, name="expense_list"),
    path("dodaj-kategorie", add_category, name="add_category"),
    path("kategorie", categories_list, name="categories_list"),
    path("kategoria/<category_id>", category_detail, name="category_detail"),
    path("edytuj-kategorie/<category_id>", edit_category, name="edit_category"),
    path("usun-kategorie/<category_id>", delete_category, name="delete_category"),
    path("generate-csv", generate_csv, name="generate_csv"),
    path("charts", chart_tab, name="chart-tab"),
    # path("wykresy", charts, name="charts"),
]
