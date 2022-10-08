from carriage import views
from django.urls import path

urlpatterns = [
    path('', views.carriage_main),
    # path('<int:pk>/', views.detail, name='project_detail'),
]