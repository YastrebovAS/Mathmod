from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib import admin
from django.utils.timezone import now

class practices(models.Model):
    template = models.FileField('Шаблон', max_length=128)
    practice = models.FileField('Файл с формулами', max_length=128)
    class Meta:
        verbose_name = 'Практика'
        verbose_name_plural = 'Практики'


class options(models.Model):
    option = models.CharField('Вариант ответа', max_length=128, unique=True)
    def __str__(self):
        return self.option
    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'

class questions(models.Model):
    question = models.CharField('Вопрос', max_length=128)
    answer = models.TextField('Ответ', max_length=128)
    options = models.ForeignKey(to = options, related_name='q_opt',  on_delete=models.CASCADE,)
    def __str__(self):
        return self.question
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class topic(models.Model):
    title = models.CharField('Заголовок', max_length=128, unique=True)
    theory = models.FileField('Теория',upload_to='theory', null=True)
    practice = models.IntegerField('Практика')
    control = models.IntegerField('Контроль')
    '''practice = models.ForeignKey(to = practices, related_name='prac_part', on_delete=models.CASCADE)
    control = models.ForeignKey(to =  questions, related_name='cont_part', on_delete=models.CASCADE)'''
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'




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
    redactor = models.ForeignKey(to=User, related_name='user_changelg',  on_delete=models.CASCADE,)
    date = models.DateField('Дата редактирования')
    changes = models.TextField('Описание изменений')
    class Meta:
        verbose_name = 'Редактирование сайта'
        verbose_name_plural = 'Логи редактирования сайта'
