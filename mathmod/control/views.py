from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import questions, topic, results, User, Activity 
from datetime import datetime


def single_test(request, control_id):  # отвечает за функционал тестов

    request.session['restest'] = None # подробный результат пройденного теста, переменная создается прямо в сессии браузера

    title = topic.objects.filter(id=control_id)[0]  # заголовок темы
    question_list = questions.objects.filter(topic_test=control_id)  # список вопросов для этой темы
    current_user = User.objects.get(id=request.user.id)  # пользователь

    if len(question_list) == 0:  # если теста не существует, система сообщает
        context = {
            'title': 'Теста не существует',
            'error': 'Теста по этой теме пока что нет',

        }
        return render(request, 'main/fail.html', context)  # перевод на страницу где выдаются ошибки

    answers_array = []
    correct_answers_array = []
    
    for c in question_list:

        number_of_correct_answers = 0
        for answer in c.get_answers():
            if answer['is_correct']:
                number_of_correct_answers += 1
        correct_answers_array.append(number_of_correct_answers) # массив из кол-ва правильных
                                                                # ответов на каждый вопрос
        answers_array.append(c.get_answers())  # массив из групп вариантов ответа(правильных и неправильных)
                                               # для каждого вопроса
    
    context = {
        'title': title.title,
        'questions': question_list,
        'answers': answers_array,
        'number_of_correct_answers': correct_answers_array
    }  # в итоге на страницу теста отправятся заголовок, список вопросов, список ответов(ВСЕХ) и кол-во правилньых ответов для каждого вопроса

    if request.method == 'POST':  # если пользователь отправил результаты теста
        restest = []  # подробные результаты
        correct_answers = []  # правильные ответы
        actual_answers = []  # ответы пользователя
        max_points = 0  # максимальные баллы за тест
        actual_points = 0  # набранные баллы за тест

        for question in question_list:
            max_points += question.marks
            if question.question in request.POST.keys():
                actual_answers.append(request.POST.getlist(question.question))  # заполняется массив ответов пользователя

        for answerset in answers_array:
            correct_answers_for_one_question = []
            for answer in answerset:
                if answer['is_correct']:
                    correct_answers_for_one_question.append(answer['answer'])
            correct_answers.append(correct_answers_for_one_question)  # создается массив из ВСЕХ правильных ответов к тесту

        for j in range(len(actual_answers)):
            points_for_question = 0
            for r in range(len(actual_answers[j])):
                if actual_answers[j][r] in correct_answers[j]:  # сравниваются правильные и введенные ответы
                    points_for_question += question_list[j].marks / len(correct_answers[j])  # за каждый правильный + баллы
                else:
                    points_for_question -= question_list[j].marks / len(correct_answers[j])  #за каждый неправильный - баллы
            if points_for_question < 0:  # если ушли в минус, оценка 0
                points_for_question = 0
            elif points_for_question.is_integer():
                points_for_question = int(str(points_for_question).split(".")[0])  # убирается десятичная часть у целого числа

            actual_points += points_for_question  # суммируются баллы за весь тест

            temp = (question_list[j].question, actual_answers[j], points_for_question, question_list[j].marks)
            restest.append(temp)  # в запись подробного результата добавляется вопрос, данные ответы, макс. баллы за вопрос и полученные баллы

        grade = float(actual_points/max_points)*100  # оценка вычисляется в процентах

        newres = results(theme=title, student=current_user, grade=grade)
        newres.save()  # создается запись в таблице результатов

        new_activity = Activity(user=current_user, datetime=datetime.now(),
                               activity=f'Прошел тест темы "{title.title}"(Баллы:{actual_points}/{max_points})')
        new_activity.save() # создается запись в таблице отслеживания действий

        request.session['restest'] = restest #подробный результат запоминается для следующей странице

        return redirect('control:TestResult', control_id=control_id) # переход на страницу результата теста
    else: # если пользователь не прошел тест, создается запись о простом посещении страницы
        new_activity = Activity(user=current_user, datetime=datetime.now(),
                               activity=f'Посетил тест темы "{title.title}"')
        new_activity.save()

    return render(request, 'control/control.html', context)


def result(request, control_id):
    return render(request, 'control/result.html')
