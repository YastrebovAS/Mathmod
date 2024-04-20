import inspect

from django.shortcuts import render
from django.http import HttpResponse
from main.models import practices
import importlib
# Create your views here.


def index(request):
    return HttpResponse("<h1>Страница практики</h1>")

def practice_id(request, practice_id):
    prac_list = practices.objects.raw(
        'SELECT id, template,practice FROM main_practices WHERE id = %s',
        [practice_id, ])
    if len(prac_list) == 0:
        context = {
            'title': 'Ошибка',
            'text': 'Такой практики не существует',

        }
        return render(request, 'main/fail.html', context)
    prac_list_x = []
    for elem in prac_list:
        e = elem.__dict__
        prac_list_x.append((e['id'], e['template'], e['practice']))
    id = prac_list_x[0][0]
    plate = prac_list_x[0][1]
    prc = prac_list_x[0][2].split('/')
    pracpath = "media." + prc[0] + "." + prc[1].replace('.py', '')
    imported_module = importlib.import_module(pracpath)
    imported_function = getattr(imported_module,'func')
    context = imported_function(request)
    return  render(request, template_name=plate, context=context)