from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wydatki/<order>", views.expanses_list, name="expanses_list"),
    path("wydatki", views.expanses_list, name="expanses_list"),
    path("wydatek/<expanse_id>", views.expanse_detail, name="expanse_detail"),
    path("usun-wydatek/<expanse_id>", views.delete_expanse, name="delete_expanse"),
    path("dodaj-wydatek", views.add_expanse, name="add_expanse"),
    path("dodaj-kategorie", views.add_category, name="add_category"),
    path("kategorie", views.categories_list, name="categories_list"),
    path("kategoria/<category_id>", views.category_detail, name="category_detail"),
    path("edytuj-wydatek/<expanse_id>", views.edit_expanse, name="edit_expanse"),
    path("edytuj-kategorie/<category_id>", views.edit_category, name="edit_category"),
    path("usun-kategorie/<category_id>", views.delete_category, name="delete_category"),
    path("generate-csv", views.generate_csv, name="generate_csv"),
    path("charts", views.chart_tab, name="chart-tab"),
    # path("wykresy", views.charts, name="charts"),
]
