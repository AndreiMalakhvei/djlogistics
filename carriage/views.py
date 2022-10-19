from django.shortcuts import render
from carriage.models import Test, Country, City, SiteContentData, News
from carriage.routefinder import shortest
from carriage.forms import RouteFindForm

site_content_variable = SiteContentData.objects.all()
all_news = News.objects.all().order_by('-date_of_news')

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



def news(request):
    return render(request, 'carriage/news.html', {'news': all_news})

def transport(request, pk):
    mode = site_content_variable.get(pk=pk)
    return render(request, 'carriage/transport.html', {'mode': mode, 'content_vars': site_content_variable})

def news_detail(request, pk):
    article = all_news.get(pk=pk)
    return render(request, 'carriage/news_details.html', {'article': article})