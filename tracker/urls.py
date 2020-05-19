from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wydatki", views.explore_expanses, name="expanses"),
]
