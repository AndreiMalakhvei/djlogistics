from django.shortcuts import render
from carriage.models import Test, Country


def test(request):
    country = Country.objects.get(pk=1)
    return render(request, 'carriage/index.html', {'country': country})


def carriage_main(request):
    pass


def carriage_result(request):
    pass