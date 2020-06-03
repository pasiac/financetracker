from django import forms


class AddExpanseForm(forms.Form):
    title = forms.CharField(label="Nazwa")
    value = forms.DecimalField(label="Kwota")


class AddCategoryForm(forms.Form):
    name = forms.CharField(label="Nazwa")
