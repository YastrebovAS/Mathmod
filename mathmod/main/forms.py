from .models import topic, practices,questions,Answer
from django import forms
from django.forms import ModelForm, TextInput, FileInput, NumberInput,NullBooleanSelect, NullBooleanField,Select,Form


class topicForm(ModelForm):
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
class practicesForm(ModelForm):
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
class questionsForm(ModelForm):
    class Meta:
        model = questions
        fields = ['question','picture','marks']
        widgets = {
            "question": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вопрос'
            }),
            'picture':FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            "marks": NumberInput(attrs={
                'class': 'form-control'
        })
        }


class inputform(Form):
    your_name = forms.CharField(label="Your name", max_length=100)
    class Meta:
        fields = ['number', 'choice']
        widgets = {
            "title": TextInput(attrs={
                'class': 'input_text',
                'placeholder': 'Тема'
            }),
            "theory": Select(attrs={
                'class': 'input_select',
                'placeholder': 'Тема'
            }),
        }