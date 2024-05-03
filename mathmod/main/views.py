from django.shortcuts import render,redirect
from django.forms import formset_factory
from .models import *
from .forms import topicForm,practicesForm,questionsForm
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

def prac_creat(request):
    error = ''
    questionformset = formset_factory(questionsForm, extra=0)

    if request.method == 'POST':
        form = topicForm(request.POST, request.FILES)
        prac_form = practicesForm(request.POST, request.FILES)
        control = questionformset(request.POST, request.FILES)

        if prac_form.is_valid() and form.is_valid() and control.is_valid():
            newtopic = topic(theory=request.FILES['theory'], title=request.POST['title'],
                             )
            newtopic.save()
            newprac = practices(topic_prac = newtopic, template = request.FILES['template'],
                             practice = request.FILES['practice'])
            newprac.save()

            for i in range(len(control)):
                if f'form-{i}-picture' in request.FILES.keys():
                    quesim = request.FILES[f'form-{i}-picture']
                else:
                    quesim = None
                newques = questions(topic_test = newtopic, question = request.POST[f'form-{i}-question'],
                                    picture = quesim,
                                    marks = request.POST[f'form-{i}-marks'])
                newques.save()
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
                        newans.save()
                except:
                    error = 'Каждый вопрос должен сопровождаться как минимум 2-мя ответами'

            return redirect('menu')
        else:
            error = "Что-то пошло не так"

    else:
        form = topicForm()
        prac_form = practicesForm()
        control = questionformset()
    data = {
        'form': form,
        'prac_form': prac_form,
        'control':control,
        'error': error
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
    activities = Activity.objects.all()
    practice_reports = PracticeReport.objects.all()
    practice_dates = []
    practice_ids = []
    practice_students = []
    for report in practice_reports:
        practice_ids.append(report.id)
        practice_students.append(report.student)
        practice_dates.append(str(report.date).split(".")[0])
    activity_lists = []
    for activity in activities:
        separated = activity.activity.replace('[','').replace(']','').replace("'",'').split(',')
        complete_array = []
        for act in separated:
            if "данные" in act:
                bog_date = act.split(".")[0]
                actual_date = bog_date[len(bog_date)-19:]
                practice_index = practice_dates.index(actual_date)
                if activity.user == practice_students[practice_index]:
                    complete_array.append((act,practice_ids[practice_index]))
                else:
                    complete_array.append((act,0))
            else:
                complete_array.append((act,0))

        activity_lists.append(complete_array)
    return render(request, 'main/activity_list.html',{'activities': activities, "activity_lists": activity_lists})