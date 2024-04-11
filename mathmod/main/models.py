from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.utils.timezone import now

class lesson(models.Model):
    title = models.CharField('Заголовок', primary_key=True, max_length=128, unique=True)
    theory = models.FileField('Теория',upload_to='theory')
    practice = models.FileField('Практика', upload_to='practice')
    control = models.FileField('Контроль', upload_to='control')
# Create your models here.
