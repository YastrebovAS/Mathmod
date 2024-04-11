from django.shortcuts import render
import os
from django.http import FileResponse
from mathmod import settings
# Create your views here.


def menu(request):
    return render(request,'main/menu.html')

def dot_kinetic_theory(request):
    filepath = os.path.join(settings.STATIC_URL, 'word/Точечная кинетика_скачок.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def ksenon_theory(request):
    filepath = os.path.join(settings.STATIC_URL, 'word/Ксенон.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


