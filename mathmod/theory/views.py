from django.shortcuts import render
import os
from django.http import FileResponse
from main.models import topic, User, Activity
from mathmod import settings
from datetime import datetime

def theory_id(request, theory_id):

    try:
        topic_list = topic.objects.get(id = theory_id)

        title = topic_list.title
        path = topic_list.theory

        filepath = os.path.join(settings.MEDIA_ROOT + '/' + str(path))

        current_user = User.objects.get(id = request.user.id)
        newactivity = Activity(user=current_user, datetime=datetime.now(), activity=f'Посетил теорию темы "{title}"')
        newactivity.save()

        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    except:
        context = {
            'title': 'Ошибка',
            'error': 'Докумена с этой теорией не существует',

        }
        return render(request, 'theory/fail.html', context)