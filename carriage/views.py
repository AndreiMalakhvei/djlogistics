from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from carriage.models import SiteContentData, News, Warehouse, ContactRequest, City
from carriage.routefinder import shortest, WarehouseResult
from carriage.forms import RouteFindForm, ContactForm, WarehouseRequestForm
from django.core.paginator import Paginator
import datetime

site_content_variable = SiteContentData.objects.all()
all_news = News.objects.all().order_by('-date_of_news')
all_warehouses = Warehouse.objects.select_related('city__country')


def search(request):
    text = request.GET.get('search')
    if text:
        articles = all_news.filter(Q(title__contains=text) | Q(body__contains=text))
        paginator = Paginator(articles, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = all_news.none()
    return render(request, 'carriage/search.html', {'page_obj': page_obj, 'text': text})



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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = ContactRequest(
                fname=form.cleaned_data['fname'],
                mail=form.cleaned_data['mail'],
                phone=form.cleaned_data['phone'],
                subject=form.cleaned_data['subject'],
                body=form.cleaned_data['body'],
                req_date=datetime.datetime.now()
                )
            contact_request.save()
            return render(request, 'carriage/contacts_result.html')
        else:
            return render(request, 'carriage/contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'carriage/contact.html', {'form': form})


def contacts_result(request):
    return render(request, 'carriage/contacts_result.html')


def warehouse(request):
    return render(request, 'carriage/warehouse.html', {'warehouses': all_warehouses})


def warehouse_detail(request, pk):
    prev_id = request.resolver_match.kwargs['pk']
    if request.method == 'POST':
        form = WarehouseRequestForm(request.POST)
        if form.is_valid():
            warehouse = all_warehouses.get(pk=prev_id)
            pricing = WarehouseResult(warehouse, form.cleaned_data)
            return render(request, 'carriage/warehouse_detail_result.html', {'warehouse': warehouse, 'pricing': pricing, 'prev_id': prev_id})
        else:
            return render(request, 'carriage/warehouse_detail.html', {'form': form, 'prev_id': prev_id})
    warehouse = all_warehouses.get(pk=pk)
    form = WarehouseRequestForm()

    if warehouse.bonded:
        form.declared_fields['t1'].disabled = False
    else:
        form.declared_fields['t1'].disabled = True
        # form.declared_fields['t1'].widget.attrs.update({'disabled':''})
    return render(request, 'carriage/warehouse_detail.html', {'warehouse': warehouse, 'form': form, 'prev_id': prev_id})


class NewsListView(ListView):
    model = News
    paginate_by = 3
    template_name = 'carriage/news.html'

    def get_queryset(self):
        queryset = News.objects.all().order_by('-date_of_news')
        return queryset


def news_detail(request, pk):
    article = all_news.get(pk=pk)
    return render(request, 'carriage/news_details.html', {'article': article})


def transport(request, pk):
    mode = site_content_variable.get(pk=pk)
    prev_id = int(request.resolver_match.kwargs['pk'])
    return render(request, 'carriage/transport.html', {'mode': mode, 'content_vars': site_content_variable, 'prev_id': prev_id})



