from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wydatki", views.expanses_list, name="expanses_list"),
    path("wydatek/<expanse_id>", views.expanse_detail, name="expanse_detail"),
    path("usun-wydatek/<expanse_id>", views.delete_expanse, name="delete_expanse"),
]
