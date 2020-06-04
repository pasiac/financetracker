import datetime
from calendar import monthrange
from datetime import timedelta
from typing import List

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddCategoryForm, AddExpanseForm
from .models import Category, IncomeOutcome


def index(request):
    return render(request, "index.html",)


def expanses_list(request):
    if request.user.is_authenticated:
        expanses = IncomeOutcome.objects.filter(user=request.user)
        context = {"expanses": expanses}
    else:
        context = {"message": "Zaloguj sie, zeby przegladac swoje wydatki"}
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
        form = AddExpanseForm(request.POST)
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
    form = AddExpanseForm(request.POST or None, instance=expanse)
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
    if request.user.is_authenticated:
        categories = Category.objects.filter(user=request.user)
        context = {"categories": categories}
    else:
        context = {"message": "Zaloguj sie, zeby przegladac swoje kategorie"}
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


# def charts(request):
#     expanses = IncomeOutcome.objects.filter(user=request.user, date=datetime.date.today().month).order_by('date')
#     chart_data, chart_label = __prepare_chart(expanses)
#     print(chart_data)
#     print(chart_label)
#     context = {
#         "chart_data": chart_data,
#         "chart_label": chart_label,
#     }
#     return render(request, "charts.html", context)


# def __prepare_chart(expanses: List[IncomeOutcome]) -> dict:
#     temp = expanses[0].date
#     chart_data = []
#     chart_label = []
#     chart_label.append(temp)
#     sum = 0
#     counter = 0
#     days_counter = 0
#     for expanse in expanses:
#         if days_counter == 10:
#             return chart_data, chart_label
#         if temp.day == expanse.date.day:
#             counter += 1
#             sum += expanse.value
#         else:
#             if temp not in chart_label:
#                 chart_label.append(temp)
#                 days_counter += 1
#             if counter != 0:
#                 chart_data.append(sum)
#                 counter = 0
#                 sum = 0
#             temp = temp + timedelta(days=1)
