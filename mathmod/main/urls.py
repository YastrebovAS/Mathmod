from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.menu, name='menu'),
    path('change', views.prac_creat, name='create'),
    path('control/', include('control.urls')),
    path('practice/', include('practice.urls')),
    path('theory/', include('theory.urls')),
    path('test_results', views.result_list, name='resultlist')
]


