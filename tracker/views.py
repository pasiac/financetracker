from django.shortcuts import redirect, render

from .models import IncomeOutcome


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


# def add_expanse(request):


# def edit_expanse(request, expanse_id):
#     expanse = IncomeOutcome.objects.get(id=expanse_id)
