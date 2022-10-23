from carriage import views
from django.urls import path

app_name = 'carriage'

urlpatterns = [
    path('', views.carriage_main, name='carriage_main'),
    path('contacts/', views.contacts, name='contacts'),
    path('warehouse/', views.warehouse, name='warehouse'),
    path('warehouse/<int:pk>', views.warehouse_detail, name='warehouse_detail'),
    path('transport/<int:pk>/', views.transport, name='transport'),
    # path('news/', views.news, name='news'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('search/', views.search, name='search'),
    # path('search/', views.SearchListView.as_view(), name='search'),

    # path('<int:pk>/', views.detail, name='project_detail'),
]