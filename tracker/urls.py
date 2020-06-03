from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wydatki", views.expanses_list, name="expanses_list"),
    path("wydatek/<expanse_id>", views.expanse_detail, name="expanse_detail"),
    path("usun-wydatek/<expanse_id>", views.delete_expanse, name="delete_expanse"),
    path("dodaj-wydatek", views.add_expanse, name="add_expanse"),
    path("dodaj-kategorie", views.add_category, name="add_category"),
    path("kategorie", views.categories_list, name="categories_list"),

]
