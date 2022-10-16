from carriage import views
from django.urls import path

app_name = 'carriage'

urlpatterns = [
    path('', views.carriage_main, name='carriage_main'),
    path('contacts/', views.contacts, name='contacts'),
    path('warehouse/', views.warehouse, name='warehouse'),

    # path('<int:pk>/', views.detail, name='project_detail'),
]