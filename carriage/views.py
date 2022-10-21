from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from carriage.models import Test, Country, City, SiteContentData, News, Warehouse
from carriage.routefinder import shortest
from carriage.forms import RouteFindForm

site_content_variable = SiteContentData.objects.all()
all_news = News.objects.all().order_by('-date_of_news')
all_warehouses = Warehouse.objects.all()

def search(request):
    text = request.GET.get('search')
    if text:
        articles = all_news.filter(Q(title__contains=text) | Q(body__contains=text))
    else:
        articles = all_news.none()
    return render(request, 'carriage/search.html', {'news': articles})


def start_page(request):
    return render(request, 'carriage/index.html', {'warehouses': all_warehouses})


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


def warehouse_detail(request, pk):
    article = all_news.get(pk=pk)
    return render(request, 'carriage/news_details.html', {'article': article})


class NewsListView(ListView):
    model = News
    paginate_by = 3
    template_name = 'carriage/news.html'



#
# def news(request):
#     return render(request, 'carriage/news.html', {'news': all_news})


def news_detail(request, pk):
    article = all_news.get(pk=pk)
    return render(request, 'carriage/news_details.html', {'article': article})


def transport(request, pk):
    mode = site_content_variable.get(pk=pk)
    return render(request, 'carriage/transport.html', {'mode': mode, 'content_vars': site_content_variable})



