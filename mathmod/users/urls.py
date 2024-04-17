from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views



urlpatterns = [
    path('register', views.register, name='registration'),
    path('', views.login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('main/', include('main.urls'))
]


