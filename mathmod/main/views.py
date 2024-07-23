from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.http import HttpResponse
from .models import *
from .forms import TopicForm, PracticeForm, QuestionForm
import os
from datetime import datetime, timedelta

# Create your views here.


def menu(request):  # функция для демонстрации всего каталога
    theory = topic.objects.all()  # все темы и файлы с теорией
    practicesids = practices.objects.select_related('topic_prac')  # все практики
    controls = topic.objects.all()  # все тесты
    perms = request.user.role  # роль ползователя. в данный момент смотрящего каталог
    context = {
        'titles': theory,
        'pracs': practicesids,
        'conts': controls,
        'role': str(perms)
    }

    return render(request, 'main/menu.html', context)


def edit_topics(request):  # функция для создания/редактирования/удаления тем
    error = ''
    delete_message = ""
    edit_message = ""
    questionformset = formset_factory(QuestionForm, extra=0)
    current_topics = topic.objects.all()

    form = TopicForm()
    prac_form = PracticeForm()
    control = questionformset()
    control_red = questionformset()
    # изначально все формы пустые

    if request.method == 'POST':  # если была нажата кнопка создания/редактирования/удаления
        if "delete" in request.POST:  # если тема удаляется
            topic_for_deletion = topic.objects.get(title=request.POST['delete_topic'])
            practice_for_deletion = practices.objects.get(topic_prac=topic_for_deletion)
            os.remove("media/" + str(topic_for_deletion.theory))  # файлы теории и практики сами не удалятся
            os.remove("media/" + str(practice_for_deletion.practice))  # поэтому надо сделать это самостоятельно
            try:  # после удаления модели topic произойдет каскадное удаление всех других связанных моделей
                topic_for_deletion.delete()
                delete_message = "Произошло удаление"
            except:
                error = "Что-то пошло не так при удалении"

        if "change" in request.POST:  # если тема редактируется
            redacted_topic = topic.objects.get(title=request.POST['change_topic'])  # выбранная тема находится в базе данных
            redacted_topic_practice = practices.objects.get(topic_prac=redacted_topic)
            control_red = questionformset(request.POST, request.FILES)  # форма вопросов заполняется введенными данными
            if "theory" in request.FILES.keys():  # если загружен новый файл теории

                os.remove("media/" + str(redacted_topic.theory))
                redacted_topic.theory = request.FILES["theory"]
                redacted_topic.save()  # теория обновляется

            if "practice" in request.FILES.keys():  # если загружен новый файл практики

                os.remove("media/" + str(redacted_topic_practice.practice))
                redacted_topic_practice.practice = request.FILES["practice"]
                redacted_topic_practice.save()  # практика обновляется

            if control_red.is_valid():  # если введены новые вопросы для теста

                if len(control_red) != 0:

                    questions_to_delete = questions.objects.filter(topic_test=redacted_topic)
                    for question in questions_to_delete:
                        answers_to_delete = Answer.objects.filter(question=question)
                        answers_to_delete.delete()  # для начала удаляются все старые ответы
                    questions_to_delete.delete()    # и вопросы, связанные с выбранной темой

                    for k in range(len(control_red)):  # затем идет просмотр введенных вопросов
                        if f'form-{k}-picture' in request.FILES.keys():  # проверка на наличие картинок для вопроса
                            
                            question_image = request.FILES[f'form-{k}-picture']
                        else:
                            question_image = None
                            
                        new_question_edited = questions(topic_test=redacted_topic, question=request.POST[f'form-{k}-question'],
                                                        picture=question_image, marks=request.POST[f'form-{k}-marks'])
                        new_question_edited.save()  # каждый новый вопрос сохраняется и связывается с выбранной темой
                        
                        for key in request.POST:
                            if key.startswith(f'form-{k}') and key.endswith('is_correct-red'):
                                current_sub_id_red = int(key.replace(f'form-{k}-', '').replace('-is_correct-red', ''))
                        try:
                            for m in range(current_sub_id_red + 1):  # цикл для КАЖДОГО варианта ответа к конкретному вопросу

                                if request.POST[f'form-{k}' + '-' + f'{m}-is_correct-red'] == 'true':  # проверка, правильный ответ или нет
                                    correction = True
                                else:
                                    correction = False

                                if f'form-{k}' + '-' + f'{m}-picture-red' in request.FILES.keys():  # проверка на наличие картинок у ответа
                                    answer_image = request.FILES[f'form-{k}' + '-' + f'{m}-picture-red']
                                else:
                                    answer_image = None

                                newans_red = Answer(question=new_question_edited,
                                                    answer=request.POST[f'form-{k}' + '-' + f'{m}-answer-red'],
                                                    image=answer_image, is_correct=correction)

                                newans_red.save()  # новый ответ к новому вопросу сохраняется
                        except:
                            error = 'Что-то пошло не так при редиктировании'

            edit_message = "Произошло Редактирование"
            
        if "create" in request.POST:  # если тема создается

            form = TopicForm(request.POST, request.FILES)
            prac_form = PracticeForm(request.POST, request.FILES)
            control = questionformset(request.POST, request.FILES)

            if prac_form.is_valid() and form.is_valid() and control.is_valid():  # если все поля заполнены правильно
                newtopic = topic(theory=request.FILES['theory'], title=request.POST['title'])
                newtopic.save()  # создается новая тема, сохраняется теория
                newprac = practices(topic_prac=newtopic, practice=request.FILES['practice'])
                newprac.save()  # создается новая практика, сохраняется файл

                for i in range(len(control)):  # просматривается каждый введенный вопрос
                    if f'form-{i}-picture' in request.FILES.keys():  # проверка на наличие картинок для вопроса
                        question_image = request.FILES[f'form-{i}-picture']
                    else:
                        question_image = None
                    newques = questions(topic_test=newtopic, question=request.POST[f'form-{i}-question'],
                                        picture=question_image, marks=request.POST[f'form-{i}-marks'])
                    newques.save()  # каждый вопрос сохраняется
                    for key in request.POST:
                        if key.startswith(f'form-{i}') and key.endswith('is_correct'):
                            current_sub_id = int(key.replace(f'form-{i}-', '').replace('-is_correct', ''))
                    try:
                        for z in range(current_sub_id+1):

                            if request.POST[f'form-{i}' + '-' + f'{z}-is_correct'] == 'true':  # проверка, правильный ответ или нет
                                correction = True
                            else:
                                correction = False

                            if f'form-{i}' + '-' + f'{z}-picture' in request.FILES.keys():  # проверка на наличие картинок у ответа
                                answer_image = request.FILES[f'form-{i}' + '-' + f'{z}-picture']
                            else:
                                answer_image = None

                            newans = Answer(question=ewques, answer=request.POST[f'form-{i}' + '-' + f'{z}-answer'],
                                            image=answer_image, is_correct=correction)
                            newans.save()  # каждый ответ к конкретному вопросу сохраняется
                    except:
                        error = 'Что-то пошло не так при создании тестовой части'

                return redirect('menu')  # возврат к каталогу, чтобы увидеть новую созданную тему

    data = {
        'current_topics': current_topics,
        'form': form,
        'prac_form': prac_form,
        'control': control,
        'control_red': control_red,
        'error': error,
        "edit_message": edit_message,
        "delete_message": delete_message
    }
    return render(request, 'main/add_to_db.html', data)


