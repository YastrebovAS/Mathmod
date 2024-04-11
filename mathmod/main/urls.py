from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.menu, name='home'),
    path('practice/', include('practice.urls')),
    path('theory/Точечная кинетика', views.dot_kinetic_theory, name = 'dot kinetic theory'),
    path('theory/Ксенон', views.ksenon_theory, name = 'ksenon theory')
]
