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
        all_expanses_value = __calculate_total_value(all_user_expanses)
        expanse = IncomeOutcome.objects.get(id=expanse_id)
        all_expanses_value -= expanse.value
        chart_data = [float(all_expanses_value), float(expanse.value)]
        chart_label = ["Wszystkie", expanse.title]
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
    # context = {"message", f"Wydatek {title} został usunięty"}
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
        expanses_list = IncomeOutcome.objects.filter(
            user=request.user, category=category
        )
        all_expanses_list = IncomeOutcome.objects.filter(user=request.user)
        context = {"expanses_list": expanses_list, "category": category}
    else:
        context = {"message": "Zaloguj sie, zeby przegladac ta zawartosc"}
    return render(request, "category_detail.html", context)


def __calculate_total_value(expanse_list: List[IncomeOutcome]) -> float:
    return sum(expanse.value for expanse in expanse_list)


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = AddCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("categories_list")
    return render(request, "add_category.html", {"form": form})
