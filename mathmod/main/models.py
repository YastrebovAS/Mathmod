from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.utils.timezone import now
import random

class practices(models.Model):
    template = models.FileField('Шаблон',upload_to='template', max_length=128)
    practice = models.FileField('Файл с формулами', upload_to='execs', max_length=128)
    class Meta:
        verbose_name = 'Практика'
        verbose_name_plural = 'Практики'

class topic(models.Model):
    title = models.CharField('Заголовок', max_length=128, unique=True)
    theory = models.FileField('Теория',upload_to='theory', null=True)
    #practice = models.IntegerField('Практика')
    practice = models.ForeignKey(to=practices, related_name='prac_part', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

class questions(models.Model):
    topic_test = models.ForeignKey(to=topic, related_name='control_part', on_delete=models.CASCADE)
    question = models.CharField( verbose_name='Вопрос', max_length=128)
    picture = models.ImageField('Изображение', upload_to='question_image', null=True)
    marks = models.IntegerField('Оценка',default = 10)
    def __str__(self):
        return self.question

    def get_answers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        data = []
        random.shuffle(answer_objs)

        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        return data
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    question = models.ForeignKey(to = questions,related_name='question_for_answer',  on_delete =models.CASCADE)
    answer = models.CharField('Вариант ответа', max_length=128)
    is_correct = models.BooleanField(verbose_name='Правильный ответ', default=False)
    def __str__(self):
        return self.answer
    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'





class User(AbstractUser):
    USER = 'user_def'
    ADMIN = 'admin'
    MOD = 'mod'
    ROLE_CHOICES = (
    ('user_def','USER'),
    ('mod', 'MOD'),
    ('admin','ADMIN'))
    patronymic = models.CharField('Отчество', max_length=128, null=True)
    role = models.CharField('Роль', choices = ROLE_CHOICES, max_length=128, default = USER)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
class results(models.Model):
    theme = models.ForeignKey(to=topic, related_name='theme_res', on_delete=models.CASCADE,)
    student = models.ForeignKey(to=User, related_name='user_res', on_delete=models.CASCADE,)
    grade = models.FloatField('Оценка', null=True)
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class changelogs(models.Model):
    topic = models.ForeignKey(to = topic,related_name='theme_changelg',  on_delete=models.CASCADE)
    redactor = models.ForeignKey(to=User, related_name='user_changelg',  on_delete=models.CASCADE)
    date = models.DateField('Дата редактирования')
    changes = models.TextField('Описание изменений')
    class Meta:
        verbose_name = 'Редактирование сайта'
        verbose_name_plural = 'Логи редактирования сайта'
