from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('Точечная кинетика', views.dot_kinetic, name='dot kinetic'),
    path('Ксенон', views.ksenon, name='ksenon'),
    path('Расчет реактора', views.reactor_calc, name='reactor'),
    path('Реактор с отражателем', views.react_deflect, name='deflector')
]