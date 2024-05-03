from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'control'
urlpatterns = [
    path('<int:control_id>', views.control_id, name = 'ctrllist'),
    path('<int:control_id>/result', views.result, name = 'testresult'),
]





