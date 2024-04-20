from django.shortcuts import render,redirect
from django.forms import formset_factory
from .models import topic, practices
from .forms import topicForm,practicesForm,questionsForm, answerForm
# Create your views here.


def menu(request):
    theory = topic.objects.raw('SELECT id, title, theory from main_topic')
    practicesids = topic.objects.select_related('practice')
    perms = request.user.role
    context = {
        'titles': theory,
        'pracs': practicesids,
        'role': str(perms)
    }
    return render(request,'main/menu.html',context)

def prac_creat(request):
    error = ''
    questionformset = formset_factory(questionsForm, extra=3)
    answerformset = formset_factory(answerForm, extra=2)
    if request.method == 'POST':
        form = topicForm(request.POST, request.FILES)
        prac_form = practicesForm(request.POST, request.FILES)
        control = questionformset(request.POST)
        ques_options = answerformset(request.POST)
        if prac_form.is_valid() and form.is_valid():
            #if control.is_valid():
            newprac = practices(template = request.FILES['template'],
                             practice = request.FILES['practice'])
            newprac.save()
            newtopic = topic(theory=request.FILES['theory'], title=request.POST['title'],
                                 practice = newprac, control=request.POST['control'])
            newtopic.save()
            return redirect('menu')
        else:
            error = "Тема не была загружена"

    else:
        form = topicForm()
        prac_form = practicesForm()
        control = questionformset()
        ques_options = answerformset()
    data = {
        'form': form,
        'prac_form': prac_form,
        'control':control,
        'options': ques_options,
        'error': error
    }
    return render(request,'main/add_to_db.html',data)



def index(request):
    return render(request, 'main/test.html')