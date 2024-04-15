from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate,login,logout

def homepage(request):
    return render(request,'users/homepage.html')


def register(request):
    error = ''
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error = "Что-то не так с регистрацией"
    else:
        form = CreateUserForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request,'users/register.html',data)

def login(request):
    error = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('menu')
            else:
                error = "Пользователь не зарегистрирован"
        else:
            error = "Что-то не так с авторизацией"
    else:
        form = LoginForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request,'users/login.html',data)
def logout(request):
    pass

# Create your views here.
