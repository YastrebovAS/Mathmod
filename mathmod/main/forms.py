from .models import lesson
from django.forms import ModelForm,TextInput, FileInput,NumberInput

class lessonForm(ModelForm):
    class Meta:
        model = lesson
        fields = ['title','theory','control']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема'
            }),
            "theory": FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Файл с теорией',
                'accept': '.pdf'
            }),
            "control": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Контроль'
            })
        }