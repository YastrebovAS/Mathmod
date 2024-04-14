from .models import topic
from django.forms import ModelForm, TextInput, FileInput, NumberInput


class topicForm(ModelForm):
    class Meta:
        model = topic
        fields = ['title', 'theory', 'practice', 'control']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема'
            }),
            "theory": FileInput(attrs={
                'class': 'form-control',
                'label': 'Select a file',
                'accept': '.pdf'
            }),
            "practice": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Практика'
            }),
            "control": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Контроль'
            })
        }
