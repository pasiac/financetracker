from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from expense.forms import ExpenseForm
from expense.models import Expense


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    paginate_by = 10
    context_object_name = "expenses"

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user).order_by("-date")


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        chart = self.prepare_chart_data()
        context.update(chart)
        return context

    def prepare_chart_data(self):
        categories_expenses = Expense.objects.values_list("value", flat=True).exclude(
            pk=self.object.pk
        )
        chart = {
            "chart_label": [self.object.title, "Others"],
            "chart_data": [
                float(self.object.value),
                sum(map(float, categories_expenses)),
            ],
        }
        return chart


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    success_url = reverse_lazy("expense_list")


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy("expense_list")
    extra_context = {"header": "Dodawanie wydatku"}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super().form_valid(form)


class ExpenseEditView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy("expense_list")
    extra_context = {"header": "Edycja wydatku"}
