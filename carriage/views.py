from django.shortcuts import render
from carriage.models import Test, Country, City
from carriage.routefinder import shortest
from carriage.forms import TestForm

def test(request):
    form = TestForm()
    return render(request, 'carriage/test.html', {'form': form})

def start_page(request):
    return render(request, 'carriage/index.html')


def carriage_main(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['from_city']
            finish = form.cleaned_data['to_city']
            selection = form.cleaned_data['selection']
            res = shortest(first.name, finish.name, selection)
            return render(request, 'carriage/carriage_result.html', {'res':res})
    form = TestForm()
    return render(request, 'carriage/carriage_main.html', {'form':form})


def carriage_result(request):
    pass