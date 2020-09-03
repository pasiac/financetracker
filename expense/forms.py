from django import forms

from expense.models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ("created_by",)
