from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from main.models import User
from django import forms
from django.forms.widgets import PasswordInput,TextInput
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name',  'patronymic', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
