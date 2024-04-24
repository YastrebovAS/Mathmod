from django.shortcuts import render,redirect
from django.forms import formset_factory
from .models import topic, practices,questions,Answer,results
from .forms import topicForm,practicesForm,questionsForm
# Create your views here.


def menu(request):
    theory = topic.objects.raw('SELECT id, title, theory from main_topic')
    practicesids = topic.objects.select_related('practice')
    controls = topic.objects.raw('SELECT id, title from main_topic')
    perms = request.user.role
    context = {
        'titles': theory,
        'pracs': practicesids,
        'conts': controls,
        'role': str(perms)
    }
    return render(request,'main/menu.html',context)

def prac_creat(request):
    error = ''
    questionformset = formset_factory(questionsForm, extra=0)
    #answerformset = formset_factory(answerForm, extra=0)
    if request.method == 'POST':
        form = topicForm(request.POST, request.FILES)
        prac_form = practicesForm(request.POST, request.FILES)
        control = questionformset(request.POST, request.FILES)
        #ques_options = answerformset(request.POST)
        print(request.POST)
        if prac_form.is_valid() and form.is_valid() and control.is_valid():
            newprac = practices(template = request.FILES['tem   plate'],
                             practice = request.FILES['practice'])
            newprac.save()
            newtopic = topic(theory=request.FILES['theory'], title=request.POST['title'],
                                 practice = newprac)
            newtopic.save()
            for i in range(len(control)):
                newques = questions(topic_test = newtopic, question = request.POST[f'form-{i}-question'],marks = request.POST[f'form-{i}-marks'])
                newques.save()
                for key in request.POST:
                    if key.startswith(f'form-{i}') and key.endswith('is_correct'):
                        current_sub_id = int(key.replace(f'form-{i}-','').replace('-is_correct',''))
                for z in range(current_sub_id+1):
                    if request.POST[f'form-{i}' + '-' + f'{z}-is_correct'] == 'true':
                        correction = True
                    else:
                        correction= False
                    newans = Answer(question = newques, answer = request.POST[f'form-{i}' + '-' + f'{z}-answer'], is_correct = correction)
                    print(newans.question)
                    print(newans.answer)
                    print(newans.is_correct)
                    newans.save()

            return redirect('menu')
        else:
            error = "Что-то пошло не так"

    else:
        form = topicForm()
        prac_form = practicesForm()
        control = questionformset()
        #ques_options = answerformset()
    data = {
        'form': form,
        'prac_form': prac_form,
        'control':control,
#        'options': ques_options,
        'error': error
    }
    return render(request,'main/add_to_db.html',data)

def result_list(request):
    all_results = results.objects.select_related('theme').select_related('student')
    print(all_results)
    return render(request, 'main/resultlist.html',{'results': all_results})