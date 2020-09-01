from django import forms

from .models import Category, Expense


class AddExpanseForm(forms.ModelForm):
    # def __init__(self, request, *args, **kwargs):
    #     super(AddExpanseForm, self).__init__(*args, **kwargs)
    #     if request:
    #         self.fields["category"].queryset = Category.objects.filter(
    #             user=request.user
    #         )

    class Meta:
        model = Expense
        fields = ["title", "value", "category", "recipe"]


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
