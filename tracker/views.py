from django.http import HttpResponse
from django.shortcuts import render

from .models import IncomeOutcome


def index(request):
    return render(request, "index.html",)


def explore_expanses(request):
    if request.user.is_authenticated:
        expanses = IncomeOutcome.objects.filter(user=request.user)
        context = {"expanses": expanses}
    else:
        context = {"message": "Zaloguj sie, zeby przegladac swoje wydatki"}
    return render(request, "expanses.html", context)
