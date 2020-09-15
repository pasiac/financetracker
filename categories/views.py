from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from categories.forms import CategoryForm
from categories.models import Category
from expense.models import Expense
from utils.exceptions import NoExpensesError


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 10
    context_object_name = "categories"

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user).order_by("-pk")


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            chart = self.prepare_chart_data()
        except NoExpensesError:
            return context
        context.update(chart)
        return context

    def prepare_chart_data(self):
        object_expenses = self.object.get_related_expenses_value_list()
        if not object_expenses:
            raise NoExpensesError(self.object)
        categories_expenses = Expense.objects.values_list("value", flat=True).exclude(
            category__pk=self.object.pk
        )
        chart = {
            "chart_label": [self.object.title, "Others"],
            "chart_data": [
                sum(map(float, object_expenses)),
                sum(map(float, categories_expenses)),
            ],
        }
        return chart


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("category_list")


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("category_list")
    extra_context = {"header": "Dodawanie kategorii"}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super().form_valid(form)


class CategoryEditView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("category_list")
    extra_context = {"header": "Edycja kategorii"}
