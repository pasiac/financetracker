import django_filters

from expense.models import Expense


class ExpenseFilter(django_filters.FilterSet):
    value__gt = django_filters.NumberFilter(field_name="value", lookup_expr="gt")
    value__lt = django_filters.NumberFilter(field_name="value", lookup_expr="lt")

    date = django_filters.DateRangeFilter(field_name="date", lookup_expr="date__lte")

    category = django_filters.ChoiceFilter()

    class Meta:
        model = Expense
        fields = {"title": ["icontains"]}
