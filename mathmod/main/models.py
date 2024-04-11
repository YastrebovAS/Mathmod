from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.utils.timezone import now



class lesson(models.Model):
    title = models.CharField('Заголовок', max_length=128, unique=True)
    theory = models.FileField('Теория', default=None)
    control = models.IntegerField()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

# Create your models here.
