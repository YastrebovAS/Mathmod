from django.shortcuts import render,redirect

from .models import topic
from .forms import topicForm
# Create your views here.


def menu(request):
    theory = topic.objects.all()
    return render(request,'main/menu.html',{'titles':theory})

def create(request):
    error = ''
    if request.method == 'POST':
        form = topicForm(request.POST, request.FILES)
        if form.is_valid():
            newtopic = topic(theory = request.FILES['theory'], title = request.POST['title'],
                             practice = request.POST['practice'], control = request.POST['control'])
            newtopic.save()
            return redirect('home')
        else:
            error = "Что-то не так с заполнением"
    else:
        form = topicForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request,'main/add_to_db.html',data)



