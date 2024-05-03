from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate

from main.models import Activity, User
from datetime import datetime


def register(request):
    error = ''
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        #print(form)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error = "Личные данные слишком совпадают"
    else:
        form = CreateUserForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request,'users/register.html',data)

def login(request):
    if dict(request.session) == {}:
        request.session['journey'] = []
    print(dict(request.session))
    error = ''
    if request.method == "POST":
        authform = LoginForm(data = request.POST)
        if authform.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('menu')
            else:
                error = "Пользователь не зарегистрирован"
        else:
            error = "Что-то не так с авторизацией"
    else:
        authform = LoginForm()
    data = {
        'authform': authform,
        'error': error
    }
    return render(request,'users/login.html',data)
def user_logout(request):
    leaving_user = User.objects.filter(username = request.user)[0]
    newactivity = Activity(user = leaving_user, datetime = datetime.now(), activity = request.session['journey'])
    newactivity.save()
    auth.logout(request)
    return redirect('login')
