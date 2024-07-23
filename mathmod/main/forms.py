from .models import topic, practices, questions, Answer
from django import forms
from django.forms import ModelForm, TextInput, FileInput, NumberInput
# формы, через которые частично производится создание/редактирование тем
# наверное, можно было бы обойтись без них, но они были созданы, когда я только начинал осваивать функционал форм


class TopicForm(ModelForm):  # форма состоящая из полей для названия темы и для загрузки файля с теориейй
    class Meta:
        model = topic
        fields = ['title', 'theory']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема'
            }),
            "theory": FileInput(attrs={
                'class': 'form-control',
                'label': 'Select a file',
                'accept': '.pdf'
            })
        }


class PracticeForm(ModelForm):  # форма состоящая из поля для загрузки файля с практикой
    class Meta:
        model = practices
        fields = ['practice']
        widgets = {
            "practice": FileInput(attrs={
                'class': 'form-control',
                'label': 'Select a file',
                'accept': '.xlsx,.xlsm'
            })
        }


class QuestionForm(ModelForm):  # форма для вопроса, состоит из полей для формулировки вопроса, загрузки изображения и баллов за вопрос
    class Meta:
        model = questions
        fields = ['question', 'picture', 'marks']
        widgets = {
            "question": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вопрос'
            }),
            'picture': FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            "marks": NumberInput(attrs={
                'class': 'form-control'
            })
        }
