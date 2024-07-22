from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('change', views.edit_topics, name='create'),
    path('control/', include('control.urls')),
    path('practice/', include('practice.urls')),
    path('theory/', include('theory.urls')),
    path('test_results', views.result_list, name='resultlist'),
    path('practice_results', views.practice_report_list, name='reportlist'),
    path('practice_results/<int:report_id>', views.practice_report, name='single_report'),
    path('activity', views.activity_list, name='activity_list')
]


