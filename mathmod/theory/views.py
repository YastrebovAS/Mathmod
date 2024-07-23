from django.shortcuts import render
import os
from django.http import FileResponse
from main.models import topic, User, Activity
from mathmod import settings
from datetime import datetime


def single_theory(request, theory_id):  # Функция для демонстрации теории

    try:
        topic_list = topic.objects.get(id=theory_id)  # Берется соответствующая теория

        title = topic_list.title
        path = topic_list.theory

        filepath = os.path.join(settings.MEDIA_ROOT + '/' + str(path))  # Находится путь к файлу с теорией

        current_user = User.objects.get(id=request.user.id)
        new_activity = Activity(user=current_user, datetime=datetime.now(), activity=f'Посетил теорию темы "{title}"')
        new_activity.save()  # Записывается факт посещения пользователем теории

        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    except:  # Если файла не существует, выдает ошибку и просит вернуться в каталог
        context = {
            'title': 'Ошибка',
            'error': 'Документа с этой теорией не существует',

        }
        return render(request, 'theory/fail.html', context)
