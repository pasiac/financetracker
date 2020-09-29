from django.urls import path

from expense.views import (ExpenseCreateView, ExpenseDeleteView,
                           ExpenseDetailView, ExpenseEditView, ExpenseListView)

urlpatterns = [
    path("", ExpenseListView.as_view(), name="expense_list"),
    path("<int:pk>/", ExpenseDetailView.as_view(), name="expense_detail"),
    path("usun/<int:pk>/", ExpenseDeleteView.as_view(), name="delete_expense"),
    path("edytuj/<int:pk>/", ExpenseEditView.as_view(), name="edit_expense"),
    path("dodaj/", ExpenseCreateView.as_view(), name="add_expense"),
]