def result_list(request):  # функция для демонстрации результатов теста на отдельной странице
    all_results = results.objects.select_related('theme').select_related('student')
    return render(request, 'main/resultlist.html', {'results': all_results})


def practice_report_list(request):  # функция для демонстрации отчетов практики на отдельной странице
    all_reports = PracticeReport.objects.select_related('practice')
    titles = []
    for report in all_reports:
        report_theme = practices.objects.select_related('topic_prac').filter(id=report.practice_id)
        titles.append(report_theme[0].topic_prac.title)
    return render(request, 'main/reportlist.html', {'reports': all_reports, "titles": titles})


def practice_report(request, report_id):  # демонстрация отдельного отчета практики
    needed_report = PracticeReport.objects.filter(id=report_id)[0]
    report_text = needed_report.report
    return render(request, 'main/report.html', {'text': report_text})


def activity_list(request):  # функция для демонстрации деятельности студентов

    complete_array = []
    students = User.objects.filter(role='user_def')  # будет показываться деятельность ТОЛЬКО СТУДЕНТОВ
                                                    # чтобы это поменять, надо заменить filter(role='user_def') на all()

    month_delta = datetime.now() - timedelta(days=30)

    for student in students:
        last_month_activities = []

        activities = Activity.objects.filter(user=student, datetime__gte=month_delta)  # демонстрируется деятельность только за последний месяц

        for activity in activities:
            activity_object = [activity.activity, activity.datetime, None]  # изначально деятельность состоит только из самой деятельности и даты

            if "отчет" in activity.activity:  # если студент присылал отчет

                two_second_lower_delta = activity.datetime - timedelta(seconds=2)
                two_second_upper_delta = activity.datetime + timedelta(seconds=2)
                report = PracticeReport.objects.get(student=student, date__range=[two_second_lower_delta, two_second_upper_delta])
                activity_object[2] = report.id  # к деятельности также прикрепляется номер этого отчета

            last_month_activities.append(activity_object)  # создается массив из деятельности студента за месяц

        complete_array.append((student, last_month_activities))  # в конечном итоге получается массив
                                                                 # с элементами вида (студент - список деятельности за месяц)

    context = {
        "complete_array": complete_array
    }

    return render(request, 'main/activity_list.html', context)
