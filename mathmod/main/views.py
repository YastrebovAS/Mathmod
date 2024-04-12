from django.shortcuts import render

from .models import lesson
from .forms import lessonForm
# Create your views here.


def menu(request):
    theory = lesson.objects.all()
    return render(request,'main/menu.html',{'titles':theory})

def create(request):
    error = ''
    if request.method == 'POST':
        form = lessonForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = "Что-то не так с заполнением"
    form = lessonForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request,'main/add_to_db.html',data)



