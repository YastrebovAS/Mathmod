from .models import topic, practices,questions,Answer
from django.forms import ModelForm, TextInput, FileInput, NumberInput,NullBooleanSelect, NullBooleanField


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
        fields = ['template','practice']
        widgets = {
            "template": FileInput(attrs={
                'class': 'form-control',
                'label': 'Select a file',
                'accept': '.html'
            }),
            "practice": FileInput(attrs={
                'class': 'form-control',
                'label': 'Select a file',
                'accept': '.py'
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
