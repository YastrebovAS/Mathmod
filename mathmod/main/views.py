from django.shortcuts import render
import os
from django.http import FileResponse
from mathmod import settings
from .models import lesson
# Create your views here.


def menu(request):
    titles = lesson.objects.all()
    print(titles)
    return render(request,'main/menu.html',{'titles':titles})


def dot_kinetic_theory(request):
    filepath = os.path.join(settings.STATIC_URL, 'word/Точечная кинетика_скачок.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def ksenon_theory(request):
    filepath = os.path.join(settings.STATIC_URL, 'word/Ксенон.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


