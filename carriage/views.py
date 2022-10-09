from django.shortcuts import render
from carriage.models import Test, Country
from carriage.routefinder import get_graph, shortest
from carriage.forms import TestForm


def test(request):
    country = Country.objects.get(pk=1)
    return render(request, 'carriage/index.html', {'country': country})


def carriage_main(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['from_city']
            finish = form.cleaned_data['to_city']
            res = shortest(first.name, finish.name)
            return render(request, 'carriage/carriage_result.html', {'res':res})
    form = TestForm()
    return render(request, 'carriage/carriage_main.html', {'form':form})


def carriage_result(request):
    pass