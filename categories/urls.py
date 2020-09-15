from django.urls import path

from categories.views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryEditView,
    CategoryListView,
)

urlpatterns = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("usun/<int:pk>/", CategoryDeleteView.as_view(), name="delete_category"),
    path("edytuj/<int:pk>/", CategoryEditView.as_view(), name="edit_category"),
    path("dodaj/", CategoryCreateView.as_view(), name="add_category"),
]
