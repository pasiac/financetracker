from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from categories.forms import CategoryForm
from categories.models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 10
    context_object_name = "categories"

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user).order_by("-pk")


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category


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
