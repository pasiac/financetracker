from django import forms

from .models import Category, IncomeOutcome


class AddExpanseForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(AddExpanseForm, self).__init__(*args, **kwargs)
        if request:
            self.fields["category"].queryset = Category.objects.filter(
                user=request.user
            )

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
