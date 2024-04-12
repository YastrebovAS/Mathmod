from django.shortcuts import render
import os
from django.http import FileResponse
from main.models import lesson
from mathmod import settings

def ksenon_theory(request):
    filepath = os.path.join(settings.STATIC_URL, 'word/Ксенон.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def lesson_id(request, lesson_id):
    lesson_list = lesson.objects.raw(
        'SELECT id, theory FROM main_lesson WHERE id = %s',
        [lesson_id, ])
    if len(lesson_list) == 0:
        context = {
            'title': 'Ошибка',
            'text': 'Докумена с этой теорией не существует',

        }
        return render(request, 'main/fail.html', context)
    lesson_list_x = []
    for elem in lesson_list:
        e = elem.__dict__
        lesson_list_x.append((e['id'], e['theory']))
    path = lesson_list_x[0][1]
    filepath = os.path.join(settings.STATIC_URL + 'word/' + path)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
