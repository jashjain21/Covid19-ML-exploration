from django.urls import path
from core import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
]