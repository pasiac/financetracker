from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from expense.models import Expense
from expense.forms import ExpenseForm
from django.http import HttpResponseRedirect


class ExpenseListView(ListView):
    model = Expense
    ordering = ("-date",)
    paginate_by = 10
    context_object_name = "expenses"


class ExpenseDetailView(DetailView):
    model = Expense


class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy("expense_list")


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy("expense_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super().form_valid(form)


class ExpenseEditView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy("expense_list")
