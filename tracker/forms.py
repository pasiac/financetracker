from django import forms

from .models import Category, IncomeOutcome


class AddExpanseForm(forms.ModelForm):
    class Meta:
        model = IncomeOutcome
        fields = [
            "title",
            "value",
            "category",
        ]


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
