from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.menu, name='menu'),
    path('change', views.prac_creat, name='create'),
    path('control', views.index, name = 'ctrl'),
    path('practice/', include('practice.urls')),
    path('theory/', include('theory.urls'))
]


