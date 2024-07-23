from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'control'
urlpatterns = [
    path('<int:control_id>', views.single_test, name = 'SingleTest'),
    path('<int:control_id>/result', views.result, name = 'TestResult'),
]





