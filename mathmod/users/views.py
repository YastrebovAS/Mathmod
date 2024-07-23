from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate

from main.models import Activity, User
from datetime import datetime


def register(request):  # функция регистрации нового пользователя
    error = ''
    if request.method == "POST":   # Если нажали на кнопку "Зарегистрироваться"
        form = CreateUserForm(request.POST)

        if form.is_valid():  # Если форма заполнена правильно
            form.save()
            return redirect('login')   # Переадресация на страницу авторизации
        else:
            error = "Что-то пошло не так при заполнении"
    else:
        form = CreateUserForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'users/register.html', data)


def login(request):   # функция авторизации
    error = ''
    if request.method == "POST":   # Если нажали на кнопку "Авторизация"
        authform = LoginForm(data=request.POST)
        if authform.is_valid():  # Если форма заполнена правильно
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)  # Происходит проверка
            if user is not None:  # Если данные пользователя есть в системе
                auth.login(request, user)
                return redirect('menu')  # Пользователь перенаправляется на страницу каталога
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
    return render(request, 'users/login.html', data)


def user_logout(request):  # функция выхода из аккаунта, перенаправляет на страницу авторизации
    auth.logout(request)
    return redirect('login')
