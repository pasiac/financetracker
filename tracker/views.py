from django.shortcuts import redirect, render

from .forms import AddCategoryForm, AddExpanseForm
from .models import IncomeOutcome, Category


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
        expanse = IncomeOutcome.objects.get(id=expanse_id)
        context = {"expanse": expanse}
    else:
        context = {"message": "Zaloguj sie, zeby przegladac swoje wydatki"}
    return render(request, "expanse_detail.html", context)


def delete_expanse(request, expanse_id):
    expanse = IncomeOutcome.objects.get(id=expanse_id)
    title = expanse.title
    expanse.delete()
    # context = {"message", f"Wydatek {title} został usunięty"}
    return redirect("expanses_list")


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


def add_category(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.update({"user": request.user})
            category = Category(**data)
            category.save()
            return redirect("expanses_list")
    else:
        form = AddCategoryForm()
    return render(request, "add_category.html", {"form": form})


def categories_list(request):
    if request.user.is_authenticated:
        categories = Category.objects.filter(user=request.user)
        context = {"categories": categories}
    else:
        context = {"message": "Zaloguj sie, zeby przegladac swoje kategorie"}
    return render(request, "categories_list.html", context)




# def edit_expanse(request, expanse_id):
#     expanse = IncomeOutcome.objects.get(id=expanse_id)
