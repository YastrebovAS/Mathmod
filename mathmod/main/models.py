from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_delete
import random

# модели, которые используются для представления различных данных в системе
# все модели созданы по одному и тому же принципу: сначала идут поля модели, потом класс Мета
# Класс Мета предназначен просто для названий в панели администратора, как и метод __str__ в некоторых моделях


class topic(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=128, unique=True)
    theory = models.FileField('Теория', upload_to='theory', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class practices(models.Model):
    topic_prac = models.ForeignKey(verbose_name="Тема", to=topic, related_name='practice_part', on_delete=models.CASCADE)
    practice = models.FileField('Файл', upload_to='execs', max_length=128)

    class Meta:
        verbose_name = 'Практика'
        verbose_name_plural = 'Практики'


class questions(models.Model):  # метод get_answers помогает получить все варианты ответа к конкретному вопросу
    topic_test = models.ForeignKey(verbose_name="Тема", to=topic, related_name='control_part', on_delete=models.CASCADE)
    question = models.CharField(verbose_name='Вопрос', max_length=128)
    picture = models.ImageField(verbose_name='Изображение', upload_to='question_image', blank=True)
    marks = models.IntegerField(verbose_name='Баллы', default=10)

    def __str__(self):
        return self.question

    def get_answers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        data = []
        random.shuffle(answer_objs)

        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'image': answer_obj.image,
                'is_correct': answer_obj.is_correct
            })
        return data

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(verbose_name="Вопрос", to=questions, related_name='question_for_answer', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to='answer_image', blank=True)
    answer = models.CharField(verbose_name='Вариант ответа', max_length=128)
    is_correct = models.BooleanField(verbose_name='Правильный ответ', default=False)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MOD = 'mod'
    ROLE_CHOICES = (
        ('user', 'USER'),
        ('mod', 'MOD'),
        ('admin', 'ADMIN'))
    patronymic = models.CharField(verbose_name='Отчество', max_length=128, null=True)
    role = models.CharField(verbose_name='Роль', choices=ROLE_CHOICES, max_length=128, default=USER)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class results(models.Model):
    theme = models.ForeignKey(verbose_name="Тема", to=topic, related_name='theme_res', on_delete=models.CASCADE,)
    student = models.ForeignKey(verbose_name="Студент", to=User, related_name='user_res', on_delete=models.CASCADE,)
    grade = models.FloatField('Баллы', null=True)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class PracticeReport(models.Model):
    practice = models.ForeignKey(verbose_name="Практика", to=practices, related_name='where_from_practice', on_delete=models.CASCADE, )
    student = models.ForeignKey(verbose_name="Студент", to=User, related_name='who_from_practice', on_delete=models.CASCADE, )
    report = models.TextField(verbose_name='HTML результата')
    date = models.DateTimeField(verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Отчеты практики'
        verbose_name_plural = 'Отчет практики'


class Activity(models.Model):
    user = models.ForeignKey(to=User, related_name='whose_activity', on_delete=models.CASCADE, )
    datetime = models.DateTimeField(verbose_name='Дата и время')
    activity = models.TextField(verbose_name='Посещенная страница')

    class Meta:
        verbose_name = 'Активность студента'
        verbose_name_plural = 'Отслеживание активности студентов'
