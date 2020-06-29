import csv
import datetime
from calendar import monthrange
from datetime import timedelta
from typing import List

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddCategoryForm, AddExpanseForm
from .models import Category, IncomeOutcome


def index(request):
    return render(request, "index.html",)


@login_required
def expanses_list(request, order="-date"):
    expanses = IncomeOutcome.objects.filter(user=request.user).order_by(order)
    paginator = Paginator(expanses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"expanses": expanses, "page_obj": page_obj}
    return render(request, "expanses_list.html", context)


def expanse_detail(request, expanse_id):
    if request.user.is_authenticated:
        all_user_expanses = IncomeOutcome.objects.filter(user=request.user)
        expanse = IncomeOutcome.objects.get(id=expanse_id)
        all_expanses_value = __calculate_total_value(all_user_expanses) - float(
            expanse.value
        )
        chart_data = [round(float(expanse.value), 2), round(all_expanses_value, 2)]
        chart_label = [expanse.title, "Inne wydatki"]
        context = {
            "expanse": expanse,
            "chart_data": chart_data,
            "chart_label": chart_label,
        }
    else:
        context = {"message": "Zaloguj sie, zeby przegladac swoje wydatki"}
    return render(request, "expanse_detail.html", context)


@login_required
def delete_expanse(request, expanse_id):
    expanse = IncomeOutcome.objects.get(id=expanse_id)
    title = expanse.title
    expanse.delete()
    return redirect("expanses_list")


@login_required
def add_expanse(request):
    if request.method == "POST":
        form = AddExpanseForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data.update({"user": request.user})
            expanse = IncomeOutcome(**data)
            expanse.save()
            return redirect("expanses_list")
    else:
        form = AddExpanseForm()
    return render(request, "add_expanse.html", {"form": form})


def edit_expanse(request, expanse_id):
    expanse = get_object_or_404(IncomeOutcome, id=expanse_id)
    form = AddExpanseForm(request.POST or None, request.FILES or None, instance=expanse)
    if form.is_valid():
        form.save()
        return redirect("expanses_list")
    return render(request, "add_expanse.html", {"form": form})


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


def category_detail(request, category_id):
    if request.user.is_authenticated:
        category = Category.objects.get(id=category_id)
        category_expanses_list = IncomeOutcome.objects.filter(
            user=request.user, category=category
        )
        all_expanses = IncomeOutcome.objects.filter(user=request.user)
        category_value = __calculate_total_value(category_expanses_list)
        total_value = __calculate_total_value(all_expanses) - category_value
        chart_data = [round(category_value, 2), round(total_value, 2)]
        chart_label = [category.name, "Inne kategorie"]
        context = {
            "expanses_list": category_expanses_list,
            "category": category,
            "chart_data": chart_data,
            "chart_label": chart_label,
        }
    else:
        context = {"message": "Zaloguj sie, zeby przegladac ta zawartosc"}
    return render(request, "category_detail.html", context)


def __calculate_total_value(expanse_list: List[IncomeOutcome]) -> float:
    return round(sum(float(expanse.value) for expanse in expanse_list), 2)


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = AddCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("categories_list")
    return render(request, "add_category.html", {"form": form})


@login_required
def delete_category(request, category_id):
    expanse = Category.objects.get(id=category_id)
    expanse.delete()
    return redirect("categories_list")


def generate_csv(request):
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{request.user}_expanses.csv"'
    expanses = IncomeOutcome.objects.filter(user=request.user).all()
    data = [
        [expanse.title, expanse.value, expanse.date, expanse.category]
        for expanse in expanses
    ]
    writer = csv.writer(response)
    writer.writerow(["title", "value", "date", "category"])
    writer.writerows(data)
    return response


def chart_tab(request):
    pass
