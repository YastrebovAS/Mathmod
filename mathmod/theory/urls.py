from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'theory'
urlpatterns = [
    path('<int:lesson_id>', views.lesson_id, name = 'theory')
]


