from django.urls import path
from expense.views import (
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseDetailView,
    ExpenseEditView,
    ExpenseListView,
)

urlpatterns = [
    path("", ExpenseListView.as_view(), name="expense_list"),
    path("<int:pk>", ExpenseDetailView.as_view(), name="expanse_detail"),
    path("usun/<int:pk>", ExpenseDeleteView.as_view(), name="delete_expanse"),
    path("edytuj/<int:pk>", ExpenseEditView.as_view(), name="edit_expanse"),
    path("dodaj/", ExpenseCreateView.as_view(), name="add_expanse"),
]
