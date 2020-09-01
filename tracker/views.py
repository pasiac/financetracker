import csv
from typing import List

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView

from tracker.forms import AddCategoryForm, AddExpanseForm
from tracker.models import Category, Expense
from django.urls import reverse_lazy


class MainPageTemplateView(TemplateView):
    template_name = "index.html"



# @login_required
# def add_expanse(request):
#     if request.method == "POST":
#         form = AddExpanseForm(request.POST, request.FILES)
#         if form.is_valid():
#             data = form.cleaned_data
#             data.update({"user": request.user})
#             expanse = Expense(**data)
#             expanse.save()
#             return redirect("expense_list")
#     else:
#         form = AddExpanseForm()
#     return render(request, "add_expanse.html", {"form": form})



@login_required
def expanse_detail(request, expanse_id):
    all_user_expense = Expense.objects.filter(user=request.user)
    try:
        expanse = Expense.objects.get(id=expanse_id)
    except ObjectDoesNotExist:
        # Obsluga 404?
        return redirect("/")
    all_expense_value = __calculate_total_value(all_user_expense) - float(
        expanse.value
    )
    chart_data = [round(float(expanse.value), 2), round(all_expense_value, 2)]
    chart_label = [expanse.title, "Inne wydatki"]
    context = {
        "expanse": expanse,
        "chart_data": chart_data,
        "chart_label": chart_label,
    }
    return render(request, "expanse_detail.html", context)


@login_required
def add_category(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.update({"user": request.user})
            category = Category(**data)
            category.save()
            return redirect("categories_list")
    else:
        form = AddCategoryForm()
    return render(request, "add_category.html", {"form": form})


@login_required
def categories_list(request):
    categories = Category.objects.filter(user=request.user)
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"categories": categories, "page_obj": page_obj}
    return render(request, "categories_list.html", context)


@login_required
def category_detail(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        # Obsluga 404?
        return redirect("/")

    expense_in_category = Expense.objects.filter(
        user=request.user, category=category
    )
    all_expense = Expense.objects.filter(user=request.user)
    category_value = __calculate_total_value(expense_in_category)
    total_value = __calculate_total_value(all_expense) - category_value
    chart_data = [round(category_value, 2), round(total_value, 2)]
    chart_label = [category.name, "Inne kategorie"]
    context = {
        "expense_list": expense_in_category,
        "category": category,
        "chart_data": chart_data,
        "chart_label": chart_label,
    }
    return render(request, "category_detail.html", context)


def __calculate_total_value(expanse_list: List[Expense]) -> float:
    return round(sum(float(expanse.value) for expanse in expanse_list), 2)


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = AddCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("categories_list")
    return render(request, "add_category.html", {"form": form})


@login_required
def delete_category(request, category_id):
    try:
        expanse = Category.objects.get(id=category_id)
        expanse.delete()
    except ObjectDoesNotExist:
        # Obsluga 404?
        return redirect("/")
    return redirect("categories_list")


def generate_csv(request):
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{request.user}_expense.csv"'
    expense = Expense.objects.values_list(
        "title", "value", "date", "category__name"
    )
    response.write("\ufeff".encode("utf8"))
    writer = csv.writer(response)
    writer.writerow(["title", "value", "date", "category"])
    writer.writerows(expense)
    return response


@login_required
def chart_tab(request):
    expense = Expense.objects.filter(user=request.user).order_by("date")
    current_expanse = expense[0]
    date_and_values = {current_expanse.date.strftime("%d/%m/%Y"): 0}
    for expanse in expense:
        if current_expanse.date.day - expanse.date.day == 0:
            date_and_values[current_expanse.date.strftime("%d/%m/%Y")] += float(
                expanse.value
            )
        else:
            current_expanse = expanse
            date_and_values.update(
                {current_expanse.date.strftime("%d/%m/%Y"): float(expanse.value)}
            )
    chart_labels = list(date_and_values.keys())
    chart_data = list(date_and_values.values())
    context = {"chart_labels": chart_labels, "chart_data": chart_data}
    return render(request, "chart_tab.html", context)
