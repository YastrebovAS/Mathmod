from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.menu, name='home'),
    path('create', views.create, name='create'),
    path('practice/', include('practice.urls')),
    path('theory/', include('theory.urls'))
]


