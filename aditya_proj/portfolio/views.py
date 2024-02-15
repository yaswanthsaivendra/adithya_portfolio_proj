from django.shortcuts import render

from .utils import data_fun


def index(request, stock):
    chart = data_fun(stock)

    return render(request, "portfolio/index.html", {"chart": chart})
