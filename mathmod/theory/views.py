from django.shortcuts import render
import os
from django.http import FileResponse
from main.models import topic
from mathmod import settings

def theory_id(request, theory_id):
    topic_list = topic.objects.raw(
        'SELECT id, theory FROM main_topic WHERE id = %s',
        [theory_id, ])
    if len(topic_list) == 0:
        context = {
            'title': 'Ошибка',
            'text': 'Докумена с этой теорией не существует',

        }
        return render(request, 'main/fail.html', context)
    topic_list_x = []
    for elem in topic_list:
        e = elem.__dict__
        topic_list_x.append((e['id'], e['theory']))
    path = topic_list_x[0][1]
    filepath = os.path.join(settings.MEDIA_ROOT + '/' + path)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')