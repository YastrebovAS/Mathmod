from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'theory'
urlpatterns = [
    path('<int:theory_id>', views.single_theory, name='SingleTheory')
]
