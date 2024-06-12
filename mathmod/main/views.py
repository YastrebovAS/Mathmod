from django.shortcuts import render,redirect
from django.forms import formset_factory
from django.http import HttpResponse
from .models import *
from .forms import topicForm,practicesForm,questionsForm
import os
from datetime import datetime,timedelta

# Create your views here.


def menu(request):
    theory = topic.objects.all()
    practicesids = practices.objects.select_related('topic_prac')
    controls = topic.objects.all()
    perms = request.user.role
    context = {
        'titles': theory,
        'pracs': practicesids,
        'conts': controls,
        'role': str(perms)
    }

    print(dict(request.session))
    return render(request,'main/menu.html',context)

def edit_topics(request):
    error = ''
    delete_message = ""
    questionformset = formset_factory(questionsForm, extra=0)
    current_topics = topic.objects.all()
    form = topicForm()
    prac_form = practicesForm()
    control = questionformset()
    control_red = questionformset()

    if request.method == 'POST':
        if "delete" in request.POST:
            topic_for_deletion = topic.objects.get(title = request.POST['delete_topic'])
            practice_for_deletion = practices.objects.get(topic_prac = topic_for_deletion)
            os.remove("media/" + str(topic_for_deletion.theory))
            os.remove("media/" + str(practice_for_deletion.practice))
            topic_for_deletion.delete()
            delete_message = "Произошло удаление"
        if "change" in request.POST:
            redacted_topic = topic.objects.get(title=request.POST['change_topic'])
            redacted_topic_practice = practices.objects.get(topic_prac = redacted_topic)
            control_red = questionformset(request.POST, request.FILES)
            if "theory" in request.FILES.keys():
                os.remove("media/" + str(redacted_topic.theory))
                redacted_topic.theory = request.FILES["theory"]
                #print(request.FILES["theory"])
                redacted_topic.save()
            if "practice" in request.FILES.keys():
                os.remove("media/" + str(redacted_topic_practice.practice))
                redacted_topic_practice.practice = request.FILES["practice"]
                #print(request.FILES["practice"])
                redacted_topic_practice.save()
            if control_red.is_valid():
                if len(control_red) != 0:
                    questions_to_delete = questions.objects.filter(topic_test = redacted_topic)
                    for question in questions_to_delete:
                        answers_to_delete = Answer.objects.filter(question = question)
                        answers_to_delete.delete()
                    questions_to_delete.delete()
                    for k in range(len(control_red)):
                        if f'form-{k}-picture' in request.FILES.keys():
                            quesim = request.FILES[f'form-{k}-picture']
                        else:
                            quesim = None
                        newques_red = questions(topic_test=redacted_topic, question=request.POST[f'form-{k}-question'],
                                            picture=quesim,
                                            marks=request.POST[f'form-{k}-marks'])
                        newques_red.save()
                        for key in request.POST:
                            if key.startswith(f'form-{k}') and key.endswith('is_correct-red'):
                                current_sub_id_red = int(key.replace(f'form-{k}-', '').replace('-is_correct-red', ''))
                        try:
                            for m in range(current_sub_id_red + 1):

                                if request.POST[f'form-{k}' + '-' + f'{m}-is_correct-red'] == 'true':
                                    correction = True
                                else:
                                    correction = False

                                if f'form-{k}' + '-' + f'{m}-picture-red' in request.FILES.keys():
                                    ansim = request.FILES[f'form-{k}' + '-' + f'{m}-picture-red']
                                else:
                                    ansim = None

                                newans_red = Answer(question=newques_red,
                                                answer=request.POST[f'form-{k}' + '-' + f'{k}-answer-red'],
                                                image=ansim, is_correct=correction)
                                newans_red.save()
                        except:
                            error = 'Каждый вопрос должен сопровождаться как минимум 2-мя ответами'



            error = "Произошло Редактирование"
        if "create" in request.POST:
            #print(request.POST)

            form = topicForm(request.POST, request.FILES)
            prac_form = practicesForm(request.POST, request.FILES)
            control = questionformset(request.POST, request.FILES)

            if prac_form.is_valid() and form.is_valid() and control.is_valid():
                newtopic = topic(theory=request.FILES['theory'], title=request.POST['title'])
                #newtopic.save()
                newprac = practices(topic_prac = newtopic,practice = request.FILES['practice'])
                #newprac.save()

                for i in range(len(control)):
                    if f'form-{i}-picture' in request.FILES.keys():
                        quesim = request.FILES[f'form-{i}-picture']
                    else:
                        quesim = None
                    newques = questions(topic_test = newtopic, question = request.POST[f'form-{i}-question'],
                                        picture = quesim,
                                        marks = request.POST[f'form-{i}-marks'])
                    #newques.save()
                    for key in request.POST:
                        if key.startswith(f'form-{i}') and key.endswith('is_correct'):
                            current_sub_id = int(key.replace(f'form-{i}-','').replace('-is_correct',''))
                    try:
                        for z in range(current_sub_id+1):

                            if request.POST[f'form-{i}' + '-' + f'{z}-is_correct'] == 'true':
                                correction = True
                            else:
                                correction= False

                            if f'form-{i}' + '-' + f'{z}-picture' in request.FILES.keys():
                                ansim = request.FILES[f'form-{i}' + '-' + f'{z}-picture']
                            else:
                                ansim = None

                            newans = Answer(question = newques, answer = request.POST[f'form-{i}' + '-' + f'{z}-answer'],
                                            image = ansim, is_correct = correction)
                            #newans.save()
                    except:
                        error = 'Каждый вопрос должен сопровождаться как минимум 2-мя ответами'

                return redirect('menu')
            else:
                error = "Что-то пошло не так"
    data = {
        'current_topics': current_topics,
        'form': form,
        'prac_form': prac_form,
        'control': control,
        'control_red':control_red,
        'error': error,
        "delete_message":delete_message
    }
    return render(request,'main/add_to_db.html',data)




def result_list(request):
    all_results = results.objects.select_related('theme').select_related('student')
    return render(request, 'main/resultlist.html',{'results': all_results})

def practice_report_list(request):
    all_reports = PracticeReport.objects.select_related('practice')
    titles = []
    for report in all_reports:
        report_theme = practices.objects.select_related('topic_prac').filter(id = report.practice_id)
        titles.append(report_theme[0].topic_prac.title)
    return render(request, 'main/reportlist.html',{'reports': all_reports, "titles":titles})

def practice_report(request, report_id):
    needed_report = PracticeReport.objects.filter(id = report_id)[0]
    report_text = needed_report.report
    return render(request,'main/report.html',{'text':report_text})

def activity_list(request):
    complete_array = []
    students = User.objects.filter(role = 'user_def')

    month_delta = datetime.now() - timedelta(days=30)

    for student in students:
        last_month_activities = []
        activities = Activity.objects.filter(user = student, datetime__gte = month_delta)
        for activity in activities:
            normal_datetime = str(activity.datetime).split(".")[1]
            activity_object = [activity.activity, activity.datetime, None]
            if "отчет" in activity.activity:
                two_second_lower_delta = activity.datetime - timedelta(seconds=2)
                two_second_upper_delta = activity.datetime + timedelta(seconds=2)
                report = PracticeReport.objects.get(student =student, date__range = [two_second_lower_delta,two_second_upper_delta])
                activity_object[2] = report.id
            last_month_activities.append(activity_object)
        complete_array.append((student,last_month_activities))


    context = {
        "complete_array":complete_array
    }

    return render(request, 'main/activity_list.html',context)