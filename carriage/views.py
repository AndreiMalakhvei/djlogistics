from django.shortcuts import render
from carriage.models import Test, Country, City
from carriage.routefinder import shortest
from carriage.forms import RouteFindForm

def start_page(request):
    return render(request, 'carriage/index.html')


def carriage_main(request):
    if request.method == 'POST':
        form = RouteFindForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['from_city']
            finish = form.cleaned_data['to_city']
            selection = form.cleaned_data['selection']
            res = shortest(first, finish, selection)
            return render(request, 'carriage/carriage_res.html', {'res': res})
        else:
            return render(request, 'carriage/carriage_main.html', {'form': form})
    form = RouteFindForm()
    return render(request, 'carriage/carriage_main.html', {'form': form})


def contacts(request):
    return render(request, 'carriage/contact.html')


def warehouse(request):
    return render(request, 'carriage/warehouse.html')

def transport(request):
    context = dict()
    return render(request, 'carriage/transport.html', {'context': context})

def news(request):
    context = dict()
    return render(request, 'carriage/news.html', {'context': context})
